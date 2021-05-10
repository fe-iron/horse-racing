from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.views import View

from .models import Registration
from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    return render(request, "index.html")


def notfound(request):
    return render(request, "404.html")


def about(request):
    return render(request, "about.html")


def affiliate(request):
    return render(request, "affiliate.html")


def contact(request):
    return render(request, "contact.html")


def faq(request):
    return render(request, "faq.html")


def hiw(request):
    return render(request, "how-it-work.html")


def lottery(request):
    return render(request, "lottery.html")


def play(request):
    return render(request, "play.html")


def tc(request):
    return render(request, "terms-conditions.html")


def tcd(request):
    return render(request, "terms-conditions-details.html")


def tournaments(request):
    return render(request, "tournaments.html")


def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        mob = request.POST.get('mob', None)
        password = request.POST.get('password', None)
        referral = request.POST.get('referral', None)
        try:
            user = User.objects.get(username=mob)
            messages.error(request, "Username has already been taken. Please try another")
            return render(request, 'signup.html')
        except User.DoesNotExist:

            new_user = User.objects.create_user(username=mob, password=password, first_name=name)

            reg = Registration(referral=referral, phone_number=mob, full_name=name, user=new_user)
            reg.save()
            # backend argument required cause we are making the ability to LOGIN by email.
            # Remember, I only extended the User model.
            auth.login(request, new_user)
            return redirect("tournaments")
    else:
        return render(request, "signup.html", {"referral": "DEFAULT000"})


def join(request, referral):
    return render(request, "signup.html", {"referral": referral})


def referral(request):
    pass


def login(request):
    if request.method == 'POST':
        mob = request.POST.get('mob', None)
        password = request.POST.get('password', None)

        user = auth.authenticate(username=mob, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("tournaments")

        messages.error(request, "Account Does not Exists!")
    return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect("/")