# -*- coding:UTF-8 -*-


import logging
import time, os, sys
import pytest

from ixnetwork_restpy import Files
from common.reboot import logger
from common.ixia.ixia_helpers import *
from common.helpers.assertions import pytest_assert
from ixnetwork_restpy import TestPlatform


"""
TO UPDATE
"""

def test_ixia_cmd(ixiahost,testbed, duthost):
    
    ###############################################################
    #                   STEP1: 准备预置条件
    ###############################################################
    
    #1.1 设置全局结果，默认为True, 如果中间检测点不通过，将该值更新为False
    result = True 
    
    #1.2 设置测试仪表IxNetwork配置文件名称，建议和测试例函数同名
    configFile = os.path.join(os.path.dirname(__file__), sys._getframe().f_code.co_name + '.ixncfg')
    #logger.info(configFile)
    
    #1.3 根据testbed.csv中dut列的输入值获取dut名字和ip
    dut_name = testbed['duts'][0]
    dut_ip = duthost.host.options['inventory_manager'].get_host(dut_name).get_vars()['ansible_host']
    dut_usr = duthost.host.options['inventory_manager'].get_host(dut_name).get_vars()['ansible_ssh_user']
    dut_pwd = duthost.host.options['inventory_manager'].get_host(dut_name).get_vars()['ansible_ssh_pass']


    #1.4 获取拓扑连接信息，获得intf, vlanid, 其中intf用于配置DUT, vlanid用于更新测试仪表配置文件
    logger_msg(u'获取拓扑连接信息。')
    intf, vlanid = get_connection_info(testbed)

    #1.5 创建Ixia session, 返回session句柄和测试环境中要使用的端口信息
    logger_msg(u'创建 Ixia Session IP。') 
    session, portList = ixiahost    
    
    
    ###############################################################
    #                   STEP2: 下发DUT配置
    ###############################################################
    CmdList = []
    CmdList.append('enable')
    CmdList.append('123!@#$%^&*()')
    CmdList.append('!12zxc@#}_*^:')
    CmdList.append('neighbor 10.0.0.23 remote-as 65200')
    CmdList.append('history | tail')
    send_cmd(dut_ip, dut_usr, dut_pwd, cmd=CmdList)

    logger_msg('11111111111111111111111111111')
    os.system('pause')
    import pdb
    pdb.set_trece()
    CmdList.append('start-shell')
    CmdList.append('ip neigh')
    CmdList.append('route')
    CmdList.append('bcmsh')
    CmdList.append('ls show')
    CmdList.append('ctrl c')
    CmdList.append('ip neigh')
    CmdList.append('route')
    send_cmd(dut_ip, dut_usr, dut_pwd, cmd=CmdList)

    CmdList = []
    CmdList.append('enable')
    CmdList.append('config')
    CmdList.append('aaaaaaaaaaa')
    send_cmd(dut_ip, dut_usr, dut_pwd, cmd=CmdList)

    CmdList = []
    CmdList.append('enable')
    CmdList.append('config')
    CmdList.append('11111111111')
    send_cmd(dut_ip, dut_usr, dut_pwd, cmd=CmdList)
    CmdList = []
    CmdList.append('enable')
    CmdList.append('config')
    CmdList.append('2222222222')
    send_cmd(dut_ip, dut_usr, dut_pwd, cmd=CmdList)
    CmdList = []
    CmdList.append('enable')
    CmdList.append('config')
    CmdList.append('3333333333333333')
    send_cmd(dut_ip, dut_usr, dut_pwd, cmd=CmdList)
    CmdList = []
    CmdList.append('enable')
    CmdList.append('config')
    CmdList.append('444444444444444444')
    send_cmd(dut_ip, dut_usr, dut_pwd, cmd=CmdList)

    CmdList = []
    CmdList.append('enable')
    CmdList.append('config')
    CmdList.append('55555555555555')
    send_cmd(dut_ip, dut_usr, dut_pwd, cmd=CmdList)
    CmdList = []
    CmdList.append('enable')
    CmdList.append('config')
    CmdList.append('6666666666666666')
    send_cmd(dut_ip, dut_usr, dut_pwd, cmd=CmdList)
    CmdList = []
    CmdList.append('enable')
    CmdList.append('config')
    CmdList.append('777777777777777')
    send_cmd(dut_ip, dut_usr, dut_pwd, cmd=CmdList)
    CmdList = []
    CmdList.append('enable')
    CmdList.append('config')
    CmdList.append('888888888888888')
    send_cmd(dut_ip, dut_usr, dut_pwd, cmd=CmdList)
    CmdList = []
    CmdList.append('enable')
    CmdList.append('config')
    CmdList.append('99999999999999')
    send_cmd(dut_ip, dut_usr, dut_pwd, cmd=CmdList)
    CmdList = []
    CmdList.append('enable')
    CmdList.append('config')
    CmdList.append('bbbbbbbbbbbb')
    send_cmd(dut_ip, dut_usr, dut_pwd, cmd=CmdList)

    
    ###############################################################
    #                   STEP3: 测试仪表相关操作
    ###############################################################
    
    #time.sleep(30)
    
        
    ###############################################################
    #                STEP4: 登录到DUT,检测协议状态
    ###############################################################
    #Step4: 登录到DUT,检测协议状态，根据check点，更新全局结果变量result
    CmdList = []
    CmdList.append('show bgp summary')
    send_cmd(dut_ip,dut_usr,dut_pwd, cmd=CmdList)
    ###############################################################
    CmdList = []
    CmdList.append('enable')
    CmdList.append('clear configuration cache')
    CmdList.append('configure  terminal')
    send_cmd(dut_ip, dut_usr, dut_pwd, cmd=CmdList)


    ###############################################################
    #                STEP7: 设置最终结果，判断测试例是否通过
    ###############################################################
    pytest_assert(result == True, 'Test case test_ixia_demo failed')


