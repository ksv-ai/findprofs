import cloudscraper
import pandas as pd
import json

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})
params = {
    "dept_ids": "1662",
    "employee_types": "Faculty,Faculty w/Admin Appointment",
    "profiles_to_exclude": "bakerd,hbryan,fegarret,fmayer,fselim,jseto3,mllind,syong4,jyaron,jbadams,allnutt,jrande,jmandino,kankit,harami1,bakerd,bbakshi,zberkson,ceboehme,hbryan,ckchan4,crozier,ldai3,jdavids,sdeng16,skdey,hemady,eforzani,cfriesen,ganeshtg,fegarret,mdgreen8,jlhollo5,qhong7,yjiao13,kjin18,lkhalife,krauses,dhl95,jli68,jylin1,atddl,telong,fmayer,linqinmu,cmuhich,bnannen,anavrots,nnewman,drnielse,bobpeck,brankin,raupp77,hlreed,krege,der9476,rroy1,icves,ierls,jlself1,fselim,sseo19,jseto3,jamishah,ashuaib,karls,msierks,knsolank,squires,jtsasu,gstepha2,ssusarl3,mllind,stongay,citorres,atseng,avarman1,mwaas,ford44,yfeng111,syang214,syong4,rdarcy1, dparviz1,dsmarsh2,ttakahas",
    "size": "100",
    "page": "1"
}
url = "https://search.asu.edu/api/v1/webdir-profiles/faculty-staff/filtered"
r = scraper.get(url, params=params)
data = r.json()

scholar_found = 0
for prof in data.get("results", []):
    name = prof.get("display_name", {}).get("raw")
    # Check all fields for scholar
    found_urls = []
    for k, v in prof.items():
        if isinstance(v, dict) and v.get("raw"):
            val_str = str(v.get("raw"))
            if "scholar.google.com" in val_str or "user=" in val_str:
                found_urls.append((k, val_str))
    if found_urls:
        print(f"{name} has scholar link in ASU API:", found_urls)
        scholar_found += 1

print(f"Total faculty with scholar link directly in ASU API: {scholar_found}")
