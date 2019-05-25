from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from server.forms import ParaModelForm
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


# 设置空调参数
def manager_set_para(request):
    if request.method == 'POST':
        WP = WorkingParameter.objects.all()[0]
        WP.mode = request.POST['mode']
        WP.Temp_highLimit = request.POST['Temp_highLimit']
        WP.Temp_lowLimit = request.POST['Temp_lowLimit']
        WP.default_TargetTemp = request.POST['default_TargetTemp']
        WP.FeeRate_H = request.POST['FeeRate_H']
        WP.FeeRate_M = request.POST['FeeRate_M']
        WP.FeeRate_L = request.POST['FeeRate_L']
        WP.save()
        return HttpResponseRedirect("/manager")
    else:
        return render(request, 'manager_set_para.html')

# 定时检查状态
def manager_check_state(request):
    room = Room.objects.all()
    return render(request, 'manager_check_state.html', {'room': room})


# 经理
def boss(request):
    return render(request, 'boss.html', locals())


# 查看周报
def boss_report(request):
    report = Report.objects.all()
    return render(request, 'boss.html', {'report': report})


# 打印报表
def boss_print_report(request):
    print(1)
    return render(request, 'boss.html', locals())


