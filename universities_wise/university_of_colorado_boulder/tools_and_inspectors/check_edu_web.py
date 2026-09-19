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

active_profs = []
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
    asurite = prof.get('asurite_id', {}).get('raw')
    edu_raw = prof.get('education', {}).get('raw')
    r_web = prof.get('research_website', {}).get('raw')
    web = prof.get('website', {}).get('raw')
    
    # parse education
    clean_edu = ''
    if edu_raw:
        soup_edu = BeautifulSoup(edu_raw, 'html.parser')
        lis = [li.get_text(separator=' ').strip() for li in soup_edu.find_all('li')]
        if lis:
            clean_edu = ' | '.join(lis)
        else:
            clean_edu = ' '.join(soup_edu.get_text(separator=' ').split())
            
    active_profs.append({
        'name': name,
        'asurite': asurite,
        'edu': clean_edu,
        'website': r_web or web or ''
    })

print(f"Total active professors: {len(active_profs)}")
print(f"With education: {sum(1 for p in active_profs if p['edu'])}")
print(f"With website: {sum(1 for p in active_profs if p['website'])}")
for p in active_profs[:5]:
    print(p)
