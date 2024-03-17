from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, ChatRoom, ChatMessage
from .forms import CreateUserForm, CreateMessageForm, ChatRoomForm, CreateChatRoomForm
from django.http import JsonResponse, StreamingHttpResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_POST
import json
import time
from django.views.decorators.csrf import csrf_exempt

# page affichant la liste des conversations pour l'utilisateur connecté
@login_required(login_url='my_login_view')
def conversation_list(request):

    # récupère toutes les salles de conversation
    chat_rooms = ChatRoom.objects.all()
    return render(request, 'conversation_list.html', {'chat_rooms': chat_rooms})

# création d'un nouvel utilisateur
def create_user(request):

    # récupère tous les utilisateurs
    users = User.objects.all()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():

            # récupère les informations du formulaire
            nom = request.POST.get('nom')
            prenom = request.POST.get('prenom')
            pseudo = request.POST.get('pseudo')
            password = request.POST.get('password1')

            # crée un nouvel utilisateur avec des informations spécifiées
            user = User.create_user_with_pseudo(nom, prenom, pseudo, password)
            return redirect('my_login_view')

    else:
        form = CreateUserForm()

    return render(request, 'create_user.html', {'users': users, 'form': form})

# affichage de la liste des utilisateurs pour l'utilisateur connecté
@login_required(login_url='my_login_view')
def user_list(request):

    # récupère tous les utilisateurs
    users = User.objects.all()
    form = CreateUserForm()
    return render(request, 'user_list.html', {'users': users, 'form': form})

# affichage des détails d'une salle de conversation spécifique
@login_required(login_url='my_login_view')
def chat_room_detail(request, room_id):
    chat_room = get_object_or_404(ChatRoom, id=room_id)
    messages = ChatMessage.objects.filter(room=chat_room)
    user_chat_rooms = request.user.chat_rooms.all()

    current_user = request.user
    user_chat_rooms = ChatRoom.objects.filter(users=current_user)
    context = {}

    if request.method == 'POST':
        chat_room_form = CreateChatRoomForm(request.POST)
        if chat_room_form.is_valid():
            chat_room = chat_room_form.save()
            chat_room.users.add(current_user)
            return redirect('my_view')
    else:
        chat_room_form = CreateChatRoomForm()

    if request.user in chat_room.users.all():
        users = chat_room.users.all()
        is_moderator = chat_room.moderator == request.user

        if request.method == 'POST':
            form = CreateMessageForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                chat_message = ChatMessage.objects.create(user=request.user, room=chat_room, content=content)
                chat_room.messages.add(chat_message)
                return redirect('chat_room_detail', room_id=room_id)
        else:
            form = CreateMessageForm()

        context = {
            'chat_room': chat_room,
            'messages': messages,
            'users': users,
            'form': form,
            'is_moderator': is_moderator,
            'moderator': chat_room.moderator,
            'user_chat_rooms': user_chat_rooms,
            'create_chat_room_form': chat_room_form,  # Include the chat room creation form in the context
        }

    return render(request, 'chat_room_detail.html', context)

# Récupération des mises à jour des messages dans une salle de conversation
def get_updates(request):
    if request.method == 'GET':
        room_id = request.GET.get('room_id')
        last_message_id = request.GET.get('last_message_id')

        if room_id and last_message_id:
            # Récupère les nouveaux messages dans la salle de conversation
            new_messages = ChatMessage.objects.filter(room__id=room_id, id__gt=last_message_id)
            
            # Utilisez une liste de dictionnaires pour stocker les données des messages
            messages_data = []
            
            for message in new_messages:
                message_info = {
                    'id': message.id,
                    'user': message.user.username,
                    'content': message.content,
                    'timestamp': message.timestamp.strftime("%Y-%m-%d %H:%M:%S")  # Convertit le timestamp en format de chaîne lisible
                }
                
                # Ajoutez le dictionnaire à la liste
                messages_data.append(message_info)
                
            return JsonResponse({'messages': messages_data})

    return JsonResponse({'messages': []})

# Envoi d'un message dans une salle de conversation
@require_POST
def send_message(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        chat_room = get_object_or_404(ChatRoom, id=room_id)

        content = request.POST.get('content')
        emoticon = request.POST.get('emoticons')

        # Crée et ajoute un nouveau message à la salle de conversation
        chat_message = ChatMessage.objects.create(
            user=request.user,
            room=chat_room,
            content=content + " " + emoticon
        )

        chat_room.messages.add(chat_message)

        return JsonResponse({'success': True})

# Suppression d'un message dans une salle de conversation (réservé aux modérateurs et auteurs des messages)
@login_required(login_url='my_login_view')
def delete_message(request, message_id):
    chat_message = get_object_or_404(ChatMessage, id=message_id)
    
    # Vérifie si l'utilisateur est autorisé à supprimer le message (modérateur ou auteur du message)
    if request.user == chat_message.room.moderator or request.user == chat_message.user:
        # Supprime le message
        chat_message.delete()
        return JsonResponse({'success': True})
    else:
        # Renvoie une réponse d'erreur si l'utilisateur n'est pas autorisé à supprimer le message
        return JsonResponse({'success': False, 'error': 'Vous n\'êtes pas autorisé à supprimer ce message.'})

# Création d'une nouvelle salle de conversation
@login_required(login_url='my_login_view')
def create_chat_room(request):
    current_user = request.user

    if request.method == 'POST':
        chat_room_form = CreateChatRoomForm(request.POST)
        if chat_room_form.is_valid():
            # Create a new chat room and add it to the current user
            chat_room = chat_room_form.save()
            chat_room.users.add(current_user)
            return redirect('my_view')
    else:
        chat_room_form = CreateChatRoomForm()

    return render(request, 'create_chat_room.html', {'chat_room_form': chat_room_form})

# Page de connexion de l'utilisateur
def my_login_view(request):
    if request.method == 'POST':
        pseudo = request.POST.get('pseudo')
        password = request.POST.get('password')

        user = authenticate(request, username=pseudo, password=password)

        if user is not None:
            # Authentifie l'utilisateur et le redirige vers la page principale
            login(request, user)
            return redirect('my_view')
        else:
            # Affiche un message d'erreur en cas de mauvaises informations de connexion
            messages.error(request, 'Invalid login credentials. Please try again. Pseudo: {}, Password: {}'.format(pseudo, password))
    return render(request, 'login.html')

# Page principale de l'utilisateur, affichant ses salles de conversation
@login_required(login_url='my_login_view')
def my_view(request):
    current_user = request.user

    # Récupère les salles de conversation de l'utilisateur actuel
    user_chat_rooms = ChatRoom.objects.filter(users=current_user)

    if request.method == 'POST':
        chat_room_form = CreateChatRoomForm(request.POST)
        if chat_room_form.is_valid():
            # Crée une nouvelle salle de conversation et l'ajoute à l'utilisateur actuel
            chat_room = chat_room_form.save()
            chat_room.users.add(current_user)
            return redirect('my_view')
    else:
        chat_room_form = CreateChatRoomForm()

    return render(request, 'my_view.html', {'user_chat_rooms': user_chat_rooms, 'chat_room_form': chat_room_form})

@login_required(login_url='my_login_view')
def logout_user(request):
    logout(request)
    return redirect('my_login_view')