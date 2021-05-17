import string
import datetime
import random
from django.conf import settings
from django.http import JsonResponse
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from .paytm_checksum import generate_checksum, verify_checksum
from .models import Registration, Transaction, TransactionDetail, Player, HorseRacing, GamePointHistory, GamePlayHistory, \
    Subscriber, Referral, CommissionHistory


time_left = datetime.datetime.now() + datetime.timedelta(minutes=4)

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


@login_required(login_url='/login')
def tournaments(request):
    global time_left
    now = datetime.datetime.now()
    time_diff = str(time_left - now)
    # print("global: ",time_left)
    # print("now: ",time_diff)
    if time_diff[0:5] == '-1 da':
        time_left = datetime.datetime.now() + datetime.timedelta(minutes=4)
        current_second = 240
        milli_sec = 240000
    else:
        current_minute = time_diff[2:4]
        current_second = time_diff[5:7]
        if '0' in current_second:
            current_second = current_second[1]
        elif '0' in current_minute:
            current_minute = current_minute[1]

        current_second = (int(current_minute) * 60) + int(current_second)
        milli_sec = current_second * 1000
    # print("minute ",current_minute)
    # print("second ",current_second)
    try:
        user = request.user
        g_no = HorseRacing.objects.latest('timestamp')
        if g_no.open:
            g_no = g_no.game_no
        else:
            g_no = g_no.game_no
            g_no += 1
            d = datetime.date.today().strftime("%Y%m%d")
            h = str(g_no)
            d += h
            g_no = int(d)
            h_race = HorseRacing(game_no=g_no)
            h_race.save()

    except HorseRacing.DoesNotExist:
        g_no = 1
        d = datetime.date.today().strftime("%Y%m%d")
        h = str(g_no)
        d += h
        g_no = int(d)
        h = HorseRacing(game_no=g_no)
        h.save()

    if Registration.objects.filter(user=user).exists():
        bal = Registration.objects.get(user=request.user)
        win_bal = bal.win_balance
        bal = bal.balance

    d = str(g_no)
    cond = ['-time']
    all_bets = GamePlayHistory.objects.all().order_by(*cond)
    my_bets = GamePlayHistory.objects.filter(player=user).order_by(*cond)

    context = {
        'play': 'active',
        "race_no": d,
        "bal": bal,
        "second_left": current_second,
        "milli_sec_left": milli_sec,
        "win_bal": win_bal,
        "all_bets": all_bets,
        "my_bets": my_bets,
    }
    return render(request, "tournaments.html", context)


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

            if referral == "DEFAULT000":
                pass
            else:
                if Referral.objects.filter(referral=referral).exists():
                    ref = Referral.objects.get(referral=referral)
                    ref.assign_to = new_user
                    ref.save()

                    # extra bonus
                    reg.balance = '30'
                    reg.save()

            auth.login(request, new_user)
            return redirect("tournaments")
    else:
        return render(request, "signup.html", {"referral": "DEFAULT000"})


def join(request, referral):
    return render(request, "signup.html", {"referral": referral})


@login_required(login_url="/login")
def referral(request):
    user = request.user
    if Referral.objects.filter(created_by=user).exists():
        referral = Referral.objects.get(created_by=user).referral
    else:
        lower_alphabet = list(string.ascii_lowercase)
        upper_alphabet = list(string.ascii_uppercase)
        hex_digits = list(string.hexdigits)
        digits = list(string.digits)

        characters = lower_alphabet + upper_alphabet + hex_digits + digits
        referral = ''
        for i in range(10):
            referral += random.choice(characters)

        ref = Referral(referral=referral, created_by=user)
        ref.save()

    data = 'Hey, Join with my referral link to get instant 30 rupees to Play Horse Racing and earn real money Here is ' \
           'the direct link to get the real money '
    referral_url = 'http://' + get_current_site(request).domain + '/join' + referral
    data += referral_url
    return JsonResponse({"result": referral_url, "referral": referral, "data": data}, status=200)


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


def initiate_payment(request):
    if request.method == "GET":
        return redirect('tournaments')

    amount = int(request.POST['amount'])

    user = request.user
    transaction = Transaction.objects.create(made_by=user, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = {
        'MID': settings.PAYTM_MERCHANT_ID,
        'ORDER_ID': str(transaction.order_id),
        'CUST_ID': 'fe-iron9091@gmail.com', # str(transaction.made_by.email),
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

        txn = Transaction.objects.get(order_id=paytm_params['ORDERID'])

        if paytm_params['STATUS'] == 'TXN_SUCCESS':
            txn_detail = TransactionDetail(made_by=txn, transaction_id=paytm_params['TXNID'],
                                           bank_txn_id=paytm_params['BANKTXNID'], currency=paytm_params['CURRENCY'],
                                           status=paytm_params['STATUS'], gateway_name=paytm_params['GATEWAYNAME'],
                                           bank_name=paytm_params['BANKNAME'], payment_mode=paytm_params['PAYMENTMODE'],
                                           user=txn.made_by)
            txn_detail.save()
            messages.info(request, "Recharged Successfully! Wallet Updated")

            user = txn.made_by
            reg = Registration.objects.get(user=user)
            bal = float(reg.balance)
            bal += float(paytm_params['TXNAMOUNT'])
            reg.balance = str(bal)
            reg.save()

        else:
            txn_detail = TransactionDetail(made_by=txn, transaction_id=paytm_params['TXNID'],
                                           bank_txn_id=paytm_params['BANKTXNID'], currency=paytm_params['CURRENCY'],
                                           status=paytm_params['STATUS'], gateway_name=paytm_params['GATEWAYNAME'],
                                           bank_name=paytm_params['BANKNAME'], payment_mode=paytm_params['PAYMENTMODE'],
                                           user=txn.made_by)
            txn_detail.save()
            messages.info(request, "Recharge Unsuccessfull! Try Again")

        return redirect("tournaments")


@csrf_exempt
def join_game(request):
    if request.is_ajax and request.method == "POST":
        user = request.user
        horse_name = request.POST.get('horse_name')
        amount = int(request.POST.get('amount'))
        # setting values for horse race and player model
        # for horse racing model
        horse_race = HorseRacing.objects.latest('timestamp')
        betted_horse_name = ''

        if horse_race.open:
            if horse_name == "horse1":
                total_amount = horse_race.horse1
                total_amount += amount
                betted_horse_name = 'Brick Red'
                horse_race.horse1 = total_amount

            elif horse_name == "horse2":
                total_amount = horse_race.horse2
                total_amount += amount
                horse_race.horse2 = total_amount
                betted_horse_name = 'Violet'

            else:
                total_amount = horse_race.horse3
                total_amount += amount
                horse_race.horse3 = total_amount
                betted_horse_name = 'Red'

            horse_race.save()
        else:
            return JsonResponse({"msg": "Wait for the game to over then try again!"}, status=200)

        # for player model
        player = Player(player=user, game=horse_race, bet_on=betted_horse_name, amount=amount)
        player.save()

        # deducting balance from users account
        reg_user = Registration.objects.get(user=user)
        reg_user_bal = float(reg_user.balance)
        reg_user_bal -= amount
        reg_user.balance = str(reg_user_bal)
        reg_user.save()

        # making history
        gph = GamePointHistory(amount=amount, made_by=user, balance=int(reg_user_bal))
        gph.save()
        return JsonResponse({"msg": True, "bal": reg_user_bal}, status=200)

    return JsonResponse({"msg": False}, status=200)


def start_race(request):
    if request.is_ajax and request.method == 'GET':
        horse_race = HorseRacing.objects.latest('timestamp')
        winner = None
        horse = ''
        if horse_race.open:
            winner = '30'
            h1 = horse_race.horse1
            h2 = horse_race.horse2
            h3 = horse_race.horse3

            if h3 <= h1 and h3 <= h2:
                horse = 'horse3'
                horse_race.winner = 'horse3'
            elif h2 <= h1 and h2 <= h3:
                horse = 'horse2'
                horse_race.winner = 'horse2'
            else:
                horse = 'horse1'
                horse_race.winner = 'horse1'
            horse_race.save()
            return JsonResponse({"winner": winner, "horse": horse}, status=200)

    return JsonResponse({"winner": False}, status=200)


@csrf_exempt
def set_result(request):
    if request.is_ajax and request.method == "POST":
        selected = request.POST.get('selected', None)
        winner = request.POST.get('winner', None)

        horse_race = HorseRacing.objects.latest('timestamp')
        user = request.user
        try:
            player = Player.objects.filter(player=user, game=horse_race)[0]
        except IndexError:
            return JsonResponse({'result': False}, status=200)

        reg_user = Registration.objects.filter(user=user)[0]
        amount = player.amount

        if winner == 'horse1':
            horse_race.winner = 'horse1'
        elif winner == 'horse2':
            horse_race.winner = 'horse2'
        elif winner == 'horse3':
            horse_race.winner = 'horse3'
        horse_race.open = False
        horse_race.save()
        total_betting = 0
        total_betting += horse_race.horse1
        total_betting += horse_race.horse2
        total_betting += horse_race.horse3

        if winner == selected:
            player.result = 'Win'
            reg_user.win_balance = str(amount * 2)
            reg_user.save()
        else:
            player.result = 'Lose'

        player.save()

        game_history = GamePlayHistory(amount=player.amount, which_horse=selected, result=player.result, game=horse_race,
                                       player=user, total_bet=total_betting)
        game_history.save()

        # setting referral bonus
        if player.result == 'Win':
            reff = reg_user.referral
            if reff == 'DDEFAULT000':
                pass
            else:
                if Referral.objects.filter(assign_to=user).exists():
                    reff = Referral.objects.get(assign_to=user)
                    awarde_user = reff.created_by
                    awarde_user = User.objects.filter(username=user)[0]
                    awarde_user = Registration.objects.filter(user=awarde_user)[0]
                    commission = float(100) * (10.0 / float(amount))  # user's commission
                    w_bal = float(awarde_user.win_balance)
                    w_bal += commission
                    commission = str(w_bal)
                    awarde_user.win_balance = commission
                    awarde_user.save()
                    # setting history
                    com_history = CommissionHistory(amount=player.amount, you_got=commission, which_horse=selected,
                                                    referred_user=user, user=awarde_user)
                    com_history.save()

        return JsonResponse({"result": True}, status=200)
    return JsonResponse({"result": False}, status=200)


@login_required(login_url='/login')
def profile(request):
    user = request.user
    game_his = GamePlayHistory.objects.filter(player=user)
    transaction = TransactionDetail.objects.filter(user=user)
    wal = GamePointHistory.objects.filter(made_by=user).order_by('-date', '-time')
    user = Registration.objects.filter(user=user)
    ref = CommissionHistory.objects.filter(user=user[0]).order_by('-timestamp')
    param = {
        'user': user,
        "game_his": game_his,
        "wallet": wal,
        "transaction": transaction,
        "referred": ref,
    }
    return render(request, "profile.html", param)


def subscribe(request):
    email = request.POST['email']
    sub = Subscriber(contact=email)
    sub.save()
    return redirect("/")