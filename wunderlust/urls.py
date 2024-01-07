
from django.contrib import admin
from django.urls import path
from myfirst_app import views
from django.urls import include

from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', include('myfirst_app.urls')),
    path('admin/', admin.site.urls),
]


urlpatterns += staticfiles_urlpatterns()