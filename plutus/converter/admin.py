from django.contrib import admin
from .models import PreparedCurrencies, SavedPairs, User

# Register your models here.
admin.site.register(PreparedCurrencies)
admin.site.register(SavedPairs)
admin.site.register(User)