import cloudscraper
from bs4 import BeautifulSoup
import re

scraper = cloudscraper.create_scraper()
params = {
    'dept_ids': '1662',
    'employee_types': 'Faculty,Faculty w/Admin Appointment',
    'profiles_to_exclude': 'bakerd,hbryan,fegarret,fmayer,fselim,jseto3,mllind,syong4,jyaron,jbadams,allnutt,jrande,jmandino,kankit,harami1,bakerd,bbakshi,zberkson,ceboehme,hbryan,ckchan4,crozier,ldai3,jdavids,sdeng16,skdey,hemady,eforzani,cfriesen,ganeshtg,fegarret,mdgreen8,jlhollo5,qhong7,yjiao13,kjin18,lkhalife,krauses,dhl95,jli68,jylin1,atddl,telong,fmayer,linqinmu,cmuhich,bnannen,anavrots,nnewman,drnielse,bobpeck,brankin,raupp77,hlreed,krege,der9476,rroy1,icves,ierls,jlself1,fselim,sseo19,jseto3,jamishah,ashuaib,karls,msierks,knsolank,squires,jtsasu,gstepha2,ssusarl3,mllind,stongay,citorres,atseng,avarman1,mwaas,ford44,yfeng111,syang214,syong4,rdarcy1, dparviz1,dsmarsh2,ttakahas',
    'size': '100',
    'page': '1'
}
r = scraper.get('https://search.asu.edu/api/v1/webdir-profiles/faculty-staff/filtered', params=params)
data = r.json().get('results', [])

EXCLUDED = ['emeritus', 'retired', 'adjunct', 'visiting', 'lecturer', 'staff', 'postdoc', 'courtesy', 'administrative', 'coordinator', 'advisor', 'manager', 'instructor']

KNOWN_LABS = {
    "Hamidreza Marvi": "Bio-Inspired Robotics, Technology, and Healthcare Laboratory (BIRTH Lab)",
    "Wanxin Jin": "Intelligent Robotics and Interactive Systems Lab (IRIS Lab)",
    "Kunal Garg": "Safe and Autonomous Robotics (STAR) Lab",
    "Jiefeng Sun": "Sun Robotics Lab",
    "Liping Wang": "Nanoscale Thermal Radiation Lab",
    "Jay Oswald": "Computational Mechanics Lab",
    "Leixin Ma": "Optimization, Autonomy, and Soft Intelligence Systems (OASIS) Lab",
    "Leila Ladani": "Manufacturing and Advanced Materials Characterization (MAGIC) Lab",
    "Spring Berman": "Autonomous Collective Systems (ACS) Laboratory",
    "Matthew Peet": "Cybernetic Systems and Controls Laboratory (CSCL)",
    "Konrad Rykaczewski": "Nano-Bio-Thermal Engineering Laboratory",
    "Aditi Chattopadhyay": "Adaptive Intelligent Materials & Systems (AIMS) Center",
    "Mohamed Houssem Kasbaoui": "Multiphase Flow and Fluid-Structure Interaction Group",
    "Ronald Calhoun": "Wind Energy and Atmospheric Boundary Layer Lab",
    "Yongming Liu": "Prognostics and Health Management (PHM) Lab",
    "Beomjin Kwon": "3D Energy Lab",
    "Jagannathan Rajagopalan": "Nanomechanics Laboratory",
    "Cindy (Xiangjia) Li": "Advanced Manufacturing and Bio-inspired Design Lab",
    "Houlong Zhuang": "Computational Materials Science and Design Lab",
}

for prof in data:
    all_strs = []
    for k in ['primary_title', 'working_title', 'titles', 'home_rank_description', 'subaffiliations', 'affiliations', 'departments', 'primary_department']:
        v = prof.get(k, {}).get('raw')
        if isinstance(v, list):
            all_strs.extend([str(x) for x in v if x])
        elif isinstance(v, str) and v:
            all_strs.append(v)
    combined = ' '.join(all_strs).lower()
    if any(exc in combined for exc in EXCLUDED):
        continue

    name = prof.get('display_name', {}).get('raw')
    rg = prof.get('research_group', {}).get('raw') or ''
    lab = KNOWN_LABS.get(name, "")
    if not lab and rg:
        soup_rg = BeautifulSoup(rg, "html.parser")
        lab = " ".join(soup_rg.get_text(separator=" ").split())
        if len(lab) > 100:
            lab = lab[:97] + "..."
    print(f"{name:30}: {lab}")
