from django.contrib import admin
from .models import Trade,Strike, Transfer

admin.site.register(Trade)
admin.site.register(Strike)
admin.site.register(Transfer)