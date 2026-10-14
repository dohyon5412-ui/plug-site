import re, json, sys, os, glob
D = sys.argv[1]
CIRC = '①②③④⑤'

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

def parse(path):
    L = clean_lines(path)
    wk = {'subject': '', 'week': None, 'title': '', 'sessions': []}
    # header
    for i, s in enumerate(L[:12]):
        if s == '과목명': wk['subject'] = L[i+1]
        if s == '주차': wk['week'] = int(L[i+1])
        if s == '주차명': wk['title'] = L[i+1]
    sess = None; mode = None; q = None
    for s in L:
        m = re.match(r'^(\d)교시\s*:\s*(.*)$', s)
        if m:
            sess = {'no': int(m.group(1)), 'title': m.group(2).strip(), 'objectives': [], 'contents': [], 'summary': [], 'quiz': []}
            wk['sessions'].append(sess); mode = 'obj'; q = None; continue
        if sess is None: continue
        if s == '[TABLE]':
            continue
        if s == '[학습내용]': mode = 'con'; continue
        if s == '[학습정리]': mode = 'sum'; continue
        if s == '[학습평가]': mode = 'quiz'; q = None; continue
        if mode == 'obj':
            if sess['objectives'] and not re.search(r'(다|다\.)$', sess['objectives'][-1]):
                sess['objectives'][-1] += ' ' + s
            else:
                sess['objectives'].append(s)
        elif mode == 'con':
            t = strip_bullet(s)
            if t: sess['contents'].append(t.rstrip('.'))
        elif mode == 'sum':
            t = strip_bullet(s)
            if t: sess['summary'].append(t)
        elif mode == 'quiz':
            t = re.sub(r'^-\s*', '', s)
            mq = re.match(r'^(\d+)\.\s*(.*)$', t)
            ma = re.match(r'^(정답|답)\s*[:)]\s*(.*)$', t)
            me = re.match(r'^해설\s*[:)]\s*(.*)$', t)
            if mq and (q is None or q.get('answer') is not None):
                q = {'question': mq.group(2).strip(), 'options': [], 'answer': None, 'explanation': ''}
                sess['quiz'].append(q); qstate = 'opt'
            elif q is None:
                continue
            elif ma:
                a = ma.group(2).strip()
                if a and a[0] in CIRC: q['answer'] = CIRC.index(a[0]) + 1
                else:
                    d = re.search(r'\d', a); q['answer'] = int(d.group()) if d else a
                qstate = 'ans'
            elif me:
                q['explanation'] = me.group(1).strip(); qstate = 'exp'
            elif qstate == 'opt':
                if q['options'] or t[0] in CIRC or len(q['question']) > 0 and q['question'][-1] in '?.':
                    q['options'].append(re.sub('^[' + CIRC + r']\s*', '', t))
                else:
                    q['question'] += ' ' + t
            elif qstate == 'exp':
                q['explanation'] = (q['explanation'] + ' ' + t).strip()
    return wk

weeks = []
for f in sorted(glob.glob(os.path.join(D, '*.txt'))):
    weeks.append(parse(f))
json.dump(weeks, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for w in weeks:
    print(w['week'], w['title'], [ (s['no'], s['title'], len(s['objectives']), len(s['contents']), len(s['summary']), [(len(q['options']), q['answer']) for q in s['quiz']]) for s in w['sessions']])
