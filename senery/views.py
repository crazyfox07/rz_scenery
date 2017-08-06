from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from senery.models import Photo
def home(request):
    # a_list = Photo.objects.filter()
    context = {'photo_list': range(10)}
    # return render(request, 'news/year_archive.html', context)
    return render(request,template_name='home.html',context=context)



