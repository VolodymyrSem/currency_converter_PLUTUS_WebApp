from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
import currencyapicom
import json
from datetime import datetime
from . import converter_methods
from .models import User, PreparedCurrencies, SavedPairs


converter_methods = converter_methods.CurrencyConverter()

def register_view(request):
    '''A view for registering a new user'''

    if request.method == 'GET':
        if 'user' in request.session:
            return redirect('my_account')
        return render(request, 'register.html')
    elif request.method == 'POST':
        user = request.POST['email']
        password = request.POST['password']
        rep_password = request.POST['rep_password']
        if User.objects.filter(user=user).values():
            context = {
                'error': 'This username already exists'
            }
        elif password != rep_password:
            context = {
                'error': "Passwords don't match"
            }
        else:
            new_user = User(user=user, password=password)
            request.session['user'] = user
            new_user.save()
            return redirect('my_account')
        return render(request, 'register.html', context)


def login_view(request):
    '''A view for logging in'''

    # pass a variable invalid_login to display/hide an error of bad login
    if request.method == 'GET':
        if 'user' in request.session:
            return redirect('my_account')

        context = {
            'invalid_login': 0
        }
        return render(request, 'login.html', context)
    elif request.method == 'POST':
        print('')
        user = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(user=user, password=password).values():
            request.session['user'] = user
            return redirect('my_account')
        else:
            context = {
                'invalid_login': 1
            }
        return render(request, 'login.html', context)

def my_account_view(request):
    '''A view for user's account'''

    converter_methods.update_rates_from_api()
    if request.method == 'POST':
        # logout: delete user from session and redirect to home page
        if 'logout' in request.POST:
            del request.session['user']
            return redirect('converter')

        # converter: redirect to converter page
        elif 'converter' in request.POST:
            return redirect('converter')

        # add new pairs to the database
        elif 'add_pairs' in request.POST:
            user = request.session['user']

            if SavedPairs.objects.filter(user=user):
                old_pairs = SavedPairs.objects.filter(user=user)
                for pair in old_pairs:
                    pair.delete()

            # get number of rows as a values associated with posting button
            number_of_pairs = int(request.POST['add_pairs'])

            # iterate through all received pairs and saving them to the database.
            # amount == 0 means user deleted current pair
            for i in range(1, number_of_pairs + 1):
                amount = request.POST[f'amount{i}']
                # print(f'Amount {i} = ', amount)
                if not amount or not float(amount):
                    # print('not amount')
                    continue

                from_currency = request.POST[f'from_currency{i}']
                to_currency = request.POST[f'to_currency{i}']

                pair = SavedPairs(
                    user=user, amount=amount, from_currency=from_currency, to_currency=to_currency
                )
                pair.save()

            # redirecting to the same page to activate 'GET' method and download all newly added pairs from the db
            return redirect('my_account')

    # download all user's saved pairs if there are any
    elif request.method == 'GET':
        if 'user' not in request.session:
            return redirect('login')

        user = request.session['user']
        pairs = SavedPairs.objects.filter(user=user)

        # add decimal part up to second digit
        for pair in pairs:
            if pair.to_currency == pair.from_currency:
                result = pair.amount
            else:
                result = converter_methods.exchange(
                    pair.from_currency,
                    pair.to_currency,
                    pair.amount
                )

            pair.amount = int(pair.amount) if pair.amount.is_integer() else pair.amount
            pair.result = converter_methods.add_2_decimal(result)

        # number of pairs is needed in js on html page
        # to create proper ids inside form tag
        context = {
            'pairs': pairs,
            'number_of_pairs': len(pairs)
        }

        # set a default pair result if there aren't any previously saved ones
        if not pairs:
            default_pair_result = converter_methods.exchange('USD', 'EUR')
            default_pair_result = converter_methods.add_2_decimal(default_pair_result)
            context['default_pair_result'] = default_pair_result

        return render(request, 'my_account.html', context)

def simple_converter_view(request):
    if request.method == 'POST':
        # create a context to load the page with django variables
        context = {}

        # get values from browser for further exchange
        if 'amount' in request.POST:
            from_currency = request.POST['from_currency']
            to_currency = request.POST['to_currency']
            amount = float(request.POST['amount'])

            # exchange
            result = converter_methods.exchange(
                from_currency, to_currency, amount
            )

            # add five decimal digits if needed
            result = converter_methods.add_5_decimal(result)

            # get rate and reverse rate for a given pair of currencies
            rate = PreparedCurrencies.objects.get(
                from_currency=from_currency,
                to_currency=to_currency
            ).rate
            reverse_rate = PreparedCurrencies.objects.get(
                from_currency=to_currency,
                to_currency=from_currency
            ).rate

            # add values to context to load the page with
            context['result_start'] = result[:-3]
            context['result_end'] = result[-3:]
            context['amount'] = request.POST['amount']
            context['from_currency'] = from_currency
            context['to_currency'] = to_currency
            context['rate'] = converter_methods.add_5_decimal(rate)
            context['reverse_rate'] = converter_methods.add_5_decimal(reverse_rate)

            return render(request, 'simple_converter.html', context)
        elif 'amount__double' in request.POST:
            from_currency__double = request.POST['from_currency__double']
            to_currency__double = request.POST['to_currency__double']
            amount__double = float(request.POST['amount__double'])
            payment__system = request.POST['payment__system']

            # exchange
            result__double = converter_methods.double_conversion(
                from_currency__double, to_currency__double, payment__system,amount__double
            )

            # add 2 decimal numbers if needed
            result__double = converter_methods.add_5_decimal(result__double)

            # add values to context to load the page with
            context['result__double_start'] = result__double[:-3]
            context['result__double_end'] = result__double[-3:]
            context['amount__double'] = request.POST['amount__double']
            context['from_currency__double'] = from_currency__double
            context['to_currency__double'] = to_currency__double
            context['payment__system'] = payment__system

            return render(request, 'simple_converter.html', context)
    else:
        return render(request, 'simple_converter.html')
