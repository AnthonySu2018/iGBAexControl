from flask import Flask, request, jsonify
import socket,time,logging
from wakeonlan import send_magic_packet
# app = Flask(__name__)
# app.json.ensure_ascii=False
# dic = {'类型':'','区域':'','指令名':'',}
#
#
#
# @app.route('/send_command', methods=['POST'])
# def receive_command():
#     data = request.get_json()  # 获取POST请求的JSON数据,并还原成字典
#     # 判断属于哪种类型，哪个区域，哪种命令。
#
#
#
#     # 在这里处理接收到的数据
#     response_data = {'message': data}
#     return jsonify(response_data)
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

server_running = True

class HandlePadCommand:
    def __init__(self,logging, commands_dic, visit_dic, device_dic):
        self.logging = logging
        self.app = Flask(__name__)
        self.app.json.ensure_ascii = False
        self.setup_routes()
        self.commands_dic = commands_dic
        self.visit_dic = visit_dic
        self.device_dic = device_dic

    def setup_routes(self):
        self.app.route('/send_command', methods=['POST'])(self.send_command)

    def run(self):
        while server_running:
            self.app.run(host='0.0.0.0', port=5000,debug=False)

    def close(self):
        pass
    def send_command(self):
        data = request.get_json()#获得json并还原成字典或者列表
        #接下来是处理数据的过程
        self.process_command(data, self.commands_dic,self.visit_dic,self.device_dic)
        result = {'message': '命令已执行', 'data': data}
        print(result)
        return jsonify(result)

    def process_command(self, data: dict, commands_dic:dict, visit_dic: dict, device_dic: dict) -> object:
        # 执行处理命令的操作
        # 先判断 什么类型：

        # 判断类型，然后获得命令集
        if data.get('类型') == '展厅介绍':# 展厅介绍，序厅大屏，视频1
            area = data.get('区域')
            command_name = data.get('命令名')
            str_commands = visit_dic[area][command_name]
        elif data.get('类型') == '展厅开关':#展厅开关，全场设备，全场设备开
            key_1st = data.get('一级键')
            command_name = data.get('命令名')
            str_commands = device_dic[key_1st][command_name][0]
        else:#灯光管理，公共参观区，开/关
            key_1st = data.get('一级键')
            key_2nd = data.get('二级键')
            command_name = 0 if data.get('命令名')=='开' else 1
            str_commands = device_dic[key_1st][key_2nd][command_name]
        # print(str_commands,commands_dic)
        Handle_commands.send_command(str_commands, commands_dic)
        self.logging.info(data)

class Handle_commands:
    def __int__(self):
        pass
    @staticmethod
    def send_command(str_commands, commands_dict):
        """
        处理传过来的指令，或者指令集，然后从commands_dict去取对应的指令参数，发送指令到终端设备
        :param str_commands: 指令，或者指令集，指令集中，有一些是有延时的，都在这里面处理
        :param commands_dict: 所有指令
        """
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
                            Handle_commands.sendudpcommand(ip=ls_of_com_detail[2], port=int(ls_of_com_detail[3]),
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
                            Handle_commands.sendtcpcommand(ip=ls_of_com_detail[2], port=int(ls_of_com_detail[3]),
                                                hex_data=ls_of_com_detail[4])
                            # 需要延迟控制
            else: #没有时延的多指令联动
                for i in ls:
                    ls_of_com_detail = commands_dict[i]
                    if ls_of_com_detail[1] == '2':
                        Handle_commands.sendudpcommand(ip=ls_of_com_detail[2], port=int(ls_of_com_detail[3]),
                                            hex_data=ls_of_com_detail[4])
                    else:
                        Handle_commands.sendtcpcommand(ip=ls_of_com_detail[2], port=int(ls_of_com_detail[3]),
                                            hex_data=ls_of_com_detail[4])
        else:  # 直接获得序号，只有一个，单指令
            ls_of_com_detail = commands_dict[str_commands]
            if ls_of_com_detail[1] == '2':
                Handle_commands.sendudpcommand(ip=ls_of_com_detail[2], port=int(ls_of_com_detail[3]), hex_data=ls_of_com_detail[4])
            else:
                Handle_commands.sendtcpcommand(ip=ls_of_com_detail[2], port=int(ls_of_com_detail[3]), hex_data=ls_of_com_detail[4])

    @staticmethod
    def sendudpcommand(ip, port, hex_data):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 将十六进制字符串转换为字节数据
        message_bytes = bytes.fromhex(hex_data)
        udp_socket.sendto(message_bytes, (ip, port))
        udp_socket.close()

    @staticmethod
    def sendtcpcommand(ip, port, hex_data):
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
            # print(f"Error: {e},有可能离线了，或者ip地址问题")

if __name__ == '__main__':

    my_app = HandlePadCommand(logging,'','','')
    my_app.run()
