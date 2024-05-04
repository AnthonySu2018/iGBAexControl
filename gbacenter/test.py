import tkinter as tk
import socket


def send_udp_command(udp_host, udp_port, udp_command):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(udp_command, (udp_host, udp_port))
    udp_socket.close()


def button_click(event, udp_host, udp_port, udp_command):
    send_udp_command(udp_host, udp_port, udp_command)
    print(f"发送到 {udp_host}:{udp_port} 的命令：{udp_command}")


root = tk.Tk()

buttons_data = [
    {"label": "按钮1", "udp_host": "172.18.0.34", "udp_port": 50505, "udp_command": bytes.fromhex("31 37 32 2E 31 38 2E 30 2E 33 34 4B 30 31 30 31 45 4E 44")},
    {"label": "按钮2", "udp_host": "172.18.0.34", "udp_port": 50505, "udp_command": bytes.fromhex("31 37 32 2E 31 38 2E 30 2E 33 34 43 54 4C 50 53 45 4E 44")},
    # 添加更多按钮数据
]

for button_data in buttons_data:
    label = button_data["label"]
    udp_host = button_data["udp_host"]
    udp_port = button_data["udp_port"]
    udp_command = button_data["udp_command"]

    button = tk.Button(root, text=label)
    button.pack()
    button.bind("<Button-1>",
                lambda event, host=udp_host, port=udp_port, cmd=udp_command: button_click(event, host, port, cmd))

root.mainloop()