import cloudscraper
import json

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})
# Let's inspect a few profiles in detail to see what fields have text
# e.g., Marcus Herrmann (CFD multiphase), Kiran Ramesh (aerodynamics/unsteady flow), Yulia Peet (turbulent flows/CFD)
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

for prof in data.get("results", []):
    name = prof.get("display_name", {}).get("raw")
    if name in ["Marcus Herrmann", "Kiran Ramesh", "Yulia Peet", "Jeonglae Kim"]:
        print("="*60)
        print("Name:", name)
        for k, v in prof.items():
            if isinstance(v, dict) and "raw" in v and v["raw"]:
                # print non-empty fields
                val_str = str(v["raw"])
                if len(val_str) > 0 and k not in ["photo_url", "eid", "deptids", "departments"]:
                    print(f"  {k}: {val_str[:150]}")
