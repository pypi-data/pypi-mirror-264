#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time,re
from .traffic_control import tc,init_tc,Background_Control
from copy import deepcopy
from .bandCalc import BandCalcByServer


from apscheduler.schedulers.background import BackgroundScheduler


constNetWorkCondition = [0,0,0,0,1000]

#{'testcase': 'down_200k_change_to_400k_samllcatch', 'direction': 'down', 'band': 200, 'delay': 0, 'jiter': 0, 'loss': 0,
 # 'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 30, 'idle': 60, 'change': '0_400'},

class trafficControl():
    def __init__(self,test_device_ip,caseInfo):
        """
        """

        self.caseName = caseInfo['testcase']
        self.DUT = {
                    "ip": test_device_ip,
                    "port": 50001,
        }
        self.scheduler = BackgroundScheduler()
        self.netWorkCondition = deepcopy(constNetWorkCondition)
        self.netWorkCondition = [caseInfo['band'],caseInfo['delay'],caseInfo['jiter'],caseInfo['loss'],caseInfo['packet']]
        print(self.netWorkCondition)
        try:
            self.udpOnlySwitch = caseInfo['only_udp']
        except:
            self.udpOnlySwitch = False
        self.lossType = caseInfo['style']  # stable：固定丢包  burst：突发丢包  real：真实场景  inter：周期性丢包
        self.netDirection = 'up'  #'up' 'down
        try:
            self.backGroundType = caseInfo['bg_type']
        except:
            pass
        try:
            self.interDuration = caseInfo['occupy']
            self.interInterval = caseInfo['idle']
        except:
            pass
        try:
            self.interMertic = caseInfo['change']
        except:
            self.interMertic = 'None'
        try:
            self.doubleNet = caseInfo['doubleNet']
        except:
            self.doubleNet = 0
        self.background_control = Background_Control()


    def reset_network(self):
        """
        :return:
        """
        self.netWorkCondition = deepcopy(constNetWorkCondition)

        if self.lossType == 'inter':
            if self.scheduler.running:
                self.scheduler.shutdown()
            init_tc(self.DUT['ip'])
        else:
            init_tc(self.DUT['ip'])
        self.background_control.stop_traffic_gen()


    def set_period_network(self, duration):

        tc(self.netDirection, self.DUT['ip'], self.netWorkCondition[0], self.netWorkCondition[1],
           self.netWorkCondition[2],
           self.netWorkCondition[3], self.netWorkCondition[4], self.udpOnlySwitch,doubleFlag=self.doubleNet)


        time.sleep(duration)
        anotherNetWorkCondition = deepcopy(self.netWorkCondition)
        if self.interMertic == 'None':
            init_tc(self.DUT['ip'])
        else:
            curMertic = self.interMertic.split("_")[0]
            curValue = self.interMertic.split("_")[1]
            anotherNetWorkCondition[int(curMertic)] = int(curValue)

            tc(self.netDirection, self.DUT['ip'],anotherNetWorkCondition[0], anotherNetWorkCondition[1],
               anotherNetWorkCondition[2],
               anotherNetWorkCondition[3], anotherNetWorkCondition[4], self.udpOnlySwitch,doubleFlag=self.doubleNet)

    def set_network(self):
        """
        :return:
        """

        if self.lossType == 'inter':

            self.scheduler = BackgroundScheduler()
            self.scheduler.add_job(self.set_period_network, 'interval', seconds=int(self.interInterval) + int(self.interDuration), args=[int(self.interDuration)])
            self.scheduler.start()

        elif self.lossType == 'background':
            self.background_control.direction = self.netDirection
            self.background_control.protocol = self.backGroundType
            self.background_control.profile = 'profile_'+ str(self.netWorkCondition[0]) +'kbps.txt'
            self.background_control.start_traffic_gen()
            tc(self.netDirection, self.DUT['ip'], self.netWorkCondition[0], self.netWorkCondition[1],
               self.netWorkCondition[2],
               self.netWorkCondition[3], self.netWorkCondition[4], self.udpOnlySwitch,is_background=True,doubleFlag=self.doubleNet)



        elif self.lossType == 'real':
            tc(self.netDirection, self.DUT['ip'], 0, self.netWorkCondition[1],
               self.netWorkCondition[2],
               self.netWorkCondition[3], self.netWorkCondition[4], self.udpOnlySwitch,model=self.netWorkCondition[0],doubleFlag=self.doubleNet)
        elif self.lossType == 'burst':
            tc(self.netDirection, self.DUT['ip'], self.netWorkCondition[0], self.netWorkCondition[1],
               self.netWorkCondition[2],
               self.netWorkCondition[3], self.netWorkCondition[4], self.udpOnlySwitch,is_burst_loss=True,doubleFlag=self.doubleNet)
        else:
            tc(self.netDirection, self.DUT['ip'], self.netWorkCondition[0], self.netWorkCondition[1],
               self.netWorkCondition[2],
               self.netWorkCondition[3], self.netWorkCondition[4], self.udpOnlySwitch,doubleFlag=self.doubleNet)

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
    #scheduler = BackgroundScheduler()

        #global_cmmD.reset_network()
    ip = '192.168.2.4'
    case = {'testcase': 'double_100k_Intermittent_samllcatch', 'direction': 'up', 'band': 100, 'delay': 0, 'jiter': 0, 'loss': 0,'packet': 1, 'style': 'inter', 'only_udp': False, 'occupy': 2, 'idle': 2,'doubleNet':1}
    global_cmmD = trafficControl(ip,case)
    global_cmmD.start_netdump()
    global_cmmD.set_network()
    time.sleep(60)
    global_cmmD.reset_network()
    global_cmmD.stop_netdump()
    exit(0)
