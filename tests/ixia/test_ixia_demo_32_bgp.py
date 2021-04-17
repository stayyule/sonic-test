# -*- coding:UTF-8 -*-


import logging
import time, os, sys
import pytest

from ixnetwork_restpy import Files
from common.reboot import logger
from common.ixia.ixia_helpers import *
from common.helpers.assertions import pytest_assert


"""
TO UPDATE
"""
pytestmark = [pytest.mark.disable_loganalyzer]
def test_ixia_demo_32_bgp(ixiahost,testbed, duthost):
    
    ###############################################################
    #                   STEP1: 准备预置条件
    ###############################################################
    
    #1.1 设置全局结果，默认为True, 如果中间检测点不通过，将该值更新为False
    result = True 
    
    #1.2 设置测试仪表IxNetwork配置文件名称，建议和测试例函数同名
    configFile = os.path.join(os.path.dirname(__file__), sys._getframe().f_code.co_name + '.ixncfg')
    #logger.info(configFile)
    
    #1.4 获取拓扑连接信息，获得intf, vlanid, 其中intf用于配置DUT, vlanid用于更新测试仪表配置文件
    logger_msg(u'获取拓扑连接信息。')
    intf, vlanid = get_connection_info(testbed)

    #1.5 创建Ixia session, 返回session句柄和测试环境中要使用的端口信息
    logger_msg(u'创建 Ixia Session IP。') 
    session, portList = ixiahost    
    
    
    ###############################################################
    #                   STEP2: 测试仪表相关操作
    ###############################################################
    
    #2.1: 加载仪表配置文件
    logger_msg(u'加载配置文件。')
    load_config(session, configFile)
    
    #2.2: 配置license server
    logger_msg(u'配置License server信息。')
    licenseInfo = get_ixia_license(testbed, duthost)
    config_license_server(session, licenseInfo)
    
    
    #2.3: 占用端口
    logger_msg(u'连接机框，开始抢占端口%s' % portList)
    reserve_port(session, portList)
    
    #2.4: 开启协议仿真进行测试
    logger_msg(u'测试仪开启ARP应答，主动发送ARP请求。')
    logger_msg(u'测试仪开启协议仿真，Port1和Port2使能BGP Session。')
    start_protocols(session)
    #time.sleep(30)
    
        
    ###############################################################
    #                STEP3: 检测协议状态
    ###############################################################
    #Step3: 输出协议状态信息
    protocolStatistics = get_statistics(session, stat_view_name='Protocols Summary')
    logger_msg('\n\nProtocol STATS: {}\n\n'.format(protocolStatistics))
    
    
    ###############################################################
    #                STEP4: 测试仪表进行流量验证
    ###############################################################
    #4.1: 测试仪表发送流量
    logger_msg(u'Ixia测试仪表下发流量配置，发送流量。')
    start_traffic(session)
    time.sleep(5)

    #4.2: 测试仪表停止流量
    logger_msg(u'Ixia测试仪表停止流量。')
    stop_traffic(session)
    stop_protocols(session)    

    #4.3: 获取流量统计结果，并打印收发端口，收发报文数
    logger_msg(u'Ixia测试仪表根据需求按照Flow统计方式定制统计结果。')
    flowStatistics = get_traffic_statistics(session, "Flow Statistics")
    logger_msg(type(flowStatistics))
    for rowNumber,flowStat in enumerate(flowStatistics.Rows):
        logger_msg('\n\nSTATS: {}\n\n'.format(flowStat))
        logger_msg('\nRow:{}  TxPort:{}  RxPort:{}  TxFrames:{}  RxFrames:{}\n'.format(
            rowNumber, flowStat['Tx Port'], flowStat['Rx Port'],
            flowStat['Tx Frames'], flowStat['Rx Frames']))
   
    #4.4: 加入check点2, 查看流量是否无丢包
    if  flowStat['Tx Frames'] ==  flowStat['Rx Frames']:
        result = True
        logger_msg(u'与DUT建立BGP邻居状态正确且协议启动时间正常，流量无丢包。测试成功结束。')
    else:
        result = False
        logger_msg(u'流量丢包,请检查配置。')


    ###############################################################
    #                STEP5: 设置最终结果，判断测试例是否通过
    ###############################################################
    pytest_assert(result == True, 'Test case test_ixia_demo failed')


