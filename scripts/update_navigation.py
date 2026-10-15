from pathlib import Path
from bs4 import BeautifulSoup
import copy
r=Path('clinicsoftware-site/www.lassomd.com')
# Reuse the existing page shell and typography for the two menu destinations.
base=BeautifulSoup((r/'index.html').read_text(),'html.parser')
core=['Dental: general, pediatric, orthodontics and oral surgery','Optometry / optical','Chiropractic','Physical therapy / rehabilitation','Podiatry','Dermatology: medical and cosmetic','Ophthalmology','Orthopedics: outpatient clinics','ENT','Urgent care / walk-in clinics','Pain management','Sports medicine']
more=['Mental health / counseling / psychiatry','OB-GYN','Independent primary care / family medicine','Audiology / hearing clinics','Allergy / asthma','Outpatient gastroenterology','Plastic surgery / med spa','Small-animal veterinary clinics','Fertility clinics','Sleep clinics']
for name,title,content in [
 ('specialties.html','Clinic specialties', '<h1>Websites built around <span class="text-color-purple">your specialty.</span></h1><p>Clear services, useful answers and an easy next step for patients—adapted to the way your clinic works.</p><div class="cs-specialty-columns"><section><h2>Core specialties</h2><ul>'+''.join('<li>'+x+'</li>' for x in core)+'</ul></section><section><h2>Additional practices</h2><ul>'+''.join('<li>'+x+'</li>' for x in more)+'</ul></section></div>'),
 ('after-hours-voice.html','After Hours Voice','<h1>A helpful voice <span class="text-color-purple">after hours.</span></h1><p>Give callers a clear next step when your clinic is closed or your front desk is busy.</p><div class="cs-specialty-columns"><section><h2>Answers from your clinic</h2><p>Shape the experience around your approved hours, location, services and office policies.</p><h2>Appointment next steps</h2><p>Help callers reach your booking system or leave an appointment request for your team, depending on the connection available.</p></section><section><h2>A clear handoff</h2><p>Define when callers should speak with staff and how urgent requests should be directed. The service is for front-desk support, not diagnosis or treatment advice.</p><h2>Configured with you</h2><p>We will review your phone setup, scheduling provider and preferred call flow before connecting the service.</p></section></div>')]:
 if (r/name).exists(): continue  # Preserve existing page content when refreshing navigation.
 s=copy.deepcopy(base);s.title.string=title+' | ClinicSoftware.ai'
 for meta in s.select('meta[name="description"],meta[property="og:description"]'):meta['content']=title+' for independent clinics. Explore ClinicSoftware.ai.'
 for meta in s.select('meta[property="og:title"]'):meta['content']=str(s.title.string)
 main=s.select_one('main');main.clear();main['class']=['main-wrapper']
 main.append(BeautifulSoup('<section class="cs-detail-page"><div class="padding-global"><div class="container-large">'+content+'<a class="button" href="/contact-sales.html">Request Site Mockup</a></div></div></section>','html.parser'))
 (r/name).write_text(str(s))
nav='''<div class="cs-solutions"><button class="cs-solutions-toggle nav-link-text" aria-expanded="false" aria-controls="cs-solutions-panel" type="button">Solutions <span aria-hidden="true">⌄</span></button><div class="cs-solutions-panel" id="cs-solutions-panel"><div><h2>Clinic Growth Solutions</h2><div class="cs-menu-grid"><a href="/dental-marketing/website-design.html">Website Design</a><a href="/dental-marketing/dental-seo.html">Search Engine Optimization</a><a href="/dental-marketing/dental-google-ads.html">Google Ads</a><a href="/dental-marketing/creative-branding.html">Creative Branding</a></div></div><div><h2>ClinicSoftware AI Platform</h2><div class="cs-menu-grid"><a href="/dental-marketing-software/lead-tracking.html">Virtual Frontdesk</a><a href="/dental-marketing-software/calls-management.html">Patient Conversations</a><a href="/dental-marketing-software/online-scheduling.html">Online Scheduling</a><a href="/after-hours-voice.html">After Hours Voice</a></div></div></div></div><a class="nav-link w-inline-block" href="/specialties.html"><div class="nav-link-text">Specialties</div></a>'''
count=0
for p in r.rglob('*.html'):
 if 'template-previews' in p.parts: continue
 s=BeautifulSoup(p.read_text(),'html.parser');header=s.select_one('.navbar')
 if not header:continue
 links=header.select_one('.nav_main_links')
 if not links:continue
 links.clear();links.append(BeautifulSoup(nav,'html.parser'))
 cta=header.select_one('.nav-cta-wrapper');cta.clear()
 cta.append(BeautifulSoup('<a class="nav-link w-inline-block" href="/dental-marketing-software/lead-tracking.html"><div class="nav-link-text">Virtual Frontdesk</div></a><a class="nav-link w-inline-block" href="/after-hours-voice.html"><div class="nav-link-text">After Hours Voice</div></a><a class="button is-purple-n is-n w-inline-block" href="/contact-sales.html">Request Site Mockup</a>','html.parser'))
 for link in s.select('link[href*="clinicsoftware-overrides.css"]'):link['href']=link['href'].split('?')[0]+'?v=20261015-approved2'
 for js in s.select('script[src*="clinicsoftware.js"]'):js['src']=js['src'].split('?')[0]+'?v=20261015-approved2'
 p.write_text(str(s));count+=1
print('Updated navigation on',count,'pages')
