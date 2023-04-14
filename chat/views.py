from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, Http404

from .models import Contact, Chat

# Create your views here.
@login_required
def index(request):
    current_user_contact, created = Contact.objects.get_or_create(user=request.user)

    # Check if the user is a participant of any chat rooms
    user_chat_rooms = Chat.objects.filter(participants=current_user_contact)
    if user_chat_rooms:
        # If the user is a participant in any chat room, redirect to the chat room page
        return redirect('chat:room', room_name=user_chat_rooms.first().pk)
    else:
        # If the user is not a participant in any chat room, render the template for the index page
        return render(request, 'chat/index.html')

@login_required
def room(request, room_name):

    # Get the current user's contact object
    current_user_contact, created = Contact.objects.get_or_create(user=request.user)

    # Check if the chat room exists
    try:
        chat_room = Chat.objects.get(pk=room_name)
    except Chat.DoesNotExist:
        # If the chat room doesn't exist, return a 404 error
        raise Http404("Chat room does not exist.")

    # Check if the current user is a participant in the chat room
    if not chat_room.participants.filter(pk=current_user_contact.pk).exists():
        # If the user is not a participant, return a 403 Forbidden error
        return HttpResponseForbidden("You are not a participant in this chat room.")
    
    # Get a list of chat rooms where the current user is a participant
    user_chat_rooms = Chat.objects.filter(participants=current_user_contact)


    other_participant = chat_room.participants.exclude(pk=current_user_contact.pk).first()

    chat_room_participants = []
    for chat_room in user_chat_rooms:
        # Get a list of participants for the chat room
        participants = chat_room.participants.exclude(pk=current_user_contact.pk)
        # Add the chat room and participant list to the result list
        chat_room_participants.append((chat_room, participants))



    context = {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
        'user_chat_rooms': user_chat_rooms,
        'chat_room_participants': chat_room_participants,
        'other_participant': other_participant,
    }
    return render(request, 'chat/chatroom.html', context=context)
