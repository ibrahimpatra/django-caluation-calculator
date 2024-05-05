from django.db import models

# Create your models here.
class Client(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=150, null=True)
  phone = models.CharField(max_length=20, null=True) 
  email=models.EmailField(max_length=150,null=True)
  valuation=models.CharField(max_length=150,null=True)
 

class Constants(models.Model):
  id = models.AutoField(primary_key=True)
  Risk_free_rate=models.CharField(max_length=10, null=True)
  Market_Premium=models.CharField(max_length=10, null=True)
  Beta=models.CharField(max_length=10, null=True)
  Effective_tax_Rate=models.CharField(max_length=10, null=True)



class Industry_Beta(models.Model):
  id = models.AutoField(primary_key=True)
  industry=models.CharField(max_length=50, null=True)
  beta=models.FloatField( null=True)
  unlevered_beta=models.FloatField(null=True)
  