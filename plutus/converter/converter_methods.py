import pandas as pd
import colorama
import os
import urllib
import json
import currencyapicom
from datetime import datetime
from .models import PreparedCurrencies

# upload table of all currencies in DataFrame
url_currencies_short = 'https://drive.google.com/file/d/1LFQO13AVf4U0LXOzKEycRYL0gKx3tv1m/'.split('/')[-2]
url_currencies_short = 'https://drive.google.com/uc?id=' + url_currencies_short
CURRENCIES_SHORT = pd.read_csv(url_currencies_short)

# The same, but upload european currencies only to check in CurrencyConverter.double_conversion method
url_europe_currencies = \
'https://drive.google.com/file/d/1JRSbtOFZ54PPCo55qwA4FfPKjw31NRY5/view?usp=share_link'.split('/')[-2]
url_europe_currencies = 'https://drive.google.com/uc?id=' + url_europe_currencies
EUROPE_CURRENCIES = pd.read_csv(url_europe_currencies)

# absolute address of this module
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# API key for accessing data
API_KEY = 'YkvsDr8AFiIpgxr5tLJPPnDQskeez3xU3JJNLgyG'

class ExchangeError(BaseException):
    '''Class for exceptions used in the program'''

    pass


class CurrencyConverter():
    """
    Contains methods for getting and computing results of user's request.
    Based on class Utilities because of using progress_bar method in it

    Methods
    -------
    exchange(from_currency, to_currency, amount=1)
        Returns rate for requested pair of currencies.
    double_conversion(from_currency, to_currency, card_type, amount=1)
        Returns amount to pay for amount of the target currency.
        Uses predefined algorithms for computing result due to the issues
        with a possibility of double/triple conversion rate by card systems.
    update_rates()
        Updates rates for pairs of currencies.
    add_5_decimal(number)
        Adds five decimal digits to inputted number
    add_2_decimal(number)
        Adds two decimal digits to inputted number
    update_rates_from_api()
        Updates PreparedCurrencies table in Django model PreparedCurrencies.
    exchange_using_usd(rates_from_usd)
        Iterates through all currencies and exchange them one by one using USD rate from API response.
    progress_bar(progress, total, color)
        Prints the progress bar
    """

    def exchange(self, from_currency: str, to_currency: str, amount=1) -> float:
        """
        Returns rate for a pair of currencies.

        Parameters
        ----------
        from_currency : str
            currency provided as currency to be exchanged by another one; owned currency
        to_currency : str
            target currency
        amount : int, optional
            amount of the owned currency

        Raises
        ------
        ExchangeError
            Raises in cases of not presence of the internal database's table (or it's emptiness)
            and as a base case for all other exceptions.
        """

        try:
            rate = PreparedCurrencies.objects.get(from_currency=from_currency, to_currency=to_currency).rate
            data = rate * amount
            return float(data)
        except AttributeError:
            raise ExchangeError('\nBad connection with the server.')
        except TypeError:
            raise ExchangeError('Your database is empty or doesn\'t exist.' + \
                                 '\nRestart the program and choose "Refresh your database".')
        except:
            raise ExchangeError('\nUnexpected error occurred.')

    def double_conversion(self, from_currency: str, to_currency: str, card_type: str, amount=1) -> float:
        """
        Returns amount of an owned currency needed to pay for amount of a target currency.
        Result depends on a card system, which may have a consequence of double/triple conversion.
        Uses CurrencyConverter.exchange method as a base method for exchanging currencies.

        Parameters
        ----------
        from_currency : str
            currency provided as currency to be exchanged by another one; owned currency
        to_currency : str
            target currency
        card_type : str
            card system for the operation. May be 'MC' or 'VISA'
        amount : int, optional
            amount of the owned currency
        """

        if card_type == 'MC' and to_currency not in EUROPE_CURRENCIES['AlphabeticCode'].unique():
            if from_currency == 'EUR':
                dc_from_EUR = amount
            else:
                dc_from_EUR = (amount / self.exchange('EUR', to_currency)) * 1.02
            result = (dc_from_EUR / self.exchange(from_currency, 'EUR')) * 1.02

        elif card_type == 'MC':
            price = self.exchange(from_currency, to_currency)
            result = (amount / price) * 1.02

        elif card_type == 'VISA' and to_currency in EUROPE_CURRENCIES['AlphabeticCode'].unique():
            if to_currency != 'EUR':
                dc_from_EUR = (amount / self.exchange('EUR', to_currency)) * 1.03
            else:
                dc_from_EUR = amount
            dc_from_USD = (dc_from_EUR / self.exchange('USD', 'EUR')) * 1.03
            if from_currency != 'USD':
                result = (dc_from_USD / self.exchange(from_currency, 'USD')) * 1.03
            else:
                result = dc_from_USD

        elif card_type == 'VISA':
            if to_currency != 'USD':
                dc_from_USD = (amount / self.exchange('USD', to_currency)) * 1.03
            else:
                dc_from_USD = amount
            if from_currency != 'USD':
                result = (dc_from_USD / self.exchange(from_currency, 'USD')) * 1.03
            else:
                result = dc_from_USD

        return float(result)

    def add_5_decimal(self, number: float) -> str:
        '''
        Adds five digits after decimal

        Parameters
        ----------
        number : float
            inputted number that must be formatted
        '''

        return f'{number:.5f}'

    def add_2_decimal(self, number: float) -> str:
        '''
        Adds two digits after decimal

        Parameters
        ----------
        number : float
            inputted number that must be formatted
        '''
        if type(number) not in (float, int):
            return number
        return f'{number:.2f}'


    def update_rates_from_api(self):
        '''
        Updates PreparedCurrencies table in the db.

        Check whether it is needed to make an update (recommended max. once a day)

        First, deletes all records from the table.
        Then, downloads json-typed data from the API ("USD - X" pairs) and backups it to json file.

        To get all other pairs from "USD - X" pairs, json-formatted data is passed to function exchange_using_usd().
        '''

        # check whether it is needed to update the db (recommended max. once a day)
        with open('backup_rates_from_usd.json') as backup_file:
            backup = json.load(backup_file)
            if datetime.timestamp(datetime.now()) - backup['timestamp']< 86400:
                # print('It is no need to refresh the db.')
                # rates_from_usd = backup
                return
            else:
                # download 'USD - X' pairs from the API
                api_object = currencyapicom.Client(API_KEY)
                rates_from_usd = api_object.latest(
                    base_currency='USD',
                    currencies=[currency for currency in CURRENCIES_SHORT['AlphabeticCode']])

                # backup downloaded data in case of an error
                with open('backup_rates_from_usd.json', 'wt') as json_file:
                    time_9_oclock = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
                    rates_from_usd['timestamp'] = datetime.timestamp(time_9_oclock)
                    json.dump(rates_from_usd, json_file)

        # delete all outdated records
        PreparedCurrencies.objects.all().delete()

        # call function to make pairs for all other currencies
        self.exchange_using_usd(rates_from_usd)

    def exchange_using_usd(self, rates_from_usd: dict):
        '''
        Iterates through all currencies and exchange them one by one using USD rate.
        Takes amount of two currencies expressed in USD and divides them one by one to get a rate for the pair.
        Changes progress bar after every nested loop iteration.

        Parameters
        ----------
        rates_from_usd : dict
            response from the API with values of USD expressed in other currencies
        '''

        # variables needed to display progress bar
        total = len(rates_from_usd['data']) * (len(rates_from_usd['data']) + 1)
        progress = 0

        self.progress_bar(progress, total)
        for base_currency in rates_from_usd['data'].items():
            for target_currency in rates_from_usd['data'].items():
                if base_currency[0] == target_currency[0]:
                    continue

                rate = round(target_currency[1]['value'] / base_currency[1]['value'], 8)
                pair = PreparedCurrencies(
                    from_currency=base_currency[0],
                    to_currency=target_currency[0],
                    rate=rate
                )
                pair.save()

                progress += 1
                self.progress_bar(progress, total)

        # pass to progress bar numbers to have 100% completion
        # in case of wrong calculation of the total amount of iterations
        self.progress_bar(1, 1)

    def progress_bar(self, progress: int, total: int, color=colorama.Fore.YELLOW):
        """
        Prints the progress bar

        Parameters
        ----------
        progress : int
            actual progress of the progress bar
        total : int
            total amount of calls needed to finish the progress bar
        color : colorama.ansi.AnsiFore, optional
            color in which the progress bar is repainted
        """

        percent = 100 * (progress / total)
        count = int(percent // 2)
        bar = '█' * count + '■' * (50 - count)
        print(color + f'\r|{bar}| {percent:.2f}%', end='\r')
        if progress == total:
            print(colorama.Fore.GREEN + f'\r|{bar}| {percent:.2f}%')
            print(colorama.Fore.RESET)