"""
由于播放盒经常死机，因此设置两个自动重启的时间。
并且上传资料后，需要重启，开发一个用户界面。
"""

# 1.所有的重启都应该产生日志,并在用户界面有一个日志显示窗口
# 2.自动重启的时间定在早上七点和晚上十点
# 3.每一个盒子都产生一个按钮

import tkinter as tk
from tkinter import messagebox
import socket
from time import sleep
import logging
import schedule
import threading


messages = [] #接收日志信息
li_locate_ip = [['序厅LED', '172.18.0.33'], ['序厅工控屏', '172.18.0.10'], ['历史墙投影仪', '172.18.0.11'],
                ['Intel Vision LED', '172.18.0.34'], ['服务器拼接屏1', '172.18.0.12'], ['服务器拼接屏2', '172.18.0.13'],
                ['服务器拼接屏3', '172.18.0.14'], ['服务器拼接屏4', '172.18.0.15'], ['XFusion工控屏', '172.18.0.20'],
                ['OCSP拼接屏1', '172.18.0.16'], ['OCSP拼接屏2', '172.18.0.17'], ['OCSP拼接屏3', '172.18.0.18'],
                ['OCSP拼接屏4', '172.18.0.19'], ['芯片产业链工控屏', '172.18.0.22'], ['Motherboard工控屏', '172.18.0.23'],
                ['显卡工控屏', '172.18.0.24'], ['CCG Vision LED', '172.18.0.35'], ['Green PC工控屏', '172.18.0.21'],
                ['NEX LED', '172.18.0.37'], ['超能云终端工控屏', '172.18.0.25'], ['5G小基站', '172.18.0.26'],
                ['闸机工控屏', '172.18.0.27'], ['智慧灯杆工控屏', '172.18.0.28'], ['AI Box工控屏', '172.18.0.29'],
                ['缺陷检测工控屏', '172.18.0.30'], ['汽车LED', '172.18.0.36'], ['大族激光工控屏', '172.18.0.31'],
                ['飞拍工控屏', '172.18.0.32'], ['机械臂工控屏', '172.18.0.39'], ['厅外LED', '172.18.0.38']]
log_text = None #只是占位，会被替换
time1 = "07:00"
time2 = "22:00"

# 添加一个处理程序，将日志消息添加到列表中
class ListHandler(logging.Handler):
    """
    复写基类，在本代码中，定义将日志消息输出到列表中
    """
    def __init__(self, log_list):
        super().__init__()
        self.log_list = log_list

    def emit(self, record):
        log_entry = self.format(record)
        self.log_list.append(log_entry)
        # 如果日志列表超过500条，移除最旧的一条日志
        if len(self.log_list) > 500:
            self.log_list.pop(0)

def set_logging():
    log_formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')
    list_handler = ListHandler(messages) # 存储的位置
    list_handler.setFormatter(log_formatter) #设置格式
    logger = logging.getLogger()
    logger.addHandler(list_handler)
    logger.setLevel(logging.INFO)


def on_closing():
    if messagebox.askokcancel("退出程序", "确定要退出吗？"):
        root.destroy()


def execute_button(event, locate_ip):
    result = messagebox.askquestion("请确认执行", f"确定要执行操作 重启{locate_ip[0]}的播放盒 吗？")
    if result == "yes":
        # 在这里执行你的操作，可以使用 param 参数
        print(f"{locate_ip[0]}的播放盒正在重启......")
        # logging.info(f"{locate_ip[0]}的播放盒正在重启......")
        update_log_text(f"{locate_ip[0]}的播放盒正在重启......", log_text)
        reboot_player(locate_ip[1])
    else:
        update_log_text(f"取消重启 {locate_ip[0]}的播放盒",log_text)
        # logging.info(f"取消重启 {locate_ip[0]}的播放盒")
        print(f"取消重启 {locate_ip[0]}的播放盒")


def reboot_player(ip):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.settimeout(2)
        try:
            udp_socket.sendto((ip+'MRWETEND').encode(), (ip, 50505))
            # 接收返回信息
            data, server = udp_socket.recvfrom(1024)
            print(f'重启播放盒成功')
            update_log_text(f'重启播放盒成功', log_text)
            # logging.info(f'重启播放盒成功')
        except:
            update_log_text('重启播放盒失败!!!!!!', log_text)
            # logging.info('重启播放盒失败!!!!!!')
            print('重启播放盒失败!!!!!!')
        udp_socket.close()


def all_reboot_at_time(li):
    def all_reboot():
        for i in li:
            update_log_text(f'{i[0]} 的播放盒盒正在重启......', log_text)
            # logging.info(f'{i[0]} 的播放盒盒正在重启......')
            print(f'{i[0]} 的播放盒盒正在重启......')
            reboot_player(i[1])
            sleep(0.8)

    all_reboot_thread = threading.Thread(target=all_reboot)
    all_reboot_thread.daemon = True
    all_reboot_thread.start()


def creat_button_log(root):
    # 创建按钮列表
    button_names = li_locate_ip

    # 创建左侧按钮区域的Frame
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.Y)
    # 左侧上半部分Frame
    button_frame_top = tk.Frame(button_frame)
    button_frame_top.pack(side=tk.TOP, padx=10, pady=3,)
    # 左侧上半部分加一个按钮
    button_all_reboot = tk.Button(button_frame_top, text="重启所有的播放盒")
    button_all_reboot.bind("<ButtonRelease-1>", lambda _: all_reboot_at_time(button_names))
    button_all_reboot.pack(side=tk.TOP, padx=10, pady=3,)
    # 左侧下半部分，区域按钮
    button_frame_bottom = tk.Frame(button_frame)
    button_frame_bottom.pack(side=tk.LEFT, padx=10, pady=5,)


    # 创建右侧日志显示区域
    log_text = tk.Text(root, wrap=tk.WORD)
    log_text.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)
    log_text.insert(tk.END, f"如果本程序正常运行，会在{time1} 和 {time2} 自动重启所有播放盒\n")

    # 创建按钮并添加到左侧Frame中
    for i, button_name in enumerate(button_names):
        row = i % 15  # 每列最多放15个按钮
        column = i // 15  # 计算列数
        # print(button_name)
        button = tk.Button(button_frame_bottom, text=button_name[0])
        button.bind("<ButtonRelease-1>", lambda event, button_name=button_name: execute_button(event,button_name))
        button.grid(row=row, column=column, padx=10, pady=3, sticky="nsew")
    return log_text


def update_log_text(message, log_text):
    """
    使用最新的日志消息更新 Text 小部件。
    """
    logging.info(message) #添加日志
    #插入在最下面，并可见
    log_text.insert(tk.END, messages[-1] + '\n')
    log_text.see(tk.END)


# 使用schedule模块安排任务执行时间
schedule.every().day.at(time1).do(lambda: all_reboot_at_time(li_locate_ip))
schedule.every().day.at(time2).do(lambda: all_reboot_at_time(li_locate_ip))
# 创建线程并启动任务调度
def schedule_thread():
    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == '__main__':
    set_logging() #设置日志的基本信息

    root = tk.Tk()
    root.title('播放盒重启程序')
    root.geometry("800x600")

    log_text = creat_button_log(root) #创建按钮，并返回日志区，以备为更新日志所引用update_log_text()

    # 创建线程对象
    schedule_thread_obj = threading.Thread(target=schedule_thread)
    schedule_thread_obj.daemon = True #如果不设置这个，退出用户界面，还是不会关程序。
    # 启动线程
    schedule_thread_obj.start()

    root.iconify() #开机最小化
    root.protocol('WM_DELETE_WINDOW',on_closing)
    root.mainloop()

# pyinstaller -F -w .\重启播放盒.py 只有exe文件，以及隐藏后台
