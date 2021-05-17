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
    path('profile', views.profile, name="profile"),
    path('contact', views.contact, name="contact"),
    path('subscribe', views.subscribe, name="subscribe"),
    path('notfound', views.notfound, name="notfound"),
    path('join_game', views.join_game, name="join_game"),
    path('start_race', views.start_race, name="start_race"),
    path('set_result', views.set_result, name="set_result"),
    path('callback', views.callback, name="callback"),
    path('how-it-work', views.hiw, name="how-it-work"),
    path('affiliate', views.affiliate, name="affiliate"),
    path('referral', views.referral, name="affliate"),
    path('join<str:referral>', views.join, name="signup"),
    path('tournaments', views.tournaments, name="tournaments"),
    path('terms-conditions', views.tc, name="terms-conditions"),
    path('initiate_payment', views.initiate_payment, name="initiate_payment"),
    path('terms-conditions-details', views.tcd, name="terms-conditions-details"),
]
