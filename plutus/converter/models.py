from django.db import models

class PreparedCurrencies(models.Model):
    from_currency = models.CharField(max_length=255)
    to_currency = models.CharField(max_length=255)
    rate = models.FloatField()

    def __str__(self):
        return f'{self.from_currency} -> {self.to_currency}: {self.rate}'

class SavedPairs(models.Model):
    user = models.EmailField(max_length=255, null=True)
    from_currency = models.CharField(max_length=255)
    to_currency = models.CharField(max_length=255)
    amount = models.FloatField()

    def __str__(self):
        return f'{self.user}: {self.from_currency} -> {self.to_currency}'


class User(models.Model):
    user = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user}'
