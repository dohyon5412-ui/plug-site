# 연구 자료 기반 비교 데이터 (자가진단 체크리스트)
IA_N,HI_N=0.94,0.77
IA_A=round((35*1.69+36*1.62)/71,2); HI_A=round((35*1.38+36*1.48)/71,2)
KJCP='한국심리학회지: 임상 31(1) 「ADHD 아동의 주의력 결함 판별을 위한 웹-기반 신경심리 연구」 – K-ARS 부모 평정, 일반 아동 82명·ADHD 아동 71명|https://accesson.kr/kjcp/assets/pdf/16760/journal-31-1-203.pdf'
VAN='Anderson 외(2022) 미국 5~12세 1,570명 Vanderbilt ADHD 부모 척도 전국 규준 – 일반 아동 문항 평균 부주의 0.90·과잉행동 0.83(국내 자료와 비슷한 수준)|https://pmc.ncbi.nlm.nih.gov/articles/PMC9172842/'
PRS=[3.11,3.20,3.21,3.11,3.05,2.97,3.14,3.20,3.09,3.28,3.41,3.33,3.13,3.27,3.28,3.22,3.27,3.21,3.11,3.29,3.33,3.29,3.33,3.43]
v=lambda a,b:round(sum(PRS[a:b])/(b-a),2)
COMPARE={
'chk-adhd':dict(mode='item',score=[3,2,1,0],min=0,max=3,ends=['전혀 없었다(0)','매일 그랬다(3)'],
  intro='이 18문항은 ADHD 진단 기준 문항과 같아서, 같은 문항을 쓰는 한국판 ADHD 평가척도(K-ARS) 연구의 부모 평정 평균과 비교했어요. 점수는 전혀 없었다 0 · 가끔 1 · 종종 2 · 매일 3으로 바꿔 계산했어요.',
  groups=[dict(name='일반 아동 평균',short='일반',values=[IA_N]*9+[HI_N]*9),dict(name='ADHD 아동 평균',short='ADHD',values=[IA_A]*9+[HI_A]*9)],
  summary=[dict(name='부주의 (1~9번)',from_=0,to=8,values=[IA_N,IA_A]),dict(name='과잉행동·충동성 (10~18번)',from_=9,to=17,values=[HI_N,HI_A])],
  note='연구에는 영역별 평균만 나와 있어서, 문항별 보기에서도 같은 영역의 평균을 표시했어요. 연구 대상은 초등학생(평균 9~11세)이에요.',
  refs=[KJCP,VAN]),
'chk-learning':dict(mode='item',score=[1,2,3,4,5],min=1,max=5,ends=['전혀 아니다(1)','매우 그렇다(5)'],
  intro='이 24문항은 마이클버스트(Myklebust)의 학습장애 선별 척도(PRS)와 문항이 같아요. 일반 아동 1,264명의 문항별 평균, 그리고 이 척도에서 학습장애를 의심하는 기준(언어성 20점·비언어성 40점·전체 65점 미만)과 비교했어요.',
  groups=[dict(name='일반 아동 평균',short='일반',values=PRS)],cutName='학습장애 의심 기준',
  summary=[dict(name='언어성 (1~9번: 듣고 이해하기·말하기)',from_=0,to=8,values=[v(0,9)],cut=round(20/9,2)),
           dict(name='비언어성 (10~24번: 시간·공간·운동·사회성)',from_=9,to=23,values=[v(9,24)],cut=round(40/15,2)),
           dict(name='전체 (1~24번)',from_=0,to=23,values=[v(0,24)],cut=round(65/24,2))],
  note='원래 척도는 또래와 비교해 1(매우 낮음)~5(매우 높음)로 평정하고, 여기서는 전혀 아니다 1 ~ 매우 그렇다 5로 바꿔 비교했어요. 기준선(빨간 점선)보다 왼쪽이면 학습의 어려움을 더 살펴볼 필요가 있다는 뜻이에요.',
  refs=['Obringer(1997) 「The Pupil Rating Scale Revised」 – Myklebust 일반 아동 1,264명 문항별 평균·선별 기준|https://files.eric.ed.gov/fulltext/ED416225.pdf']),
'chk-autism':dict(mode='total',
  intro='이 체크리스트의 많은 문항은 클랜시 행동 척도(Clancy Behavior Scale)와 비슷해요. 연구에서 진단받은 아이들이 이 척도에서 받은 점수를 최고점 대비 비율로 바꿔, ‘그렇다’에 답한 문항 비율과 나란히 놓았어요.',
  groups=[dict(name='자폐스펙트럼 아동',value=round(14.35/28*100,1)),dict(name='발달지연 아동',value=round(9.26/28*100,1))],
  cutNote='이 연구에서는 최고점의 약 43%(28점 중 12점) 이상일 때 자폐스펙트럼 가능성을 더 살펴보도록 제안했어요.',
  note='비교 대상인 발달지연 아동도 발달에 어려움이 있는 아이들이라 일반 아동보다 점수가 높아요. 연구 대상은 18~29개월 영유아이고, 원래 척도는 ‘전혀/가끔/자주’ 3단계라서 이 체크리스트와 정확히 같지는 않아요.',
  refs=['Chu 외(2024) 「Comparison between the Clancy Behavior Scale and the M-CHAT in Taiwan」 – 자폐스펙트럼 117명·발달지연 98명|https://pmc.ncbi.nlm.nih.gov/articles/PMC11119399/']),
'chk-development':dict(mode='age',
  intro='CDC(미국 질병통제예방센터)의 발달 이정표에서 같은 행동을 찾아, 또래 아이들의 75% 이상이 할 수 있게 되는 시기를 문항 옆에 표시했어요.',
  ages=['30개월 무렵','', '', '24개월 무렵','', '30개월 무렵','', '24개월 무렵','', '24개월 무렵','', '', '30개월 무렵','24개월 무렵','', '', '18개월 무렵','', '', '', '18개월 무렵','', '30개월 무렵',''],
  note='이정표에 같은 행동이 없는 문항은 표시하지 않았어요. 표시된 시기보다 아이가 많이 지났는데 아직 어렵다면(빨간 글씨) 발달 검사를 받아 보는 것이 좋아요.',
  refs=['CDC 「Learn the Signs. Act Early.」 18개월·2세·30개월 발달 이정표|https://www.cdc.gov/act-early/milestones/index.html'])
}
NOTE_NONE={'chk-tic':'틱 체크리스트는 문항이 같은 연구 자료를 찾지 못해 비교표 없이 결과 안내만 보여드려요.','chk-language':'언어 체크리스트는 문항이 같은 연구 자료를 찾지 못해 비교표 없이 결과 안내만 보여드려요.'}
def apply(posts):
    for p in posts:
        if p['id'] in NOTE_NONE: p['sections'][0]['compare']=dict(mode='none',note=NOTE_NONE[p['id']])
        if p['id'] in COMPARE:
            c=dict(COMPARE[p['id']])
            if 'summary' in c: c['summary']=[{('from' if k=='from_' else k):x for k,x in r.items()} for r in c['summary']]
            c['refs']=[r.replace('|',' | ') for r in c['refs']]
            p['sections'][0]['compare']=c
