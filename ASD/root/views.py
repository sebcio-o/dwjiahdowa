from django.shortcuts import render

def index(request):
    return render(request, 'root/index.html')

def room(request, room_name):
    return render(request, 'root/room.html', {
        'room_name': room_name
    })