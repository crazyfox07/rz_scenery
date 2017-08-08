from django.http import HttpResponse
from django.shortcuts import render, render_to_response

# Create your views here.


from django.shortcuts import render
from senery.models import Photo

import os
import datetime

ROWS=5
COLS=4
NUM=ROWS*COLS
def home(request):
    # a_list = Photo.objects.filter()
    try:
        page=int(request.GET.get('page'))
    except:
        page=1
    print(page)
    query_res=Photo.objects.order_by('-id')[(page-1)*NUM:page*NUM]
    photo_urls=['{}{}'.format('/static',photo.photo_url.split('static')[1]) for photo in query_res]
    photo_list=[(photo_urls[i],photo_urls[i+1],photo_urls[i+2],photo_urls[i+3],photo_urls[i+4]) for i in  range(0,len(photo_urls),ROWS)]
    #print(photo_list[:10])
    context = {'photo_list':photo_list,'current_page':page,'total_page':(Photo.objects.count()+NUM-1)//NUM}
    return render_to_response('home.html',context=context)

def save_to_db(request):
    import os

    for picture in os.listdir('D:/project/rz/rz_scenery/senery/static/imgs'):
        photo_name=picture
        photo_url='D:/project/rz/rz_scenery/senery/static/imgs/{}'.format(photo_name)
        pub_date=datetime.datetime.now()
        photo=Photo(photo_name=photo_name,photo_url=photo_url,pub_date=pub_date)
        photo.save()
    return HttpResponse('over   {}'.format(len(os.listdir('D:/project/rz/rz_scenery/senery/static/imgs'))))


# def save_to_mongodb(request):
#     from pymongo import MongoClient
#     conn = MongoClient('127.0.0.1', 27017)
#     my_db = conn.mydb
#     my_set = my_db.rz_scenery
#     for picture in os.listdir('D:/project/rz/rz_scenery/senery/static/imgs'):
#         photo_name = picture
#         photo_url = 'D:/project/rz/rz_scenery/senery/static/imgs/{}'.format(photo_name)
#         pub_date = datetime.datetime.now()
#         photo=Photo_Mongodb(photo_name=photo_name,photo_url=photo_url,pub_date=pub_date)
#         photo.save()
#         #my_set.insert({'photo_name':photo_name,'photo_url':photo_url,'pub_date':pub_date})
#     return HttpResponse('over   {}'.format(len(os.listdir('D:/project/rz/rz_scenery/senery/static/imgs'))))


if __name__ == '__main__':
    a='/static'
    b='/hello'
    c=os.path.join(a,b)
    print(c)