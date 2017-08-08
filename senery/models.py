from django.db import models

# Create your models here.


from django.db import models


class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    photo_name = models.CharField(max_length=64)
    photo_url=models.CharField(max_length=128)
    pub_date = models.DateField()



# class Article(models.Model):
#     pub_date = models.DateField()
#     headline = models.CharField(max_length=200)
#     content = models.TextField()
#     reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
#     def __str__(self): # __unicode__ on Python 2
#         return self.headline