import time


import paramiko



class BandCalcByServer:

    def __init__(self, src_ip, dst_ip,pcap_name):
        self.src = src_ip
        self.dst = dst_ip
        self.pcap_name = pcap_name

    def start_capture(self):
        # 创建SSH对象
        ssh = paramiko.SSHClient()
        # 把要连接的机器添加到known_hosts文件中
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname='10.219.120.82', port=22, username='netease', password='Nora3390', allow_agent=False,
                    look_for_keys=False)
        cmd = './get_traffic_info.py 1 ' + self.src + " " + self.dst + " " + self.pcap_name
        print(cmd)
        ssh.exec_command(cmd, timeout=1)
        ssh.close()


    def stop_capture(self):
        # 创建SSH对象
        ssh = paramiko.SSHClient()
        # 把要连接的机器添加到known_hosts文件中
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname='10.219.120.82', port=22, username='netease', password='Nora3390', allow_agent=False,
                    look_for_keys=False)
        cmd = './get_traffic_info.py 0 ' + self.src + " " + self.dst + " " + self.pcap_name
        print(cmd)
        stdin, stdout, stderr = ssh.exec_command(cmd,timeout=360)
        result = stdout.read()
        if not result:
            result = stderr.read()
        ssh.close()
        print(result.decode())
        return result.decode()


if __name__ == '__main__':
    import re
    band = BandCalcByServer('192.168.2.4', '192.168.2.4','test')
    band.start_capture()
    time.sleep(25)
    lines = band.stop_capture()
    twoline = lines.split('\n')
    for a in twoline:
        en = re.split(':|kbps',a)
        print(en)

