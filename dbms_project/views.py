from audioop import reverse
from http.client import HTTPResponse
from math import inf
import re
from socket import *
from sqlite3 import Cursor
from subprocess import call
from turtle import pos
from django.db import connection
from django.db.models.functions import Cast
from django.db.models.fields import DateField
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse , HttpResponseRedirect
from django.db.models import Sum
from dbms_project.models import *
import json 
import requests
from datetime import date
import datetime
today = date.today()



def index(request):  
    cursor = connection.cursor()
    cursor2 = connection.cursor()
    modify_=modify.objects.filter(id=666).values('date')
    modify_ =modify_[0]['date']

    cursor.callproc('get_active_infected',[modify_])
    result = cursor.fetchall()
    result=list(result)
    cursor.close()
    cursor2.callproc('get_recover_death',[modify_])
    result2 = cursor2.fetchall()
    result2=list(result2)
    cursor2.close()
    new_result = zip(result,result2)
    india_data=find_sum()
    total=india.objects.filter(date=modify_).values_list()
    return render(request,'index.html',{'data':new_result,'india_data':india_data,"output_data":modify_,'total':total}) 

def run_data(request): 
    count_data ='hello'
    date_=[]
    
    try:
        date_ = india.objects.get(date=today)
        count_data='data updated'
    except:
        count_data = 'data stored'
        URL = "https://www.mohfw.gov.in/data/datanew.json"
        page = requests.get(URL)
        data=json.loads(page.content)

        state_wise = []
        for da in data:
            dic ={}
            dic['id']=da['sno']
            dic['name']=da['state_name']
            dic['new_active'] = int(da['new_active'])-int(da['active'])
            dic['new_cured']=int(da['new_cured'])-int(da['cured'])
            if(da['total'] == ''):
                dic['new_death'] = 0
            else:
                dic['new_death']=int(da['total'])
            dic['new_positive']=int(da['new_positive'])-int(da['positive'])
            dic['total_active'] = int(da['new_active'])
            dic['total_cured'] = int(da['new_cured'])
            dic['total_death']=int(da['new_death'])
            dic['total_positive']=int(da['new_positive'])
            state_wise.append(dic)
        
        for da in state_wise:
            if(da['name'] is not ''):
                add_active=active(state=da['name'],date=today,active_case=da['total_active'],new_infected=da['new_active'])
                add_active.save()
                add_death=death(state=da['name'],date=today,decreased=da['total_death'],new_decreased=da['new_death'])
                add_death.save()
                add_recovery=recover(state=da['name'],date=today,recovered_case=da['total_cured'],new_recovered=da['new_cured'])
                add_recovery.save()
                add_infected=infected(state=da['name'],date=today,total_infected=da['total_positive'],new_infected=da['new_positive'])
                add_infected.save()
            
        add_india=india(date=today,total_death=state_wise[-1]['total_death'],total_recovery=state_wise[-1]['total_cured'],total_newcase=state_wise[-1]['total_active'],total_positive=state_wise[-1]['total_positive'])
        add_india.save() 
        a =modify.objects.get(id=666)
        a.date=today
        a.save() 
    return HttpResponseRedirect('/')
     

def find_sum():
    total=[]
    modify_=modify.objects.filter(id=666).values('date')
    modify_ =modify_[0]['date']
    total.append(infected.objects.filter(date=modify_).aggregate(Sum('new_infected')))
    total.append(active.objects.filter(date=modify_).aggregate(Sum('new_infected')))
    total.append(recover.objects.filter(date=modify_).aggregate(Sum('new_recovered')))
    total.append(death.objects.filter(date=modify_).aggregate(Sum('new_decreased')))
    return total

def search(request):
   
    search= request.POST['search']
    search = search.title()
    a = active.objects.filter(state=search).values()
    b= recover.objects.filter(state=search).values()
    c= death.objects.filter(state=search).values()
    d=infected.objects.filter(state=search).values()
    final = zip(a,b,c,d)
    final1=zip(a,b,c,d)
    if(len(d) != 0):
        xval=[]
        inf = []
        dea=[]
        reco=[]
        act=[]
        for a,b,c,d in final1:
            xval.append(a['date'])
            inf.append(d['new_infected'])
            dea.append(c['new_decreased'])
            act.append(abs(a['new_infected']))
            reco.append(b['new_recovered'])
        return render(request,'state.html',{'search':search , 'final':final,'xval':xval,'inf':inf,'dea':dea,'reco':reco,'act':act})
    else:
        return HttpResponseRedirect('/')


def help(request):
    return render(request,'help.html')


def Ind(request):
    modify_=modify.objects.filter(id=666).values('date')
    modify_ =modify_[0]['date']
    data=[]
    date=[]
    for i in range(6,-1,-1):
        data_temp =[]
        new = datetime.timedelta(days=i)
        da = modify_-new
        date.append(da)
        data_temp.append(da)
        data_temp.append(infected.objects.filter(date=da).aggregate(Sum('new_infected')))
        data_temp.append(active.objects.filter(date=da).aggregate(Sum('new_infected')))
        data_temp.append(recover.objects.filter(date=da).aggregate(Sum('new_recovered')))
        data_temp.append(death.objects.filter(date=da).aggregate(Sum('new_decreased')))
        data.append(data_temp)
    return render(request,'Ind.html',{'data_':data,'date':date})