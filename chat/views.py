# chat/views.py
from django.http import HttpResponseNotAllowed, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views.decorators.csrf import csrf_exempt

from chat.models import Room


def home(request):
    return HttpResponseRedirect(reverse('index'))


@csrf_exempt
def index(request):
    if request.method == 'GET':
        return render(request, 'chat/index.html')

    if request.method == 'POST':
        current_uuid = request.session.get('user_uuid')
        try:
            room = Room.objects.get(user_uuid=current_uuid)
        except Room.DoesNotExist:
            room = Room.objects.filter(num_users=1).first()
        if room:
            if str(room.user_uuid) != current_uuid and room.num_users == 1:
                room.is_open = True
                room.num_users = 2
                room.save()
        else:
            room = Room.objects.create(user_uuid=current_uuid)
        return JsonResponse({'name': room.name, 'num_users': room.num_users,
                             'user_uuid': room.user_uuid, 'is_open': room.is_open})
    return HttpResponseNotAllowed(['GET', 'POST'])


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })
