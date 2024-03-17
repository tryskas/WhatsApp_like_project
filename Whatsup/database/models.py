from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

# modele utilisateur personnalise
class User(AbstractUser):
    id_utilisateur = models.AutoField(primary_key=True)
    pseudo = models.CharField(max_length=30, unique=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)

    @classmethod
    def create_user_with_pseudo(cls, nom, prenom, pseudo, password, **extra_fields):
        user = cls(username=pseudo, pseudo=pseudo, nom=nom, last_name=nom, prenom=prenom, first_name=prenom, **extra_fields)
        user.set_password(password)
        user.save()
        return user

# Modele pour stocker des textes associes à un utilisateur
class Texte(models.Model):
    id_utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    id_message = models.AutoField(primary_key=True)
    message = models.TextField()

# modèle pour stocker les messages dans une salle de chat
class ChatMessage(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    room = models.ForeignKey('ChatRoom', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f'{self.user.username} ({self.timestamp}): {self.content}'

# modele pour representer une salle de chat
class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(User, related_name='chat_rooms')
    messages = models.ManyToManyField('ChatMessage', related_name='chat_room', blank=True)
    moderator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='moderated_rooms')
    
    def __str__(self):
        return self.name

# modele pour stocker les messages génériques dans une salle de chat
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
