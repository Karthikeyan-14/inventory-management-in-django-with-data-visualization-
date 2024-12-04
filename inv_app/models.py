from django.db import models

# Create your models here.
class register_data(models.Model):
    reg_user=models.CharField(max_length=20)
    reg_mail=models.EmailField(max_length=40)
    reg_type=models.CharField(max_length=10,default="client")
    reg_pass=models.CharField(max_length=12)

    def __str__(self):
        return self.reg_mail


class new_query(models.Model):
    id_user=models.ForeignKey(register_data,on_delete=models.CASCADE)

    query_title=models.CharField(max_length=50)
    query_data=models.CharField(max_length=5000)
    query_date=models.DateField()
    query_status=models.CharField(max_length=20)

    def _str_(self):
        return self.id_user
    
class response_queries(models.Model):
    res_id=models.ForeignKey(register_data,on_delete=models.CASCADE)
    res_title=models.CharField(max_length=50)
    query_date=models.DateField()
    response_data=models.CharField(max_length=5000)
    resonded_date=models.DateField()

    status=models.CharField(max_length=20)

    def __str__(self):
        return self.response_data

from django.db import models
from django.db import models
from django.utils import timezone
from django.db import models
from django.utils import timezone

class TaskList(models.Model):
    CATEGORY_CHOICES = [
        ('upcoming', 'Up-coming'),
        ('ongoing', 'On-going'),
        ('hold', 'Hold'),
        ('closed', 'Closed'),
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    task_date = models.DateField()

    def __str__(self):
        return f"{self.get_category_display()}: {self.title}"

class Report(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20)
    task_date = models.DateField()
    closed_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.category}: {self.title}"