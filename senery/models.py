from django.db import models

# Create your models here.


from django.db import models

class Photo(models.Model):
    photo_name = models.CharField(max_length=70)
    pub_date = models.DateField()
    path=models.CharField(max_length=100)
    def __str__(self): # __unicode__ on Python 2
        return self.full_name
# class Article(models.Model):
#     pub_date = models.DateField()
#     headline = models.CharField(max_length=200)
#     content = models.TextField()
#     reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
#     def __str__(self): # __unicode__ on Python 2
#         return self.headline