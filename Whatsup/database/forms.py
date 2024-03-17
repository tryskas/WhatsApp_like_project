from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User, ChatRoom

# formulaire de creation d utilisateur
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['pseudo', 'nom', 'prenom', 'password1', 'password2']

        # Validation personnalisée pour le champ password1
        def clean_password1(self):
            password1 = self.cleaned_data.get('password1')
            return password1

# formulaire de creation de message dans une salle de chat
class CreateMessageForm(forms.Form):
    content = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Votre message'}))

# formulaire de creation de salle de chat
class CreateChatRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['name', 'users', 'moderator']

# formulaire de salle de chat
class ChatRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['name', 'users']
