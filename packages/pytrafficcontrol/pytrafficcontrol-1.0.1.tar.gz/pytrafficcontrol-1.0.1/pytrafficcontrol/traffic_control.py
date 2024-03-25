#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
真是弱网场景：
dl-canteen-rate
dl-drive-rate
dl-parking-rate
india-office-ul
india-station-ul
sa-ul
ul-canteen-rate
ul-drive-rate
ul-parking-rate
vn-office-rate
vn-parking-ul
"""

import paramiko
# 重载sys模块，以支持对utf8编码
import sys


import requests
#from apscheduler.schedulers.background import BackgroundScheduler

Background_IP = '192.168.2.7'
TC_IP = '192.168.2.1'


class Background_Control:
    def __init__(self):
        self.tc_ip = TC_IP
        self.background_ip = Background_IP
        self.protocol = 'udp'
        self.profile = 'profile_2000kbps.txt'
        self.direction = 'up'

    @staticmethod
    def send_request(dst_ip, api, para=None):
        url = "http://" + dst_ip + ":50001/" + api
        print(url, para)
        res = requests.post(url, json=para)
        print(res)
        return res

    def start_traffic_gen(self):
        if self.direction == 'up':
            server_ip, client_ip = self.tc_ip, self.background_ip
        elif self.direction == 'down':
            server_ip, client_ip = self.background_ip, self.tc_ip
        else:
            print('direction error should be up or down')
        api = 'start_traffic_gen'
        data = {'type': 'server', 'protocol': self.protocol, 'profile': self.profile, 'server_ip': server_ip}
        self.send_request(server_ip, api, data)
        data = {'type': 'client', 'protocol': self.protocol, 'profile': self.profile, 'server_ip': server_ip}
        self.send_request(client_ip, api, data)

    def stop_traffic_gen(self):
        if self.direction == 'up':
            server_ip, client_ip = self.tc_ip, self.background_ip
        elif self.direction == 'down':
            server_ip, client_ip = self.background_ip, self.tc_ip
        else:
            print('direction error should be up or down')
        api = 'stop_traffic_gen'
        data = {'type': 'server', 'protocol': self.protocol, 'profile': self.profile, 'server_ip': server_ip}
        self.send_request(server_ip, api, data)
        data = {'type': 'client', 'protocol': self.protocol, 'profile': self.profile, 'server_ip': server_ip}
        self.send_request(client_ip, api, data)

    def clear_all(self):
        server_ip, client_ip = self.tc_ip, self.background_ip
        api = 'stop_traffic_gen'
        data = {'type': 'server', 'protocol': self.protocol, 'profile': self.profile, 'server_ip': server_ip}
        self.send_request(server_ip, api, data)
        data = {'type': 'client', 'protocol': self.protocol, 'profile': self.profile, 'server_ip': server_ip}
        self.send_request(client_ip, api, data)


def init_tc(ip):
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 把要连接的机器添加到known_hosts文件中
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname='10.219.120.82', port=22, username='netease', password='Nora3390', allow_agent=False,
                look_for_keys=False)
    # ssh.connect(hostname='10.219.28.184', port=22, username='wang', password='0321', allow_agent=False,
    #             look_for_keys=False)
    cmd = "./tc_config_allinone.py clear " + ip + " 0 0 0 0 200000;./tc_config_allinone.py clear " + Background_IP + " 0 0 0 0 200000"
    print(cmd)

    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
    result = stdout.read()
    print(result.decode())
    ssh.close()


def tc(direction, ip, band, delay, jitter, loss, buffer, is_udp=False, is_burst_loss=False, model='na',
       is_background=False,doubleFlag=0):
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 把要连接的机器添加到known_hosts文件中
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='10.219.120.82', port=22, username='netease', password='Nora3390', allow_agent=False,
                look_for_keys=False)
    background_ip = Background_IP if is_background else ''
    cmd = './tc_config_allinone.py ' + direction + ' ' + str(ip) + ' ' + str(band) + ' ' + str(delay) + ' ' + str(
        jitter) + ' ' + str(loss) + ' ' + str(buffer) + ' ' + str(is_udp) + ' ' + str(is_burst_loss) + ' ' + model \
          + ' ' + str(background_ip)
    # 多个命令用;隔开
    if doubleFlag:
        curdirction = 'down' if direction == "up" else 'up'
        cmd += '; ./tc_config_allinone.py ' + curdirction + ' ' + str(ip) + ' ' + str(band) + ' ' + str(delay) + ' ' + str(
        jitter) + ' ' + str(loss) + ' ' + str(buffer) + ' ' + str(is_udp) + ' ' + str(is_burst_loss) + ' ' + model \
          + ' ' + str(background_ip)
    print(cmd)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    result = stdout.read() 
    if not result:
        result = stderr.read()
    ssh.close()
    print(result.decode())


if __name__ == '__main__':
    # bgc = Background_Control()
    # bgc.start_traffic_gen()
    # time.sleep(10)
    # bgc.stop_traffic_gen()
    import time            #band delay jitter loss buffer

    tc('down', '192.168.2.4', 0, 1000, 500, 80, 200, True, True)
    time.sleep(20)
    init_tc('192.168.2.4')
    exit(0)
