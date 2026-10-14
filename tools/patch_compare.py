import sys
src,dst=sys.argv[1],sys.argv[2]
t=open(src,encoding='utf-8').read()
def rep(a,b):
    global t
    assert t.count(a)==1,(a[:70],t.count(a)); t=t.replace(a,b)
# hook: after links in check result
rep("""     if((s.links||[]).length)h+='<div class="chk-links">""","""     h+=cmpHtml(s,st);
     if((s.links||[]).length)h+='<div class="chk-links">""")
rep("var XK={",r"""function cmpHtml(s,st){var c=s.compare;if(!c)return '';var sc=s.scale||[],its=s.items||[];
 var h='<div class="cmp"><h4>연구 자료와 비교해 보기</h4>'+(c.intro?'<p class="cmp-intro">'+esc(c.intro)+'</p>':'');
 function v(i){var n=st[i];return n==null?null:(c.score?c.score[n]:n)}
 var mn=c.min||0,mx=c.max||3;function pct(x){return Math.max(0,Math.min(100,(x-mn)/(mx-mn)*100))}
 function f(x){return (Math.round(x*100)/100).toFixed(2).replace(/0$/,'')}
 var G=c.groups||[];
 function legend(extra){return '<div class="cmp-leg"><span><i class="mk me"></i>우리 아이</span>'+G.map(function(g,k){return '<span><i class="mk g'+k+'"></i>'+esc(g.name)+'</span>'}).join('')+(extra||'')+'</div>'}
 function track(me,vals,line){var x='<div class="cmp-tr">';if(line!=null)x+='<i class="cmp-line" style="left:'+pct(line)+'%"></i>';
   vals.forEach(function(y,k){if(y!=null)x+='<i class="mk g'+k+'" style="left:'+pct(y)+'%" title="'+esc(G[k].name)+' '+f(y)+'"></i>'});
   if(me!=null)x+='<i class="mk me" style="left:'+pct(me)+'%" title="우리 아이 '+f(me)+'"></i>';return x+'</div>'}
 if(c.mode==='item'){
   var ends=c.ends||[];
   h+=legend(c.cutName?'<span><i class="cmp-line-k"></i>'+esc(c.cutName)+'</span>':'');
   h+='<div class="cmp-scale"><span>'+esc(ends[0]||'')+'</span><span>'+esc(ends[1]||'')+'</span></div>';
   (c.summary||[]).forEach(function(r){var a=0,n=0;for(var i=r.from;i<=r.to;i++){var y=v(i);if(y!=null){a+=y;n++}}var me=n?a/n:null;
     h+='<div class="cmp-row sum"><div class="cmp-l"><b>'+esc(r.name)+'</b><small>우리 아이 '+(me==null?'-':f(me))+' · '+G.map(function(g,k){return esc(g.short||g.name)+' '+(r.values[k]==null?'-':f(r.values[k]))}).join(' · ')+(r.cut!=null?' · 기준 '+f(r.cut):'')+'</small></div>'+track(me,r.values,r.cut)+'</div>'});
   h+='<details class="cmp-items"><summary>문항별로 보기</summary>';
   its.forEach(function(q,i){var vals=G.map(function(g){return g.values?g.values[i]:null});
     h+='<div class="cmp-row"><div class="cmp-l"><span class="chk-n">'+(i+1)+'</span><span>'+esc(q)+'</span></div>'+track(v(i),vals,null)+'</div>'});
   h+='</details>';
 }else if(c.mode==='total'){
   var yes=0;its.forEach(function(q,i){if(st[i]!=null&&(c.concern||s.concern||[]).indexOf(sc[st[i]])>=0)yes++});var me=its.length?yes/its.length*100:0;
   h+='<div class="cmp-bars">';
   [{name:'우리 아이',val:me,cls:'me'}].concat(G.map(function(g,k){return {name:g.name,val:g.value,cls:'g'+k}})).forEach(function(b){
     h+='<div class="cmp-bar"><span class="cmp-bn">'+esc(b.name)+'</span><span class="cmp-bt"><i class="'+b.cls+'" style="width:'+Math.max(2,b.val)+'%"></i></span><b>'+Math.round(b.val)+'%</b></div>'});
   h+='</div>'+(c.cutNote?'<p class="cmp-intro">'+esc(c.cutNote)+'</p>':'');
 }else if(c.mode==='age'){
   h+='<div class="cmp-age">';its.forEach(function(q,i){var a=(c.ages||[])[i];if(!a)return;var n=st[i];var hard=n!=null&&(s.concern||[]).indexOf(sc[n])>=0;
     h+='<div class="cmp-age-r'+(hard?' hard':'')+'"><span class="chk-n">'+(i+1)+'</span><span class="q">'+esc(q)+'</span><span class="a">'+esc(a)+'</span><span class="me">'+(n==null?'-':esc(sc[n]))+'</span></div>'});
   h+='</div>';
 }
 if(c.note)h+='<p class="cmp-note">'+esc(c.note)+'</p>';
 if((c.refs||[]).length)h+='<div class="cmp-refs"><span>참고 자료</span><ul>'+c.refs.map(function(r){var a=splitBar(r);return '<li>'+(a[1]?'<a href="'+esc(a[1])+'" target="_blank" rel="noopener">'+esc(a[0])+'</a>':esc(a[0]))+'</li>'}).join('')+'</ul></div>';
 return h+'</div>'}
var XK={""")
css=r"""
.cmp{margin-top:16px;padding:16px;border-radius:14px;background:var(--surface)}
.cmp h4{margin:0 0 6px;font-size:16px}
.cmp-intro{margin:0 0 10px!important;font-size:14px!important;color:var(--ink-2)!important}
.cmp-leg{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:13px;color:var(--ink-2);margin:6px 0 4px}
.cmp-leg span{display:inline-flex;align-items:center;gap:6px}
.mk{display:inline-block;width:12px;height:12px;border-radius:50%;border:2px solid var(--surface);box-shadow:0 0 0 1px rgba(0,0,0,.08)}
.mk.me{background:var(--brand)}.mk.g0{background:#2b8a3e}.mk.g1{background:#e8590c}.mk.g2{background:#7048e8}
.cmp-tr .mk{position:absolute;top:50%;transform:translate(-50%,-50%)}
.cmp-tr .mk.me{width:16px;height:16px;z-index:2}
.cmp-tr{position:relative;height:22px;border-radius:11px;background:var(--surface-2);margin:2px 8px}
.cmp-line{position:absolute;top:2px;bottom:2px;width:0;border-left:2px dashed #c92a2a}
.cmp-line-k{display:inline-block;width:14px;border-top:2px dashed #c92a2a}
.cmp-scale{display:flex;justify-content:space-between;font-size:12px;color:var(--ink-3);margin:8px 8px 0}
.cmp-row{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:10px;align-items:center;padding:8px 0;border-top:1px solid var(--line)}
.cmp-row.sum .cmp-l b{display:block;font-size:15px}
.cmp-row small{color:var(--ink-3);font-size:12.5px}
.cmp-l{display:flex;gap:8px;font-size:14px;line-height:1.45;color:var(--ink-2)}
.cmp-row.sum .cmp-l{display:block}
.cmp-items{margin-top:6px}
.cmp-items>summary{cursor:pointer;font-weight:700;color:var(--brand-ink);font-size:14px;padding:8px 0}
.cmp-bars{display:grid;gap:8px;margin:8px 0}
.cmp-bar{display:grid;grid-template-columns:110px minmax(0,1fr) 44px;gap:10px;align-items:center;font-size:14px}
.cmp-bt{height:14px;border-radius:7px;background:var(--surface-2);overflow:hidden}
.cmp-bt i{display:block;height:100%;border-radius:7px}
.cmp-bt i.me{background:var(--brand)}.cmp-bt i.g0{background:#e8590c}.cmp-bt i.g1{background:#2b8a3e}
.cmp-bar b{text-align:right;color:var(--ink)}
.cmp-age{display:grid;gap:0}
.cmp-age-r{display:grid;grid-template-columns:auto minmax(0,1fr) auto auto;gap:10px;align-items:center;padding:8px 0;border-top:1px solid var(--line);font-size:14px}
.cmp-age-r .a{font-size:13px;color:var(--brand-ink);font-weight:600;white-space:nowrap}
.cmp-age-r .me{font-size:13px;color:var(--ink-3);white-space:nowrap}
.cmp-age-r.hard .me{color:#c92a2a;font-weight:700}
.cmp-note{font-size:13px!important;color:var(--ink-3)!important;margin:10px 0 0!important}
.cmp-refs{margin-top:8px;font-size:12.5px;color:var(--ink-3)}
.cmp-refs ul{margin:4px 0 0;padding-left:1.2em}
.cmp-refs a{color:var(--ink-2)}
@media (max-width:600px){.cmp-row{grid-template-columns:minmax(0,1fr)}.cmp-bar{grid-template-columns:84px minmax(0,1fr) 40px}.cmp-age-r{grid-template-columns:auto minmax(0,1fr);}.cmp-age-r .a,.cmp-age-r .me{grid-column:2}}
.apple .cmp{background:var(--glass);box-shadow:var(--glass-edge),var(--sh-stat)}
"""
rep("</style>\n<div id=\"root\">", css+"</style>\n<div id=\"root\">")
open(dst,'w',encoding='utf-8').write(t);print('ok')
