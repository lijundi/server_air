import json

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from dwebsocket.decorators import accept_websocket
from .models import *


# Create your views here.
def index(request):
    return render(request, 'index.html')


# 前台
def reception(request):
    return render(request, 'reception.html')


def get_records_and_invoice(request):
    if request.method == 'post':
        room_id = request.POST['room_id']
        records = RequestDetailRecords.objects.filter(room_id=room_id).order_by('request_time')
        report = Report.objects.get(room_id=room_id)
        total_fee = report.total_Fee
        return render(request, 'reception.html', {'records': records, 'total_fee': total_fee})
    else:
        return render(request, 'reception.html')


# 管理员
def manager(request):
    return render(request, 'manager.html', locals())


# 设置空调参数
def manager_set_para(request):
    if request.method == 'POST':
        WP = WorkingParameter.objects.all()[0]
        str =request.POST.get('mode')
        WP.mode =int(str)
        WP.Temp_highLimit = int(request.POST.get('Temp_highLimit'))
        WP.Temp_lowLimit = int(request.POST.get('Temp_lowLimit'))
        WP.default_TargetTemp = int(request.POST.get('default_TargetTemp'))
        WP.FeeRate_H = request.POST.get('FeeRate_H')
        WP.FeeRate_M = request.POST.get('FeeRate_M')
        WP.FeeRate_L = request.POST.get('FeeRate_L')
        WP.save()
        return HttpResponseRedirect("/server/manager/")
    else:
        return render(request, 'manager_set_para.html')

# 定时检查状态
def manager_check_state(request):
    room = Room.objects.all()
    return render(request, 'manager_check_state.html', {'room': room})


# 经理
def boss(request):
    report = Report.objects.all()
    return render(request, 'boss.html', {'report': report})


# 打印报表
def boss_print_report(request):
    print(1)
    return render(request, 'boss.html', locals())


# 对外服务接口
# @accept_websocket
# def websocket(request):
#     if request.is_websocket():
#         message = bytes.decode(request.websocket.wait())  # string
#         info = json.loads(message)  # json
#
#
#
#         request.websocket.send(msg.encode())
#     else:
#         return HttpResponse("error")
