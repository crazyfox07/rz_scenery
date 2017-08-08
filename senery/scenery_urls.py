# -*- coding:utf-8 -*-
"""
File Name: scenery_urls
Version:
Description:
Author: liuxuewen
Date: 2017/8/7 16:43
"""
from django.conf.urls import url, include
from django.contrib import admin

from senery.views import home,save_to_db

urlpatterns = [
    url(r'^save/',save_to_db),

]