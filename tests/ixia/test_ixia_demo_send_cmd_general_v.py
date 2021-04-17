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
def test_ixia_demo_ecmp(ixiahost,testbed, duthost):
    

    #4.2:向leaf fanout发送interface down命令
    logger_msg(u'发送interface down命令')
    ip = '10.36.78.110'
    usr = 'admin'
    pwd = 'YourPaSsWoRd'
    cmd = 'sudo config interface shutdown Ethernet64'
    send_cmd(ip, usr, pwd, cmd)
    logger_msg(u'已经向fanout交换机发送interface down命令')



