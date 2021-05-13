from django.views import View
from datetime import date
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
from .paytm_checksum import generate_checksum, verify_checksum
from .models import Registration, Transaction, TransactionDetail, Player, HorseRacing


# Create your views here.
def index(request):
    return render(request, "index.html", {'home': 'active'})


def notfound(request):
    return render(request, "404.html")


def about(request):
    return render(request, "about.html", {'other': 'active'})


def affiliate(request):
    return render(request, "affiliate.html", {'other': 'active'})


def contact(request):
    return render(request, "contact.html", {'contact': 'active'})


def faq(request):
    return render(request, "faq.html", {'other': 'active'})


def hiw(request):
    return render(request, "how-it-work.html", {'other': 'active'})


def lottery(request):
    return render(request, "lottery.html", {'lottery': 'active'})


def play(request):
    return render(request, "play.html", {'play': 'active'})


def tc(request):
    return render(request, "terms-conditions.html", {'other': 'active'})


def tcd(request):
    return render(request, "terms-conditions-details.html", {'other': 'active'})


def tournaments(request):
    try:
        g_no = HorseRacing.objects.latest('timestamp')
        if g_no.open:
            g_no = g_no.game_no
        else:
            g_no = g_no.game_no
            g_no += 1

    except HorseRacing.DoesNotExist:
        h = HorseRacing(game_no=1)
        h.save()
        g_no = 1
    d = date.today().strftime("%Y%m%d")
    h = str(g_no)
    d += h


    return render(request, "tournaments.html", {'play': 'active', "race_no": d})


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


def redirect(request):
    return render(request, "payments/redirect.html")


def initiate_payment(request):
    if request.method == "GET":
        return redirect('tournaments')

    amount = int(request.POST['amount'])
    horse_name = request.POST['name']

    user = request.user
    transaction = Transaction.objects.create(made_by=user, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    # setting values for horse race and player model
    # for horse racing model
    horse_race = HorseRacing.objects.latest('timestamp')
    betted_horse_name = ''
    if horse_race.open:
        if horse_name == "horse1":
            total_amount = horse_race.horse1
            betted_horse_name = 'Brick Red'
        elif horse_name == "horse2":
            total_amount = horse_race.horse2
            betted_horse_name = 'Violet'
        else:
            total_amount = horse_race.horse3
            betted_horse_name = 'Red'

        total_amount += amount
        horse_race.horse1 = total_amount
        horse_race.save()

    # for player model
    player = Player(player=user, game=horse_race, bet_on=betted_horse_name, amount=amount)
    player.save()


    params = {
        'MID': settings.PAYTM_MERCHANT_ID,
        'ORDER_ID': str(transaction.order_id),
        'CUST_ID': 'elahifaiz00@gmail.com',#str(transaction.made_by.email),
        'TXN_AMOUNT': str(transaction.amount),
        'CHANNEL_ID': settings.PAYTM_CHANNEL_ID,
        'WEBSITE': settings.PAYTM_WEBSITE,
        # ('EMAIL': request.user.email),
        # ('MOBILE_N0': '9911223388'),
        'INDUSTRY_TYPE_ID': settings.PAYTM_INDUSTRY_TYPE_ID,
        'CALLBACK_URL': 'http://'+get_current_site(request).domain+'/callback',
        # ('PAYMENT_MODE_ONLY', 'NO'),
    }
    checksum = generate_checksum(params, merchant_key)

    transaction.checksum = checksum
    transaction.save()
    params['CHECKSUMHASH'] = checksum
    return render(request, 'payments/redirect.html', context=params)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'payments/callback.html', context=received_data)
        return render(request, 'payments/callback.html', context=received_data)

