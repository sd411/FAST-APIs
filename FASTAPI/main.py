from typing import Optional

from fastapi import Request, FastAPI
import re
import smtplib
import dns.resolver
import json
import requests
import re
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
    
    
    
def get_people(company,keywords,li_at,num_pages = 1):
    headers = {"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
           }
    
    with requests.session() as s:
                                    res = s.get("https://www.linkedin.com/feed/?trk=guest_homepage-basic_nav-header-signin") 
                                    jid = s.cookies["JSESSIONID"]
                                    s.cookies['li_at'] = li_at
                                    s.cookies["JSESSIONID"] = jid
                                    s.headers = headers
                                    s.headers["csrf-token"] = jid.strip('"')
                                    params = {
                                                "decorationId": "com.linkedin.voyager.deco.organization.web.WebFullCompanyMain-12",
                                                "q": "universalName",
                                                "universalName": company,
                                            }
                                    response = s.get("https://www.linkedin.com/voyager/api/organization/companies", params=params)
                                    response_dict2 = response.json()
    
    cmpny_urn = response_dict2["elements"][0]["entityUrn"].split(":")[-1]
    keys = "%20".join(keywords.split(" "))
    
    
    sd = set([])
    for i in range(1,num_pages+1):
        url = f'https://www.linkedin.com/search/results/people/?currentCompany=%5B%22{cmpny_urn}%22%5D&origin=FACETED_SEARCH&sid=S%3B.&title={keys}&page={i}'
        print(url)
        with requests.session() as s:
                    res = s.get("https://www.linkedin.com/feed/?trk=guest_homepage-basic_nav-header-signin") 
                    jid = s.cookies["JSESSIONID"]
                    s.cookies['li_at'] = li_at
                    s.cookies["JSESSIONID"] = jid
                    s.headers = headers
                    s.headers["csrf-token"] = jid.strip('"')
                    #default_params = {"filters":["resultType->COMPANIES"],"keywords":"internet","origin":"SWITCH_SEARCH_VERTICAL","searchId":"fbc2a217-50cd-4252-99f3-6a94650241ba"}
                    response = s.get(url, headers=headers)
    
        s = response.text
        sd1 = re.findall(r"https://www.linkedin.com/in/[a-z0-9_-]+",s)
        if(len(sd1)==0):
            break
        for item in sd1:
            sd.add(item)
    print(sd)
    print(f"Found {len(sd)} profiles from your url :")
    print("-----------------------------------------------------------------------------------------------------")
    result = []
    for item in sd:
        try:
            
            
            ul = item
            with requests.session() as s:
                                            res = s.get("https://www.linkedin.com/feed/?trk=guest_homepage-basic_nav-header-signin") 
                                            jid = s.cookies["JSESSIONID"]
                                            s.cookies['li_at'] = li_at
                                            s.cookies["JSESSIONID"] = jid
                                            s.headers = headers
                                            s.headers["csrf-token"] = jid.strip('"')
                                            url = ul.split("/")[4]
                                            res3 = s.get(f"https://www.linkedin.com/voyager/api/identity/profiles/{url}/profileView")
                                            data = res3.json()
                                    
            urnid = data["positionGroupView"]["elements"][0]["miniCompany"]["entityUrn"]

            urn = urnid.split(":")[-1]
            company_link = 'https://www.linkedin.com/voyager/api/entities/companies/' + str(urn)
            with requests.session() as s:
                            res = s.get("https://www.linkedin.com/feed/?trk=guest_homepage-basic_nav-header-signin") 
                            jid = s.cookies["JSESSIONID"]
                            s.cookies['li_at'] = li_at
                            s.cookies["JSESSIONID"] = jid
                            s.headers = headers
                            s.headers["csrf-token"] = jid.strip('"')
                            response = s.get(company_link)
                            response_dict = response.json()
            
            try:
                website_url = response_dict["websiteUrl"]
            except:
                website_url = "NA"    
            
            
            
            
            
            
            name = data["profile"]["miniProfile"]["firstName"] +" "+ data["profile"]["miniProfile"]["lastName"]
            location = data["profile"]["geoCountryName"]
            tagline = data["profile"]["headline"]
            url2 = ul
            company_url = "https://www.linkedin.com/company/" + str(urn)
            company_name = response_dict["basicCompanyInfo"]["miniCompany"]["name"]
            print(f"Name: {name}\nURL : {url2}\nLocation: {location}\nTagline : {tagline}\nLatest Company: {company_name}\nCompany_url: {company_url}\nWebsite_url: {website_url}")
            print("\n--------------------------------------------------------------------------\n")
            result.append({"Name": name,"URL" : url2,"Location": location,"Tagline" : tagline,"Recent Company": company_name,"Company URL" : company_url,"Website URL" : website_url})
        
        except:
            pass
    
    return result


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/provName/{email}")
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

@app.post("/getpeoplelist/")
async def get_p(request: Request):
    data = await request.json()
    keys = data["keys"]
    cookie = data["cookie"]
    company = data["company"]
    num = data["num_pages"]
    return get_people(company,keys,cookie,num)
    
