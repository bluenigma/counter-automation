from django.db import models

class CounterReport(models.Model):
    date_generated = models.DateField()
    serial_number = models.ForeignKey(Unit, on_delete=models.PROTECT)
    black_total = models.IntegerField()
    color_total = models.IntegerField()

class Unit(models.Model):
    serial_number = models.CharField(max_length=25)
    vendor = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    black_count = models.IntegerField()
    color_count = models.IntegerField()
    client = models.ForeignKey(Client, on_delete=models.SET_DEFAULT)


class Client(models.Model):
    name = models.CharField(max_length=100)
    black_rate = models.FloatField()
    color_rate = models.FloatField()
    min_monthly_pay = models.IntegerField()

class MonthlyPrints(models.Model):
    month = models.DateField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    blackPrints = models.IntegerField()
    colorPrints = models.IntegerField()

class MonthlyPay(models.Model):
    month = models.DateField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField() # or FloatField?
    paid = models.BooleanField()
