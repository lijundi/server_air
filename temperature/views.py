# import datetime
# import json
#
# from django.shortcuts import HttpResponse
# from dwebsocket.decorators import accept_websocket, require_websocket
# from .models import *
#
#
# # Create your views here.
# @accept_websocket
# def start(request):  # 启动室温模拟
#     if request.is_websocket():
#         message = bytes.decode(request.websocket.wait())  # string
#         info = json.loads(message)  # json
#         if info['start']:
#             temperature = Temperature.objects.all()[0]
#             temperature.pre_change_date = datetime.datetime.now()
#             temperature.save()
#             msg = json.dumps({'status': "success"})
#         else:
#             msg = json.dumps({'status': "fail"})
#         request.websocket.send(msg.encode())
#     else:
#         return HttpResponse("error")
#
#
# @accept_websocket
# def get_current_temp(request):  # 获取温度值
#     if request.is_websocket():
#         message = bytes.decode(request.websocket.wait())  # string
#         # print(message)
#         info = json.loads(message)  # json
#
#         temperature = Temperature.objects.all()[0]
#         # 设置目标温度
#         temperature.target_temp = info['tar_temp']
#         temperature.save()
#         # 先判断是否有温度变化
#         now = datetime.datetime.now()  # 获取当前时间
#         if temperature.serving and info['fanSpeed'] == 2:
#             pre_time = now - datetime.timedelta(seconds=(60//temperature.rate_h))  # 获取高速风前一个温度变化时间
#         elif temperature.serving and info['fanSpeed'] == 1:
#             pre_time = now - datetime.timedelta(seconds=(60//temperature.rate_m))  # 获取中速风前一个温度变化时间
#         elif temperature.serving and info['fanSpeed'] == 0:
#             pre_time = now - datetime.timedelta(seconds=(60//temperature.rate_l))  # 获取低速风前一个温度变化时间
#         else:
#             pre_time = now - datetime.timedelta(seconds=(60//temperature.rate_default))  # 获取回温程序前一个温度变化时间
#         temp_set = Temperature.objects.filter(pre_change_date__lt=pre_time)  # 判断是否需要温度变化
#         if temp_set:  # 如果存在，温度变化
#             temperature = temp_set[0]
#             temperature.pre_change_date = now  # 改时间
#             if temperature.temp > temperature.target_temp:
#                 temperature.temp -= 1
#             elif temperature.temp < temperature.target_temp:
#                 temperature.temp += 1
#         else:
#             temperature = Temperature.objects.all()[0]
#         t = temperature.temp  # 返回给客户端的当前温度
#         # 再判断是否需要重新设置时间
#         if temperature.serving != info['serving']:  # 开始新的计时
#             temperature.serving = info['serving']
#             temperature.pre_change_date = now
#         temperature.save()  # 统一保存
#
#         msg = json.dumps({'temp': t})
#         request.websocket.send(msg.encode())
#     else:
#         return HttpResponse("error")
#
#
#
