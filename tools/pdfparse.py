import re, sys, os, glob, json, subprocess
U, OUT = sys.argv[1], sys.argv[2]
L1 = '●⚫'; L2 = '▪■'; L3 = '•·-–'

def pages(path):
    t = subprocess.run(['pdftotext', '-layout', path, '-'], capture_output=True, text=True).stdout
    return t.split('\f')

def parse(path):
    pg = pages(path)
    week = {'title': '', 'sessions': []}
    sess = None
    for p in pg:
        lines = [l.rstrip() for l in p.split('\n')]
        nonempty = [l for l in lines if l.strip()]
        if not nonempty: continue
        joined = ' '.join(l.strip() for l in nonempty)
        mt = re.search(r'(?m)^\s*(\d{2})\.\s+(\S.*)$', p)
        if not week['title'] and mt and len(nonempty) <= 4:
            week['title'] = mt.group(2).strip()
        ms = re.search(r'(?m)^\s*(\d)교시\s+(\S.*)$', p)
        if ms and len(nonempty) <= 5:
            sess = {'title': ms.group(2).strip(), 'slides': []}
            week['sessions'].append(sess); continue
        if sess is None: continue
        # header + slide title
        body = nonempty[:]
        header = body.pop(0).strip()
        title = ''
        if body:
            m = re.match(r'^\s*(\d+)\s{2,}(\S.*)$', body[0]) or re.match(r'^\s*(\d+)\s+(\S.*)$', body[0])
            if m:
                title = m.group(2).strip(); body.pop(0)
            elif re.match(r'^\s*\d+\s*$', body[0]):
                body.pop(0)
                if body: title = body.pop(0).strip()
        items = []  # (level, text)
        seen_l1 = False
        for raw in body:
            s = raw.strip()
            if not s or re.match(r'^\d+$', s): continue
            c = s[0]
            if c in L1:
                items.append([1, s[1:].strip()]); seen_l1 = True
            elif c in L2:
                items.append([2 if seen_l1 else 1, s[1:].strip()])
            elif c in L3 and len(s) > 1 and s[1] in ' 　':
                items.append([3 if seen_l1 else 2, s[1:].strip()])
            elif re.match(r'^\(\d+\)\s*\S', s):
                items.append([0, re.sub(r'^\((\d+)\)\s*', r'\1) ', s)])
            elif re.match(r'^\d+\.\s+\S', s):
                items.append([1, re.sub(r'\s+', ' ', s)])
            elif items and items[-1][0] != 0:
                items[-1][1] += ' ' + s
            else:
                items.append([1, s])
        for it in items: it[1] = re.sub(r'\s{2,}', ' ', it[1]).strip()
        if sess['slides'] and sess['slides'][-1]['title'] == title:
            sess['slides'][-1]['items'] += items
        else:
            sess['slides'].append({'title': title, 'items': items})
    return week

def to_detail(sess):
    out = []
    for sl in sess['slides']:
        if sl['title']: out.append('1. ' + sl['title'])
        last1 = None
        for lv, t in sl['items']:
            if not t: continue
            if lv == 0: out.append(t); last1 = None
            elif lv == 1:
                if t == last1: continue
                out.append('- ' + t); last1 = t
            else: out.append(t)
    return out

res = []
for f in sorted(glob.glob(os.path.join(U, '*.pdf'))):
    b = os.path.basename(f); n = int(b.split('-', 1)[1][:2])
    w = parse(f)
    secs = []
    for s in w['sessions']:
        titles = []
        for sl in s['slides']:
            t = re.sub(r'\d+$', '', sl['title']).strip() if False else sl['title']
            if t and t not in titles: titles.append(t)
        secs.append({'title': s['title'], 'contents': titles, 'detail': to_detail(s)})
    res.append({'week': n, 'title': w['title'], 'sessions': secs})
res.sort(key=lambda x: x['week'])
json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for w in res:
    print(w['week'], w['title'], [(s['title'], len(s['contents']), len(s['detail'])) for s in w['sessions']])
