from .models import *
import threading
import datetime

serving_count = 3
waiting_count = 1
waiting_time_length = 120


#问题。。。调度后之前设置的定时器怎么办...饱和判断

# 刚开机或等待101  服务110 服务饱和100

def set_waiting_to_serving(room):
    room.state_serving = True
    room.state_waiting = False
    room.last_serving_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    room.is_timer = False
    room.save()


def set_serving_to_waiting(room):
    room.state_serving = False
    room.state_waiting = True
    room.serving_duration += (
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') - room.last_serving_time).total_seconds()
    room.is_timer = True
    room.save()


def waiting_timer(room_id):
    room = Room.objects.get(room_id=room_id)
    # 判断他当前是否已经在服务队列中
    if False == room.state_serving:
        set_waiting_to_serving(room)
        # 将服务时长最长的房间调入等待队列
        serving_list = Room.objects.filter(state_working=True, state_waiting=False, state_serving=True).order_by(
            '-serving_duration')
        set_serving_to_waiting(serving_list[0])
        timer = threading.Timer(waiting_time_length, waiting_timer(serving_list[0].room_id))
        timer.start()


def scheduling():
    # serving_list = Room.objects.filter(state_working=True, state_waiting=False, state_serving=True).order_by(
    #     '-fan_speed')
    # waiting_list = Room.objects.filter(state_working=True, state_waiting=True, state_serving=False).order_by(
    #     '-fan_speed')

    # # 服务对象数大于等于服务对象上限
    # if serving_count <= serving_list.count():
        room_list = Room.objects.filter(state_working=True).exclude(state_waiting=False, state_serving=False).order_by(
            '-fan_speed')
        i = 0
        while i < serving_count:
            if room_list[i].state_waiting:
                set_waiting_to_serving(room_list[i])
            i += 1
        while i < room_list:
            if room_list[i].state_serving:
                    set_serving_to_waiting(room_list[i])
            if room_list[i].fan_speed == room_list[serving_count - 1].fan_speed and not room_list[i].is_timer:
                timer = threading.Timer(waiting_time_length, waiting_timer(room_list[i].room_id))
                room_list[i].is_timer = True
                room_list[i].save()
                timer.start()
            i += 1
    # # 服务对象数小于服务对象上限
    # else:
    #     i = 0
    #     num = min(waiting_list.count(), serving_count - serving_list.count())
    #     # 将等待队列中对象调入服务队列
    #     while i < num:
    #         set_serving(waiting_list[i])
    #         i += 1
    #     # 将等待队列中对象未能调入服务队列的对象开启定时器
    #     while i < waiting_list.count():
    #         if not waiting_list[i].is_timer:
    #             timer = threading.Timer(waiting_time_length, waiting_timer(waiting_list[i].room_id))
    #             timer.start()
    #         i += 1


def m_poweron(room_id, cur_temp):
    room = Room.objects.get(room_id=room_id)
    room.state_working = True
    room.state_waiting = True
    room.current_temp = cur_temp
    room.save()
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
    scheduling()
    # 返回信息
    room = Room.objects.get(room_id=room_id)
    if False == room.state_working:
        return {'poweroff': 'ok'}
    else:
        return {'poweroff': 'fail'}


def m_config(room_id, fan, target_temp):
    room = Room.objects.get(room_id=room_id)
    room.fan_speed = fan
    room.target_temp = target_temp
    room.save()
    scheduling()
    # 返回信息
    room = Room.objects.get(room_id=room_id)
    if fan == room.fan_speed and target_temp == room.target_temp:
        return {'config': 'ok'}
    else:
        return {'config': 'fail'}


def temp_update(room_id, cur_temp):
    room = Room.objects.get(room_id=room_id)
    room.current_temp = cur_temp
    # 当前温度达到目标温度时，room的状态从服务变为服务饱和,调整服务队列
    if cur_temp == room.target_temp:
        room.state_serving = False
        room.serving_duration += (
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') - room.last_serving_time).total_seconds()
        room.save()
        scheduling()
        return {'finish': ''}
    # 当前温度与目标温度不等且room的状态为服务饱和，则变为等待服务,调整服务队列
    elif room.state_working and not room.state_serving and not room.state_waiting:
        room.state_waiting = True
        room.save()
        scheduling()
