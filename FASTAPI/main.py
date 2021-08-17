from typing import Optional

from fastapi import FastAPI
import re
import smtplib
import dns.resolver
import json
import requests
app = FastAPI()


def findEmail(fn,ln,domain):
    
    if (domain[0:4] == 'http'):
            domain = domain.replace('//', '')
            domain = domain.replace('/', '')
            domain = domain.split(":")[1]
            domain = domain.split(".")
            domain = domain[len(domain) - 2] + '.' + domain[len(domain) - 1]
    elif (domain[0:4] == 'www.'):
            domain = domain.replace('/', '')
            domain = domain.split(".")
            domain = domain[len(domain) - 2] + '.' + domain[len(domain) - 1]
            
    fn = fn.lower()
    ln = ln.lower()
    domain = domain.lower()
    
    fi = fn[0]
    li = ln[0]
    
    emails = [
        fn + '@' + domain,
        fi + ln + '@' + domain,
        ln + '@' + domain,
        fn + ln + '@' + domain,
        fn + '.' + ln + '@' + domain,
        fi + '.' + ln + '@' + domain,
        fn + li + '@' + domain,
        fn + '.' + li + '@' + domain,
        fi + li + '@' + domain,
        fi + '.' + li + '@' + domain,
        ln + fn + '@' + domain,
        ln + '.' + fn + '@' + domain,
        ln + fi + '@' + domain,
        ln + '.' + fi + '@' + domain,
        li + fn + '@' + domain,
        li + '.' + fn + '@' + domain,
        li + fi + '@' + domain,
        li + '.' + fi + '@' + domain,
        fn + '-' + ln + '@' + domain,
        fi + '-' + ln + '@' + domain,
        fn + '-' + li + '@' + domain,
        fi + '-' + li + '@' + domain,
        ln + '-' + fn + '@' + domain,
        ln + '-' + fi + '@' + domain,
        li + '-' + fn + '@' + domain,
        li + '-' + fi + '@' + domain,
        fn + '_' + ln + '@' + domain,
        fi + '_' + ln + '@' + domain,
        fn + '_' + li + '@' + domain,
        fi + '_' + li + '@' + domain,
        ln + '_' + fn + '@' + domain,
        ln + '_' + fi + '@' + domain,
        li + '_' + fn + '@' + domain,
        li + '_' + fi + '@' + domain,
        ]
    
    email = 'unknown'
    vdt = 'knknown'
    for i,e in enumerate(emails):
        
    
        data = {
            'from_email': 'gfosho69@gmail.com',
            'hello_name': 'gfosho',
            'to_email': e
            }
    
        json_mylist = json.dumps(data, separators=(',', ':'))
        
        
        response = requests.post('https://visum-email.herokuapp.com/v0/check_email',headers = {
                'x-saasify-proxy-secret': 'lolwut'
                },data = json_mylist)
        
        response = json.loads(response.text)
        if response["smtp"]["is_catch_all"]:
            email = "catch all"
            break
        if response["mx"]["accepts_mail"] and response["smtp"]["can_connect_smtp"] and response["smtp"]["is_deliverable"]:
            email = e
            break
        
        
    return email

def check_validity(email):
        msg= 'unknown'
        data = {
            'from_email': 'gfosho69@gmail.com',
            'hello_name': 'gfosho',
            'to_email': email
            }
    
        json_mylist = json.dumps(data, separators=(',', ':'))
        
        
        response = requests.post('https://visum-email.herokuapp.com/v0/check_email',headers = {
                'x-saasify-proxy-secret': 'lolwut'
                },data = json_mylist)
        
        response = json.loads(response.text)
        if response["smtp"]["is_catch_all"]:
            msg = "catch all"

        elif response["mx"]["accepts_mail"] and response["smtp"]["can_connect_smtp"] and response["smtp"]["is_deliverable"]:
            msg = "valid"
            
        elif not(response["mx"]["accepts_mail"]) or not(response["smtp"]["can_connect_smtp"]) or not(response["smtp"]["is_deliverable"]):
            msg = "invalid"
        
        return msg

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/verify/{email}")
def check_dom(email: str):
    splitAddress = email.split('@')
    domain = str(splitAddress[1])
    print('Domain:', domain)
    
    # MX record lookup
    records = dns.resolver.resolve(domain, 'MX')
    mxRecord = records[0].exchange
    mxRecord = str(mxRecord)
    if "yahoo" in mxRecord:
        prov = "Yahoo"
    elif "google" in mxRecord or "gmail" in mxRecord:
        prov = "Google"
    elif "microsoft" in mxRecord or "outlook" in mxRecord:
        prov = "Microsoft"
    elif "icloud" in mxRecord:
        prov = "Apple"
    elif "zoho" in mxRecord:
        prov = "Zoho"
    else:
        prov = "Others"

    return {"Email Mxrecord" : prov}

@app.get("/findE/")
def get_e(fn : str,ln : str,domain : str):
    return findEmail(fn,ln,domain)

@app.get("/checkValidity/{email}")
def get_vdty(email: str):
    return check_validity(email)
