from django.contrib import admin

from .models import Nodetype


@admin.register(Nodetype)
class NodetypeAdmin(admin.ModelAdmin):
    pass
