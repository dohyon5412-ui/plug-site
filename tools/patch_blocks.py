import sys
src,dst=sys.argv[1],sys.argv[2]
t=open(src,encoding='utf-8').read()
def rep(a,b):
    global t
    assert t.count(a)==1,(a[:70],t.count(a)); t=t.replace(a,b)
# render new kinds
rep("  if(s.kind==='text'){return h+'<div class=\"blk\"><div class=\"text-body\">'+esc(s.body||'')+'</div></div></section>'}",
"""  if(s.kind==='text'){return h+'<div class="blk"><div class="text-body">'+esc(s.body||'')+'</div></div></section>'}
  if(XK[s.kind])return h+XK[s.kind](p,s)+'</section>';""")
rep("function sectionHtml(p,s){",
r"""function splitBar(x){var i=String(x).indexOf('|');return i<0?[String(x).trim(),'']:[String(x).slice(0,i).trim(),String(x).slice(i+1).trim()]}
function leadHtml(s){return s.lead?'<p class="x-lead">'+esc(s.lead)+'</p>':''}
var CHK_NOTE='이 체크리스트는 진단이 아니라 아이의 평소 모습을 돌아보기 위한 참고 자료예요. 걱정되는 쪽으로 답한 문항이 많거나 일상생활의 어려움이 이어진다면 전문가와 상담해 보세요.';
var XK={
 info:function(p,s){return '<div class="blk">'+detailHtml(s.lines||[])+'</div>'},
 defs:function(p,s){return '<div class="blk">'+leadHtml(s)+'<dl class="defs">'+(s.lines||[]).map(function(x){var a=splitBar(x);return '<div class="def"><dt>'+esc(a[0])+'</dt>'+(a[1]?'<dd>'+esc(a[1])+'</dd>':'')+'</div>'}).join('')+'</dl></div>'},
 steps:function(p,s){return '<div class="blk">'+leadHtml(s)+'<ol class="steps">'+(s.lines||[]).map(function(x,i){var a=splitBar(x);return '<li><span class="sn">'+(i+1)+'</span><div><b>'+esc(a[0])+'</b>'+(a[1]?'<p>'+esc(a[1])+'</p>':'')+'</div></li>'}).join('')+'</ol></div>'},
 faq:function(p,s){var items=[],cur=null;(s.lines||[]).forEach(function(x){x=String(x);if(/^Q\s/.test(x)){cur={q:x.slice(2).trim(),a:[]};items.push(cur)}else if(cur)cur.a.push(x.replace(/^A\s/,'').trim())});
   return '<div class="blk faq">'+items.map(function(it){return '<details class="faq-i"><summary>'+esc(it.q)+'</summary>'+it.a.map(function(a){return '<p>'+esc(a)+'</p>'}).join('')+'</details>'}).join('')+'</div>'},
 check:function(p,s){var key=p.id+'/'+s.id;var st=ui.check[key]||{};var sc=s.scale||[],con=s.concern||[],its=s.items||[];var a=0,c=0;
   var h='<div class="blk check"><p class="x-lead">각 문항에서 아이의 모습과 가장 가까운 답을 골라 주세요.</p>';
   its.forEach(function(q,i){var sel=st[i];if(sel!=null){a++;if(con.indexOf(sc[sel])>=0)c++}
     h+='<div class="chk-q"><p><span class="chk-n">'+(i+1)+'</span><span>'+esc(q)+'</span></p><div class="chk-opts" role="group" aria-label="'+(i+1)+'번 답">'+sc.map(function(o,n){return '<button class="chk-o'+(sel===n?' on':'')+(con.indexOf(o)>=0?' warn':'')+'" data-act="chk" data-key="'+esc(key)+'" data-i="'+i+'" data-n="'+n+'" aria-pressed="'+(sel===n)+'">'+esc(o)+'</button>'}).join('')+'</div></div>'});
   h+='<div class="chk-res" role="status">';
   if(a<its.length)h+='<b>'+a+' / '+its.length+' 문항 답함</b><p>남은 문항 '+(its.length-a)+'개에 답하면 결과를 볼 수 있어요.</p>';
   else{var lv=-1,rr=null;(s.results||[]).forEach(function(x,k){var a3=String(x).split('|').map(function(y){return y.trim()});if(c>=Number(a3[0])){lv=k;rr=a3}});
     h+='<p class="chk-count">걱정되는 쪽으로 답한 문항 <b>'+c+'</b>개 / 전체 '+its.length+'개</p>';
     if(rr)h+='<div class="chk-lv lv'+Math.min(lv,2)+'"><b>'+esc(rr[1]||'')+'</b><p>'+esc(rr.slice(2).join(' | '))+'</p></div>';
     if((s.links||[]).length)h+='<div class="chk-links"><span>함께 보면 좋아요</span>'+s.links.map(function(x){var a=splitBar(x);return '<a href="#p-'+esc(a[1])+'">'+esc(a[0])+'</a>'}).join('')+'</div>';}
   h+='<p class="chk-note">'+esc(s.note||CHK_NOTE)+'</p>'+(a?'<button class="link-btn" data-act="chk-reset" data-key="'+esc(key)+'">처음부터 다시</button>':'')+'</div>';
   return h+'</div>'}
};
function sectionHtml(p,s){""")
rep("quiz:{},openGroups:{},openSecs:{}};","quiz:{},check:{},openGroups:{},openSecs:{}};")
rep("   case 'quiz-reset':delete ui.quiz[d('key')];rerenderKeep();break;",
"""   case 'quiz-reset':delete ui.quiz[d('key')];rerenderKeep();break;
   case 'chk':var ck=d('key');ui.check[ck]=ui.check[ck]||{};var ci=+d('i'),cn=+d('n');if(ui.check[ck][ci]===cn)delete ui.check[ck][ci];else ui.check[ck][ci]=cn;rerenderKeep();break;
   case 'chk-reset':delete ui.check[d('key')];rerenderKeep();break;""")
# search
rep("s.detail||[],s.body?[s.body]:[]);","s.detail||[],s.body?[s.body]:[],s.lines||[],s.items||[],s.lead?[s.lead]:[]);")
# editor
rep("    if(s.kind==='text'){h+=fText('본문',sb+'.body',s.body||'',{area:1,rows:8})}",
"""    if(s.kind==='text'){h+=fText('본문',sb+'.body',s.body||'',{area:1,rows:8})}
    else if(s.kind==='check'){h+=fText('보기 (한 줄에 하나)',sb+'.scale',(s.scale||[]).join('\\n'),{area:1,lines:1,rows:4})+fText('걱정되는 쪽 보기 (위 보기 중에서, 한 줄에 하나)',sb+'.concern',(s.concern||[]).join('\\n'),{area:1,lines:1,rows:2})+fText('문항 (한 줄에 하나)',sb+'.items',(s.items||[]).join('\\n'),{area:1,lines:1,rows:10})+fText('결과 안내',sb+'.results',(s.results||[]).join('\\n'),{area:1,lines:1,rows:4,hint:'한 줄에 ‘걱정되는 쪽 답이 몇 개 이상일 때 | 제목 | 설명’. 위에서부터 낮은 단계 순서로 입력'})+fText('함께 보면 좋은 자료',sb+'.links',(s.links||[]).join('\\n'),{area:1,lines:1,rows:3,hint:'한 줄에 ‘보일 이름 | 자료 id’'})+fText('안내 문구 (비우면 기본 문구)',sb+'.note',s.note||'',{area:1,rows:2})}
    else if(XK[s.kind]){var KH={info:'‘1)’로 시작하면 작은 제목, ‘-’는 항목, 그 밖의 줄은 문단이 돼요.',defs:'한 줄에 ‘이름 | 설명’',steps:'한 줄에 ‘단계 이름 | 설명’ (순서대로 번호가 붙어요)',faq:'‘Q ’로 시작하는 줄은 질문, ‘A ’로 시작하는 줄은 답'};
      h+=(s.kind==='defs'||s.kind==='steps'?fText('안내 글 (선택)',sb+'.lead',s.lead||'',{area:1,rows:2}):'')+fText('내용',sb+'.lines',(s.lines||[]).join('\\n'),{area:1,lines:1,rows:10,hint:KH[s.kind]})}""")
# CSS
css=r"""
/* plug info blocks */
.x-lead{margin:0 0 14px;color:var(--ink-2)}
.defs{margin:0;display:grid;gap:10px}
.def{padding:12px 14px;border-radius:12px;background:var(--surface-2)}
.def dt{font-weight:700;line-height:1.45}
.def dd{margin:4px 0 0;color:var(--ink-2);font-size:15px}
.steps{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.steps li{display:flex;gap:12px;align-items:flex-start}
.steps .sn{flex:none;width:30px;height:30px;border-radius:50%;background:var(--brand);color:#fff;display:inline-flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;margin-top:1px}
.steps b{display:block;line-height:1.5;padding-top:3px}
.steps p{margin:2px 0 0;color:var(--ink-2);font-size:15px}
.faq{padding:6px 22px}
.faq-i{border-top:1px solid var(--line)}
.faq-i:first-child{border-top:0}
.faq-i summary{cursor:pointer;list-style:none;padding:14px 0;font-weight:700;display:flex;gap:10px;line-height:1.5}
.faq-i summary::-webkit-details-marker{display:none}
.faq-i summary::before{content:"Q";flex:none;color:var(--brand-ink);font-weight:800}
.faq-i[open] summary{color:var(--brand-ink)}
.faq-i p{margin:0 0 12px 22px;color:var(--ink-2)}
.chk-q{padding:14px 0;border-top:1px solid var(--line)}
.chk-q:first-of-type{border-top:0;padding-top:4px}
.chk-q>p{margin:0 0 10px;display:flex;gap:10px;font-weight:600;line-height:1.55}
.chk-n{flex:none;min-width:24px;height:24px;border-radius:12px;background:var(--surface-2);color:var(--ink-2);font-size:13px;display:inline-flex;align-items:center;justify-content:center;padding:0 6px;margin-top:1px}
.chk-opts{display:flex;flex-wrap:wrap;gap:6px;padding-left:34px}
.chk-o{border:1px solid var(--line);background:var(--surface);border-radius:999px;padding:6px 14px;font-size:14px;line-height:1.4}
.chk-o:hover{border-color:var(--brand)}
.chk-o.on{background:var(--brand);border-color:var(--brand);color:#fff;font-weight:600}
.chk-res{margin-top:14px;padding:16px 18px;border-radius:14px;background:color-mix(in srgb,var(--brand) 8%,var(--surface))}
.chk-res b{font-size:17px;color:var(--brand-ink)}
.chk-res p{margin:4px 0 0;color:var(--ink-2);font-size:15px}
.chk-res .chk-note{font-size:14px;color:var(--ink-3);margin-top:10px}
@media (max-width:600px){.chk-opts{padding-left:0}.faq{padding:4px 16px}}
.apple .def{background:var(--surface-2);border-radius:14px}
.apple .chk-o{border:0;background:var(--surface-2)}
.apple .chk-o.on{background:var(--brand);color:#fff}
.apple .chk-res{border-radius:16px}
.chk-count{margin:0!important;font-size:15px;color:var(--ink-2)}
.chk-count b{font-size:20px;color:var(--brand-ink)}
.chk-lv{margin-top:12px;padding:14px 16px;border-radius:12px;background:var(--surface);border-left:4px solid var(--lvc)}
.chk-lv.lv0{--lvc:#2b8a3e}.chk-lv.lv1{--lvc:#e67700}.chk-lv.lv2{--lvc:#c92a2a}
.chk-lv b{font-size:17px;color:var(--ink)}
.chk-lv p{margin:6px 0 0;color:var(--ink-2);font-size:15px;line-height:1.65}
.chk-links{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-top:12px}
.chk-links span{font-size:13px;color:var(--ink-3);margin-right:2px}
.chk-links a{text-decoration:none;font-size:14px;font-weight:600;color:var(--brand-ink);background:var(--surface);border-radius:999px;padding:6px 12px;box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--brand) 25%,transparent)}
.apple .chk-lv{background:var(--glass);box-shadow:var(--glass-edge),var(--sh-stat)}
"""
rep("</style>\n<div id=\"root\">", css+"</style>\n<div id=\"root\">")
rep("s.groups.length+'</span></button>'","s.groups.reduce(function(n,g){return n+(g.name?1:g.cats.length)},0)+'</span></button>'")
open(dst,'w',encoding='utf-8').write(t)
print('ok')
