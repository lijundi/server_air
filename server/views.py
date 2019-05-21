from django.shortcuts import render
from .models import *


# Create your views here.
def index(request):
    return render(request, 'index.html')


# 前台
def reception(request):
    return render(request, 'reception.html')


def get_records(request):
    if request.method == 'post':
        room_id = request.POST['room_id']
        records = RequestDetailRecords.objects.filter(room_id=room_id).order_by('request_time')
        return render(request, 'reception.html', {'records': records})
    else:
        return render(request, 'reception.html')


def get_invoice(request):
    if request.method == 'post':
        room_id = request.POST['room_id']
        room = Room.objects.get(room_id=room_id)
    return render(request, 'reception.html', locals())


# 管理员
def manager(request):
    return render(request, 'manager.html', locals())


def manager_set_para(request):
    return render(request, 'manager_set_para.html', locals())


def manager_check_state(request):
    return render(request, 'manager_check_state.html', locals())


# 经理
def boss(request):
    return render(request, 'boss.html', locals())



