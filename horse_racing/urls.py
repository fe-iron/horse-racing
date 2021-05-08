from django.urls import path
from . import views

urlpatterns = [
    path('faq', views.faq, name="faq"),
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('play', views.play, name="play"),
    path('about', views.about, name="about"),
    path('how-it-work', views.hiw, name="how-it-work"),
    path('terms-conditions', views.tc, name="terms-conditions"),
    path('contact', views.contact, name="contact"),
    path('lottery', views.lottery, name="lottery"),
    path('notfound', views.notfound, name="notfound"),
    path('tournaments', views.tournaments, name="tournaments"),
    path('affiliate', views.affiliate, name="affiliate"),
    path('terms-conditions-details', views.tcd, name="terms-conditions-details"),
]
