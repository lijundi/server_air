from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from channels.layers import get_channel_layer
import datetime
import json


# 开启定时工作
scheduler = BackgroundScheduler()  # 实例化调度器
try:
    # 调度器使用DjangoJobStore()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    @register_job(scheduler, "interval", seconds=10)
    def send_cost():
        # 计算各房间费用并返回
        room_list = Room.objects.all()
        for room in room_list:
            # 计算详单的总费用
            RDR_list = RequestDetailRecords.objects.filter(room_id=room.room_id)
            total = 0
            for record in RDR_list:
                total += record.fee
            # 计算正在服务的费用
            if room.state_serving or room.state_waiting:
                time = (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') - room.last_serving_time).total_seconds()
                total += time * room.fee_rate  # 按秒算费用
            room.fee = total
            channel_layer = get_channel_layer()
            channel_layer.send(room.channel_name, json.dumps({'cost': total}))
            report = Report.objects.get(room_id=room.room_id)
            report.total_Fee = total
            report.save()
            room.save()
        pass

    register_events(scheduler)
    scheduler.start()
except Exception as e:
    print(e)
    # 有错误就停止定时器
    scheduler.shutdown()


# Create your views here.
def index(request):
    return render(request, 'index.html')


# 前台
def reception(request):
    return render(request, 'reception.html')


def get_records_and_invoice(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        if room_id:
            records = RequestDetailRecords.objects.filter(room_id=room_id).order_by('request_time')
            report = Report.objects.get(room_id=room_id)
            total_fee = report.total_Fee
            return render(request, 'reception.html', {'records': records, 'total_fee': total_fee, 'room_id': room_id})
    return render(request, 'reception.html')


# 打印详单、账单
def reception_print_records_and_invoice(request):
    print(1)
    return render(request, 'reception.html', locals())


# 管理员
def manager(request):
    return render(request, 'manager.html', locals())


# 设置空调参数
def manager_set_para(request):
    if request.method == 'POST':
        WP = WorkingParameter.objects.all()[0]
        WP.mode = int(request.POST.get('mode'))
        WP.Temp_highLimit = int(request.POST.get('Temp_highLimit'))
        WP.Temp_lowLimit = int(request.POST.get('Temp_lowLimit'))
        WP.default_TargetTemp = int(request.POST.get('default_TargetTemp'))
        WP.FeeRate_H = request.POST.get('FeeRate_H')
        WP.FeeRate_M = request.POST.get('FeeRate_M')
        WP.FeeRate_L = request.POST.get('FeeRate_L')
        WP.lowfan_change_temp = request.POST.get('lowfan_change_temp')
        WP.medfan_change_temp = request.POST.get('medfan_change_temp')
        WP.highfan_change_temp = request.POST.get('highfan_change_temp')
        WP.fan = request.POST.get('fan')
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



