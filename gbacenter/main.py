import socket
import json

def sendudpcommand(ip,port,hex_data):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 将十六进制字符串转换为字节数据
    message_bytes = bytes.fromhex(hex_data)
    # message_bytes = message.encode("utf-8")
    udp_socket.sendto(message_bytes, (ip, port))
    udp_socket.close()

def sendtcpcommand(ip,port,hex_data):
    # 创建 TCP 套接字
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 连接到目标服务器
    tcp_socket.connect((ip, port))
    # 将十六进制字符串转换为字节数据
    message_bytes = bytes.fromhex(hex_data)
    # 发送数据
    tcp_socket.send(message_bytes)
    # 关闭连接
    tcp_socket.close()

#
#
# target_ip = "172.18.0.34"
# target_port = 50505
# hex_data = "31 37 32 2E 31 38 2E 30 2E 33 34 4B 30 31 30 31 45 4E 44"
# hex_data = "31 37 32 2E 31 38 2E 30 2E 33 34 43 54 4C 50 53 45 4E 44"
# sendcommand(target_ip,target_port,hex_data)

with open('commands.csv',mode='r',encoding='utf-8') as f1, open('command_group.csv', mode='r', encoding='utf-8') as f2:
    commands = f1.readlines()
    g_commands= f2.readlines()
commands = [i.strip().split(',') for i in commands]
g_commands = [i.strip().split(',') for i in g_commands]

# print(commands)
# print(g_commands)
rows = [
    ("序厅", ['视频1','播放','暂停','停止','拍照模式','拍照灯关','音量+','音量-','静音']),
    ("投影仪", ['视频1','播放','暂停','停止']),
    ("Intel Vision", ['视频1','播放','暂停','停止','音量+','音量-','静音']),
    ("服务器",['视频1','全屏','取消全屏']),
    ("全场设备", ['设备开','设备关'])
]
rows_visit = [
    ("序厅大屏", ['视频1','视频2','视频3','视频4','播放','暂停','停止','拍照模式','拍照灯关','音量+','音量-','静音']),
    ("序厅欢迎屏", ['视频1','视频2','视频3','播放','暂停','停止']),
    ("投影仪", ['视频1','视频2','视频3','视频4','播放','暂停','停止','音量+','音量-','静音','渐暗','渐亮']),
    ("Intel Vision", ['视频1','视频2','视频3','视频4','播放','暂停','停止','音量+','音量-','静音','渐暗','渐亮']),
    ("服务器",['视频1','视频2','视频3','视频4','播放','暂停','停止','全屏模式','全屏退出']),
    ("CCG",['视频1','视频2','视频3','播放','暂停','停止','音量+','音量-','静音','输入1','输入2','输入3']),
    ("NEX", ['视频1','视频2','视频3','视频4','播放','暂停','停止','音量+','音量-','静音']),
    ("全场设备", ['设备开','设备关'])
]

ls_序厅大屏 = ['1,80','2,80','3,80','4,80','7','8','9,63','6,63','80','10','11','12']
ls_序厅欢迎屏 = ['202','203','204','205','206','207',]
ls_投影仪 = ['13,122','14,122','15,122','16,122','17','18','19,118','20','21','22','130','126']
ls_IntelVison = ['23,120','24,120','25,120','26,120','27','28','29,116','30','31','32','128','124']
ls_Server = ['196,39','197,39','198,39','199,39','33','34','35','39','40']
ls_CCG = ['41','42','43','44','45','46','47','48','49','50','51','52']
ls_NEX = ['53','54','55','56','57','58','59','60','61','62']
ls_全场设备 = ['0,208,0,132,0.5,79,1,105,1.5,116,2,117,2.5,118,3,119,0,134,0,136,0,138,0,140,0,142,0,144,0,146,0,148,0,150,0,152,0,154,0,156,0,158,0,160,0,162,0,164,0,166,0,168,0,170,0,172,0,174,0,176,0,178,0,180,0,182,0,184,0,186,0,188,0,190,0,192,0,200',
               '0,209,0,133,0.5,96,1,115,1.5,120,2,121,2.5,122,3,123,0,135,0,137,0,139,0,141,0,143,0,145,0,147,0,149,0,151,0,153,0,155,0,157,0,159,0,161,0,163,0,165,0,167,0,169,0,171,0,173,0,175,0,177,0,179,0,181,0,183,0,185,0,187,0,189,0,191,0,193,0,201,0,256,0,255,0,254,0,253,0,252,0,251,0,250,0,249,0,248,0,247,0,246,0,245,0,244,0,243,0,242,0,241,0,240,0,239,0,238,0,237,0,236,0,235,0,234,0,233,0,232,0,231,0,230,0,229,0,228,0,227,0,226,0,225,0,224,0,223,0,222,0,221,0,220,0,219,0,218,0,217,0,216,0,215,0,214,0,213,0,212']
dic = dict(rows_visit)
# print(dic)
dic['序厅大屏'] = dict(zip(dic['序厅大屏'],ls_序厅大屏))
dic['序厅欢迎屏'] = dict(zip(dic['序厅欢迎屏'],ls_序厅欢迎屏))
dic['投影仪'] = dict(zip(dic['投影仪'],ls_投影仪))
dic['Intel Vision'] = dict(zip(dic['Intel Vision'],ls_IntelVison))
dic['服务器'] = dict(zip(dic['服务器'],ls_Server))
dic['CCG'] = dict(zip(dic['CCG'],ls_CCG))
dic['NEX'] = dict(zip(dic['NEX'],ls_NEX))
dic['全场设备'] = dict(zip(dic['全场设备'],ls_全场设备))

print(dic)
# with open('dict_visit.json', "w", encoding='utf-8') as json_file:
#     json.dump(dic, json_file, indent=4,ensure_ascii=False)

rows_device = [
    ('灯光管理', ['公共参观区','DCAI','CCG','NEX','保洁灯光','总灯光']),
    ('DCAI', ['服务器拼接屏','XFusion工控屏','OCSP拼接屏','DCAI区域灯光']),
    ('CCG', ['芯片产业链工控屏','Mother board工控屏','PC Booth','显卡工控屏','CCG LED','Green PC工控屏','CCG区域灯光']),
    ('NEX', ['NEX LED','超能云终端工控屏','5G 小基站','会议解决方案工控屏1','会议解决方案工控屏2','会议解决方案Max Hub',
             '会议解决方案全场智能平板','闸机工控屏','智慧灯杆工控屏','AI Box工控屏','智慧教室Max Hub','智慧校园拼接屏',
             '缺陷检测工控屏','汽车LED','大族激光工控屏','飞拍工控屏','机械臂工控屏','NEX区域灯光']),
    ('公共参观区', ['序厅LED','序厅欢迎屏','投影仪','Intel Vision LED','裸眼3D','公共参观区灯光']),
]

dic_device = dict(rows_device)
for i in dic_device.keys():
    dic_device[i] = dict(zip(dic_device[i],[["",""]]*len(dic_device[i])))
print(dic_device)

with open('dict_device.json', "w", encoding='utf-8') as json_file:
    json.dump(dic_device, json_file, indent=4,ensure_ascii=False)