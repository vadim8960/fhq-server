#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import libfhqcli

admin_session = None
loggined = False
GAME_UUID1 = "00000000-0000-0000-1000-000000000001"
GAME_UUID2 = "00000000-0000-0000-1000-000000000002"
USER1_UUID = "00000000-0000-0000-0000-000000000001"
USER2_UUID = "00000000-0000-0000-0000-000000000002"
USER3_UUID = "00000000-0000-0000-0000-000000000003"
GAME1 = None
admin_email = "admin" # deprecated
admin_password = "admin" # deprecated
ADMIN_EMAIL = "admin"
ADMIN_PASSWORD = "admin"
TEST_SERVER = "ws://localhost:1234/"
TMP_DIR = "./tmp"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(msg):
    global bcolors
    print(bcolors.HEADER + "OK: " + msg + bcolors.ENDC)

def print_success(msg):
    global bcolors
    print(bcolors.OKGREEN + "OK: " + msg + bcolors.ENDC)

def print_bold(msg):
    global bcolors
    print(bcolors.BOLD + msg + bcolors.ENDC)

def log_warn(msg):
    global bcolors
    print(bcolors.WARNING + "Warning: " + msg + bcolors.ENDC)

def log_err(msg):
    global bcolors
    print(bcolors.FAIL + "ERROR: " + msg + bcolors.ENDC)

def alert(check, msg):
    if(check == True):
        log_err(msg)
        raise Exception(msg)
        sys.exit(0)

def check_response(resp, msg_success):
    if(resp['result'] == 'FAIL'):
        log_err(resp['error'])
    else:
        print_success(msg_success)

def init_enviroment():
    global admin_session
    global user1_uuid
    global user2_uuid
    global user3_uuid
    global ADMIN_EMAIL
    global ADMIN_PASSWORD
    global TEST_SERVER
    
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)

    admin_session = libfhqcli.FHQCli(TEST_SERVER)
    resp = admin_session.login({"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    alert(resp == None, 'Could not login as admin (1)')
    alert(resp['result'] == 'FAIL', 'Could not login as admin (2)')
    
    # loggined = True
    GAME1 = admin_session.game_info({"uuid": GAME_UUID1})
    alert(resp == None, 'Could not get test game (2)');
    if GAME1['result'] == 'FAIL':
        GAME1 = admin_session.game_create({
            "uuid": GAME_UUID1,
            "name": "test",
            "description": "test",
            "state": "official",
            "form": "online",
            "type": "jeopardy",
            "date_start": "2000-01-01 00:00:00",
            "date_stop": "2001-01-01 00:00:00",
            "date_restart": "2002-01-01 00:00:00",
            "organizators": "test"
        })
        alert(GAME1 == None, 'Could not send message (2)')
        alert(GAME1['result'] == 'FAIL', 'Could not create test game ' + str(resp))
        GAME1 = admin_session.game_info({"uuid": GAME_UUID1})

    GAME1 = GAME1['data']

def deinit_enviroment():
    global admin_session

    # try remove all test objects
    if loggined == True:
        admin_session.game_delete({"uuid": GAME_UUID1, "admin_password": "admin"})

    admin_session.close()