import re, json, sys, collections
pdf_txt, hwpx_txt, OUT = sys.argv[1:4]
CH = int(sys.argv[4]) if len(sys.argv) > 4 else 1
raw = open(pdf_txt, encoding='utf-8').read().split('\n')

# ---------- token stats for line-wrap joining ----------
tok = collections.Counter()
for l in raw:
    for t in l.split():
        tok[t] += 1
ENDCH = set('다.,)]:;?!”"’\'·은는이가을를의에도와과로서며고면만요음임함됨')

def joinpair(a, b):
    if not a: return b
    if not b: return a
    A = a.split()[-1]; B = b.split()[0]
    if a.endswith(' ') or b.startswith(' '): return a.rstrip() + ' ' + b.lstrip()
    if re.match(r'[A-Za-z0-9]', A[-1]) and re.match(r'[A-Za-z(]', B[0]): return a + ' ' + b
    if tok.get(A + B, 0) > 0: return a + b
    # strip punctuation for lookup
    Bc = re.sub(r'[.,):;]+$', '', B)
    if tok.get(A + Bc, 0) > 0: return a + b
    Bk = re.sub(r'[.,):;“”‘’"\']+', '', B)
    if Bk and Bk[0] in '는나서도을를에의로와과은이가' and len(Bk) <= 3 and tok.get(B, 0) <= 2 and re.match(r'[가-힣’”)]', A[-1]): return a + b
    if A[-1] in ENDCH: return a + ' ' + b
    if A[-1] in '(-–→/': return a + b
    if tok.get(A, 0) > 1 and tok.get(B, 0) > 1: return a + ' ' + b
    return a + b

def join(lines):
    s = ''
    for l in lines:
        l = re.sub(r'\s{2,}', ' ', l.strip())
        s = joinpair(s, l)
    return s

CIT = re.compile(r'\s*\[\d+(?:\s*[,\-–]\s*\d+)*\]')
def clean(s): return CIT.sub('', s).strip()

# ---------- paragraphs ----------
if CH == 1:
    SECS0 = ['신경세포의 구조와 신호 전달', '시냅스와 신경전달물질 시스템', '신경가소성과 발달', '신경발달과 기능적 연결성',
            '좌·우 대뇌반구의 기능적 편측화와 협력', '중력과 감각·운동 발달']
    START = 90; SUMMARK = lambda t: t == 'Ⅰ장 종합'; SECRE = r'^(\d{1,2})\.\s+(.+)$'
    NEW_TITLES = ['신경세포는 어떻게 신호를 보낼까', '시냅스와 신경전달물질', '경험이 뇌를 바꾼다: 신경가소성', '뇌는 네트워크로 일한다',
                  '좌뇌·우뇌는 경쟁이 아니라 협력', '중력과 감각·운동 발달']
    SUMTITLE = '아이의 발달을 바라보는 원칙'
elif CH == 3:
    SECS0 = ['신경계의 에너지 대사와 항상성', '미토콘드리아와 산화스트레스·항산화 시스템', '신경전달물질의 합성·대사와 영양 보조인자',
             '메틸화와 1탄소 대사', '지방산·인지질·콜레스테롤과 신경막·수초', '장-뇌 축과 장내미생물·장 장벽', '면역계·사이토카인과 신경염증',
             '혈액-뇌 장벽과 신경계 내부환경의 보호', '스트레스와 HPA Axis·자율신경계', '수면·일주기리듬과 신경대사 항상성',
             '신체활동과 신경대사 환경', '생화학적 환경과 정서·행동·사회적 기능', 'ASD·ADHD·틱 등 신경발달장애의 대사·면역 연구',
             '신경계 대사와 발작 취약성·뇌전증', '영양·보충제 중재의 근거와 주의점', '기능의학·생화학적 해석의 근거와 한계']
    START = 294; SUMMARK = lambda t: t == 'Ⅲ장 종합'; SECRE = r'^(\d{1,2})\.\s+(.+)$'
    NEW_TITLES = SECS0[:]
    SUMTITLE = '생화학 정보를 아이 이해에 쓰는 원칙'
else:
    SECS0 = ['대뇌피질의 구조와 기능', '전두엽과 실행기능·행동조절', '두정엽과 체성감각·신체도식·공간처리', '측두엽과 청각·언어·기억',
             '후두엽과 시각정보 처리', '기저핵과 운동·행동 선택·습관', '소뇌와 타이밍·예측·오류수정', '시상과 감각정보 조절',
             '시상하부와 항상성·자율신경·내분비 조절', '변연계와 정서·동기·기억', '뇌간과 각성·안구운동·자세조절',
             '척수와 주요 상행·하행 신경로', '전정계·안구운동계와 자세·공간 안정화', '사회적 기능을 구성하는 신경네트워크',
             '주요 기능적 회로와 네트워크의 통합']
    START = 329; SUMMARK = lambda t: t.startswith('Ⅱ장 종합.'); SECRE = r'^(\d{1,2})절\.\s+(.+)$'
    NEW_TITLES = SECS0[:]
    SUMTITLE = '뇌 구조 지식을 아이 이해에 쓰는 원칙'
def is_head(l, summ):
    t = l.strip()
    if re.match(r'^\d+-\d+\.\s', t) or re.match(r'^\[[^\]]+\]$', t) or SUMMARK(t) or (CH == 3 and t == '참고문헌'): return True
    m = re.match(SECRE, t)
    if m and m.group(2).strip() in SECS0: return True
    if summ and re.match(r'^\d{1,2}\.\s', t): return True
    return False
paras = []; cur = []; summ = False
for l in raw[START:]:
    if SUMMARK(l.strip()): summ = True
    if l.strip() == '':
        if cur: paras.append(cur); cur = []
    elif is_head(l, summ):
        if cur: paras.append(cur)
        cur = [l]
    else:
        cur.append(l)
if cur: paras.append(cur)

SECS = SECS0
EXCLUDE = re.compile(r'참고문헌|장 핵심 결론|종합으로의 연결|장과의 연결|장 핵심 정리|학습목표|다음 절과의 연결|다음 장과의 연결|약리학적 연결|약물치료를 통해 이해하는 원칙|합성에 관여하는 주요 요소|주요 합성 경로|주요 합성 및 대사|\d절 핵심 정리')
CAUTION = re.compile(r'해석상 주의|피해야 할|권장되는')
posts = []; post = None; sec = None; box = None; in_summary = False; stop = False

def new_sec(title):
    global sec
    sec = dict(title=title, easy=[], key=[], caution=[], terms=[], detail=[])
    post['sections'].append(sec)

for p in paras:
    first = p[0].strip()
    if stop: break
    if re.match(r'^\[(Ⅰ|Ⅱ|Ⅲ)장 핵심 정리\]$', first) or re.match(r'^\[(Ⅲ|Ⅳ)장과의 연결\]$', first): stop = True; continue
    if CH == 3 and first == '참고문헌': box = '참고문헌'; continue
    text_lines = [x.strip() for x in p]
    m = re.match(SECRE, first)
    if m and m.group(2).strip() in SECS and not in_summary:
        i = SECS.index(m.group(2).strip())
        post = dict(no=i + 1, title=NEW_TITLES[i], orig=m.group(2).strip(), sections=[]); posts.append(post)
        sec = None; box = None; continue
    if SUMMARK(first):
        in_summary = True
        post = dict(no=len(SECS) + 1, title=SUMTITLE, orig=first, sections=[]); posts.append(post)
        sec = None; box = None
        if len(p) > 1 and not re.match(r'^\(', p[1].strip()): pass
        continue
    if post is None: continue
    if re.match(r'^\(.*\)$', first) and len(p) == 1 and sec is None: continue  # english subtitle
    if in_summary and first == '신경발달을 바라보는 기본 임상 원칙': continue
    if re.match(r'^\(', first) and in_summary and sec is None and len(' '.join(text_lines)) < 200 and re.search(r'[A-Za-z]', first): continue
    ms = re.match(r'^(\d+-\d+)\.\s+(.+)$', first)
    mp = re.match(r'^(\d{1,2})\.\s+(.+)$', first) if in_summary else None
    if ms or mp:
        new_sec((ms or mp).group(2).strip()); box = None
        rest = text_lines[1:]
        if rest:
            if in_summary: sec['easy'].append(clean(join(rest)))
            else: sec['detail'].append(clean(join(rest)))
        continue
    if sec is None:
        new_sec('들어가며' if not in_summary else '들어가며')
    mb = re.match(r'^\[([^\]]+)\]\s*$', first)
    if mb:
        box = mb.group(1).strip()
        body = text_lines[1:]
    else:
        body = text_lines
        if box and box not in ('참고문헌', '핵심 정리') and (re.search(r'\[\d+\]', ' '.join(body)) or re.match(r'^\d+\)\s', first) or re.match(r'^[•▪-]\s', first) and box != '용어 이해'):
            box = None
    if not body: continue
    if box and EXCLUDE.search(box): continue
    if not box:
        if post['no'] == 2 and sec['title'].startswith('영양과'): continue
        t = clean(join(body))
        if re.search(r'조효소|보조인자', t) and post['no'] == 2: continue
        if in_summary: sec['easy'].append(t)
        else:
            if re.match(r'^\d+\)\s', t) and len(t) < 60: sec['detail'].append(t)
            else: sec['detail'].append(t)
        continue
    if box == '쉽게 이해하기':
        sec['easy'].append(clean(join(body)))
    elif box in ('핵심 이해', '핵심 원칙'):
        sec['key'].append(clean(join(body)))
    elif box == '현장 적용 팁':
        sec['tip'] = ((sec.get('tip') or '') + ' ' + clean(join(body))).strip()
    elif box == '핵심 정리':
        items = []
        for l in body:
            if re.match(r'^\d+\)\s*', l): items.append(re.sub(r'^\d+\)\s*', '', l))
            elif items: items[-1] = joinpair(items[-1], l)
        post.setdefault('pdfsum', []).extend(clean(i) for i in items)
    elif box == '용어 이해':
        entries = []
        for l in body:
            if re.match(r'^[^:：]{1,45}[:：]\s', l) and not (entries and not entries[-1].rstrip().endswith(('.', '다', '분', '것', '질', '정', '조', '체', '능', '상', '태', '위', '자', '역', '물', '로', '현', '름', '성', '계', '력', '용', '름', '향'))):
                entries.append(l)
            elif re.match(r'^[^:：]{1,45}[:：]\s', l):
                entries.append(l)
            elif entries:
                entries[-1] = joinpair(entries[-1], l)
            else:
                entries.append(l)
        sec['terms'] += [clean(re.sub(r'\s{2,}', ' ', e)) for e in entries]
    elif CAUTION.search(box):
        lbl = '' if box == '해석상 주의' else box
        if lbl and (not sec['caution'] or sec['caution'][-1] != '## ' + lbl): sec['caution'].append('## ' + lbl)
        elif not lbl and sec['caution'] and sec['caution'][-1].startswith('## '): sec['caution'].append('## 해석상 주의')
        starts = [i for i, l in enumerate(body) if l[:1] in '“"']
        if len(starts) >= 2:
            if starts[0] != 0: sec['caution'].append(clean(join(body[:starts[0]])))
            for k, st in enumerate(starts):
                en = starts[k + 1] if k + 1 < len(starts) else len(body)
                sec['caution'].append(clean(join(body[st:en])))
        else:
            sec['caution'].append(clean(join(body)))
    else:
        if not sec['detail'] or sec['detail'][-1] != '0) ' + box:
            sec['detail'].append('0) ' + box)
        # list-like boxes keep line structure
        if all(re.match(r'^([•▪-]|\d+\.|\d+\)|[^:]{1,30}:)', l) for l in body[:1]) and len(body) > 1 and box in ('주요 기능', '주요 기시부', '주요 분포', '대표적인 도파민 경로', '관련 물질', 'Ⅰ장 핵심 원칙', 'Ⅰ장 핵심 임상 질문', '핵심 질문'):
            items = []
            for l in body:
                if re.match(r'^([•▪-]|\d+\.|\d+\))\s*', l) or re.match(r'^[^:]{1,30}:', l): items.append(l)
                elif items: items[-1] = joinpair(items[-1], l)
            for it in items:
                it = clean(re.sub(r'^([•▪-]|\d+\.|\d+\))\s*', '', it))
                sec['detail'].append('- ' + it)
        else:
            sec['detail'].append(clean(join(body)))

# ---------- HWPX: summaries + staff tips ----------
H = [l.strip() for l in open(hwpx_txt, encoding='utf-8').read().split('\n') if l.strip()]
if CH == 3:
    H2 = []
    for l in H:
        if H2 and not re.match(r'^(\d+\.|\d+-\d+\.|\d+절\.|\[|※|"|“|•|-|\d+\))', l) and not H2[-1].startswith('※'):
            H2[-1] = joinpair(H2[-1], l)
        else:
            H2.append(l)
    H = H2
tips = {}; sums = {}
i = 0
while i < len(H):
    l = H[i]
    m = re.match(r'^(\d+)-\d+\.', l)
    if m: curn = int(m.group(1))
    if l.startswith('※ 현장 적용 팁'):
        t = []; j = i + 1
        while j < len(H) and not H[j].startswith('[') and not re.match(r'^\d+절|^\d-\d', H[j]):
            t.append(H[j]); j += 1
        tips[curn] = (' '.join(x.strip('"“” ') for x in t) if CH != 3 else join([x for x in t]).strip('"“” ')).strip()
        i = j; continue
    ms = re.match(r'^\[(\d+)절 핵심 정리\]$', l)
    if ms:
        n = int(ms.group(1)); s = []; j = i + 1
        while j < len(H) and re.match(r'^\d+\.\s', H[j]):
            s.append(re.sub(r'^\d+\.\s*', '', H[j])); j += 1
        sums[n] = s; i = j; continue
    i += 1

for p in posts:
    p['summary'] = sums.get(p['no'], []) or p.get('pdfsum', [])
    p['tip'] = tips.get(p['no'], '')
json.dump(posts, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for p in posts:
    print(p['no'], p['title'], '| tip', len(p['tip']), '| sum', len(p['summary']))
    for s in p['sections']:
        print('   ', s['title'][:40], 'easy', len(s['easy']), 'key', len(s['key']), 'caut', len(s['caution']), 'terms', len(s['terms']), 'detail', len(s['detail']))
