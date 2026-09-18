import cloudscraper
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
print("Faculty in Aerospace and Mechanical Engineering (Total:", len(data.get("results", [])), "):")
for prof in data.get("results", []):
    name = prof.get("display_name", {}).get("raw")
    title_raw = prof.get("primary_title", {}).get("raw") or prof.get("titles", {}).get("raw") or []
    title = title_raw[0] if title_raw else "Professor"
    email = prof.get("email_address", {}).get("raw") or ""
    asurite = prof.get("asurite_id", {}).get("raw") or ""
    interests = prof.get("research_interests", {}).get("raw") or ""
    expertise = prof.get("expertise_areas", {}).get("raw") or []
    short_bio = prof.get("short_bio", {}).get("raw") or prof.get("bio", {}).get("raw") or ""
    print(f"- {name} | {title} | {asurite} | {email}")
