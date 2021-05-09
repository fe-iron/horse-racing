from django.urls import path
from . import views

urlpatterns = [
    path('faq', views.faq, name="faq"),
    path('', views.index, name="index"),
    path('play', views.play, name="play"),
    path('login', views.login, name="login"),
    path('about', views.about, name="about"),
    path('logout', views.logout, name="logout"),
    path('signup', views.signup, name="signup"),
    path('lottery', views.lottery, name="lottery"),
    path('contact', views.contact, name="contact"),
    path('notfound', views.notfound, name="notfound"),
    path('how-it-work', views.hiw, name="how-it-work"),
    path('affiliate', views.affiliate, name="affiliate"),
    path('referral', views.referral, name="affliate"),
    path('join<str:referral>', views.join, name="signup"),
    path('tournaments', views.tournaments, name="tournaments"),
    path('terms-conditions', views.tc, name="terms-conditions"),
    path('terms-conditions-details', views.tcd, name="terms-conditions-details"),
]
