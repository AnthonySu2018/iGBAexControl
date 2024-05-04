a = '''序厅LED	172.18.0.33
序厅工控屏	172.18.0.10
历史墙投影仪	172.18.0.11
Intel Vision LED	172.18.0.34
服务器拼接屏1	172.18.0.12
服务器拼接屏2	172.18.0.13
服务器拼接屏3	172.18.0.14
服务器拼接屏4	172.18.0.15
XFusion工控屏	172.18.0.20
OCSP拼接屏1	172.18.0.16
OCSP拼接屏2	172.18.0.17
OCSP拼接屏3	172.18.0.18
OCSP拼接屏4	172.18.0.19
芯片产业链工控屏	172.18.0.22
Motherboard工控屏	172.18.0.23
显卡工控屏	172.18.0.24
CCG Vision LED	172.18.0.35
Green PC工控屏	172.18.0.21
NEX LED	172.18.0.37
超能云终端工控屏	172.18.0.25
5G小基站	172.18.0.26
闸机工控屏	172.18.0.27
智慧灯杆工控屏	172.18.0.28
AI Box工控屏	172.18.0.29
缺陷检测工控屏	172.18.0.30
汽车LED	172.18.0.36
大族激光工控屏	172.18.0.31
飞拍工控屏	172.18.0.32
机械臂工控屏	172.18.0.39
厅外LED	172.18.0.38
'''
# b= a.split('\n')
# print(b)
# c = [i.split('\t') for i in b]
# print(c)
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

# print(len(li_locate_ip))

import json

data = [{'cid': '001', 'cameraName': 'test01', 'cameraLocation': '序厅', 'url': 'rtsp://testing:bun@2o16@172.18.0.100:554/Streaming/Channels/101', 'status': '0', 'algoInfoList': [{'algoId': 10702, 'algoName': '打电话识别'}, {'algoId': 10856, 'algoName': '反光衣识别'}, {'algoId': 9842, 'algoName': '抽烟识别'}]}, {'cid': '002', 'cameraName': 'test02', 'cameraLocation': '历史墙', 'url': 'rtsp://testing:bun@2o16@172.18.0.100:554/Streaming/Channels/301', 'status': '0', 'algoInfoList': [{'algoId': 10702, 'algoName': '打电话识别'}, {'algoId': 10856, 'algoName': '反光衣识别'}, {'algoId': 9842, 'algoName': '抽烟识别'}]}, {'cid': '003', 'cameraName': 'test03', 'cameraLocation': 'vision', 'url': 'rtsp://testing:bun@2o16@172.18.0.100:554/Streaming/Channels/401', 'status': '0', 'algoInfoList': [{'algoId': 10702, 'algoName': '打电话识别'}, {'algoId': 10856, 'algoName': '反光衣识别'}, {'algoId': 9842, 'algoName': '抽烟识别'}]}, {'cid': '004', 'cameraName': 'test04', 'cameraLocation': 'pcbooth', 'url': 'rtsp://testing:bun@2o16@172.18.0.100:554/Streaming/Channels/501', 'status': '0', 'algoInfoList': [{'algoId': 10702, 'algoName': '打电话识别'}, {'algoId': 10856, 'algoName': '反光衣识别'}]}, {'cid': '005', 'cameraName': 'test05', 'cameraLocation': 'greenpc', 'url': 'rtsp://testing:bun@2o16@172.18.0.100:554/Streaming/Channels/801', 'status': '0', 'algoInfoList': [{'algoId': 10702, 'algoName': '打电话识别'}, {'algoId': 10856, 'algoName': '反光衣识别'}]}]

# 将字典转换为JSON字符串，并使用四个空格进行缩进
json_string = json.dumps(data, indent=4)

# 将字典转换为JSON字符串，并使用四个空格进行缩进
json_string = json.dumps(data, indent=4, ensure_ascii=False)

# 指定要写入的文件名
file_name = "output.json"

# 打开文件并写入JSON数据
with open('heart_beat.txt', "w", encoding='utf-8') as json_file:
    json_file.write(json_string)

print(f"JSON数据已写入到文件 '{file_name}'")