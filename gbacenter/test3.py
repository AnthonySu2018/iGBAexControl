import tkinter as tk
import logging
import json
import time
from wakeonlan import send_magic_packet
import socket
import ping3
import concurrent.futures
import threading

# 展厅讲解及全场设备开关
rows_visit = [
    ("序厅大屏",
     ['视频1', '视频2', '视频3', '视频4', '播放', '暂停', '停止', '拍照模式', '拍照灯关', '音量+', '音量-', '静音']),
    ("序厅欢迎屏", ['视频1', '视频2', '视频3', '播放', '暂停', '停止']),
    ("投影仪", ['视频1', '视频2', '视频3', '视频4', '播放', '暂停', '停止', '音量+', '音量-', '静音', '渐暗', '渐亮']),
    ("Intel Vision",
     ['视频1', '视频2', '视频3', '视频4', '播放', '暂停', '停止', '音量+', '音量-', '静音', '渐暗', '渐亮']),
    ("服务器", ['视频1', '视频2', '视频3', '视频4', '播放', '暂停', '停止', '全屏模式', '全屏退出']),
    ("CCG", ['视频1', '视频2', '视频3', '播放', '暂停', '停止', '音量+', '音量-', '静音', '输入1', '输入2', '输入3']),
    ("NEX", ['视频1', '视频2', '视频3', '视频4', '播放', '暂停', '停止', '音量+', '音量-', '静音'])
]

# 设备管理
rows_device = [
    ('灯光管理', ['公共参观区', 'DCAI', 'CCG', 'NEX', '保洁灯光', '总灯光']),
    ('DCAI', ['服务器拼接屏', 'XFusion工控屏', 'OCSP拼接屏', 'DCAI区域灯光']),
    ('CCG',
     ['芯片产业链工控屏', 'Mother board工控屏', 'PC Booth', '显卡工控屏', 'CCG LED', 'Green PC工控屏', 'CCG区域灯光']),
    ('NEX',
     ['NEX LED', '超能云终端工控屏', '5G 小基站', '会议解决方案工控屏1', '会议解决方案工控屏2', '会议解决方案Max Hub',
      '会议解决方案全场智能平板', '闸机工控屏', '智慧灯杆工控屏', 'AI Box工控屏', '智慧教室Max Hub', '智慧校园拼接屏',
      '缺陷检测工控屏', '汽车LED', '大族激光工控屏', '飞拍工控屏', '机械臂工控屏', 'NEX区域灯光']),
    ('公共参观区', ['序厅LED', '序厅欢迎屏', '投影仪', 'Intel Vision LED', '裸眼3D', '公共参观区灯光']),
    ("全场设备", ['全场设备开', '全场设备关'])
]

log_messages = []  # 用于存储日志消息的列表


def get_commands_and_button_nums():
    """
    获得所有的命令信息，以及按钮对应的命令序号，都是字典
    :return: ls_ip -> ip集合，commands_dict ->所有命令字典，button_nums_dic-> NEX：视频1：53,
    button_device_dic-> 灯光管理：公共参观区：【开指令，关指令】
    """
    with open('commands.csv', mode='r', encoding='utf-8') as f:
        commands = f.readlines()
    commands = [i.strip().split(',') for i in commands]
    ls_ip = {i[3] for i in commands}
    commands_dict = {}
    for item in commands:
        key = item[0]
        values = item[1:]
        commands_dict[key] = values

    with open('dict_visit.json', mode='r', encoding='utf-8') as f:
        buttons_visit_dic = json.load(f)

    with open('dict_device.json', mode='r', encoding='utf-8') as f:
        button_device_dic = json.load(f)

    return ls_ip, commands_dict, buttons_visit_dic, button_device_dic


def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[LogListHandler(log_messages)])


class App:
    def __init__(self, root):
        self.root = root
        self.button_visible = False  # 记录按钮的可见性状态

        # 左侧区域（按钮区域）
        self.left_frame = tk.Frame(self.root, highlightthickness=2, highlightbackground="white")
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        # 右侧区域（日志内容或控制界面）
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # 创建日志内容区域，初始时显示
        self.log_text = tk.Text(self.right_frame)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.insert(tk.END, f"Click 'Show Log' to view log messages.\n")

        # 创建控制按钮区域，初始时不显示
        self.in_right_frame_1 = tk.Frame(self.right_frame)
        self.in_right_frame_1.pack_forget()  # 在右侧right_frame的基础上建立一下一样大小的frame,用于隐藏用。
        self.in_right_frame_2 = tk.Frame(self.right_frame)
        self.in_right_frame_2.pack_forget()  # 在右侧right_frame的基础上建立一下一样大小的frame,用于隐藏用。

        # 创建 "Show Log" 按钮，点击后显示日志内容区域
        self.show_log_button = tk.Button(self.left_frame, text="日志", height=1, width=8,
                                         command=lambda: self.show('log'))
        self.show_log_button.pack(side=tk.TOP, padx=10, pady=10)

        # 创建 "Show Control" 按钮，点击后显示控制按钮区域
        self.show_control_button = tk.Button(self.left_frame, text="控制界面", height=1, width=8,
                                             command=lambda: self.show('control'))
        self.show_control_button.pack(side=tk.TOP, padx=10, pady=10)
        self.show_control_button.pack_forget()  # 隐藏按钮

        # 创建 "Show Control" 按钮，点击后显示控制按钮区域
        self.show_devices_button = tk.Button(self.left_frame, text="设备管理", height=1, width=8,
                                             command=lambda: self.show('devices'))
        self.show_devices_button.pack(side=tk.TOP, padx=10, pady=10)
        self.show_devices_button.pack_forget()  # 隐藏按钮

        # 建立后在线程，不会导致阻塞，不然，后台已经运行很久，但是界面不会弹出来
        logging_thread = threading.Thread(target=self.check_devices_on_line)
        logging_thread.start()

        # 绑定 Ctrl+F1 快捷键到特定函数
        self.root.bind("<Control-F1>", self.toggle_hidden_button)
        self.create_control_buttons()  # 创建展厅介绍控制按钮
        # self.create_devices_buttons()  # 创建展厅设备管理按钮
        _thread =  threading.Thread(target=self.create_devices_buttons)
        _thread.start()


    def check_devices_on_line(self):
        """
        用于在启动程序时，检查设备是否在线
        :return:
        """
        def ping_host(host):
            response_time = ping3.ping(host) #ping命令，如果有时延值，说明通的
            print(host,response_time)
            if response_time:
                return f"Host {host} is online. Response time: {response_time} ms"
            else:
                return f"Host {host} is offline or unreachable."

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 使用多线程并发执行设备在线检测
            results = executor.map(ping_host, ls_ip)

            # 输出检测结果
            for result in results:
                if 'online' in result:
                    logging.info(result)
                else:
                    logging.warning(result)

                self.add_log()

    def add_log(self):
        """
        向文本框添加日志条
        """
        if len(log_messages) > 500:
            log_messages.pop(0)  # 删除最早的日志消息
        self.log_text.delete(1.0, tk.END)  # 清空文本框
        for message in reversed(log_messages):
            self.log_text.insert(tk.END, message + '\n')


    def show(self, button_name):
        """
        通用函数，为了给在显示其中一个的时候，其他两个隐藏起来
        :rtype: object
        """
        dic_button_and_show = {"log": self.log_text,
                               "control": self.in_right_frame_1,
                               "devices": self.in_right_frame_2}

        dic_button_and_show[button_name].pack(fill=tk.BOTH, expand=True)  # 显示

        del dic_button_and_show[button_name]
        for i in dic_button_and_show.values():
            i.pack_forget()  # 隐藏

    def create_control_buttons(self):
        Buttons(self.add_log, self.in_right_frame_1, button_visit_dic)

    def create_devices_buttons(self):
        Buttons(self.add_log, self.in_right_frame_2, button_device_dic)
        # _thread = threading.Thread(target=lambda:Buttons(self.add_log, self.in_right_frame_2, button_device_dic))
        # _thread.start()


    def toggle_hidden_button(self, event):  # event,不可以去除，会出错，
        # 切换按钮的可见性状态
        if self.button_visible:
            self.show_control_button.pack_forget()
            self.show_devices_button.pack_forget()
            logging.info("控制界面不可见")
        else:
            self.show_control_button.pack(side=tk.TOP, padx=10, pady=10)
            self.show_control_button.pack()
            self.show_devices_button.pack(side=tk.TOP, padx=10, pady=10)
            self.show_devices_button.pack()
            logging.info("控制界面可见")
        self.button_visible = not self.button_visible

        self.add_log()

        # if len(log_messages) > 500:
        #     log_messages.pop(0)  # 删除最早的日志消息
        # self.log_text.delete(1.0, tk.END)  # 清空文本框
        # for message in reversed(log_messages):
        #     self.log_text.insert(tk.END, message + '\n')


class LogListHandler(logging.Handler):
    def __init__(self, log_messages):
        super().__init__()
        self.log_messages = log_messages

    def emit(self, record):
        log_message = self.format(record)
        self.log_messages.append(log_message)


class Buttons:
    def __init__(self, add_log, right_frame, button_num_dic):
        """
        :param add_log: 这是一个方法，显示日志用的
        :param right_frame: 这是app类的 右边frame
        :param button_num_dic: 全局的常量 有可能是button_visit_dic，也有可能是button_device_dic
        """
        self.add_log = add_log
        self.right_frame = right_frame
        if '序厅大屏' in list(button_num_dic.keys()):# 识别是展厅界绍还是设备管理
            self.visit_button(button_num_dic)
        else:
            self.device_button(button_num_dic)


    def visit_button(self, button_num_dic):
        """
        使展厅介绍的按钮可排布在右边frame
        :param button_num_dic:
        """
        for row_index, (label_text, button_name) in enumerate(rows_visit):
            label = tk.Label(self.right_frame, text=label_text)  # label_text=序厅， button_count=每一个按键的总和
            label.pack()
            buttons_frame = tk.Frame(self.right_frame)
            buttons_frame.pack()
            # print(button_name)
            for col in button_name:  # col=具体每一个按键，如"视频1”
                str_commands = button_num_dic[label_text][col]  # 获得按钮对应的命令参数的序号
                button = tk.Button(buttons_frame, text=f"{col}", height=2, width=8)
                button.bind("<Button-1>",
                            lambda event, str_commands=str_commands: self.button_click(event, str_commands,
                                                                                       commands_dict))
                button.pack(side="left", padx=10, pady=10)


    def device_button(self,button_num_dic):
        for row_index, (label_text, button_name) in enumerate(rows_device):
            label = tk.Label(self.right_frame, text=label_text)
            label.pack()
            if label_text == "全场设备":
                pass
            buttons_frame = tk.Frame(self.right_frame,highlightthickness=2, highlightbackground="white")
            buttons_frame.pack()

            for col in button_name:  # col=具体每一个按键，如"视频1”
                if button_name.index(col)%9==0: # 一行最多放9个按钮，如果多了，就再建一个button_frame
                    buttons_frame = tk.Frame(self.right_frame)
                    buttons_frame.pack()
                str_commands = button_num_dic[label_text][col]  # 获得按钮对应的命令参数的序号
                inner_button = tk.Frame(buttons_frame, highlightthickness=1, highlightbackground="black")
                inner_button.pack(side=tk.LEFT)
                label_button = tk.Label(inner_button, text=col)
                label_button.pack()
                if col == '全场设备开':
                    button_on = tk.Button(inner_button, text=f"开", height=0, width=0)
                    button_on.bind("<Button-1>",
                                   lambda event, str_commands=str_commands[0]: self.button_click(event, str_commands,
                                                                                              commands_dict))
                    button_on.pack(side="left", padx=5, pady=8)
                elif col == '全场设备关':
                    button_on = tk.Button(inner_button, text=f"关", height=0, width=0)
                    button_on.bind("<Button-1>",
                                   lambda event, str_commands=str_commands[0]: self.button_click(event, str_commands,
                                                                                              commands_dict))
                    button_on.pack(side="left", padx=5, pady=8)
                else:
                    button_on = tk.Button(inner_button, text=f"开", height=0, width=0)
                    button_on.bind("<Button-1>",lambda event, str_commands=str_commands[0]: self.button_click(event, str_commands,
                                                                                           commands_dict))
                    button_on.pack(side=tk.LEFT, padx=5, pady=8)
                    button_on = tk.Button(inner_button, text=f"关", height=0, width=0)
                    button_on.bind("<Button-1>",lambda event, str_commands=str_commands[1]: self.button_click(event, str_commands,
                                                                                              commands_dict))
                    button_on.pack(side=tk.LEFT, padx=5, pady=8)



    def button_click(self, event, str_commands, commands_dict):
        button = event.widget
        if ',' in str_commands:  # 不止一个序号，也就是有同步的命令。
            ls = str_commands.split(',')
            # print(ls)
            if '0' in ls:  # 有时延
                len_ls = len(ls)  # 获得列表长度
                # print(len_ls)
                for i in range(len_ls):
                    if i % 2 == 0:  # 偶数就休眠
                        time.sleep(float(ls[i]))
                    else:
                        ls_of_com_detail = commands_dict[ls[i]]
                        # print(ls_of_com_detail)
                        if ls_of_com_detail[1] == '2': # udp连接
                            self.sendudpcommand(ip=ls_of_com_detail[2], port=int(ls_of_com_detail[3]),
                                                hex_data=ls_of_com_detail[4])
                        elif ls_of_com_detail[1] == 'None':  # 唤醒裸眼3D
                            mac_address = "CC-96-E5-24-6F-57"  # 要唤醒计算机的 MAC 地址
                            try:
                                send_magic_packet(mac_address)
                                logging.info('3D主机已发送唤醒命令。')
                                # print("已发送唤醒命令成功。")
                            except Exception as e:
                                logging.warning('3D主机唤醒失败，请确认。')
                                # print("发送唤醒命令失败：", e)
                        else:# Tcp连接
                            self.sendtcpcommand(ip=ls_of_com_detail[2], port=int(ls_of_com_detail[3]),
                                                hex_data=ls_of_com_detail[4])
                            # 需要延迟控制
            else: #没有时延的多指令联动
                for i in ls:
                    ls_of_com_detail = commands_dict[i]
                    if ls_of_com_detail[1] == '2':
                        self.sendudpcommand(ip=ls_of_com_detail[2], port=int(ls_of_com_detail[3]),
                                            hex_data=ls_of_com_detail[4])
                    else:
                        self.sendtcpcommand(ip=ls_of_com_detail[2], port=int(ls_of_com_detail[3]),
                                            hex_data=ls_of_com_detail[4])
        else:  # 直接获得序号，只有一个，单指令
            ls_of_com_detail = commands_dict[str_commands]
            if ls_of_com_detail[1] == '2':
                self.sendudpcommand(ip=ls_of_com_detail[2], port=int(ls_of_com_detail[3]), hex_data=ls_of_com_detail[4])
            else:
                self.sendtcpcommand(ip=ls_of_com_detail[2], port=int(ls_of_com_detail[3]), hex_data=ls_of_com_detail[4])
        # print(f"按钮 {button['text']}（序号：{str_commands}）被点击了")
        logging.info(f"按钮 {button['text']}（序号：{str_commands}）被点击了")
        self.add_log()

    def sendudpcommand(self, ip, port, hex_data):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 将十六进制字符串转换为字节数据
        message_bytes = bytes.fromhex(hex_data)
        udp_socket.sendto(message_bytes, (ip, port))
        udp_socket.close()

    def sendtcpcommand(self, ip, port, hex_data):
        # 创建 TCP 套接字
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 连接到目标服务器
        try:
            tcp_socket.settimeout(0.5)
            tcp_socket.connect((ip, port))
            # 将十六进制字符串转换为字节数据
            message_bytes = bytes.fromhex(hex_data)
            # 发送数据
            tcp_socket.send(message_bytes)
            # 关闭连接
            tcp_socket.close()
        except socket.error as e:
            logging.warning(f"Error: {e}, {ip} 有可能离线了，或者ip地址问题")
            self.add_log()
            # print(f"Error: {e},有可能离线了，或者ip地址问题")


if __name__ == '__main__':
    setup_logging()
    ls_ip, commands_dict, button_visit_dic, button_device_dic = get_commands_and_button_nums()
    root = tk.Tk()
    root.title("中控系统替代平板")
    root.geometry("800x600")  # 设置默认窗口尺寸
    app = App(root)
    root.mainloop()

# 开机所有设备检测，如果不在线显示日志 OK
# 把按键界面移植过来,已经移植展厅界绍，还要移植，设备管理，就变成要三个按钮，不同点击,已经OK,要显示第三页。
# 设备管理的页面，OK,还要加入日志和功能。
# 还需将 错误 如无网络时，获得警靠日志
# 开机有一些屏幕开不了
# 写一个每天重启播放盒的软件
