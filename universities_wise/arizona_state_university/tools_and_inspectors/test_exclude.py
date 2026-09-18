import cloudscraper
import urllib.parse
import json

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})

# Test sending profiles_to_exclude
params = {
    "dept_ids": "1662",
    "employee_types": "Faculty,Faculty w/Admin Appointment",
    "profiles_to_exclude": "bakerd,hbryan,fegarret,fmayer,fselim,jseto3,mllind,syong4,jyaron,jbadams,allnutt,jrande,jmandino,kankit,harami1,bakerd,bbakshi,zberkson,ceboehme,hbryan,ckchan4,crozier,ldai3,jdavids,sdeng16,skdey,hemady,eforzani,cfriesen,ganeshtg,fegarret,mdgreen8,jlhollo5,qhong7,yjiao13,kjin18,lkhalife,krauses,dhl95,jli68,jylin1,atddl,telong,fmayer,linqinmu,cmuhich,bnannen,anavrots,nnewman,drnielse,bobpeck,brankin,raupp77,hlreed,krege,der9476,rroy1,icves,ierls,jlself1,fselim,sseo19,jseto3,jamishah,ashuaib,karls,msierks,knsolank,squires,jtsasu,gstepha2,ssusarl3,mllind,stongay,citorres,atseng,avarman1,mwaas,ford44,yfeng111,syang214,syong4,rdarcy1, dparviz1,dsmarsh2,ttakahas",
    "size": "100",
    "page": "1"
}
url = "https://search.asu.edu/api/v1/webdir-profiles/faculty-staff/filtered?" + urllib.parse.urlencode(params)
r = scraper.get(url)
print("Status:", r.status_code)
data = r.json()
print("Total results after exclude:", data.get("meta", {}).get("page", {}).get("total_results"))
print("Total returned in page 1:", len(data.get("results", [])))
for prof in data.get("results", [])[:5]:
    print("-", prof.get("display_name", {}).get("raw"), "|", prof.get("primary_title", {}).get("raw"))
