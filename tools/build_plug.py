import json,re,sys
SEC='우리 아이 알아보기'
CATS={'diag':('c-plug-diag','자가진단','체크리스트로 우리 아이의 평소 모습을 살펴봐요','#1947ba'),
      'symp':('c-plug-symp','증상 정보','ADHD, 틱, 언어장애, 발달장애, 자폐스펙트럼, 학습장애 알아보기','#0c8599'),
      'test':('c-plug-test','검사 프로그램','플러그에서 진행하는 검사의 종류와 구성','#7048e8'),
      'sol':('c-plug-sol','플러그 솔루션','아이에게 맞춘 플러그 개선 프로그램','#c2255c')}
SRC='출처: 플러그 홈페이지(plugkids.co.kr)'
posts=[];cat=None;post=None;sec=None
def endsec():
    global sec
    if sec is None:return
    if sec['kind'] in('defs','steps'):
        lead=[l for l in sec['lines'] if '|' not in l]; sec['lines']=[l for l in sec['lines'] if '|' in l]
        if lead: sec['lead']=' '.join(lead)
    if sec['kind']=='check':
        L=sec.pop('lines');
        sec['scale']=L[0].split(':',1)[1].strip().split('|');sec['concern']=L[1].split(':',1)[1].strip().split('|')
        assert L[0].startswith('scale') and L[1].startswith('concern')
        sec['items']=L[2:]
        for c in sec['concern']: assert c in sec['scale'],c
    post['sections'].append(sec);sec=None
text=''.join(open(f,encoding='utf-8').read()+'\n' for f in sys.argv[1:])
for raw in text.split('\n'):
    l=raw.rstrip()
    if not l.strip():continue
    if l.startswith('@cat '):cat=l[5:].strip();continue
    if l.startswith('@post '):
        endsec();pid,title=[x.strip() for x in l[6:].split('|',1)]
        post={'id':pid,'cat':CATS[cat][0],'title':title,'intro':'','sections':[]};posts.append(post);continue
    if l.startswith('>'):post['intro']=l[1:].strip();continue
    m=re.match(r'@(check|info|defs|steps|faq) (.+)',l)
    if m:
        endsec();sec={'id':'s%d'%(len(post['sections'])+1),'kind':m.group(1),'title':m.group(2).strip(),'lines':[]};continue
    assert not l.startswith('@'),l
    sec['lines'].append(l.strip())
endsec()
for p in posts: p['intro']+='\n'+SRC
import results;results.apply(posts)
cats=[{'id':v[0],'name':v[1],'group':'','section':SEC,'color':v[3],'desc':v[2]} for v in CATS.values()]
json.dump({'categories':cats,'posts':posts},open('plug_new.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
from collections import Counter
print(len(posts),Counter(p['cat'] for p in posts))
for p in posts: print(p['id'],[ (s['kind'],len(s.get('lines',s.get('items',[])))) for s in p['sections']])
