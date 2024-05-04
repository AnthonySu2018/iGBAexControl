import tkinter as tk
import socket
import json
import time
from wakeonlan import send_magic_packet

# 生成以指令序号为键，其他内容为值的字典
with open('commands.csv', mode='r', encoding='utf-8') as f:
    commands = f.readlines()
commands = [i.strip().split(',') for i in commands]
commands_dict = {}
for item in commands:
    key = item[0]
    values = item[1:]
    commands_dict[key]=values
# print(commands_dict)


def button_click(event, str_commands):
    button = event.widget
    if ',' in str_commands:#不止一个序号
        ls = str_commands.split(',')
        # print(ls)
        if '0' in ls:#有时延
            len_ls = len(ls)#获得列表长度
            print(len_ls)
            for i in range(len_ls):
                if i % 2 == 0:# 偶数就休眠
                    time.sleep(float(ls[i]))
                    print('sleep')
                else:
                    ls_of_com_detail = commands_dict[ls[i]]
                    print(ls_of_com_detail)
                    if ls_of_com_detail[1] == '2':
                        sendudpcommand(ip=ls_of_com_detail[2], port=int(ls_of_com_detail[3]),
                                       hex_data=ls_of_com_detail[4])
                    elif ls_of_com_detail[1] == 'None': # 唤醒裸眼3D
                        mac_address = "CC-96-E5-24-6F-57"  # 要唤醒计算机的 MAC 地址
                        try:
                            send_magic_packet(mac_address)
                            print("已发送唤醒命令成功。")
                        except Exception as e:
                            print("发送唤醒命令失败：", e)
                    else:
                        sendtcpcommand(ip=ls_of_com_detail[2], port=int(ls_of_com_detail[3]),
                                       hex_data=ls_of_com_detail[4])
                                # 需要延迟控制
        else:
            for i in ls:
                ls_of_com_detail = commands_dict[i]
                if ls_of_com_detail[1] == '2':
                    sendudpcommand(ip=ls_of_com_detail[2], port=int(ls_of_com_detail[3]), hex_data=ls_of_com_detail[4])
                else:
                    sendtcpcommand(ip=ls_of_com_detail[2], port=int(ls_of_com_detail[3]), hex_data=ls_of_com_detail[4])
    else:#直接获得序号，只有一个
        ls_of_com_detail = commands_dict[str_commands]
        if ls_of_com_detail[1] == '2':
            sendudpcommand(ip=ls_of_com_detail[2],port=int(ls_of_com_detail[3]),hex_data=ls_of_com_detail[4])
        else:
            sendtcpcommand(ip=ls_of_com_detail[2], port=int(ls_of_com_detail[3]), hex_data=ls_of_com_detail[4])
    print(f"按钮 {button['text']}（序号：{str_commands}）被点击了")


def sendudpcommand(ip,port,hex_data):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 将十六进制字符串转换为字节数据
    message_bytes = bytes.fromhex(hex_data)
    udp_socket.sendto(message_bytes, (ip, port))
    udp_socket.close()


def sendtcpcommand(ip,port,hex_data):
    # 创建 TCP 套接字
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 连接到目标服务器
    try:
        tcp_socket.settimeout(2)
        tcp_socket.connect((ip, port))
        # 将十六进制字符串转换为字节数据
        message_bytes = bytes.fromhex(hex_data)
        # 发送数据
        tcp_socket.send(message_bytes)
        # 关闭连接
        tcp_socket.close()
    except socket.error as e:
        print((f"Error: {e},有可能离线了，或者ip地址问题"))




root = tk.Tk()
root.title("中控系统替代平板")
root.geometry("800x600")  # 设置默认窗口尺寸

# 全屏化按钮
def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))
# 最大化按钮
def maximize(event=None):
    root.state('zoomed')
# 退出按钮
def close(event=None):
    root.destroy()

# 创建工具栏
toolbar = tk.Frame(root)
toolbar.pack(side="top", fill="x")

fullscreen_btn = tk.Button(toolbar, text="全屏化", command=toggle_fullscreen)
fullscreen_btn.pack(side="left")

maximize_btn = tk.Button(toolbar, text="最大化", command=maximize)
maximize_btn.pack(side="left")

close_btn = tk.Button(toolbar, text="关闭", command=close)
close_btn.pack(side="right")

# 展厅讲解及全场设备开关
rows_visit = [
    ("序厅大屏", ['视频1','视频2','视频3','视频4','播放','暂停','停止','拍照模式','拍照灯关','音量+','音量-','静音']),
    ("序厅欢迎屏", ['视频1','视频2','视频3','播放','暂停','停止']),
    ("投影仪", ['视频1','视频2','视频3','视频4','播放','暂停','停止','音量+','音量-','静音','渐暗','渐亮']),
    ("Intel Vision", ['视频1','视频2','视频3','视频4','播放','暂停','停止','音量+','音量-','静音','渐暗','渐亮']),
    ("服务器",['视频1','视频2','视频3','视频4','播放','暂停','停止','全屏模式','全屏退出']),
    ("CCG",['视频1','视频2','视频3','播放','暂停','停止','音量+','音量-','静音','输入1','输入2','输入3']),
    ("NEX", ['视频1','视频2','视频3','视频4','播放','暂停','停止','音量+','音量-','静音'])
]
# 设备管理
rows_device = [
    ('灯光管理', ['公共参观区','DCAI','CCG','NEX','保洁灯光','总灯光']),
    ('DCAI', ['服务器拼接屏','XFusion工控屏','OCSP拼接屏','DCAI区域灯光']),
    ('CCG', ['芯片产业链工控屏','Mother board工控屏','PC Booth','显卡工控屏','CCG LED','Green PC工控屏','CCG区域灯光']),
    ('NEX', ['NEX LED','超能云终端工控屏','5G 小基站','会议解决方案工控屏1','会议解决方案工控屏2','会议解决方案Max Hub',
             '会议解决方案全场智能平板','闸机工控屏','智慧灯杆工控屏','AI Box工控屏','智慧教室Max Hub','智慧校园拼接屏',
             '缺陷检测工控屏','汽车LED','大族激光工控屏','飞拍工控屏','机械臂工控屏','NEX区域灯光']),
    ('公共参观区', ['序厅LED','序厅欢迎屏','投影仪','Intel Vision LED','裸眼3D','公共参观区灯光']),
    ("全场设备", ['设备开','设备关'])
]

with open('dict_visit.json', mode='r', encoding='utf-8') as f:
    dic = json.load(f)
# print(type(dic))
# print(dic)

for row_index, (label_text, button_count) in enumerate(rows_visit):
    label = tk.Label(root, text=label_text) #label_text=序厅， button_count=每一个按键的总和
    label.pack()
    buttons_frame = tk.Frame(root)
    buttons_frame.pack()
    print(button_count)
    for col in button_count:#col=具体每一个按键，如"视频1”
        str_commands = dic[label_text][col] # 获得按钮对应的命令参数的序号
        button = tk.Button(buttons_frame, text=f"{col}", height=1, width=10)
        button.bind("<Button-1>", lambda event, str_commands=str_commands: button_click(event,str_commands))
        button.pack(side="left", padx=10, pady=10)

root.mainloop()
