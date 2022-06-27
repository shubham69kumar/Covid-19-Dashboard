from operator import mod
from django.db import models


# Create your models here.
class active(models.Model):
    state = models.CharField(max_length=50)
    date=models.DateField()
    active_case = models.IntegerField()
    new_infected=models.IntegerField()

    def __str__(self) -> str:
        return super().__str__()


class death(models.Model):
    state = models.CharField(max_length=50)
    date=models.DateField()
    decreased = models.IntegerField()
    new_decreased=models.IntegerField()

    def __str__(self) -> str:
        return super().__str__()

class recover(models.Model):
    state = models.CharField(max_length=50)
    date=models.DateField()
    recovered_case = models.IntegerField()
    new_recovered=models.IntegerField()

    def __str__(self) -> str:
        return super().__str__()

class india(models.Model):
    date = models.DateField(primary_key=True)
    total_death = models.IntegerField()
    total_recovery = models.IntegerField()
    total_newcase = models.IntegerField()
    total_positive = models.IntegerField()

    def __str__(self) -> str:
        return super().__str__()

class vaccine(models.Model):
    date = models.DateTimeField(primary_key=True)
    dose_1=models.IntegerField()
    dose_2=models.IntegerField()

    def __str__(self) -> str:
        return super().__str__()


class infected(models.Model):
    state = models.CharField(max_length=50)
    date = models.DateField()
    total_infected = models.IntegerField()
    new_infected=models.IntegerField()
    
    def __str__(self) -> str:
        return super().__str__()

class modify(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateField()

    def __str__(self) -> str:
        return super().__str__()