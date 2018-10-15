#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys, os, re
import argparse
from bs4 import BeautifulSoup
from config import PLUS, WARNING, INFO, LESS, LINE, FORBI
from default_creds import DEFAULT
from input import INPUT
from fake_useragent import UserAgent


# disable warning https
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

#check if url is good
def check_url(url, req, stat, error_log):
    if stat == 200:
        print "\n{} url found \n".format(PLUS)
        check_input(url, req, error_log)
    else:
        print "\n{} url not found \n".format(LESS)
        sys.exit()

#search input to connexion with list in "default_creds"
def check_input(url, req, error_log):
    ids = []
    usr = ""
    passwd = ""
    soup = BeautifulSoup(req.text,"html.parser")
    for input_all in soup.find_all('input'):
        all_id = input_all.get('name')
        ids.append(all_id)
    for input_login in INPUT['login']:
        if input_login in ids:
            usr = input_login
            for input_passwd in INPUT['passwd']:
                if input_passwd in ids:
                    print "{} inputs found: \n {} : {}\n".format(PLUS, input_login, input_passwd)
                    passwd = input_passwd
                    default(url, usr, passwd, error_log)
                else:
                    pass 
        else:
             pass
    if usr == "" or passwd == "":
        print "{} login input or password input not found use args pls".format(LESS)                 


#check default username and password
def default(url, usr, passwd, error_log):
    ua = UserAgent()
    user_agent = {'User-agent': ua.random}
    print "test default creds: \n"
    for default_user in DEFAULT['username']:
        for default_pass in DEFAULT['password']:
            query = {
                     usr : str(default_user),
                     passwd : str(default_pass),
            }
            res = requests.post(url, data=query, headers=user_agent, allow_redirects=True, verify=False, timeout=5)
            sys.stdout.write("...\r")
            sys.stdout.flush()
            if error_log not in res.text:
                print "{} connexion win with {} : {}".format(PLUS, default_user, default_pass)
                sys.exit()
            else:
                pass

if __name__ == '__main__':
    #arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", help="URL to scan [required]", dest='url')
    parser.add_argument("-e", help="Message in error connexion [required]", dest='error_log')
    parser.add_argument("-c", help="If they are a captcha on website", dest='captcha', required=False)
    parser.add_argument("-p", help="Input pseudo", dest="pseudo", required=False)
    parser.add_argument("-m", help="Input password", dest="mdp", required=False)
    results = parser.parse_args()
                                     
    url = results.url
    error_log = results.error_log
    captcha = results.captcha
    pseudo = results.pseudo
    mdp = results.mdp
    
    if url == None or error_log == None:
        print '\nurl or error log missing pls check "tiexpress.py -h" \n'
        sys.exit()
    req = requests.get(url, verify=False)
    stat = req.status_code
    check_url(url, req, stat, error_log)
