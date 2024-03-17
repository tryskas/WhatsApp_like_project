from django.contrib import admin
from .models import User, Texte

class UserAdmin(admin.ModelAdmin):
    list_display = ('id_utilisateur', 'pseudo', 'nom', 'prenom', 'email')
    search_fields = ('pseudo', 'nom', 'prenom', 'email')

admin.site.register(User, UserAdmin)

class TexteAdmin(admin.ModelAdmin):
    list_display = ('id_message', 'id_utilisateur', 'message')
    search_fields = ('id_utilisateur__pseudo', 'message')

admin.site.register(Texte, TexteAdmin)
