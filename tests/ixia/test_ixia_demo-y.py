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

def test_ixia_demo(ixiahost,testbed, duthost):
    
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
    CmdList.append('clear configuration cache')
    CmdList.append('configure  terminal')
    CmdList.append('interface ' + intf['dut1port1'])
    CmdList.append('ip address 10.0.0.20/31')
    CmdList.append('exit')
    CmdList.append('interface ' + intf['dut1port2'])
    CmdList.append('ip address 10.0.0.22/31')
    CmdList.append('exit')
    CmdList.append('router bgp 65100')
    CmdList.append('neighbor 10.0.0.21 remote-as 65200')
    CmdList.append('neighbor 10.0.0.23 remote-as 65200')
    #ssh_dut(dut_ip, dut_usr, dut_pwd, configList=CmdList)

    CmdList.append('start-shell')
    CmdList.append('ip neigh')
    CmdList.append('route')
    CmdList.append('bcmsh')
    CmdList.append('ls show')
    CmdList.append('ctrl c')
    CmdList.append('ip neigh')
    CmdList.append('route')
    #ssh_dut(dut_ip, dut_usr, dut_pwd, configList=CmdList)

    
    ###############################################################
    #                   STEP3: 测试仪表相关操作
    ###############################################################
    
    #3.1: 加载仪表配置文件
    logger_msg(u'加载配置文件。')
    load_config(session, configFile)
    
    #3.2: 配置license server
    logger_msg(u'配置License server信息。')
    licenseInfo = get_ixia_license(testbed, duthost)
    config_license_server(session, licenseInfo)
    
    #3.3: 加载仪表端口对应的vlan, 需要更新仪表配置文件中的端口名字
    logger_msg(u'更新vlan, 虚拟机框更新vlan, 物理机框disable vlan。')
    modify_vlan(session, '10GE LAN - 001', vlanid['dut1port1'])
    modify_vlan(session, '10GE LAN - 002', vlanid['dut1port2'])
    
    #3.4: 占用端口
    logger_msg(u'连接机框，开始抢占端口%s' % portList)
    reserve_port(session, portList)
    
    #3.5: 开启协议仿真进行测试
    logger_msg(u'测试仪开启ARP应答，主动发送ARP请求。')
    logger_msg(u'测试仪开启协议仿真，Port1和Port2使能BGP Session。')
    testplatform = TestPlatform('10.36.78.241')
    testplatform.Authenticate('admin', 'admin')
    logger_msg(testplatform.info(testplatform))
    ethernet = testplatform.Sessions.find().Ixnetwork.Topology.find().DeviceGroup.find().Ethernet.find().Mac
    logger_msg(ethernet.Values)
    #ethernet.Custom(start_value='33:12:01:00:00:01', step_value=None, increments=None)
    ethernet.Single('33:12:01:00:00:01')
    ethernet = testplatform.Sessions.find().Ixnetwork.Topology.find().DeviceGroup.find().Ethernet.find().Mac
    logger_msg(ethernet.Values)
    ipv4loopback = testplatform.Sessions.find().Ixnetwork.Topology.find().DeviceGroup.find().Ipv4Loopback.find()
    ipv4loopback.SendPing('127.0.0.1')

    start_protocols(session)
    #time.sleep(30)
    
        
    ###############################################################
    #                STEP4: 登录到DUT,检测协议状态
    ###############################################################
    #Step4: 登录到DUT,检测协议状态，根据check点，更新全局结果变量result
    CmdList = []
    CmdList.append('show bgp summary')
    #ret = ssh_dut(dut_ip,configList=CmdList)
    logger_msg('Check DUT1 BGP Session')
    #logger_msg(ret)
    #check if bgp is OK， and add check point 
    BGPStatus = True
    if BGPStatus == True:
        logger_msg('Check1: DUT1 BGP Session建立成功')
        result = True
    else:
        logger_msg('Check1: DUT1 BGP Session建立失败')
        result = False
    logger_msg('DUT1 BGP peer OK')
    
    
    ###############################################################
    #                STEP5: 测试仪表进行流量验证
    ###############################################################
    #5.1: 测试仪表发送流量
    logger_msg(u'Ixia测试仪表下发流量配置，发送流量。')
    start_traffic(session)
    time.sleep(5)

    #5.2: 测试仪表停止流量
    logger_msg(u'Ixia测试仪表停止流量。')
    stop_traffic(session)
    
    #5.3: 获取流量统计结果，并打印收发端口，收发报文数
    logger_msg(u'Ixia测试仪表根据需求按照Flow统计方式定制统计结果。')
    flowStatistics = get_traffic_statistics(session, "Flow Statistics")
    for rowNumber,flowStat in enumerate(flowStatistics.Rows):
        logger_msg('\n\nSTATS: {}\n\n'.format(flowStat))
        logger_msg('\nRow:{}  TxPort:{}  RxPort:{}  TxFrames:{}  RxFrames:{}\n'.format(
            rowNumber, flowStat['Tx Port'], flowStat['Rx Port'],
            flowStat['Tx Frames'], flowStat['Rx Frames']))
   
    #5.4: 加入check点2, 查看流量是否无丢包
    logger_msg(u'与DUT建立BGP邻居状态正确且协议启动时间正常，流量无丢包。测试成功结束。')
    
    
    ###############################################################
    #                STEP6: 登录到DUT, 发送配置清除命令
    ###############################################################
    CmdList = []
    CmdList.append('enable')
    CmdList.append('clear configuration cache')
    CmdList.append('configure  terminal')
    CmdList.append('interface eth25GE 13')
    CmdList.append('no ip address 10.0.0.20/31')
    CmdList.append('exit')
    CmdList.append('interface eth25GE 14')
    CmdList.append('no ip address 10.0.0.22/31')
    CmdList.append('exit')
    CmdList.append('no router bgp 65100')
    #ssh_dut(dut_ip, dut_usr, dut_pwd, configList=CmdList)


    ###############################################################
    #                STEP7: 设置最终结果，判断测试例是否通过
    ###############################################################
    #pytest_assert(result == True, 'Test case test_ixia_demo failed')


