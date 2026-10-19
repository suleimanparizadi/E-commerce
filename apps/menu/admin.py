from django.contrib import admin
from apps.menu.models import menu_model


admin.site.register(menu_model.QRMenu)
admin.site.register(menu_model.MenuItem)
admin.site.register(menu_model.MenuSection)