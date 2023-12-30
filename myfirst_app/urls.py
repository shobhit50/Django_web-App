from django.urls import path
from myfirst_app import views





urlpatterns = [
    path('', views.index, name='index'),#listings_data
    path('new', views.new, name='new'),
    
    path('newPost', views.newPost, name='newPost'),
     path('search', views.search, name='search'),
    path('show/<int:listing_id>/', views.show, name='show'),
    path('edit/<int:listing_id>/', views.edit, name='edit'),
    path('edit/update/<int:listing_id>/', views.update, name='update'),
    path('delete/<int:listing_id>/', views.delete, name='delete'),
    path('Reviews/<int:listing_id>/', views.Reviews, name='Reviews'),
    path('deleteReview/<int:listing_id>/<int:review_id>/', views.deleteReview, name='deleteReview'),
    path('singup', views.singup, name='singup'),
    path('createUser', views.createUser, name='createUser'),
    path('login', views.loginform, name='loginform'),
    path('loginHandler', views.loginHandler, name='loginHandler'),
    path('logoutHandler', views.logoutHandler, name='logoutHandler'),
    path('changePassword', views.changePassword, name='changePassword'),
    

]

