"""data/site-data.json + src/template.html -> index.html

사용법:  python build_site.py
"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
HEAD = ('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
        'body{margin:0;font:14px system-ui,-apple-system,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>'
        '</head><body>')


def main():
    with open(os.path.join(ROOT, 'data', 'site-data.json'), encoding='utf-8') as f:
        data = json.load(f)
    with open(os.path.join(ROOT, 'src', 'template.html'), encoding='utf-8') as f:
        tpl = f.read()
    js = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    html = HEAD + tpl.replace('__SITE_DATA__', js) + '</body></html>'
    with open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print('index.html 생성 완료: 자료 %d개, 카테고리 %d개' % (len(data['posts']), len(data['categories'])))


if __name__ == '__main__':
    main()
