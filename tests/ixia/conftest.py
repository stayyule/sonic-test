"""
This module contains the necessary fixtures for running test cases with
Ixia devices and IxNetwork. If more fixtures are required, they should be 
included in this file.
/var/johnar/sonic-mgmt/tests/ixia/reporter
"""

import pytest
from ixnetwork_restpy import SessionAssistant
import pandas as pd
import re
import sys
import time
import os
from os.path import dirname, abspath
import site
site.addsitedir(dirname(abspath(__file__)) + '/lib')

###############
time_now=time.time()
@pytest.fixture(scope = "session",autouse=True)
def timestamp_sotre_dir(testbed):
    f=open(format(time_now)+'.txt','w')
    yield
    f.close()
    os.remove(format(time_now)+'.txt')


timestamp_list=[]
try:
    with open(format(time_now)+'.txt','r+') as f:
        for r in f.readlines():
            timestamp_list.append(float(r.strip()))
except:
    timestamp_list = []

timestamp_list.insert(0,time_now)
timestamp_now=min(timestamp_list)
timestamp_real_now = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(timestamp_now))

with open(format(time_now)+'.txt','w+') as f:
    timestamp_list = [str(i) for i in timestamp_list]
    f.write('\n'.join(timestamp_list))

##############

@pytest.fixture(scope = "module")
def ixia_api_serv_ip(testbed):
    """ 
    In an Ixia testbed, there is no PTF docker. 
    Hence, we use ptf_ip field to store Ixia API server. 
    This fixture returns the IP address of the Ixia API server.

    Args: 
       testbed (pytest fixture): The testbed fixture.

    Returns:
        Ixia API server IP
    """
    return testbed['ptf_ip']


@pytest.fixture(scope = "module")
def ixia_api_serv_user(duthost):
    """
    Return the username of Ixia API server.

    Args:
        duthost (pytest fixture): The duthost fixture.
 
    Returns:
        Ixia API server username.
    """
    #return duthost.host.options['variable_manager']._hostvars[duthost.hostname]['secret_group_vars']['ixia_api_server']['user']
    return 'admin'


@pytest.fixture(scope = "module")
def ixia_api_serv_passwd(duthost):
    """
    Return the password of Ixia API server.

    Args:
        duthost (pytest fixture): The duthost fixture.
 
    Returns:
        Ixia API server password.
    """
    #return duthost.host.options['variable_manager']._hostvars[duthost.hostname]['secret_group_vars']['ixia_api_server']['password']
    return 'admin'

@pytest.fixture(scope = "module")
def ixia_api_serv_port(duthost):
    """
    This fixture returns the TCP port for REST API of the ixia API server.

    Args:
        duthost (pytest fixture): The duthost fixture.
 
    Returns:
        Ixia API server REST port.
    """
    #return duthost.host.options['variable_manager']._hostvars[duthost.hostname]['secret_group_vars']['ixia_api_server']['rest_port']
    return '443'

@pytest.fixture(scope = "module")
def ixia_api_serv_session_id(duthost):
    """
    Ixia API server can spawn multiple session on the same REST port.
    Optional for LINUX, required for windows return the session ID.

    Args:
        duthost (pytest fixture): The duthost fixture.

    Returns:
        Ixia API server session id.
    """
    #return duthost.host.options['variable_manager']._hostvars[duthost.hostname]['secret_group_vars']['ixia_api_server']['session_id']
    return 'None'

#@pytest.fixture(scope = "module")
#def ixia_dev(duthost, fanouthosts):
#    """
#    Returns the Ixia chassis IP. This fixture can return multiple IPs if 
#    multiple Ixia chassis are present in the test topology.
#
#    Args:
#        duthost (pytest fixture): The duthost fixture. 
#        fanouthosts (pytest fixture): The fanouthosts fixture.
#
#    Returns:
#        Dictionary of Ixia Chassis IP/IPs.
#    """
#    result = dict()
#    ixia_dev_hostnames = fanouthosts.keys()
#    for hostname in ixia_dev_hostnames:
#        result[hostname] = duthost.host.options['inventory_manager'].get_host(hostname).get_vars()['ansible_host']
#    return result


@pytest.fixture(scope = "module")
def ixia_chassis(testbed, duthost):
    """
    Returns the Ixia chassis IP. This fixture can return multiple IPs if 
    multiple Ixia chassis are present in the test topology.

    Args:
        duthost (pytest fixture): The duthost fixture. 
        fanouthosts (pytest fixture): The fanouthosts fixture.s

    Returns:
        Dictionary of Ixia Chassis IP/IPs.
    """
    host_name = testbed["vm_base"]
    host_ip = duthost.host.options['inventory_manager'].get_host(host_name).get_vars()['ansible_host']
    return host_ip

@pytest.fixture(scope = "module")
def ixia_chassis_typ(testbed):
    """
    Returns the Ixia chassis IP. This fixture can return multiple IPs if 
    multiple Ixia chassis are present in the test topology.

    Args:
        duthost (pytest fixture): The duthost fixture. 
        fanouthosts (pytest fixture): The fanouthosts fixture.

    Returns:
        Dictionary of Ixia Chassis IP/IPs.
    """
    vm_base = testbed["vm_base"]
    if vm_base == '':
         chassis_typ = 'vm'
    else:
         chassis_typ = 'phy'
    chassis_typ = 'phy'
    return chassis_typ


@pytest.fixture(scope = "function")
def ixia_api_server_session(
        ixia_api_serv_ip,
        ixia_api_serv_user,
        ixia_api_serv_passwd,
        ixia_api_serv_port,
        ixia_api_serv_session_id) :
    """
    Ixia session manager fixture.

    Args:
        ixia_api_serv_ip (pytest fixture): ixia_api_serv_ip fixture
        ixia_api_serv_user (pytest fixture): ixia_api_serv_user fixture.
        ixia_api_serv_passwd (pytest fixture): ixia_api_serv_passwd fixture.
        ixia_api_serv_port (pytest fixture): ixia_api_serv_port fixture.
        ixia_api_serv_session_id (pytest fixture): ixia_api_serv_session_id 
            fixture.
  
    Returns:
        IxNetwork Session
    """

    if (ixia_api_serv_session_id.lower() != 'none') :
        session = SessionAssistant(IpAddress=ixia_api_serv_ip,
                                   UserName=ixia_api_serv_user,
                                   Password=ixia_api_serv_passwd,
                                   RestPort=ixia_api_serv_port,
                                   SessionId=ixia_api_serv_session_id)
    else :
        session = SessionAssistant(IpAddress=ixia_api_serv_ip,
                                   UserName=ixia_api_serv_user,
                                   Password=ixia_api_serv_passwd,
                                   RestPort=ixia_api_serv_port,
                                   LogLevel='all', LogFilename='restpy.log')
    ixNetwork = session.Ixnetwork
    ixNetwork.NewConfig()
    
    yield session

    #ixNetwork.NewConfig()
    #session.Session.remove()

 # move to helper file?
@pytest.fixture(scope = "function")
def get_ixia_port_list( ixia_chassis, testbed):
    #get port list from csv file
    ixia = ixia_chassis
    ixChassisIpList = [ixia]
    confvalue = testbed['conf-name']
    table = pd.read_csv(r'../ansible/files/sonic_ixia_links.csv')
    portlist = []
    table1 = table.loc[table['conf-name'] == confvalue]
    #check if 'ixia_port' column is null
    portinfolist = table1['ixia_port'].values.tolist()
    for portinfo in portinfolist:
        pattern = r'card(\d+)/port(\d+)'
        if isinstance(portinfo, str):
            m = re.match(pattern, portinfo)
            card = m.group(1) 
            port = m.group(2)
            portlist.append([ixChassisIpList[0],card,port])
    #portlist = [[ixChassisIpList[0], 1, 53], [ixChassisIpList[0], 1, 54]]
    return portlist

@pytest.fixture(scope = "function")
def ixiahost(ixia_api_server_session, get_ixia_port_list):
    session = ixia_api_server_session
    portlist = get_ixia_port_list
    yield session, portlist
    
    #clean up
    session.Ixnetwork.NewConfig()
    session.Session.remove()
'''
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.start = call.start
    report.stop = call.stop  
    call_result = report.outcome.upper()
    print(report.nodeid)    
    print(report.start)  
    print (time.strftime("%Y-%m-%d %H:%M:%S", call.start)) 
'''
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
   
    global call_result
    global teardown_result
   # global setup_result
    global report
    global time_stop
    global time_start
    global resinfo
    global report_file 
    out = yield
    report = out.get_result()
   # csv_save_path= f'/var/johnar/sonic-mgmt/tests/ixia/reporter/{time_now}.csv'
    if report.when == "call":
        call_result = report.outcome.upper()
        # print('Call_Result: ' + call_result)
        time_stop = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(call.stop))
        time_start = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(call.start))
        resinfo = call.excinfo
	report_file=timestamp_real_now+".csv"
    if report.when == "teardown":
        teardown_result = report.outcome.upper()
        print('\n' + 'Statistics of test case results:')
        print(report.nodeid)
       # print('Setup_Result: ' + setup_result)
       # print('Call_Result: ' + call_result)
       # print('Teardown_Result: ' + teardown_result)
        #print(time_now)
        # print('_'*95)
	print(time_start)
	print(time_stop)
	csv_save_path='/var/johnar/sonic-mgmt/tests/ixia/reporter/'+format(timestamp_real_now)+'.csv'
        columns=['id','starttime','finishtime','result','report_file','info']
        if os.path.lexists(csv_save_path):
	    df_new = pd.DataFrame({"id": report.nodeid, "starttime": [time_start], "finishtime":[time_stop],"result":[call_result],"report_file":[report_file],'info':[resinfo]})
            df_new.to_csv(csv_save_path,index=False, mode='a', header=False,columns=columns)
        else:
            df = pd.DataFrame({"id": report.nodeid, "starttime": [time_start], "finishtime":[time_stop],"result":[call_result],"report_file":[report_file],'info':[resinfo]})
            df.to_csv(csv_save_path,index=False,columns=columns)
            
'''
 pd.DataFrame( {"id": report.nodeid, "starttime": [time_start], "finishtime": [time_stop], "result": [call_result],"result_file": [timestamp_real_now], 'info': [resinfo]}) pd.DataFrame({"id": report.nodeid, "starttime": [time_start], "finishtime":[time_stop],"result":[call_result],"result_file":[timestamp_real_now],'info':[resinfo]})        if setup_result == 'PASSED' \
                and (call_result == 'PASSED' or call_result == 'SKIPPED') \
                and teardown_result == 'PASSED':
            print('Global test environment tear-down')
            print('[  PASSED  ]')
        else:
            print('Global test environment tear-down')
            print('[  FAILED  ]')
'''
