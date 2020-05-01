from django.urls import path, include
from django.contrib.auth import views
from django.conf.urls import include, url


from . import views

app_name = 'DictIt'
urlpatterns = [
    path('list/', views.lists, name = 'lists'),
    path('', views.index, name = 'index'),
    path('list/<int:quest_id>/', views.detail, name = 'detail'),
    path('list/<int:quest_id>/answer', views.answer, name = 'answer'),
    path('user_data/', views.user_data, name = 'user_data'),
]

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
  #  path('accounts/login/', views.LoginView.as_view()),
    
    ]