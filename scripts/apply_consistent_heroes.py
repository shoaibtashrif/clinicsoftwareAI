"""Normalize active service heroes and assign section-specific artwork."""
from pathlib import Path
from bs4 import BeautifulSoup
from html import escape
import copy
R=Path(__file__).resolve().parents[1]/'www.lassomd.com'
P='/brand-assets/consistent/'
pages={
'index.html':('Home','/brand-assets/clinic-website-preview-original.webp','photo'),
'dental-marketing/website-design.html':('Website Design','/brand-assets/clinic-website-preview.webp','photo'),
'dental-marketing/creative-branding.html':('Creative Branding','/brand-assets/clinic-branding-generated.webp','photo'),
'dental-marketing/dental-seo.html':('Search Engine Optimization',P+'search-hero.svg','graphic'),
'dental-marketing/dental-google-ads.html':('Google Ads','/brand-assets/ads-phone-generated.webp','phone'),
'dental-marketing-software/lead-tracking.html':('Virtual Frontdesk',P+'appointment-demo.mp4','video'),
'dental-marketing-software/calls-management.html':('Patient Conversations',P+'conversation-hero.svg','graphic'),
'dental-marketing-software/online-scheduling.html':('Online Scheduling',P+'calendar-hero.svg','graphic'),
'specialties.html':('Specialties','/brand-assets/clinic-website-preview-original.webp','photo'),
'after-hours-voice.html':('After Hours Voice',P+'voice-hero.svg','device'),
}
for name,(label,media,kind) in pages.items():
 path=R/name;s=BeautifulSoup(path.read_text(),'html.parser');main=s.find('main');first=main.find(recursive=False)
 if first.get('class') and 'cs-service-hero' in first['class']:continue
 h=copy.deepcopy(first.find('h1'));h.attrs={'class':['cs-hero-title']}
 if name=='index.html':
  h=BeautifulSoup('<h1 class="cs-hero-title">Modern clinic websites that turn visits into <span class="text-color-purple">patient action.</span></h1>','html.parser').h1
  intro='Managed websites, virtual frontdesk and scheduling connections for independent healthcare practices.'
 else:
  paras=[p for p in first.find_all('p') if not p.find_parent('nav') and not p.find_parent('a')]
  intro=paras[0].get_text(' ',strip=True) if paras else 'A clearer online experience for your clinic and your patients.'
 extras=[]
 if name not in ['index.html','specialties.html','after-hours-voice.html']:
  # Keep additional introductory copy below the shared hero instead of shrinking the media.
  for e in first.select('p,ul,h2'):
   if e.find_parent('nav') or e.find_parent('a') or e.find_parent('ul'):continue
   if e.get_text(' ',strip=True)==intro:continue
   extras.append(str(e))
 cta=first.select_one('a.button');href=cta.get('href','/contact-sales.html') if cta else '/contact-sales.html'
 label_cta=(cta.select_one('.button-text') or cta).get_text(' ',strip=True) if cta else 'Request Site Mockup'
 if kind=='video':visual=f'<video class="cs-hero-media" autoplay muted loop playsinline controls preload="metadata" poster="{P}appointment-poster.webp" data-appointment-demo aria-label="Illustrative appointment booking conversation"><source src="{media}" type="video/mp4"/></video>'
 else:visual=f'<img class="cs-hero-media" src="{media}" width="1200" height="1000" alt="{escape(label)} illustration" fetchpriority="high"/>'
 breadcrumb='' if name=='index.html' else f'<nav class="cs-hero-breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true"> / </span><span>{escape(label)}</span></nav>'
 markup=f'<section class="cs-service-hero"><div class="cs-hero-grid"><div class="cs-hero-copy">{breadcrumb}{h}<p class="cs-hero-intro">{escape(intro)}</p><a class="cs-primary-button" href="{href}">{escape(label_cta)}</a></div><div class="cs-hero-frame cs-media-{kind}">{visual}</div></div></section>'
 new=BeautifulSoup(markup,'html.parser').section
 # Preserve the source video node which was already hidden behind the home artwork.
 if name=='index.html':
  original_video=first.find('video')
  if original_video:
   original_video.attrs.pop('autoplay',None);original_video['preload']='none';holder=s.new_tag('div',hidden=True);holder.append(copy.deepcopy(original_video));new.append(holder)
 first.replace_with(new)
 if extras:new.insert_after(BeautifulSoup('<section class="cs-hero-details"><div>'+''.join(extras)+'</div></section>','html.parser').section)
 # The After Hours page's text is rebuilt below with its own illustrations.
 if name=='after-hours-voice.html':
  sections=[('voice-knowledge','Answers from your clinic','Your hours, directions, services and first-visit guidance—using information you approve.'),('voice-handoff','Every call has a clear next step','Guide callers toward your scheduling options or the right person on your team.'),('voice-summary','A useful handoff when your team returns','Review appointment requests and follow-ups that need a member of staff. The exact workflow depends on your phone and scheduling setup.')]
  for n,(asset,title,body) in enumerate(sections):
   part=f'<section class="cs-visual-section {"cs-tinted" if n%2==0 else ""}"><div class="cs-visual-row {"cs-reverse" if n%2 else ""}"><div class="cs-section-frame"><img src="{P}{asset}.svg" width="1200" height="900" loading="lazy" alt="{title}"/></div><div><h2>{title}</h2><p>{body}</p></div></div></section>'
   main.append(BeautifulSoup(part,'html.parser').section)
  main.append(BeautifulSoup('<section class="cs-visual-section"><div class="cs-closing"><h2>Make your after-hours experience feel like your clinic.</h2><p>We’ll review your approved answers, phone setup and staff handoff before connecting the service. Front-desk support does not replace clinical advice.</p><a class="cs-primary-button" href="/contact-sales.html">Request Site Mockup</a></div></section>','html.parser').section)
 if not s.select_one('link[href*="service-consistency.css"]'):s.head.append(s.new_tag('link',rel='stylesheet',href='/service-consistency.css?v=20261015-1'))
 if name=='dental-marketing-software/lead-tracking.html':s.body.append(s.new_tag('script',src='/appointment-demo.js',defer=True))
 path.write_text(str(s))
# Distinct imagery per content topic; desktop/mobile copies represent the same section.
name='dental-marketing/creative-branding.html';path=R/name;s=BeautifulSoup(path.read_text(),'html.parser')
classes={'is-1':'brand-direction','is-2':'brand-logo','is-3':'brand-cards','is-4':'brand-signage','is-3rd-copy':'brand-direction','is-brand1':'brand-logo','is-brand2':'brand-cards','is-brand3':'brand-signage'}
for img in s.select('main .product-image-wrap img,main .ssp-category-img'):
 for cls,asset in classes.items():
  if cls in img.get('class',[]):
   img['src']=P+asset+'.webp';img['alt']={'brand-direction':'Clinic brand mood board and design consultation','brand-logo':'Original clinic logo sketches and embossed mark','brand-cards':'Original clinic business card designs','brand-signage':'Clinic entrance signage and printed display'}[asset];img['data-artwork']='photo';img.attrs.pop('srcset',None);break
path.write_text(str(s))
# UI illustrations match the purpose of each section rather than repeating a single dashboard.
assignments={
'dental-marketing-software/calls-management.html': [('main .product-image-wrap img',['call-review','missed-call','callback-queue']),('main .ssp-category-img',['search-hero','search-details','content-plan'])],
'dental-marketing-software/online-scheduling.html':[('main .ssp-category-img',['voice-handoff','booking-confirmation'])],
'dental-marketing-software/lead-tracking.html':[('main .product-image-wrap img',['knowledge','calendar-hero','visit-preparation']),('main .ssp-category-img',['handoff','conversation-insights','content-plan']),('main .content-creation-image',['booking-confirmation'])],
'dental-marketing/dental-seo.html':[('main .calendar-2-col-img',['search-details']),('main .calendar-3-rows-img.is-seo-s',['content-plan']),('main .calendar-3-rows-img.is-portrait',['local-content','knowledge','conversation-insights'])],
'dental-marketing/website-design.html':[('main .ssp-category-img',['design-process','content-plan'])],
}
for name,groups in assignments.items():
 path=R/name;s=BeautifulSoup(path.read_text(),'html.parser')
 for selector,assets in groups:
  for n,img in enumerate(s.select(selector)):
   img['src']=P+assets[n%len(assets)]+'.svg';img['alt']=assets[n%len(assets)].replace('-',' ')+' illustration';img['data-artwork']='graphic';img.attrs.pop('srcset',None)
 path.write_text(str(s))
# Remove obsolete multi-layer phone artwork while retaining each existing section frame.
path=R/'dental-marketing-software/lead-tracking.html';s=BeautifulSoup(path.read_text(),'html.parser')
for wrapper,asset in zip(s.select('main .product-image-wrap'),['knowledge','calendar-hero','knowledge','calendar-hero']):
 wrapper.clear();img=s.new_tag('img',src=P+asset+'.svg',alt=asset.replace('-',' ')+' illustration',loading='lazy');img['class']=['cs-section-art'];img['data-artwork']='graphic';wrapper.append(img)
path.write_text(str(s))
