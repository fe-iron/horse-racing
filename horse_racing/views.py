from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.views import View
import pyrebase

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

            # backend argument required cause we are making the ability to LOGIN by email.
            # Remember, I only extended the User model.
            auth.login(request, new_user)
            return redirect("/")
    else:
        return render(request, "signup.html", {"referral": "DEFAULT000"})


def login(request):
    if request.method == 'POST':
        mob = request.POST.get('mob', None)
        password = request.POST.get('password', None)

        user = auth.authenticate(username=mob, password=password)
        if user is not None:
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("/")

        messages.error(request, "Account Does not Exists!")
    return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect("/")


# This class returns the string needed to generate the key
class GenerateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"


class GetPhoneNumberRegistered(View):
    # Get to Create a call for OTP
    @staticmethod
    def get(request, phone):
        try:
            Mobile = phoneModel.objects.get(Mobile=phone)  # if Mobile already exists the take this else create New One
        except ObjectDoesNotExist:
            phoneModel.objects.create(
                Mobile=phone,
            )
            Mobile = phoneModel.objects.get(Mobile=phone)  # user Newly created Model
        Mobile.counter += 1  # Update Counter At every Call
        Mobile.save()  # Save the data
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
        OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created
        print(OTP.at(Mobile.counter))
        # Using Multi-Threading send the OTP Using Messaging Services like Twilio or Fast2sms
        return Response({"OTP": OTP.at(Mobile.counter)}, status=200)  # Just for demonstration

    # This Method verifies the OTP
    @staticmethod
    def post(request, phone):
        try:
            Mobile = phoneModel.objects.get(Mobile=phone)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)  # False Call

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
        OTP = pyotp.HOTP(key)  # HOTP Model
        if OTP.verify(request.data["otp"], Mobile.counter):  # Verifying the OTP
            Mobile.isVerified = True
            Mobile.save()
            return Response("You are authorised", status=200)
        return Response("OTP is wrong", status=400)




# firebase = pyrebase.initialize_app(config)
# auth_firebase = firebase.auth()
