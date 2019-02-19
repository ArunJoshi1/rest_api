from django.db import models

# Create your models here.
class Profession(models.Model):
    description=models.CharField(max_length=50)
    def __str__(self):
        return self.description



class DataSheet(models.Model):
    description=models.CharField(max_length=50)
    historical_data=models.TextField()
    def __str__(self):
        return self.description



class Customers(models.Model):
    name=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    profession=models.ManyToManyField(Profession)
    data_sheet=models.OneToOneField(DataSheet,on_delete=models.CASCADE,null=True,blank=True)
    active=models.BooleanField(default=True)
    def __str__(self):
        return self.name
    @property
    def statuc_active(self):
        if self.active:
            return "Customer is active"
        return "Customer is not active"


    def num_profession(self):
        return self.profession.count()


class Document(models.Model):
    doc_type=(
        ('PP','Passport'),
        ('ID','Identity Card'),
        ('OT','Others')
    )
    dtype=models.CharField(max_length=2,choices=doc_type)
    doc_number=models.CharField(max_length=50)
    customer=models.ForeignKey(Customers,on_delete=models.CASCADE)
    def __str__(self):
        return self.doc_number
