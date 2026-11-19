# -*- coding: utf-8 -*-
"""Build the static GitHub Pages site from features.json."""
import json, io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = [a for a in sys.argv[1:] if a != "--local"]
LOCAL = "--local" in sys.argv          # build the copy that sits beside the PDFs
OUT = args[0] if args else ROOT
D = json.load(io.open(os.path.join(ROOT, "features.json"), encoding="utf-8"))
os.makedirs(OUT, exist_ok=True)

DATA = json.dumps(D, ensure_ascii=False, separators=(",", ":"))

HTML = r"""<!doctype html>
<html lang="en" data-theme="auto">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Contineo SIMS Atlas</title>
<meta name="description" content="Every function in the Contineo SIMS student ERP, the login it lives in, and what you can do there.">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><rect width='16' height='16' fill='%230a0a0a'/><rect x='3' y='3' width='4' height='4' fill='%23fff'/><rect x='9' y='3' width='4' height='4' fill='%23fff'/><rect x='3' y='9' width='4' height='4' fill='%23fff'/><rect x='9' y='9' width='4' height='4' fill='%23888'/></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">
<style>
:root{
  --bg:#ffffff; --surface:#f6f6f5; --raised:#ffffff;
  --ink:#0a0a0a; --ink-2:#3a3a39; --ink-3:#6e6e6c; --ink-4:#9b9b98;
  --line:#dededa; --line-2:#c2c2bd; --solid:#0a0a0a; --on-solid:#ffffff;
  --shadow:0 1px 2px rgba(0,0,0,.05),0 8px 24px rgba(0,0,0,.07);
  --f-sans:"IBM Plex Sans",ui-sans-serif,system-ui,sans-serif;
  --f-mono:"IBM Plex Mono",ui-monospace,"Cascadia Mono",Consolas,monospace;
  color-scheme:light;
}
@media (prefers-color-scheme:dark){ :root:not([data-theme="light"]){
  --bg:#0a0a0a; --surface:#151514; --raised:#121211;
  --ink:#f6f6f4; --ink-2:#cfcfca; --ink-3:#9b9b96; --ink-4:#6e6e6a;
  --line:#2a2a28; --line-2:#3d3d3a; --solid:#f6f6f4; --on-solid:#0a0a0a;
  --shadow:0 1px 2px rgba(0,0,0,.5),0 8px 24px rgba(0,0,0,.6);
  color-scheme:dark; } }
/* an explicit light choice must beat the media query, whatever the OS says */
html[data-theme="light"]{
  --bg:#ffffff; --surface:#f6f6f5; --raised:#ffffff;
  --ink:#0a0a0a; --ink-2:#3a3a39; --ink-3:#6e6e6c; --ink-4:#9b9b98;
  --line:#dededa; --line-2:#c2c2bd; --solid:#0a0a0a; --on-solid:#ffffff;
  --shadow:0 1px 2px rgba(0,0,0,.05),0 8px 24px rgba(0,0,0,.07);
  color-scheme:light; }
html[data-theme="dark"]{
  --bg:#0a0a0a; --surface:#151514; --raised:#121211;
  --ink:#f6f6f4; --ink-2:#cfcfca; --ink-3:#9b9b96; --ink-4:#6e6e6a;
  --line:#2a2a28; --line-2:#3d3d3a; --solid:#f6f6f4; --on-solid:#0a0a0a;
  --shadow:0 1px 2px rgba(0,0,0,.5),0 8px 24px rgba(0,0,0,.6);
  color-scheme:dark; }

*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--f-sans);font-size:15px;line-height:1.5;
  -webkit-font-smoothing:antialiased}
.wrap{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));
  max-width:1360px;margin:0 auto}
button{font:inherit;color:inherit}
:focus-visible{outline:2px solid var(--solid);outline-offset:2px}
img{max-width:100%}

/* masthead */
header{border-bottom:1px solid var(--line);padding-block:28px 20px}
.top{display:flex;justify-content:space-between;align-items:flex-start;gap:16px}
.eyebrow{font-family:var(--f-mono);font-size:11px;letter-spacing:.17em;text-transform:uppercase;color:var(--ink-3)}
h1{font-size:clamp(27px,5vw,42px);line-height:1.04;letter-spacing:-.025em;margin:12px 0 0;font-weight:600;
  text-wrap:balance;max-width:17ch}
.tagline{color:var(--ink-2);margin:12px 0 0;max-width:64ch}
.theme{display:flex;border:1px solid var(--line);border-radius:2px;overflow:hidden;flex:none}
.theme button{background:var(--bg);border:0;border-right:1px solid var(--line);padding:7px 9px;cursor:pointer;
  display:grid;place-items:center;color:var(--ink-3)}
.theme button:last-child{border-right:0}
.theme button[aria-pressed="true"]{background:var(--solid);color:var(--on-solid)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(104px,1fr));gap:1px;background:var(--line);
  border:1px solid var(--line);margin-top:24px}
.stat{background:var(--bg);padding:12px 13px}
.stat b{display:block;font-size:25px;line-height:1;letter-spacing:-.03em;font-weight:600;font-variant-numeric:tabular-nums}
.stat span{display:block;font-family:var(--f-mono);font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--ink-3);margin-top:7px;line-height:1.35}

/* tabs */
.tabs{display:flex;border-bottom:1px solid var(--line);margin-top:24px;overflow-x:auto;scrollbar-width:none}
.tabs::-webkit-scrollbar{display:none}
.tab{background:none;border:0;border-bottom:2px solid transparent;padding:11px 2px;margin-right:26px;cursor:pointer;
  font-weight:500;color:var(--ink-3);white-space:nowrap}
.tab[aria-selected="true"]{color:var(--ink);border-bottom-color:var(--solid)}
.tab small{font-family:var(--f-mono);font-size:10.5px;color:var(--ink-4);margin-left:6px}

/* toolbar */
.bar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;padding-block:16px}
.search{flex:1 1 220px;min-width:0;position:relative}
.search input{width:100%;background:var(--surface);border:1px solid var(--line);border-radius:2px;
  padding:9px 11px 9px 32px;color:var(--ink);font-size:14px;font-family:inherit}
.search input::placeholder{color:var(--ink-4)}
.search svg{position:absolute;left:10px;top:50%;transform:translateY(-50%);stroke:var(--ink-4);fill:none;stroke-width:2.2}
.seg{display:flex;border:1px solid var(--line);border-radius:2px;overflow:hidden;flex-wrap:wrap}
.seg button{background:var(--bg);border:0;border-right:1px solid var(--line);padding:9px 12px;cursor:pointer;
  font-family:var(--f-mono);font-size:11.5px;letter-spacing:.08em;color:var(--ink-3)}
.seg button:last-child{border-right:0}
.seg button[aria-pressed="true"]{background:var(--solid);color:var(--on-solid)}
select{background:var(--surface);border:1px solid var(--line);border-radius:2px;padding:9px 10px;color:var(--ink);
  font-size:13.5px;max-width:100%;font-family:inherit}
.count{font-family:var(--f-mono);font-size:11.5px;color:var(--ink-3);margin-left:auto;white-space:nowrap}
.reset{background:none;border:1px solid var(--line);border-radius:2px;padding:9px 12px;cursor:pointer;
  font-family:var(--f-mono);font-size:11.5px;color:var(--ink-3)}
.reset:hover{border-color:var(--line-2);color:var(--ink)}

.cols{display:grid;grid-template-columns:1fr 372px;gap:22px;align-items:start;padding-bottom:56px}
@media (max-width:980px){ .cols{grid-template-columns:1fr} }

/* capability cards */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(228px,1fr));gap:1px;background:var(--line);
  border:1px solid var(--line);min-width:0}
.card{background:var(--bg);border:0;text-align:left;padding:13px;cursor:pointer;display:flex;
  flex-direction:column;gap:8px;min-width:0;transition:background .12s}
.card:hover{background:var(--surface)}
.card[aria-current="true"]{background:var(--solid);color:var(--on-solid)}
.card[aria-current="true"] .cid,.card[aria-current="true"] .ccat{color:var(--on-solid);opacity:.72}
.card[aria-current="true"] .chip{border-color:var(--on-solid);color:var(--on-solid)}
.card[aria-current="true"] .chip.on{background:var(--on-solid);color:var(--solid)}
.card[aria-current="true"] .opn,.card[aria-current="true"] .mrk{border-color:var(--on-solid);color:var(--on-solid);opacity:.8}
.ctop{display:flex;justify-content:space-between;align-items:center;gap:8px}
.cid{font-family:var(--f-mono);font-size:10.5px;color:var(--ink-4);letter-spacing:.04em}
.cname{font-weight:500;font-size:14px;line-height:1.3;letter-spacing:-.008em}
.cbot{display:flex;justify-content:space-between;align-items:flex-end;gap:6px;margin-top:auto;flex-wrap:wrap}
.ccat{font-family:var(--f-mono);font-size:9.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-4)}
.chipset{display:inline-flex;gap:2px;flex-wrap:wrap}
.chip{display:inline-grid;place-items:center;min-width:25px;height:15px;padding:0 2px;
  border:1px solid var(--line-2);border-radius:1px;font-family:var(--f-mono);font-size:8px;font-weight:600;
  color:var(--ink-4)}
.chip.on{background:var(--solid);color:var(--on-solid);border-color:var(--solid)}
.st{font-size:11px;line-height:1}
.opn,.mrk{font-family:var(--f-mono);font-size:9px;letter-spacing:.05em;color:var(--ink-4);
  border:1px solid var(--line);padding:1px 4px;white-space:nowrap}

/* detail panel */
.panel{position:sticky;top:12px;background:var(--raised);border:1px solid var(--line);box-shadow:var(--shadow);
  padding:18px;min-width:0;max-height:calc(100vh - 24px);overflow:auto}
@media (max-width:980px){ .panel{position:static;max-height:none} }
.panel .pid{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.1em;color:var(--ink-3)}
.panel h2{font-size:21px;line-height:1.18;letter-spacing:-.02em;margin:7px 0 0;font-weight:600;text-wrap:balance}
.panel .desc{color:var(--ink-2);margin:12px 0 0;font-size:14px}
.dl{margin:16px 0 0;border-top:1px solid var(--line)}
.dl div{display:grid;grid-template-columns:76px 1fr;gap:10px;padding:9px 0;border-bottom:1px solid var(--line);
  font-size:13px;min-width:0}
.dl dt{font-family:var(--f-mono);font-size:10px;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-3);padding-top:2px}
.dl dd{margin:0;min-width:0;overflow-wrap:anywhere}
.where{display:flex;flex-direction:column;gap:7px}
.where b{font-family:var(--f-mono);font-size:10px;letter-spacing:.07em;color:var(--ink-3);display:block}
.ops{margin:16px 0 0;border-top:1px solid var(--line);padding-top:13px}
.ops h3,.mref h3{margin:0 0 9px;font-family:var(--f-mono);font-size:10px;letter-spacing:.11em;text-transform:uppercase;
  color:var(--ink-3);font-weight:600;display:flex;justify-content:space-between;gap:8px}
.ops h3 em{font-style:normal;color:var(--ink-4)}
.ops ol{list-style:none;margin:0;padding:0;counter-reset:o}
.ops li{counter-increment:o;position:relative;padding:5px 0 5px 24px;font-size:13px;color:var(--ink-2);
  border-bottom:1px dotted var(--line);line-height:1.42}
.ops li:last-child{border-bottom:0}
.ops li::before{content:counter(o,decimal-leading-zero);position:absolute;left:0;top:6px;
  font-family:var(--f-mono);font-size:9.5px;color:var(--ink-4)}
.flag{border-left:2px solid var(--solid);padding:8px 0 8px 11px;margin-top:14px;font-size:13px;color:var(--ink-2);
  background:var(--surface)}
.mref{margin-top:16px;border-top:1px solid var(--line);padding-top:13px}
.rel{display:flex;flex-wrap:wrap;gap:5px;margin-top:7px}
.rel button{background:var(--surface);border:1px solid var(--line);border-radius:1px;padding:4px 8px;cursor:pointer;
  font-size:12px;color:var(--ink-2);text-align:left}
.rel button:hover{border-color:var(--solid);color:var(--ink)}
.empty{color:var(--ink-3);font-size:13.5px}
.empty h2{color:var(--ink)}

/* manuals */
.mans{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:1px;background:var(--line);
  border:1px solid var(--line)}
.man{background:var(--bg);padding:16px;display:flex;flex-direction:column;gap:10px;min-width:0}
.man .mt{display:flex;justify-content:space-between;gap:10px;align-items:flex-start}
.man h3{margin:0;font-size:15.5px;font-weight:600;letter-spacing:-.01em;line-height:1.25}
.man .mid{font-family:var(--f-mono);font-size:10px;color:var(--ink-4);letter-spacing:.08em;flex:none}
.man p{margin:0;font-size:13.5px;color:var(--ink-2)}
.meta{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.pill{font-family:var(--f-mono);font-size:9.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3);
  border:1px solid var(--line);padding:2px 6px;white-space:nowrap}
.pill.k{background:var(--solid);color:var(--on-solid);border-color:var(--solid)}
.acts{display:flex;flex-wrap:wrap;gap:7px;margin-top:auto}
.dl-btn{display:inline-flex;align-items:center;gap:7px;background:var(--solid);color:var(--on-solid);border:0;
  padding:8px 12px;cursor:pointer;font-family:var(--f-mono);font-size:11px;letter-spacing:.08em;
  text-transform:uppercase;text-decoration:none;align-self:flex-start}
.dl-btn:hover{opacity:.84}
.dl-btn.ghost{background:none;color:var(--ink-2);border:1px solid var(--line-2)}
.dl-btn.ghost:hover{border-color:var(--solid);color:var(--ink);opacity:1}

/* overlaps */
.ovl{border:1px solid var(--line);border-bottom:0;min-width:0}
.ov{border-bottom:1px solid var(--line);background:var(--bg)}
.ovh{width:100%;background:none;border:0;display:flex;gap:12px;align-items:center;padding:13px 14px;cursor:pointer;
  text-align:left;min-width:0}
.ovh:hover{background:var(--surface)}
.ovh .ovn{font-weight:500;flex:1 1 auto;min-width:0;font-size:14.5px}
.ovb{padding:0 14px 14px;font-size:13.5px;color:var(--ink-2)}

/* menus */
.menus{display:grid;grid-template-columns:repeat(auto-fit,minmax(252px,1fr));gap:16px;min-width:0}
.menu{border:1px solid var(--line);padding:15px;min-width:0}
.menu h3{margin:0 0 11px;font-size:13px;font-family:var(--f-mono);letter-spacing:.09em;text-transform:uppercase;
  border-bottom:1px solid var(--solid);padding-bottom:8px;font-weight:600}
.menu ol{list-style:none;margin:0;padding:0;counter-reset:m}
.menu li{counter-increment:m;position:relative;padding:5px 0 5px 26px;font-size:13.5px;border-bottom:1px dotted var(--line)}
.menu li:last-child{border-bottom:0}
.menu li::before{content:counter(m,decimal-leading-zero);position:absolute;left:0;top:6px;font-family:var(--f-mono);
  font-size:9.5px;color:var(--ink-4)}
.steps{border:1px solid var(--line);min-width:0;overflow-x:auto}
.steps table{border-collapse:collapse;width:100%;font-size:13.5px;min-width:420px}
.steps th{background:var(--solid);color:var(--on-solid);text-align:left;padding:9px 11px;font-family:var(--f-mono);
  font-size:10px;letter-spacing:.1em;text-transform:uppercase;font-weight:600}
.steps td{padding:8px 11px;border-bottom:1px solid var(--line);color:var(--ink-2)}
.steps .n{font-family:var(--f-mono);color:var(--ink-4);font-size:11.5px;width:38px}
.hint{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-4);margin:0}
footer{border-top:1px solid var(--line);padding-block:20px 34px;color:var(--ink-3);font-size:12.5px}
footer a{color:var(--ink-2)}
@media (prefers-reduced-motion:reduce){ *{transition:none!important} }
</style>
</head>
<body>
<div class="wrap">
<header>
  <div class="top">
    <div>
      <div class="eyebrow">Contineo SIMS &nbsp;/&nbsp; ncet-sims &nbsp;/&nbsp; internal requirement capture</div>
      <h1>Every function, and the login it lives in.</h1>
      <p class="tagline">Click any capability to see what it does, where it sits in the menus, which of the seven
      logins expose it, and every operation available once you are there. Built from the walkthrough recordings
      and the nineteen Contineo user manuals.</p>
    </div>
    <div class="theme" role="group" aria-label="Colour theme">
      <button data-th="light" title="Light" aria-pressed="false"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M19.1 4.9l-1.4 1.4M6.3 17.7l-1.4 1.4"/></svg></button>
      <button data-th="auto" title="Match system" aria-pressed="true"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2.5" y="4" width="19" height="13" rx="1.5"/><path d="M8 20h8"/></svg></button>
      <button data-th="dark" title="Dark" aria-pressed="false"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5z"/></svg></button>
    </div>
  </div>
  <div class="stats" id="stats"></div>
</header>

<div class="tabs" role="tablist">
  <button class="tab" role="tab" id="t-atlas" aria-selected="true" aria-controls="v-atlas">Capabilities <small id="n1"></small></button>
  <button class="tab" role="tab" id="t-manuals" aria-selected="false" aria-controls="v-manuals">Manuals <small id="n4"></small></button>
  <button class="tab" role="tab" id="t-overlaps" aria-selected="false" aria-controls="v-overlaps">Repeated <small id="n2"></small></button>
  <button class="tab" role="tab" id="t-menus" aria-selected="false" aria-controls="v-menus">Menus <small id="n3"></small></button>
</div>

<section id="v-atlas" role="tabpanel" aria-labelledby="t-atlas">
  <div class="bar">
    <div class="search">
      <svg width="14" height="14" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>
      <input id="q" type="search" placeholder="Search capabilities, operations, menus&hellip;" aria-label="Search">
    </div>
    <div class="seg" role="group" aria-label="Filter by login" id="lgseg"></div>
    <select id="cat" aria-label="Filter by category"><option value="">All categories</option></select>
    <select id="shared" aria-label="Filter by sharing">
      <option value="">Shared or not</option>
      <option value="multi">Shared across logins</option>
      <option value="all3">In three or more logins</option>
      <option value="solo">Unique to one login</option>
      <option value="unused">Present but unused</option>
    </select>
    <select id="src" aria-label="Filter by source">
      <option value="">Any source</option>
      <option value="video">Seen in a recording</option>
      <option value="manual">From a manual only</option>
      <option value="both">Both</option>
      <option value="hasman">Has a manual</option>
    </select>
    <button class="reset" id="reset" type="button">Clear</button>
    <div class="count" id="count"></div>
  </div>
  <div class="cols">
    <div class="grid" id="grid"></div>
    <aside class="panel" id="panel" aria-live="polite"></aside>
  </div>
</section>

<section id="v-manuals" role="tabpanel" aria-labelledby="t-manuals" hidden>
  <div class="bar"><p class="hint" id="manhint">Nineteen manuals &middot; 387 pages &middot; every step folded into the capabilities above</p></div>
  <div class="cols">
    <div class="mans" id="mans"></div>
    <aside class="panel" id="panel3" aria-live="polite"></aside>
  </div>
</section>

<section id="v-overlaps" role="tabpanel" aria-labelledby="t-overlaps" hidden>
  <div class="bar"><p class="hint">Where the same job is done in more than one place</p></div>
  <div class="cols">
    <div class="ovl" id="ovl"></div>
    <aside class="panel" id="panel2" aria-live="polite"></aside>
  </div>
</section>

<section id="v-menus" role="tabpanel" aria-labelledby="t-menus" hidden>
  <div class="bar"><p class="hint">Transcribed from the screen &mdash; spelling as the product shows it</p></div>
  <div style="padding-bottom:26px">
    <div class="menus" id="menus"></div>
    <h3 style="font-size:13px;font-family:var(--f-mono);letter-spacing:.09em;text-transform:uppercase;margin:26px 0 11px">Term setup activities</h3>
    <div class="steps"><table><thead><tr><th class="n">#</th><th>Activity</th><th style="width:150px">Responsibility</th></tr></thead><tbody id="steps"></tbody></table></div>
  </div>
</section>

<footer>
  Internal requirement capture for Nagarjuna College of Engineering and Technology. Seven logins mapped;
  Admission and Examination remain outside every walkthrough.
  The Contineo user manuals are the vendor's confidential documents and are <strong>not</strong> republished here &mdash;
  only what they describe, in our own words.
</footer>
</div>

<script>
const D = __DATA__;
const LOCAL = __LOCAL__;   /* true only in the copy that sits in the same folder as the PDFs */
const LOGINS = ["DC","FAC","HOD","SPOC","CNS","SP","IQAC"];
const LNAME = {DC:"Department Coordinator",FAC:"Faculty / Staff",HOD:"HOD",SPOC:"SPOC",
               CNS:"Counsellor",SP:"Student / Parent portal",IQAC:"IQAC Head"};
const LSHORT = {DC:"DC",FAC:"FAC",HOD:"HOD",SPOC:"SPOC",CNS:"CNS",SP:"S/P",IQAC:"IQAC"};
const STAT = {live:["\u25cf","Live"],partial:["\u25d0","Partial"],unused:["\u25cb","Present, unused"],
              listed:["\u25b3","Listed only \u2014 screen not shown"]};
const SRC = {video:"Seen in a recording",manual:"Documented in a manual",both:"Recording and manual"};
const F = D.features, M = D.manuals || [], byid = {}, byman = {};
F.forEach(f => byid[f.id] = f);
M.forEach(m => byman[m.id] = m);
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

/* ── theme ─────────────────────────── */
const root = document.documentElement;
function setTheme(t){
  root.setAttribute("data-theme", t);
  try { localStorage.setItem("atlas-theme", t); } catch(e) {}
  document.querySelectorAll(".theme button").forEach(b =>
    b.setAttribute("aria-pressed", b.dataset.th === t ? "true" : "false"));
}
try { const s = localStorage.getItem("atlas-theme"); if (s) setTheme(s); } catch(e) {}
document.querySelectorAll(".theme button").forEach(b =>
  b.onclick = () => setTheme(b.dataset.th));

/* ── stats ─────────────────────────── */
const ops = f => (f.ops || []).length;
const totalOps = F.reduce((a,f) => a + ops(f), 0);
const touch = F.reduce((a,f) => a + f.logins.length, 0);
const menuN = Object.values(D.menus).reduce((a,m) => a + m.items.length, 0);
document.getElementById("stats").innerHTML = [
  [F.length,"Capabilities"],[totalOps,"Operations"],[7,"Logins mapped"],[touch,"Login touchpoints"],
  [M.length,"User manuals"],[M.reduce((a,m)=>a+m.pages,0),"Manual pages"],
  [D.duplicates.length,"Overlap groups"],[menuN,"Menu entries"]
].map(([n,l]) => `<div class="stat"><b>${n}</b><span>${l}</span></div>`).join("");
document.getElementById("n1").textContent = F.length;
document.getElementById("n2").textContent = D.duplicates.length;
document.getElementById("n3").textContent = Object.keys(D.menus).length;
document.getElementById("n4").textContent = M.length;

/* ── filters ───────────────────────── */
document.getElementById("lgseg").innerHTML = LOGINS.map(l =>
  `<button data-lg="${l}" aria-pressed="false" title="${esc(LNAME[l])}">${LSHORT[l]}</button>`).join("");
const cats = [...new Set(F.map(f => f.cat))].sort();
document.getElementById("cat").insertAdjacentHTML("beforeend",
  cats.map(c => `<option>${esc(c)}</option>`).join(""));

let state = {q:"", lg:new Set(), cat:"", shared:"", src:"", sel:null, selMan:null};

function match(f){
  if (state.lg.size && ![...state.lg].every(l => f.logins.includes(l))) return false;
  if (state.cat && f.cat !== state.cat) return false;
  if (state.shared === "multi" && f.logins.length < 2) return false;
  if (state.shared === "all3" && f.logins.length < 3) return false;
  if (state.shared === "solo" && f.logins.length !== 1) return false;
  if (state.shared === "unused" && f.status !== "unused") return false;
  if (state.src === "hasman") { if (!(f.man || []).length) return false; }
  else if (state.src && f.src !== state.src) return false;
  if (state.q){
    const hay = [f.id,f.name,f.cat,f.desc,f.note||"",(f.ops||[]).join(" "),
                 Object.values(f.path||{}).join(" "),(f.man||[]).map(i=>byman[i]?byman[i].title:"").join(" ")]
                .join(" ").toLowerCase();
    if (!hay.includes(state.q.toLowerCase())) return false;
  }
  return true;
}

function chips(f){
  return `<span class="chipset">${LOGINS.map(l =>
    `<span class="chip ${f.logins.includes(l)?"on":""}">${LSHORT[l]}</span>`).join("")}</span>`;
}

function renderGrid(){
  const list = F.filter(match);
  document.getElementById("grid").innerHTML = list.length ? list.map(f => `
    <button class="card" data-id="${f.id}" aria-current="${state.sel===f.id}">
      <div class="ctop"><span class="cid">${f.id}</span>
        <span class="st ${f.status}" title="${esc(STAT[f.status][1])}">${STAT[f.status][0]}</span></div>
      <div class="cname">${esc(f.name)}</div>
      <div class="cbot"><span class="ccat">${esc(f.cat)}</span>
        <span style="display:flex;gap:4px;align-items:center">
        ${(f.man||[]).length?`<span class="mrk" title="Documented in ${(f.man||[]).length} manual(s)">\u00a7${(f.man||[]).length}</span>`:""}
        <span class="opn">${ops(f)} ops</span></span></div>
      ${chips(f)}
    </button>`).join("")
    : `<div style="padding:30px;background:var(--bg)" class="empty">Nothing matches those filters.</div>`;
  document.getElementById("count").textContent =
    `${list.length} of ${F.length} \u00b7 ${list.reduce((a,f)=>a+ops(f),0)} operations`;
  document.querySelectorAll(".card").forEach(c =>
    c.onclick = () => { state.sel = c.dataset.id; renderGrid(); renderPanel(); });
}

function manLink(id){
  const m = byman[id]; if (!m) return "";
  return `<button data-man="${id}">\u00a7 ${esc(m.title)}</button>`;
}

function renderPanel(){
  const p = document.getElementById("panel");
  const f = byid[state.sel];
  if (!f){ p.innerHTML = `<div class="empty"><h2 style="margin:0 0 8px;font-size:18px">Pick a capability</h2>
    Every card opens the full record: what the screen does, the path to it in each login that has it,
    every operation available there, and which user manual documents it.</div>`; return; }
  const rel = F.filter(o => o.id !== f.id && (
      (f.dup && o.dup === f.dup) || (o.cat === f.cat && o.logins.some(l => f.logins.includes(l)))
    )).slice(0,6);
  p.innerHTML = `
    <div class="pid">${f.id} &nbsp;\u00b7&nbsp; ${esc(STAT[f.status][1])}</div>
    <h2>${esc(f.name)}</h2>
    <p class="desc">${esc(f.desc)}</p>
    <dl class="dl">
      <div><dt>Category</dt><dd>${esc(f.cat)}</dd></div>
      <div><dt>Logins</dt><dd>${chips(f)}</dd></div>
      <div><dt>Where</dt><dd class="where">${f.logins.map(l =>
        `<span><b>${esc(LNAME[l])}</b>${esc((f.path||{})[l] || "\u2014")}</span>`).join("")}</dd></div>
      <div><dt>Source</dt><dd>${esc(SRC[f.src] || f.src)}</dd></div>
    </dl>
    ${(f.ops||[]).length ? `<div class="ops"><h3>What you can do here <em>${ops(f)}</em></h3>
      <ol>${f.ops.map(o => `<li>${esc(o)}</li>`).join("")}</ol></div>` : ""}
    ${f.note ? `<div class="flag">${esc(f.note)}</div>` : ""}
    ${(f.man||[]).length ? `<div class="mref"><h3>Documented in</h3>
      <div class="rel">${f.man.map(manLink).join("")}</div></div>` : ""}
    ${rel.length ? `<div class="mref"><h3>Related</h3>
      <div class="rel">${rel.map(o => `<button data-id="${o.id}">${esc(o.name)}</button>`).join("")}</div></div>` : ""}`;
  wire(p);
}

function wire(el){
  el.querySelectorAll("[data-id]").forEach(b => b.onclick = () => {
    show("atlas"); state.sel = b.dataset.id; renderGrid(); renderPanel();
    document.getElementById("v-atlas").scrollIntoView({block:"start"});
  });
  el.querySelectorAll("[data-man]").forEach(b => b.onclick = () => {
    show("manuals"); state.selMan = b.dataset.man; renderMans(); renderManPanel();
  });
}

/* ── manuals ───────────────────────── */
document.getElementById("manhint").innerHTML = LOCAL
  ? "Nineteen manuals · 387 pages · <strong>Open the PDF</strong> works because this copy sits in the same folder as the files"
  : "Nineteen manuals · 387 pages · the PDFs are Contineo's and are not served here — every step they describe is in the capabilities";
function renderMans(){
  document.getElementById("mans").innerHTML = M.map(m => `
    <div class="man">
      <div class="mt"><h3>${esc(m.title)}</h3><span class="mid">${m.id}</span></div>
      <div class="meta">
        <span class="pill">${m.pages} pages</span>
        ${m.logins.map(l => `<span class="pill k">${LSHORT[l]}</span>`).join("")}
        <span class="pill">${m.covers.length} capabilities</span>
        ${m.conf ? `<span class="pill">Vendor confidential</span>` : ""}
      </div>
      <p>${esc(m.sum)}</p>
      <div class="acts">
        ${LOCAL ? `<a class="dl-btn" href="${encodeURIComponent(m.file)}" target="_blank" rel="noopener">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 3v12M7 11l5 5 5-5M4 20h16"/></svg>
          Open the PDF</a>` : ""}
        <button class="dl-btn ghost" data-man="${m.id}">What it covers \u2192</button>
      </div>
    </div>`).join("");
  document.querySelectorAll("#mans [data-man]").forEach(b => b.onclick = () => {
    state.selMan = b.dataset.man; renderManPanel();
  });
}

function renderManPanel(){
  const p = document.getElementById("panel3");
  const m = byman[state.selMan];
  if (!m){ p.innerHTML = `<div class="empty"><h2 style="margin:0 0 8px;font-size:18px">Pick a manual</h2>
    Each one lists the capabilities it documents. The PDFs themselves are Contineo's confidential
    documents and are not published here \u2014 open your local copy, or ask the vendor for consent to host them.</div>`;
    return; }
  p.innerHTML = `
    <div class="pid">${m.id} &nbsp;\u00b7&nbsp; ${m.pages} pages</div>
    <h2>${esc(m.title)}</h2>
    <p class="desc">${esc(m.sum)}</p>
    <dl class="dl">
      <div><dt>Logins</dt><dd>${m.logins.map(l => esc(LNAME[l])).join(", ")}</dd></div>
      <div><dt>File</dt><dd><code style="font-family:var(--f-mono);font-size:12px">${esc(m.file)}</code></dd></div>
      <div><dt>Status</dt><dd>${m.conf
        ? "Carries a Contineo confidentiality notice \u2014 not republished"
        : "No confidentiality notice found, still not republished"}</dd></div>
    </dl>
    ${LOCAL ? `<a class="dl-btn" style="margin-top:14px" href="${encodeURIComponent(m.file)}" target="_blank" rel="noopener">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 3v12M7 11l5 5 5-5M4 20h16"/></svg>
      Open the PDF</a>`
    : `<div class="flag" style="margin-top:14px">The PDF is not served from this site. Open your own copy of
       <strong>${esc(m.file)}</strong>, or use the offline build of this page, which sits in the same folder as
       the manuals and opens them directly.</div>`}
    <div class="mref"><h3>Capabilities it documents <em></em></h3>
      <div class="rel">${m.covers.filter(i => byid[i]).map(i =>
        `<button data-id="${i}">${esc(byid[i].name)}</button>`).join("")}</div></div>
    <div class="flag">Every step in this manual is folded into those capabilities &mdash; open one to read the
    operations in order.</div>`;
  wire(p);
}

/* ── overlaps ──────────────────────── */
document.getElementById("ovl").innerHTML = D.duplicates.map((d,i) => `
  <div class="ov">
    <button class="ovh" data-ov="${i}">
      <span class="ovn">${esc(d.label)}</span>
      <span class="chipset">${LOGINS.map(l =>
        `<span class="chip ${d.logins.includes(l)?"on":""}">${LSHORT[l]}</span>`).join("")}</span>
      <span class="pill">${d.ids.length}</span>
    </button>
    <div class="ovb" hidden>
      <p style="margin:0 0 4px">${esc(d.note||"")}</p>
      <div class="rel">${d.ids.filter(i => byid[i]).map(i =>
        `<button data-id="${i}">${esc(byid[i].name)}</button>`).join("")}</div>
    </div>
  </div>`).join("");
document.querySelectorAll("[data-ov]").forEach(b => b.onclick = () => {
  const body = b.nextElementSibling; body.hidden = !body.hidden; wire(body);
});

/* ── menus ─────────────────────────── */
document.getElementById("menus").innerHTML = Object.entries(D.menus).map(([k,m]) => `
  <div class="menu"><h3>${esc(m.label)}</h3>
    <ol>${m.items.map(it => `<li>${esc(it)}</li>`).join("")}</ol></div>`).join("");
document.getElementById("steps").innerHTML = (D.termsetup||[]).map(s =>
  `<tr><td class="n">${s.n}</td><td>${esc(s.act)}</td><td>${esc(s.by)}</td></tr>`).join("");

/* ── tabs ──────────────────────────── */
function show(name){
  ["atlas","manuals","overlaps","menus"].forEach(n => {
    document.getElementById("v-"+n).hidden = n !== name;
    document.getElementById("t-"+n).setAttribute("aria-selected", n === name);
  });
}
document.querySelectorAll(".tab").forEach(t =>
  t.onclick = () => show(t.id.slice(2)));

/* ── bind ──────────────────────────── */
document.getElementById("q").oninput = e => { state.q = e.target.value; renderGrid(); };
document.getElementById("cat").onchange = e => { state.cat = e.target.value; renderGrid(); };
document.getElementById("shared").onchange = e => { state.shared = e.target.value; renderGrid(); };
document.getElementById("src").onchange = e => { state.src = e.target.value; renderGrid(); };
document.querySelectorAll("[data-lg]").forEach(b => b.onclick = () => {
  const l = b.dataset.lg;
  state.lg.has(l) ? state.lg.delete(l) : state.lg.add(l);
  b.setAttribute("aria-pressed", state.lg.has(l));
  renderGrid();
});
document.getElementById("reset").onclick = () => {
  state = {q:"",lg:new Set(),cat:"",shared:"",src:"",sel:state.sel,selMan:state.selMan};
  document.getElementById("q").value = "";
  ["cat","shared","src"].forEach(i => document.getElementById(i).value = "");
  document.querySelectorAll("[data-lg]").forEach(b => b.setAttribute("aria-pressed","false"));
  renderGrid();
};

renderGrid(); renderPanel(); renderMans(); renderManPanel();
</script>
</body>
</html>
"""

io.open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(
    HTML.replace("__DATA__", DATA).replace("__LOCAL__", "true" if LOCAL else "false"))
print("site written:", os.path.join(OUT, "index.html"), len(HTML) + len(DATA), "bytes")
