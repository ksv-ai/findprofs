import cloudscraper
from bs4 import BeautifulSoup
import time

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

offices = {}
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
    if asurite:
        try:
            p_res = scraper.get(f'https://search.asu.edu/profile/{asurite}', timeout=8)
            soup = BeautifulSoup(p_res.text, 'html.parser')
            addr = soup.find('address', class_='person-address')
            street = addr.find('span', class_='person-street').get_text(strip=True) if addr and addr.find('span', class_='person-street') else ''
            city = addr.find('span', class_='person-city').get_text(strip=True) if addr and addr.find('span', class_='person-city') else ''
            campus_el = soup.find('div', class_='campus')
            campus = campus_el.get_text(strip=True).replace('Campus:', '').strip() if campus_el else ''
            
            loc = street
            if loc and city:
                loc = f"{street} ({city})"
            elif not loc and campus:
                loc = f"Campus: {campus}"
                
            if loc:
                offices[name] = loc
        except Exception as e:
            pass
        time.sleep(0.05)

print(f"Total active: 48, Found location for: {len(offices)}")
for n, loc in list(offices.items())[:10]:
    print(f"  {n}: {loc}")
