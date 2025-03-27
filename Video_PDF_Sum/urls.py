
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homePage),
    path('summarize/youtube/', views.summarize_youtube),

]
