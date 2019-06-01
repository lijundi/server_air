from .models import *
import threading
import datetime

serving_count = 3
waiting_count = 1
waiting_time_length = 120


#问题

# 刚开机或等待101  服务110 服务饱和100


def get_time_now():
    return datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')


# whichtype取值含义 1:开关次数     2:调度次数     3:详单次数      4:温度变化次数    5:风速改变次数
def update_Report(room, whichtype):
    report = Report.objects.get(room=room)
    if 1 == whichtype:
        report.times_of_on_and_off += 1
    elif 2 == whichtype:
        report.times_of_dispatch += 1
    elif 3 == whichtype:
        report.number_of_RDR += 1
    elif 4 == whichtype:
        report.times_of_changeTemp += 1
    elif 5 == whichtype:
        report.times_of_changeFanSpeed += 1
    report.save()

def create_RequestDetailRecords(room):
    RequestDetailRecords.objects.create(room=room, request_time=room.last_serving_time,
                                        request_duration=(get_time_now() - room.last_serving_time).total_seconds())
    update_Report(room, 3)


def set_waiting_to_serving(room):
    room.state_serving = True
    room.state_waiting = False
    room.last_serving_time = get_time_now()
    room.is_timer = False
    room.save()


def set_serving_to_waiting(room):
    room.state_serving = False
    room.state_waiting = True
    room.serving_duration += (get_time_now() - room.last_serving_time).total_seconds()
    room.is_timer = True
    room.save()


def waiting_timer(room_id):
    room = Room.objects.get(room_id=room_id)
    # 判断他当前是否已经在服务队列中
    if room.state_waiting:
        set_waiting_to_serving(room)
        # 将服务时长最长的房间调入等待队列
        serving_list = Room.objects.filter(state_working=True, state_waiting=False, state_serving=True).order_by(
            '-serving_duration')
        set_serving_to_waiting(serving_list[0])
        timer = threading.Timer(waiting_time_length, waiting_timer(serving_list[0].room_id))
        timer.start()


def scheduling():
        room_list = Room.objects.filter(state_working=True).exclude(state_waiting=False, state_serving=False).order_by(
            '-fan_speed')
        i = 0
        while i < serving_count:
            if room_list[i].state_waiting:
                set_waiting_to_serving(room_list[i])
            update_Report(room_list[i], 2)
            i += 1
        while i < room_list:
            if room_list[i].state_serving:
                    set_serving_to_waiting(room_list[i])
            if room_list[i].fan_speed == room_list[serving_count - 1].fan_speed and not room_list[i].is_timer:
                timer = threading.Timer(waiting_time_length, waiting_timer(room_list[i].room_id))
                room_list[i].is_timer = True
                room_list[i].save()
                timer.start()
            update_Report(room_list[i], 2)
            i += 1



def m_poweron(room_id, cur_temp, channel_name):
    room = Room.objects.get(room_id=room_id)
    wp = WorkingParameter.objects.all()[0]
    room.target_temp = wp.default_TargetTemp
    room.fan_speed = wp.fan
    room.state_working = True
    room.state_waiting = True
    room.current_temp = cur_temp
    room.channel_name = channel_name
    room.save()
    update_Report(room, 1)
    scheduling()
    # 返回信息
    room = Room.objects.get(room_id=room_id)
    if True == room.state_serving and False == room.state_waiting:
        return {'poweron': 'ok'}
    else:
        return {'poweron': 'busy'}


def m_poweroff(room_id):
    room = Room.objects.get(room_id=room_id)
    room.state_working = False
    room.state_serving = False
    room.state_waiting = False
    room.save()
    update_Report(room, 1)
    scheduling()
    # 返回信息
    room = Room.objects.get(room_id=room_id)
    if False == room.state_working:
        return {'poweroff': 'ok'}
    else:
        return {'poweroff': 'fail'}


def m_config(room_id, fan, target_temp):
    room = Room.objects.get(room_id=room_id)
    if fan != room.fan_speed:
        room.fan_speed = fan
        update_Report(room, 5)
    if target_temp != room.target_temp:
        room.target_temp = target_temp
        update_Report(room, 4)
    room.save()
    scheduling()
    # 返回信息
    room = Room.objects.get(room_id=room_id)
    if True == room.state_serving and False == room.state_waiting:
        return {'poweron': 'ok'}
    else:
        return {'poweron': 'busy'}


def temp_update(room_id, cur_temp):
    room = Room.objects.get(room_id=room_id)
    room.current_temp = cur_temp
    # 当前温度达到目标温度时，room的状态从服务变为服务饱和,调整服务队列
    wp = WorkingParameter.objects.all()[0]
    if (cur_temp <= room.target_temp) and (wp.mode == 0) or (cur_temp >= room.target_temp) and (wp.mode == 1):
        room.state_serving = False
        room.serving_duration += (get_time_now() - room.last_serving_time).total_seconds()
        room.save()
        scheduling()
        return {'finish': ''}
    # 当前温度与目标温度不等且room的状态为服务饱和，则变为等待服务,调整服务队列
    elif room.state_working and not room.state_serving and not room.state_waiting:
        room.state_waiting = True
        room.save()
        scheduling()
    return {}
