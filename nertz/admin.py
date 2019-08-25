from django.contrib import admin

# Register your models here.
from nertz.models import *

admin.site.register(Room)
admin.site.register(Game)
admin.site.register(Round)
admin.site.register(Hand)
