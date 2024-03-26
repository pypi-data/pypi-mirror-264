#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .test_case import testSuite,testcases
import time,re
from .traffic_control import tc,init_tc,Background_Control
from copy import deepcopy
from .bandCalc import BandCalcByServer


from apscheduler.schedulers.background import BackgroundScheduler


constNetWorkCondition = [0,0,0,0,1000]

#{'testcase': 'down_200k_change_to_400k_samllcatch', 'direction': 'down', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,
 # 'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 30, 'idle': 60, 'change': '0_400'},

class trafficControl():
    def __init__(self,test_device_ip,caseName):
        """
        """
        # 预设若弱网 or 自定义弱网
        try:
            caseInfo = testSuite[caseName]
            self.caseName = caseName
        except:
            caseInfo = caseName
            self.caseName = 'usrDefine'
        #
        self.DUT = {
                    "ip": test_device_ip,
                    "port": 50001,
        }

        self.upscheduler = BackgroundScheduler()
        self.downscheduler = BackgroundScheduler()
        # 初始化网络
        self.upnetWorkCondition = deepcopy(constNetWorkCondition)
        self.downnetWorkCondition = deepcopy(constNetWorkCondition)
        # 网络赋值
        self.upnetWorkCondition = [caseInfo['up']['band'],caseInfo['up']['delay'],caseInfo['up']['jiter'],caseInfo['up']['loss'],caseInfo['up']['packet']]
        self.downnetWorkCondition = [caseInfo['down']['band'], caseInfo['down']['delay'], caseInfo['down']['jiter'], caseInfo['down']['loss'],caseInfo['down']['packet']]
        print(self.upnetWorkCondition)
        print(self.downnetWorkCondition)
        # upd 开关
        try:
            self.upudpOnlySwitch = caseInfo['up']['only_udp']
        except:
            self.upudpOnlySwitch = False

        try:
            self.downudpOnlySwitch = caseInfo['down']['only_udp']
        except:
            self.downudpOnlySwitch = False
        # 弱网类型   stable：固定丢包  burst：突发丢包  real：真实场景  inter：周期性丢包
        self.uplossType = caseInfo['up']['style']
        self.downlossType = caseInfo['down']['style']

        # 背景流量类型  tcp udp
        try:
            self.upbackGroundType = caseInfo['bg_type']
        except:
            pass
        try:
            self.downbackGroundType = caseInfo['bg_type']
        except:
            pass
        # 周期网络赋值
        try:
            self.upinterDuration = caseInfo['occupy']
            self.upinterInterval = caseInfo['idle']
        except:
            self.upinterDuration = 5
            self.upinterInterval = 30

        try:
            self.downinterDuration = caseInfo['occupy']
            self.downinterInterval = caseInfo['idle']
        except:
            self.downinterDuration = 5
            self.downinterInterval = 30
        # 网络变换 赋值
        try:
            self.upinterMertic = caseInfo['change']
        except:
            self.upinterMertic = 'None'

        try:
            self.downinterMertic = caseInfo['change']
        except:
            self.downinterMertic = 'None'

        self.upbackground_control = Background_Control()

        self.downbackground_control = Background_Control()

    def reset_network(self):
        """
        :return:
        """
        self.upnetWorkCondition = deepcopy(constNetWorkCondition)
        self.downnetWorkCondition = deepcopy(constNetWorkCondition)

        if self.uplossType == 'inter' or self.downlossType == 'inter':
            if self.upscheduler.running:
                self.upscheduler.shutdown()
            if self.downscheduler.running:
                self.downscheduler.shutdown()
            init_tc(self.DUT['ip'])
        else:
            init_tc(self.DUT['ip'])
        self.upbackground_control.stop_traffic_gen()
        self.downbackground_control.stop_traffic_gen()


    def set_period_network(self, direciton,duration):
        if direciton == 'up':
            tc(direciton, self.DUT['ip'], self.upnetWorkCondition[0], self.upnetWorkCondition[1],
               self.upnetWorkCondition[2],
               self.upnetWorkCondition[3], self.upnetWorkCondition[4], self.upudpOnlySwitch)


            time.sleep(duration)
            anotherNetWorkCondition = deepcopy(self.upnetWorkCondition)
            if self.upinterMertic == 'None':
                init_tc(self.DUT['ip'])
            else:
                curMertic = self.upinterMertic.split("_")[0]
                curValue = self.upinterMertic.split("_")[1]
                anotherNetWorkCondition[int(curMertic)] = int(curValue)

                tc(direciton, self.DUT['ip'],anotherNetWorkCondition[0], anotherNetWorkCondition[1],
                   anotherNetWorkCondition[2],
                   anotherNetWorkCondition[3], anotherNetWorkCondition[4], self.upudpOnlySwitch)
        elif direciton == 'down':
            tc(direciton, self.DUT['ip'], self.downnetWorkCondition[0], self.downnetWorkCondition[1],
               self.downnetWorkCondition[2],
               self.downnetWorkCondition[3], self.downnetWorkCondition[4], self.downudpOnlySwitch)

            time.sleep(duration)
            anotherNetWorkCondition = deepcopy(self.downnetWorkCondition)
            if self.downinterMertic == 'None':
                init_tc(self.DUT['ip'])
            else:
                curMertic = self.downinterMertic.split("_")[0]
                curValue = self.downinterMertic.split("_")[1]
                anotherNetWorkCondition[int(curMertic)] = int(curValue)

                tc(direciton, self.DUT['ip'], anotherNetWorkCondition[0], anotherNetWorkCondition[1],
                   anotherNetWorkCondition[2],
                   anotherNetWorkCondition[3], anotherNetWorkCondition[4], self.upudpOnlySwitch)
    def set_network(self):
        self.set_up_network()
        self.set_down_network()
    def set_up_network(self):
        """
        :return:
        """

        if self.uplossType == 'inter':

            self.upscheduler = BackgroundScheduler()
            self.upscheduler.add_job(self.set_period_network, 'interval', seconds=int(self.upinterInterval) + int(self.upinterDuration), args=['up',int(self.upinterDuration)])
            self.upscheduler.start()

        elif self.uplossType == 'background':
            self.upbackground_control.direction = 'up'
            self.upbackground_control.protocol = self.upbackGroundType
            self.upbackground_control.profile = 'profile_'+ str(self.upnetWorkCondition[0]) +'kbps.txt'
            self.upbackground_control.start_traffic_gen()
            tc('up', self.DUT['ip'], self.upnetWorkCondition[0], self.upnetWorkCondition[1],
               self.upnetWorkCondition[2],
               self.upnetWorkCondition[3], self.upnetWorkCondition[4], self.upudpOnlySwitch,is_background=True)



        elif self.uplossType == 'real':
            tc('up', self.DUT['ip'], 0, self.upnetWorkCondition[1],
               self.upnetWorkCondition[2],
               self.upnetWorkCondition[3], self.upnetWorkCondition[4], self.upudpOnlySwitch,model=self.upnetWorkCondition[0])
            tc('up', self.DUT['ip'], 0, self.upnetWorkCondition[1],
               self.upnetWorkCondition[2],
               self.upnetWorkCondition[3], self.upnetWorkCondition[4], self.upudpOnlySwitch,model=self.upnetWorkCondition[0])
        elif self.uplossType == 'burst':
            tc('up', self.DUT['ip'], self.upnetWorkCondition[0], self.upnetWorkCondition[1],
               self.upnetWorkCondition[2],
               self.upnetWorkCondition[3], self.upnetWorkCondition[4], self.upudpOnlySwitch,is_burst_loss=True)
        else:
            tc('up', self.DUT['ip'], self.upnetWorkCondition[0], self.upnetWorkCondition[1],
               self.upnetWorkCondition[2],
               self.upnetWorkCondition[3], self.upnetWorkCondition[4], self.upudpOnlySwitch)
    def set_down_network(self):
        """
        :return:
        """
        if self.downlossType == 'inter':

            self.downscheduler = BackgroundScheduler()
            self.downscheduler.add_job(self.set_period_network, 'interval', seconds=int(self.downinterInterval) + int(self.downinterDuration), args=['down',int(self.downinterDuration)])
            self.downscheduler.start()

        elif self.downlossType == 'background':
            self.downbackground_control.direction = 'down'
            self.downbackground_control.protocol = self.downbackGroundType
            self.downbackground_control.profile = 'profile_'+ str(self.downnetWorkCondition[0]) +'kbps.txt'
            self.downbackground_control.start_traffic_gen()
            tc('down', self.DUT['ip'], self.downnetWorkCondition[0], self.downnetWorkCondition[1],
               self.downnetWorkCondition[2],
               self.downnetWorkCondition[3], self.downnetWorkCondition[4], self.downudpOnlySwitch,is_background=True)

        elif self.downlossType == 'real':
            tc('down', self.DUT['ip'], 0, self.downnetWorkCondition[1],
               self.downnetWorkCondition[2],
               self.downnetWorkCondition[3], self.downnetWorkCondition[4], self.downudpOnlySwitch,model=self.downnetWorkCondition[0])
            tc('down', self.DUT['ip'], 0, self.downnetWorkCondition[1],
               self.downnetWorkCondition[2],
               self.downnetWorkCondition[3], self.downnetWorkCondition[4], self.downudpOnlySwitch,model=self.downnetWorkCondition[0])
        elif self.downlossType == 'burst':
            tc('down', self.DUT['ip'], self.downnetWorkCondition[0], self.downnetWorkCondition[1],
               self.downnetWorkCondition[2],
               self.downnetWorkCondition[3], self.downnetWorkCondition[4], self.downudpOnlySwitch,is_burst_loss=True)
        else:
            tc('down', self.DUT['ip'], self.downnetWorkCondition[0], self.downnetWorkCondition[1],
               self.downnetWorkCondition[2],
               self.downnetWorkCondition[3], self.downnetWorkCondition[4], self.downudpOnlySwitch)


    def start_netdump(self):
        """
        :return:
        """
        self.bandres = {"up_mean":0,"up_max":0,"up_min":0,"down_mean":0,"down_max":0,"down_min":0}
        self.band = BandCalcByServer(self.DUT['ip'], self.DUT['ip'], self.caseName)

        self.band.start_capture()

    def stop_netdump(self):
        """
        :return:
        """
        res = self.band.stop_capture()
        allines = res.split('\n')
        print(allines)
        if 'upband' in allines[0] and 'downband' in allines[1]:
            self.bandres['up_mean'] = re.split(':|kbps',allines[0])[2]
            self.bandres['up_max'] = re.split(':|kbps', allines[0])[4]
            self.bandres['up_min'] = re.split(':|kbps', allines[0])[6]
            self.bandres['down_mean'] = re.split(':|kbps',allines[1])[2]
            self.bandres['down_max'] = re.split(':|kbps', allines[1])[4]
            self.bandres['down_min'] = re.split(':|kbps', allines[1])[6]
        else:
            self.bandres = {"up_mean": 0, "up_max": 0, "up_min": 0, "down_mean": 0, "down_max": 0, "down_min": 0}









if __name__ == '__main__':
    ip = '192.168.2.4'
    case = {'testcase': 'double_100k_Intermittent_samllcatch', 'direction': 'up', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 2, 'idle': 2,'doubleNet':1}
    global_cmmD = trafficControl(ip,case)
    global_cmmD.start_netdump()
    global_cmmD.set_network()
    time.sleep(60)
    global_cmmD.reset_network()
    global_cmmD.stop_netdump()
    exit(0)
