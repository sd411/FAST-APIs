from typing import Optional

from fastapi import FastAPI
import re
import smtplib
import dns.resolver
import json
app = FastAPI()


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
