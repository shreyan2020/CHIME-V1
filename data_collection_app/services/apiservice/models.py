from django.db import models

# Create your models here.

class Consent(models.Model):
    Id = models.AutoField(primary_key=True)
    WorkerId = models.CharField(max_length=300)
    Consent = models.BooleanField()
    DateSubmitted = models.DateTimeField(auto_now_add=True, blank=True, null=True)

class Images(models.Model):
    Id = models.AutoField(primary_key=True)
    ImageName = models.CharField(max_length=100)
    Pred1Label = models.CharField(max_length=100, null=True)
    Pred1Score = models.IntegerField(null=True)
    Pred2Label = models.CharField(max_length=100, null=True)
    Pred2Score = models.IntegerField(null=True)
    Pred3Label = models.CharField(max_length=100, null=True)
    Pred3Score = models.IntegerField(null=True)
    ModelName = models.CharField(max_length=100)
    Status = models.IntegerField(default=0)
    Iteration = models.IntegerField(default=0)
    DateFetched = models.DateTimeField(blank=True, null=True)

class Annotations(models.Model):
    Id = models.AutoField(primary_key=True)
    ImageId = models.IntegerField()
    ObjectName = models.CharField(max_length=300)
    PartObject = models.CharField(max_length=300, blank=True, null=True)
    Color = models.CharField(max_length=100)
    ParentObject = models.CharField(max_length=300, null=True)
    Shape = models.CharField(max_length=100,blank=True, null=True)
    WorkerId = models.CharField(max_length=300)
    DateSubmitted = models.DateTimeField(auto_now_add=True, blank=True, null=True)
