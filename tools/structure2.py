import re, json, sys, os, glob
D = sys.argv[1]
CIRC = '①②③④⑤⑥⑦⑧'

def clean_lines(path):
    out = []
    for l in open(path, encoding='utf-8'):
        s = l.strip()
        if not s or s == '[CELL]': continue
        out.append(s)
    return out

def strip_bullet(s):
    s = re.sub(r'^[\*\-•·]\s*', '', s)
    s = re.sub(r'^\d+\.\s+', '', s)
    return s.strip()

ENDS = ('.', '다', '임', '함', '음', '됨', '요', ')', '”', '"', '>')

def parse(path):
    L = clean_lines(path)
    wk = {'subject': '', 'week': None, 'title': '', 'sessions': []}
    for i, s in enumerate(L[:12]):
        if s == '과목명': wk['subject'] = L[i+1]
        if s == '주차': wk['week'] = int(L[i+1])
        if s == '주차명': wk['title'] = L[i+1]
    sess = None; mode = None; q = None; qstate = None
    for s in L:
        m = re.match(r'^(\d)교시\s*:\s*(.*)$', s)
        if m:
            sess = {'no': int(m.group(1)), 'title': m.group(2).strip(), 'objectives': [], 'contents': [], 'body': [], 'summary': [], 'quiz': []}
            wk['sessions'].append(sess); mode = 'obj'; q = None; continue
        if sess is None or s == '[TABLE]': continue
        if s == '[학습내용]': mode = 'con'; continue
        if s == '[본 학습]': mode = 'body'; continue
        if s == '[학습정리]': mode = 'sum'; continue
        if s == '[학습평가]': mode = 'quiz'; q = None; continue
        if mode == 'obj':
            if sess['objectives'] and not sess['objectives'][-1].endswith(('다', '다.')):
                sess['objectives'][-1] += ' ' + s
            else:
                sess['objectives'].append(s)
        elif mode == 'con':
            t = strip_bullet(s)
            if t: sess['contents'].append(t.rstrip('.'))
        elif mode == 'body':
            sess['body'].append(s)
        elif mode == 'sum':
            sess.setdefault('sumraw', []).append(s)
            t = re.sub(r'^[\*\-•·]\s*', '', s).strip()
            if not t: continue
            head = re.match(r'^\d+\.\s*(.*)$', t)
            body = head.group(1).strip() if head else t
            if len(body) < 45 and not body.rstrip().endswith(ENDS):
                sess['summary'].append('## ' + body)
            elif head:
                sess['summary'].append(body)
            else:
                sess['summary'].append(t)
        elif mode == 'quiz':
            t = re.sub(r'^-\s*', '', s)
            if re.match(r'^(정답|답)\s*[:)]?\s*_+\s*$', t) or re.match(r'^_+$', t): continue
            mq = re.match(r'^(\d+)\.\s*(.*)$', t)
            ma = re.match(r'^(정답|답)\s*[:)]\s*(.*)$', t)
            me = re.match(r'^해설\s*[:)]\s*(.*)$', t)
            if (mq and (q is None or q.get('answer') is not None)) or (q is None and not ma and not me):
                q = {'question': (mq.group(2) if mq else t).strip(), 'options': [], 'answer': None, 'explanation': ''}
                sess['quiz'].append(q); qstate = 'opt'
            elif q is None:
                continue
            elif ma:
                a = ma.group(2).strip()
                if a and a[0] in CIRC: q['answer'] = CIRC.index(a[0]) + 1
                elif re.match(r'^\d+\s*(번)?\.?$', a): q['answer'] = int(re.match(r'\d+', a).group())
                else: q['answer'] = a
                qstate = 'ans'
            elif me:
                q['explanation'] = me.group(1).strip(); qstate = 'exp'
            elif qstate == 'opt':
                if q['options'] and q.get('circ') and t[0] not in CIRC:
                    q['options'][-1] += ' ' + t
                elif q['options'] or t[0] in CIRC or q['question'][-1:] in '?.':
                    if t[0] in CIRC: q['circ'] = True
                    q['options'].append(re.sub('^[' + CIRC + r']\s*', '', t))
                else:
                    q['question'] += ' ' + t
            elif qstate == 'exp':
                q['explanation'] = (q['explanation'] + ' ' + t).strip()
    TABLES = json.loads(os.environ.get("TABLES", "{}")); TABLES = {tuple(map(int, k.split(","))): v for k, v in TABLES.items()}
    for se in wk['sessions']:
        for q in se['quiz']:
            if not isinstance(q['answer'], int) and not q.get('circ'):
                q['passage'] = ' '.join(q['options']).strip(); q['options'] = []
            q.pop('circ', None)
        k = TABLES.get((wk['week'], se['no']))
        if k:
            cells = [x[3:] if x.startswith('## ') else x for x in se['summary']]
            se['summaryTable'] = {'head': cells[:k], 'rows': [cells[i:i+k] for i in range(k, len(cells), k)]}
            se['summary'] = []
    return wk

weeks = [parse(f) for f in sorted(glob.glob(os.path.join(D, '*.txt')))]
json.dump(weeks, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for w in weeks:
    print(w['week'], w['title'], [(s['no'], len(s['objectives']), len(s['contents']), len(s['body']), len(s['summary']), [(len(q['options']), q['answer']) for q in s['quiz']]) for s in w['sessions']])
