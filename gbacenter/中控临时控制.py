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
    tcp_socket.connect((ip, port))
    # 将十六进制字符串转换为字节数据
    message_bytes = bytes.fromhex(hex_data)
    # 发送数据
    tcp_socket.send(message_bytes)
    # 关闭连接
    tcp_socket.close()



root = tk.Tk()
root.title("分行布局示例")
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

# 分行布局
rows = [
    ("序厅", ['视频1','播放','暂停','停止','拍照模式','拍照灯关','音量+','音量-','静音']),
    ("投影仪", ['视频1','播放','暂停','停止']),
    ("Intel Vision", ['视频1','播放','暂停','停止','音量+','音量-','静音']),
    ("服务器",['视频1','全屏','取消全屏']),
    ("全场设备", ['设备开','设备关'])
]
with open('dict_look.json', mode='r', encoding='utf-8') as f:
    dic = json.load(f)
# print(type(dic))
# print(dic)

for row_index, (label_text, button_count) in enumerate(rows):
    label = tk.Label(root, text=label_text) #label_text=序厅， button_count=每一个按键的总和
    label.pack()

    buttons_frame = tk.Frame(root)
    buttons_frame.pack()

    for col in button_count:#col=具体每一个按键，如"视频1”
        str_commands = dic[label_text][col] # 获得按钮对应的命令参数的序号
        button = tk.Button(buttons_frame, text=f"{col}", height=3, width=10)
        button.bind("<Button-1>", lambda event, str_commands=str_commands: button_click(event,str_commands))
        button.pack(side="left", padx=10, pady=10)

root.mainloop()
