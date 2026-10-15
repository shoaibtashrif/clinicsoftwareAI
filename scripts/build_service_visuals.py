"""Build original, lightweight UI illustrations for distinct service sections."""
from pathlib import Path
from html import escape
A=Path(__file__).resolve().parents[1]/'www.lassomd.com/brand-assets/consistent'
A.mkdir(exist_ok=True)
INK='#362650';PURPLE='#7958b6';SOFT='#f0e9f8';ROSE='#d9859f'
def rect(x,y,w,h,fill='white',r=22,stroke='none'):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>'
def text(x,y,value,size=24,fill=INK,weight=400):return f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}">{escape(str(value))}</text>'
def line(x,y,w):return f'<path d="M{x} {y}h{w}" stroke="#e5dced" stroke-width="2"/>'
def badge(x,y,label):return rect(x,y,150,42,SOFT,21)+text(x+18,y+28,label,17,PURPLE,700)
def save(name,body):
 (A/(name+'.svg')).write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="900" viewBox="0 0 1200 900">'+rect(0,0,1200,900,'#f5f0f7',0)+'<circle cx="1100" cy="100" r="260" fill="#e9dff4"/>'+body+'</svg>')
def shell(title,subtitle):return rect(80,100,1040,700,'white',30)+rect(80,100,1040,80,PURPLE,30)+text(120,150,'clinicsoftware.ai',25,'white',700)+text(120,235,title,34,INK,700)+text(120,274,subtitle,21,'#887796')
def rows(name,title,subtitle,items):
 b=shell(title,subtitle)
 for n,(head,desc,state) in enumerate(items):
  y=320+n*130;b+=rect(120,y,960,108,'#faf8fc',18)+rect(142,y+20,62,62,SOFT,18)+text(163,y+62,str(n+1),28,PURPLE,700)+text(229,y+42,head,25,INK,700)+text(229,y+77,desc,20,'#887796')+badge(892,y+30,state)
 save(name,b)
rows('knowledge','Answers grounded in your clinic','A clear source of information for the virtual frontdesk.', [('Office information','Hours, location and parking information','Approved'),('Services and first visits','Your services and preparation instructions','Reviewed'),('When to contact staff','Clear boundaries and contact options','Connected')])
rows('call-review','A useful summary after each call','Illustrative call handoff for the clinic team.', [('Reason for calling','New patient asking about a first visit','New visit'),('Next step discussed','Appointment link shared with the caller','Link sent'),('Follow-up for the team','Patient requested a callback tomorrow','Follow up')])
rows('callback-queue','Keep follow-ups in view','A simple example of the next steps after a conversation.', [('Appointment enquiry','Return a call about available visit times','Today'),('Office question','Share directions and parking information','Resolved'),('Scheduling request','Check the clinic calendar with the team','Pending')])
rows('voice-knowledge','A helpful voice, with your answers','Office-approved information, even after closing time.', [('Hours and directions','“What time do you open tomorrow?”','Answer'),('Visit preparation','“What should I bring to my first visit?”','Guide'),('Scheduling options','“How can I request an appointment?”','Connect')])
rows('voice-summary','A clear morning handoff','An illustrative summary for your front-desk team.', [('Call received · 7:42 PM','Caller asked about arranging a first visit','After hours'),('Next step shared','Your appointment-request link was offered','Guided'),('Staff follow-up','Review any requests that need your help','For review')])
rows('content-plan','Clear content for every visit','A page plan built around the questions patients ask.', [('Services','Explain care options in plain language','Discover'),('Your team','Introduce the people behind the practice','Meet'),('Plan your visit','Give patients one clear next step','Book')])
# A distinct call interface for the after-hours hero.
b=rect(115,65,400,770,'#51416c',48)+rect(127,77,376,746,'#fbf9fd',39)+rect(245,77,140,22,'#51416c',11)
b+=text(195,160,'Willow Clinic',31,INK,700)+text(210,200,'After Hours Voice',20,'#8c77a1')+rect(250,245,130,130,SOFT,65)+text(289,332,'☾',70,PURPLE)
b+=text(231,427,'Call connected',24,INK,700)+text(285,468,'00:42',22,'#8c77a1')
for n,h in enumerate([25,50,85,40,110,65,95,45,75,25]):b+=rect(194+n*25,555-h/2,10,h,PURPLE,5)
b+=rect(267,690,96,70,ROSE,35)+text(293,736,'⌁',38,'white')+rect(570,225,510,290,'white',28)+badge(605,259,'Office closed')+text(605,345,'A helpful next step.',31,INK,700)+text(605,393,'Answers from your clinic.',23)+text(605,435,'A handoff for your team.',23)+text(590,600,'Even when the lights are off.',25,PURPLE,700)+text(590,643,'Illustrative call experience',20,'#8c77a1')
save('voice-hero',b)
# Three-step horizontal journey.
for name,title,steps in [('voice-handoff','A smooth handoff from call to clinic',[('01','Someone calls','After your office closes'),('02','Your assistant helps','Answers and next steps'),('03','Your team follows up','Requests are reviewed')]),('handoff','Keep the right people involved',[('01','Patient asks','A question needs staff'),('02','Assistant explains','A clear contact option'),('03','Clinic takes over','Your team stays in control')]),('design-process','From your clinic to your new website',[('01','Discover','Your brand and services'),('02','Preview','Review your mockup'),('03','Refine','Make the details yours')])]:
 b=text(100,170,title,38,INK,700)
 for n,(num,head,desc) in enumerate(steps):
  x=80+n*365;b+=rect(x,280,310,340,'white',28)+rect(x+30,315,75,75,SOFT,24)+text(x+45,366,num,31,PURPLE,700)+text(x+30,450,head,26,INK,700)+text(x+30,495,desc,19,'#887796')
  if n<2:b+=text(x+323,460,'→',35,PURPLE)
 b+=text(100,725,'Built around your approved process.',25,'#887796');save(name,b)
# Calendar and appointment selection, not an invented records dashboard.
b=shell('Find a time that works','Connect visitors to your clinic’s scheduling options.')+text(130,345,'THURSDAY',20,PURPLE,700)
for row in range(4):
 for col in range(7):
  x=125+col*79;y=380+row*79;day=row*7+col+1;selected=day==18
  b+=rect(x,y,65,65,PURPLE if selected else '#f5f0f8',14)+text(x+20,y+42,day,23,'white' if selected else INK,700)
b+=rect(735,325,340,350,'#faf8fc',24)+text(766,375,'Available times',26,INK,700)
for n,t in enumerate(['10:00 AM','1:00 PM','3:30 PM']):b+=rect(767,410+n*75,270,58,PURPLE if n==2 else 'white',14)+text(825,448+n*75,t,23,'white' if n==2 else INK,700)
b+=text(130,750,'Illustrative availability · Your connected calendar is the source of truth',19,'#887796');save('calendar-hero',b)
# Booking confirmation is its own concept.
b=rect(230,110,740,680,'white',34)+rect(530,160,140,140,SOFT,70)+text(568,258,'✓',76,PURPLE)+text(348,365,'Your visit is confirmed',37,INK,700)+line(300,410,600)
for n,(k,v) in enumerate([('WHEN','Thursday · 3:30 PM'),('VISIT','New patient appointment'),('NEXT','Check your clinic’s instructions')]):b+=text(300,465+n*90,k,17,PURPLE,700)+text(300,500+n*90,v,26)
save('booking-confirmation',b)
# Search preview combines map and results in a different composition.
b=shell('Make your clinic easier to find','A consistent local presence with clear patient information.')+rect(120,310,500,410,'#f0eaf5',22)
for x in [210,340,470]:b+=f'<path d="M{x} 315v400" stroke="white" stroke-width="22"/>'
for y in [400,540,650]:b+=f'<path d="M125 {y}h490" stroke="white" stroke-width="20"/>'
b+='<path d="M365 450c-60 0-85 75-40 115l40 45 40-45c45-40 20-115-40-115Z" fill="#7958b6"/><circle cx="365" cy="510" r="22" fill="white"/>'
for n,(a,btext) in enumerate([('Willow Clinic','Services · Hours · Directions'),('Care close to home','Information for your first visit'),('Plan your visit','Find the right appointment link')]):
 y=325+n*132;b+=rect(655,y,420,108,'#faf8fc',15)+text(680,y+43,a,24,INK,700)+text(680,y+78,btext,18,'#887796')
save('search-hero',b)
rows('search-details','Keep your clinic details consistent','Useful information across your website and listings.',[('Clinic details','Name, location and contact details','Consistent'),('Services','Clear pages for the care you provide','Relevant'),('Patient questions','Helpful answers before a first visit','Useful')])
# Message visual distinct from the booking demo.
b=shell('A missed call can still get a reply','Illustrative follow-up conversation.')+rect(155,325,630,95,SOFT,20)+text(185,365,'Sorry we missed your call.',26)+text(185,402,'How can our front desk help?',25)+rect(430,455,610,95,PURPLE,20)+text(460,511,'I’m checking your opening hours.',25,'white')+rect(155,585,720,105,SOFT,20)+text(185,627,'We’re open from 9 AM tomorrow.',25)+text(185,665,'You can also view our hours online.',24)
save('missed-call',b)
# A compact review overview with useful topics rather than fabricated ROI claims.
b=shell('Learn from common questions','Illustrative conversation themes for your next content update.')
for n,(label,value) in enumerate([('First visits',.82),('Opening hours',.62),('Appointment options',.73),('Directions',.40)]):
 y=345+n*90;b+=text(130,y,label,24,INK,700)+rect(470,y-24,540,28,'#f0eaf5',14)+rect(470,y-24,int(540*value),28,PURPLE if n%2==0 else ROSE,14)
b+=text(130,755,'Sample themes only · No patient records shown',20,'#887796');save('conversation-insights',b)

rows('conversation-hero','Keep patient conversations connected','Helpful context for your front-desk team.', [('Enquiries','See what patients need help with','Review'),('Conversations','Keep the next step easy to understand','Respond'),('Follow-ups','Bring requests back to the right team','Connect')])
rows('visit-preparation','Help patients prepare for a visit','Simple guidance using your approved practice information.', [('Before a visit','Share what to bring and where to arrive','Prepare'),('During a visit','Explain what patients can expect','Understand'),('Questions for staff','Connect patients with your clinic','Ask')])
rows('local-content','Answer the questions people search for','Helpful pages about your practice and your community.', [('Care near home','Explain the services your clinic provides','Services'),('Getting here','Share directions and parking details','Location'),('Taking the next step','Make contact and booking options clear','Contact')])
