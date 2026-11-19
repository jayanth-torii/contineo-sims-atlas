# -*- coding: utf-8 -*-
"""Build the Contineo SIMS Atlas site from features.json.

    python build/site.py [outdir] [--local]

--local emits the copy that sits beside the PDFs, with working manual links.
"""
import json, io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = [a for a in sys.argv[1:] if a != "--local"]
LOCAL = "--local" in sys.argv
OUT = args[0] if args else ROOT
D = json.load(io.open(os.path.join(ROOT, "features.json"), encoding="utf-8"))
os.makedirs(OUT, exist_ok=True)
DATA = json.dumps(D, ensure_ascii=False, separators=(",", ":"))

HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Contineo SIMS Atlas</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="Every function in the Contineo SIMS student ERP, the login it lives in, and what you can do there.">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><rect width='16' height='16' fill='%230b0b0a'/><rect x='3' y='3.5' width='10' height='1.6' fill='%23fff'/><rect x='3' y='7.2' width='10' height='1.6' fill='%23fff'/><rect x='3' y='10.9' width='6' height='1.6' fill='%238a8a86'/></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Serif:ital,wght@0,400;1,400&display=swap">
<style>
/* Layout: a scannable index of 154 capabilities on the left, one always-populated
   reading pane on the right. Monochrome, warm-biased neutrals. Three type roles:
   sans for the interface, serif for prose, mono for data and short labels. */
:root{
  --paper:#ffffff; --sunk:#f5f5f3; --raise:#ffffff; --ink:#0b0b0a; --ink-2:#383835;
  --ink-3:#6b6b66; --ink-4:#9a9a94; --rule:#e2e2dd; --rule-2:#c6c6c0;
  --mark:#0b0b0a; --on-mark:#ffffff;
  --f-ui:"IBM Plex Sans",ui-sans-serif,system-ui,-apple-system,sans-serif;
  --f-read:"IBM Plex Serif",ui-serif,Georgia,serif;
  --f-data:"IBM Plex Mono",ui-monospace,"Cascadia Mono",Consolas,monospace;
  color-scheme:light;
}
@media (prefers-color-scheme:dark){ :root:not([data-theme="light"]){
  --paper:#0b0b0a; --sunk:#151513; --raise:#111110; --ink:#f5f5f2; --ink-2:#cbcbc5;
  --ink-3:#95958f; --ink-4:#6a6a65; --rule:#272725; --rule-2:#3b3b38;
  --mark:#f5f5f2; --on-mark:#0b0b0a; color-scheme:dark; } }
:root[data-theme="light"]{
  --paper:#ffffff; --sunk:#f5f5f3; --raise:#ffffff; --ink:#0b0b0a; --ink-2:#383835;
  --ink-3:#6b6b66; --ink-4:#9a9a94; --rule:#e2e2dd; --rule-2:#c6c6c0;
  --mark:#0b0b0a; --on-mark:#ffffff; color-scheme:light; }
:root[data-theme="dark"]{
  --paper:#0b0b0a; --sunk:#151513; --raise:#111110; --ink:#f5f5f2; --ink-2:#cbcbc5;
  --ink-3:#95958f; --ink-4:#6a6a65; --rule:#272725; --rule-2:#3b3b38;
  --mark:#f5f5f2; --on-mark:#0b0b0a; color-scheme:dark; }

*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--f-ui);font-size:15px;
  line-height:1.5;-webkit-font-smoothing:antialiased}
.wrap{max-width:1380px;margin:0 auto;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
button{font:inherit;color:inherit;background:none;border:0}
:focus-visible{outline:2px solid var(--mark);outline-offset:2px}
.lbl{font-family:var(--f-data);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3)}
.num{font-variant-numeric:tabular-nums}

/* ── masthead ───────────────────────────────────────── */
header{padding-block:30px 0}
.head{display:flex;justify-content:space-between;align-items:flex-start;gap:24px;flex-wrap:wrap}
.brand{max-width:40ch}
h1{font-size:clamp(26px,4.2vw,37px);line-height:1.06;letter-spacing:-.028em;margin:9px 0 0;font-weight:600;
  text-wrap:balance}
.sub{font-family:var(--f-read);font-size:15px;line-height:1.55;color:var(--ink-2);margin:11px 0 0;max-width:58ch}
.theme{display:flex;border:1px solid var(--rule);flex:none}
.theme button{border-right:1px solid var(--rule);padding:7px 9px;cursor:pointer;display:grid;place-items:center;
  color:var(--ink-3)}
.theme button:last-child{border-right:0}
.theme button[aria-pressed="true"]{background:var(--mark);color:var(--on-mark)}
.theme button:hover:not([aria-pressed="true"]){color:var(--ink)}

.figs{display:flex;flex-wrap:wrap;gap:0;margin-top:26px;border-top:1px solid var(--ink);
  border-bottom:1px solid var(--rule)}
.fig{padding:13px 26px 13px 0;margin-right:26px;border-right:1px solid var(--rule)}
.fig:last-child{border-right:0;margin-right:0;padding-right:0}
.fig b{display:block;font-size:27px;line-height:1;letter-spacing:-.035em;font-weight:600;
  font-variant-numeric:tabular-nums}
.fig span{display:block;margin-top:6px}

/* ── tabs ───────────────────────────────────────────── */
nav.tabs{display:flex;gap:28px;border-bottom:1px solid var(--rule);margin-top:0;overflow-x:auto;
  scrollbar-width:none}
nav.tabs::-webkit-scrollbar{display:none}
.tab{padding:14px 0 12px;cursor:pointer;color:var(--ink-3);font-weight:500;white-space:nowrap;
  border-bottom:2px solid transparent;margin-bottom:-1px}
.tab[aria-selected="true"]{color:var(--ink);border-bottom-color:var(--mark)}
.tab b{font-family:var(--f-data);font-size:11px;font-weight:500;color:var(--ink-4);margin-left:7px;
  font-variant-numeric:tabular-nums}

/* ── toolbar ────────────────────────────────────────── */
.tools{display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding-block:14px;
  position:sticky;top:env(safe-area-inset-top,0px);background:var(--paper);z-index:5;
  border-bottom:1px solid var(--rule)}
.find{flex:1 1 230px;min-width:0;position:relative}
.find input{width:100%;background:var(--sunk);border:1px solid var(--rule);padding:9px 11px 9px 33px;
  color:var(--ink);font:inherit;font-size:14px}
.find input::placeholder{color:var(--ink-4)}
.find svg{position:absolute;left:11px;top:50%;transform:translateY(-50%);stroke:var(--ink-4);fill:none;
  stroke-width:2.2}
.logins{display:flex;border:1px solid var(--rule);flex-wrap:wrap}
.logins button{border-right:1px solid var(--rule);padding:9px 11px;cursor:pointer;font-family:var(--f-data);
  font-size:11px;letter-spacing:.07em;color:var(--ink-3)}
.logins button:last-child{border-right:0}
.logins button[aria-pressed="true"]{background:var(--mark);color:var(--on-mark)}
.logins button:hover:not([aria-pressed="true"]){color:var(--ink);background:var(--sunk)}
select{background:var(--sunk);border:1px solid var(--rule);padding:9px 9px;color:var(--ink);font:inherit;
  font-size:13.5px;max-width:100%}
.clear{border:1px solid var(--rule);padding:9px 12px;cursor:pointer;font-family:var(--f-data);font-size:11px;
  letter-spacing:.07em;color:var(--ink-3)}
.clear:hover{border-color:var(--rule-2);color:var(--ink)}
.tally{margin-left:auto;font-family:var(--f-data);font-size:11.5px;color:var(--ink-3);white-space:nowrap;
  font-variant-numeric:tabular-nums}

/* ── two-pane ───────────────────────────────────────── */
.panes{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,452px);gap:30px;align-items:start;
  padding-bottom:64px}
@media (max-width:1020px){
  .panes{grid-template-columns:1fr;gap:22px}
  .read{order:-1;position:static!important;max-height:none!important}
}

/* ── the index ──────────────────────────────────────── */
.group{margin-top:22px}
.group:first-child{margin-top:8px}
.group > h2{display:flex;align-items:baseline;gap:9px;margin:0 0 2px;padding-bottom:7px;
  border-bottom:1px solid var(--ink);font-size:13px;font-weight:600;letter-spacing:.02em}
.group > h2 i{font-style:normal;font-family:var(--f-data);font-size:11px;color:var(--ink-4);font-weight:400}
.row{display:grid;grid-template-columns:40px minmax(0,1fr) auto auto;gap:12px;align-items:baseline;width:100%;
  text-align:left;padding:9px 8px 9px 0;cursor:pointer;border-bottom:1px solid var(--rule)}
.row:hover{background:var(--sunk)}
.row[aria-current="true"]{background:var(--mark);color:var(--on-mark);padding-left:8px}
.row[aria-current="true"] .rid,.row[aria-current="true"] .tag,.row[aria-current="true"] .rops{
  color:var(--on-mark);opacity:.74;border-color:currentColor}
.rid{font-family:var(--f-data);font-size:11px;color:var(--ink-4);letter-spacing:.03em}
.rname{font-size:14.5px;line-height:1.35;min-width:0;letter-spacing:-.006em}
.rname u{text-decoration:none;background:var(--rule-2);color:var(--ink);padding:0 1px}
.row[aria-current="true"] .rname u{background:var(--on-mark);color:var(--mark)}
.dot{display:inline-block;margin-left:6px;font-size:10px;color:var(--ink-4);vertical-align:1px}
.tags{display:flex;gap:4px;flex-wrap:wrap;justify-content:flex-end}
.tag{font-family:var(--f-data);font-size:9.5px;letter-spacing:.06em;color:var(--ink-3);border:1px solid var(--rule-2);
  padding:1px 4px;white-space:nowrap}
.tag.more{border-style:dashed}
.rops{font-family:var(--f-data);font-size:11px;color:var(--ink-4);font-variant-numeric:tabular-nums;
  min-width:44px;text-align:right}
.none{padding:34px 0;color:var(--ink-3);font-family:var(--f-read)}

/* ── the reading pane ───────────────────────────────── */
.read{position:sticky;top:calc(env(safe-area-inset-top,0px) + 70px);background:var(--raise);
  border:1px solid var(--rule);padding:22px;max-height:calc(100vh - 96px);overflow:auto}
.eyebrow{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.read h2{font-size:24px;line-height:1.14;letter-spacing:-.022em;margin:10px 0 0;font-weight:600;
  text-wrap:balance}
.lead{font-family:var(--f-read);font-size:15.5px;line-height:1.6;color:var(--ink-2);margin:13px 0 0}
.block{margin-top:22px;border-top:1px solid var(--rule);padding-top:14px}
.block > h3{margin:0 0 11px;display:flex;justify-content:space-between;align-items:baseline;gap:10px}
.block > h3 i{font-style:normal;font-family:var(--f-data);font-size:11px;color:var(--ink-4);
  font-variant-numeric:tabular-nums}
.paths{display:flex;flex-direction:column;gap:11px}
.path{display:grid;grid-template-columns:62px minmax(0,1fr);gap:11px;align-items:baseline}
.path code{font-family:var(--f-data);font-size:12.5px;color:var(--ink-2);overflow-wrap:anywhere;line-height:1.45}
.path span{font-family:var(--f-data);font-size:9.5px;letter-spacing:.06em;color:var(--on-mark);
  background:var(--mark);padding:2px 0;text-align:center}
ol.steps{list-style:none;margin:0;padding:0;counter-reset:s}
ol.steps li{counter-increment:s;display:grid;grid-template-columns:24px minmax(0,1fr);gap:9px;
  padding:6px 0;border-bottom:1px dotted var(--rule);font-size:13.5px;color:var(--ink-2);line-height:1.45}
ol.steps li:last-child{border-bottom:0}
ol.steps li::before{content:counter(s,decimal-leading-zero);font-family:var(--f-data);font-size:10.5px;
  color:var(--ink-4);padding-top:2px}
.caution{margin-top:18px;background:var(--sunk);border-left:2px solid var(--mark);padding:12px 14px;
  font-family:var(--f-read);font-size:14px;line-height:1.55;color:var(--ink-2)}
.chipline{display:flex;flex-wrap:wrap;gap:6px}
.chipline button,.chipline a{border:1px solid var(--rule);padding:6px 9px;cursor:pointer;font-size:12.5px;
  color:var(--ink-2);text-align:left;text-decoration:none}
.chipline button:hover,.chipline a:hover{border-color:var(--mark);color:var(--ink)}
.rest dl{margin:0;display:grid;grid-template-columns:1fr auto auto;gap:0 14px;align-items:baseline}
.rest dt{padding:7px 0;border-bottom:1px solid var(--rule);font-size:13.5px}
.rest dd{margin:0;padding:7px 0;border-bottom:1px solid var(--rule);font-family:var(--f-data);font-size:11.5px;
  color:var(--ink-3);font-variant-numeric:tabular-nums;text-align:right}

/* ── manuals ────────────────────────────────────────── */
.shelf{display:grid;grid-template-columns:repeat(auto-fill,minmax(258px,1fr));gap:18px;margin-top:20px}
.vol{border:1px solid var(--rule);border-top:2px solid var(--ink);padding:16px;display:flex;
  flex-direction:column;gap:9px;min-width:0}
.vol:hover{background:var(--sunk)}
.vol h3{margin:0;font-size:15.5px;font-weight:600;line-height:1.26;letter-spacing:-.012em}
.vol p{margin:0;font-family:var(--f-read);font-size:13.5px;line-height:1.5;color:var(--ink-2)}
.volmeta{display:flex;gap:9px;flex-wrap:wrap;align-items:baseline}
.acts{display:flex;flex-wrap:wrap;gap:7px;margin-top:auto;padding-top:4px}
.go{display:inline-flex;align-items:center;gap:7px;background:var(--mark);color:var(--on-mark);
  padding:8px 12px;cursor:pointer;font-family:var(--f-data);font-size:10.5px;letter-spacing:.09em;
  text-transform:uppercase;text-decoration:none}
.go:hover{opacity:.85}
.go.quiet{background:none;color:var(--ink-2);border:1px solid var(--rule-2)}
.go.quiet:hover{border-color:var(--mark);color:var(--ink);opacity:1}

/* ── overlaps + menus ───────────────────────────────── */
.stack{border-top:1px solid var(--ink);margin-top:20px}
.pair{border-bottom:1px solid var(--rule)}
.pairhead{display:grid;grid-template-columns:minmax(0,1fr) auto auto;gap:14px;align-items:center;width:100%;
  text-align:left;padding:13px 0;cursor:pointer}
.pairhead:hover{color:var(--ink)}
.pairhead strong{font-weight:500;font-size:15px;min-width:0}
.pairbody{padding:0 0 16px;max-width:76ch}
.pairbody p{margin:0 0 10px;font-family:var(--f-read);font-size:14px;line-height:1.55;color:var(--ink-2)}
.cols{columns:2;column-gap:28px;margin-top:20px}
@media (max-width:760px){ .cols{columns:1} }
.card{break-inside:avoid;border:1px solid var(--rule);padding:15px;margin-bottom:18px}
.card h3{margin:0 0 10px;padding-bottom:8px;border-bottom:1px solid var(--ink);font-size:12.5px;
  font-family:var(--f-data);letter-spacing:.08em;text-transform:uppercase;font-weight:600}
.card ol{list-style:none;margin:0;padding:0;counter-reset:n}
.card li{counter-increment:n;display:grid;grid-template-columns:22px minmax(0,1fr);gap:8px;padding:4px 0;
  font-size:13.5px;border-bottom:1px dotted var(--rule)}
.card li:last-child{border-bottom:0}
.card li::before{content:counter(n,decimal-leading-zero);font-family:var(--f-data);font-size:10px;
  color:var(--ink-4);padding-top:3px}
table.seq{border-collapse:collapse;width:100%;margin-top:20px;font-size:13.5px}
table.seq th{background:var(--mark);color:var(--on-mark);text-align:left;padding:9px 11px;font-family:var(--f-data);
  font-size:10px;letter-spacing:.1em;text-transform:uppercase;font-weight:600}
table.seq td{padding:8px 11px;border-bottom:1px solid var(--rule);color:var(--ink-2)}
table.seq td:first-child{font-family:var(--f-data);color:var(--ink-4);width:40px}
.note{font-family:var(--f-read);font-size:14px;color:var(--ink-3);margin:14px 0 0;max-width:72ch;line-height:1.55}
footer{border-top:1px solid var(--rule);padding-block:22px 36px;color:var(--ink-3);font-family:var(--f-read);
  font-size:13.5px;line-height:1.6;max-width:78ch}
@media (prefers-reduced-motion:reduce){ *{transition:none!important} }
</style>
</head>
<body>
<div class="wrap">

<header>
  <div class="head">
    <div class="brand">
      <div class="lbl">Contineo SIMS &nbsp;&middot;&nbsp; ncet-sims.contineo.in</div>
      <h1>Every function, and the login it lives in.</h1>
      <p class="sub">A working index of the student ERP as it actually runs: what each screen does,
      where it sits in the menus, and every operation available once you are there.</p>
    </div>
    <div class="theme" role="group" aria-label="Colour theme">
      <button data-th="light" title="Light" aria-pressed="false"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4.4"/><path d="M12 2v2.2M12 19.8V22M2 12h2.2M19.8 12H22M4.9 4.9l1.6 1.6M17.5 17.5l1.6 1.6M19.1 4.9l-1.6 1.6M6.5 17.5l-1.6 1.6"/></svg></button>
      <button data-th="auto" title="Match the system" aria-pressed="true"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2.6" y="4.2" width="18.8" height="13" rx="1.4"/><path d="M8.5 20.2h7"/></svg></button>
      <button data-th="dark" title="Dark" aria-pressed="false"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 14.6A8.6 8.6 0 0 1 9.4 4 8.6 8.6 0 1 0 20 14.6z"/></svg></button>
    </div>
  </div>
  <div class="figs" id="figs"></div>
</header>

<nav class="tabs" role="tablist">
  <button class="tab" role="tab" id="t-index" aria-selected="true" aria-controls="v-index">Capabilities <b id="c1"></b></button>
  <button class="tab" role="tab" id="t-manuals" aria-selected="false" aria-controls="v-manuals">Manuals <b id="c4"></b></button>
  <button class="tab" role="tab" id="t-repeats" aria-selected="false" aria-controls="v-repeats">Repeated <b id="c2"></b></button>
  <button class="tab" role="tab" id="t-menus" aria-selected="false" aria-controls="v-menus">Menus <b id="c3"></b></button>
</nav>

<section id="v-index" role="tabpanel" aria-labelledby="t-index">
  <div class="tools">
    <div class="find">
      <svg width="14" height="14" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4.2-4.2"/></svg>
      <input id="q" type="search" placeholder="Search names, operations and menu paths" aria-label="Search capabilities">
    </div>
    <div class="logins" role="group" aria-label="Filter by login" id="lg"></div>
    <select id="cat" aria-label="Filter by area"><option value="">Every area</option></select>
    <select id="reach" aria-label="Filter by reach">
      <option value="">Any reach</option>
      <option value="solo">Only one login has it</option>
      <option value="multi">Two or more logins</option>
      <option value="all3">Three or more logins</option>
      <option value="unused">Present but unused</option>
    </select>
    <select id="src" aria-label="Filter by evidence">
      <option value="">Any evidence</option>
      <option value="video">Seen in a recording</option>
      <option value="manual">Only in a manual</option>
      <option value="both">Recording and manual</option>
      <option value="hasman">Has a manual</option>
    </select>
    <button class="clear" id="clear" type="button">Reset</button>
    <div class="tally" id="tally"></div>
  </div>
  <div class="panes">
    <div id="index"></div>
    <aside class="read" id="read" aria-live="polite"></aside>
  </div>
</section>

<section id="v-manuals" role="tabpanel" aria-labelledby="t-manuals" hidden>
  <p class="note" id="manhint"></p>
  <div class="shelf" id="shelf"></div>
</section>

<section id="v-repeats" role="tabpanel" aria-labelledby="t-repeats" hidden>
  <p class="note">Thirty-nine jobs that more than one login can do. Each one is a decision for a rebuild:
  keep the duplication deliberately, or collapse it.</p>
  <div class="stack" id="repeats"></div>
</section>

<section id="v-menus" role="tabpanel" aria-labelledby="t-menus" hidden>
  <p class="note">Every menu, transcribed from the screen, spelling and all &mdash; including
  &ldquo;Calender Of Events&rdquo;, which the product has always misspelt.</p>
  <div class="cols" id="menus"></div>
  <h3 class="lbl" style="margin:28px 0 0">The term setup sequence</h3>
  <table class="seq"><thead><tr><th>#</th><th>Activity</th><th style="width:170px">Owner</th></tr></thead>
  <tbody id="seq"></tbody></table>
</section>

<footer id="foot"></footer>
</div>

<script>
const D = __DATA__;
const LOCAL = __LOCAL__;
const LOGINS = ["DC","FAC","HOD","SPOC","CNS","SP","IQAC"];
const LNAME = {DC:"Department Coordinator",FAC:"Faculty / Staff",HOD:"HOD",SPOC:"SPOC",
               CNS:"Counsellor",SP:"Student / Parent portal",IQAC:"IQAC Head"};
const SHORT = {DC:"DC",FAC:"FAC",HOD:"HOD",SPOC:"SPOC",CNS:"CNS",SP:"S/P",IQAC:"IQAC"};
const STATE = {live:["●","In use"],partial:["◐","Partly built"],
               unused:["○","Present, unused"],listed:["△","Listed, never opened"]};
const EVID = {video:"Seen in a recording",manual:"Documented in a manual only",both:"Recording and manual"};
const F = D.features, M = D.manuals || [];
const byid = {}, byman = {};
F.forEach(f => byid[f.id] = f);
M.forEach(m => byman[m.id] = m);
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const nops = f => (f.ops || []).length;

/* theme ------------------------------------------------ */
const root = document.documentElement;
function theme(t){
  if (t === "auto") root.removeAttribute("data-theme"); else root.setAttribute("data-theme", t);
  try { localStorage.setItem("sims-theme", t); } catch(e) {}
  document.querySelectorAll(".theme button").forEach(b =>
    b.setAttribute("aria-pressed", String(b.dataset.th === t)));
}
let saved = "auto";
try { saved = localStorage.getItem("sims-theme") || "auto"; } catch(e) {}
theme(saved);
document.querySelectorAll(".theme button").forEach(b => b.onclick = () => theme(b.dataset.th));

/* headline figures ------------------------------------- */
const totalOps = F.reduce((a,f) => a + nops(f), 0);
const menuN = Object.values(D.menus).reduce((a,m) => a + m.items.length, 0);
document.getElementById("figs").innerHTML = [
  [F.length,"capabilities"],[totalOps,"operations"],["7","logins"],
  [M.length,"manuals read"],[D.duplicates.length,"repeated jobs"],[menuN,"menu entries"]
].map(([n,l]) => `<div class="fig"><b>${n}</b><span class="lbl">${l}</span></div>`).join("");
document.getElementById("c1").textContent = F.length;
document.getElementById("c2").textContent = D.duplicates.length;
document.getElementById("c3").textContent = Object.keys(D.menus).length;
document.getElementById("c4").textContent = M.length;
document.getElementById("foot").innerHTML =
  `Internal requirement capture for Nagarjuna College of Engineering and Technology, built from three
   walkthrough recordings and ${M.length} Contineo user manuals. Seven logins are mapped; Admission and
   Examination were never issued, so they stay unmapped. The manuals themselves are Contineo’s
   confidential documents and are not republished here.`;

/* filters ---------------------------------------------- */
document.getElementById("lg").innerHTML = LOGINS.map(l =>
  `<button data-lg="${l}" aria-pressed="false" title="${esc(LNAME[l])}">${SHORT[l]}</button>`).join("");
const areas = [...new Set(F.map(f => f.cat))].sort();
document.getElementById("cat").insertAdjacentHTML("beforeend",
  areas.map(c => `<option>${esc(c)}</option>`).join(""));

let S = {q:"", lg:new Set(), cat:"", reach:"", src:"", pick:null, vol:null};

function hit(f){
  if (S.lg.size && ![...S.lg].every(l => f.logins.includes(l))) return false;
  if (S.cat && f.cat !== S.cat) return false;
  if (S.reach === "multi" && f.logins.length < 2) return false;
  if (S.reach === "all3" && f.logins.length < 3) return false;
  if (S.reach === "solo" && f.logins.length !== 1) return false;
  if (S.reach === "unused" && f.status !== "unused") return false;
  if (S.src === "hasman") { if (!(f.man || []).length) return false; }
  else if (S.src && f.src !== S.src) return false;
  if (S.q){
    const hay = [f.id,f.name,f.cat,f.desc,f.note||"",(f.ops||[]).join(" "),
                 Object.values(f.path||{}).join(" ")].join(" ").toLowerCase();
    if (!hay.includes(S.q.toLowerCase())) return false;
  }
  return true;
}
function mark(text){
  if (!S.q) return esc(text);
  const i = text.toLowerCase().indexOf(S.q.toLowerCase());
  if (i < 0) return esc(text);
  return esc(text.slice(0,i)) + "<u>" + esc(text.slice(i, i + S.q.length)) + "</u>" + esc(text.slice(i + S.q.length));
}
function tags(f){
  const shown = f.logins.slice(0,3).map(l => `<span class="tag">${SHORT[l]}</span>`).join("");
  const extra = f.logins.length > 3 ? `<span class="tag more">+${f.logins.length - 3}</span>` : "";
  return `<span class="tags">${shown}${extra}</span>`;
}

function drawIndex(){
  const list = F.filter(hit);
  const groups = [];
  list.forEach(f => {
    let g = groups.find(x => x.cat === f.cat);
    if (!g) groups.push(g = {cat:f.cat, rows:[]});
    g.rows.push(f);
  });
  document.getElementById("index").innerHTML = list.length ? groups.map(g => `
    <section class="group">
      <h2>${esc(g.cat)} <i>${g.rows.length}</i></h2>
      ${g.rows.map(f => `
        <button class="row" data-id="${f.id}" aria-current="${S.pick === f.id}">
          <span class="rid">${f.id}</span>
          <span class="rname">${mark(f.name)}<span class="dot" title="${esc(STATE[f.status][1])}">${STATE[f.status][0]}</span></span>
          ${tags(f)}
          <span class="rops">${nops(f)} ops</span>
        </button>`).join("")}
    </section>`).join("")
    : `<p class="none">Nothing matches those filters. <button class="clear" onclick="document.getElementById('clear').click()">Reset them</button></p>`;
  document.getElementById("tally").textContent =
    `${list.length} of ${F.length} · ${list.reduce((a,f)=>a+nops(f),0)} operations`;
  document.querySelectorAll(".row").forEach(r => r.onclick = () => {
    S.pick = r.dataset.id; drawIndex(); drawRead();
    if (window.matchMedia("(max-width:1020px)").matches)
      document.getElementById("read").scrollIntoView({block:"start", behavior:"smooth"});
  });
}

function drawRead(){
  const el = document.getElementById("read"), f = byid[S.pick];
  if (!f){
    const rank = LOGINS.map(l => ({l, n:F.filter(x => x.logins.includes(l)).length,
      o:F.filter(x => x.logins.includes(l)).reduce((a,x)=>a+nops(x),0)})).sort((a,b) => b.n - a.n);
    el.innerHTML = `
      <div class="lbl">Start here</div>
      <h2>Seven logins, ${F.length} capabilities</h2>
      <p class="lead">Pick any row to read what that screen does, the exact menu path in each login that
      has it, and every operation available once you are inside. The counts below are how the system is
      actually weighted &mdash; SPOC and the HOD carry most of it, the Counsellor almost none.</p>
      <div class="block rest"><h3 class="lbl">Capabilities per login <i>ops</i></h3>
        <dl>${rank.map(r => `<dt>${esc(LNAME[r.l])}</dt><dd>${r.n}</dd><dd>${r.o}</dd>`).join("")}</dl>
      </div>
      <div class="caution">Admission and Examination are missing because the vendor never issued those
      logins &mdash; confirmed on the third recording. They sit at either end of the student life-cycle;
      everything between them is here.</div>`;
    return;
  }
  const kin = F.filter(o => o.id !== f.id &&
      ((f.dup && o.dup === f.dup) || (o.cat === f.cat && o.logins.some(l => f.logins.includes(l))))).slice(0,6);
  el.innerHTML = `
    <div class="eyebrow">
      <span class="lbl">${f.id}</span><span class="tag">${esc(f.cat)}</span>
      <span class="tag">${STATE[f.status][0]} ${esc(STATE[f.status][1])}</span>
      <span class="tag">${esc(EVID[f.src] || f.src)}</span>
    </div>
    <h2>${esc(f.name)}</h2>
    <p class="lead">${esc(f.desc)}</p>
    <div class="block"><h3 class="lbl">Where to find it <i>${f.logins.length} ${f.logins.length === 1 ? "login" : "logins"}</i></h3>
      <div class="paths">${f.logins.map(l => `
        <div class="path"><span>${SHORT[l]}</span><code>${esc((f.path||{})[l] || "—")}</code></div>`).join("")}
      </div></div>
    ${nops(f) ? `<div class="block"><h3 class="lbl">What you can do here <i>${nops(f)}</i></h3>
      <ol class="steps">${f.ops.map(o => `<li><span>${esc(o)}</span></li>`).join("")}</ol></div>` : ""}
    ${f.note ? `<div class="caution">${esc(f.note)}</div>` : ""}
    ${(f.man||[]).length ? `<div class="block"><h3 class="lbl">Documented in</h3>
      <div class="chipline">${f.man.filter(i => byman[i]).map(i =>
        `<button data-man="${i}">${esc(byman[i].title)} · ${byman[i].pages}pp</button>`).join("")}</div></div>` : ""}
    ${kin.length ? `<div class="block"><h3 class="lbl">Nearby</h3>
      <div class="chipline">${kin.map(o => `<button data-id="${o.id}">${esc(o.name)}</button>`).join("")}</div></div>` : ""}`;
  link(el);
}

function link(el){
  el.querySelectorAll("[data-id]").forEach(b => b.onclick = () => {
    open_("index"); S.pick = b.dataset.id; drawIndex(); drawRead();
    document.querySelector('.row[aria-current="true"]')?.scrollIntoView({block:"center"});
  });
  el.querySelectorAll("[data-man]").forEach(b => b.onclick = () => {
    open_("manuals"); S.vol = b.dataset.man; drawShelf();
    document.querySelector(`.vol[data-v="${S.vol}"]`)?.scrollIntoView({block:"center"});
  });
}

/* manuals ---------------------------------------------- */
document.getElementById("manhint").textContent = LOCAL
  ? "Nineteen manuals, 387 pages. Because this copy sits in the same folder as the files, Open the PDF works."
  : "Nineteen manuals, 387 pages, every step folded into the capabilities. The PDFs are Contineo’s and are not served from this site — open your own copy.";

function drawShelf(){
  document.getElementById("shelf").innerHTML = M.map(m => {
    const open = S.vol === m.id;
    return `<article class="vol" data-v="${m.id}">
      <div class="volmeta"><span class="lbl">${m.id}</span>
        <span class="tag">${m.pages} pages</span>
        ${m.logins.map(l => `<span class="tag">${SHORT[l]}</span>`).join("")}
        ${m.conf ? `<span class="tag">confidential</span>` : ""}</div>
      <h3>${esc(m.title)}</h3>
      <p>${esc(m.sum)}</p>
      ${open ? `<div class="block" style="margin-top:4px"><h3 class="lbl">Documents <i>${m.covers.length}</i></h3>
        <div class="chipline">${m.covers.filter(i => byid[i]).map(i =>
          `<button data-id="${i}">${esc(byid[i].name)}</button>`).join("")}</div></div>` : ""}
      <div class="acts">
        ${LOCAL ? `<a class="go" href="${encodeURIComponent(m.file)}" target="_blank" rel="noopener">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M12 3v12M7 11l5 5 5-5M4 20h16"/></svg>Open the PDF</a>` : ""}
        <button class="go quiet" data-v="${m.id}">${open ? "Hide" : "What it covers"}</button>
      </div>
    </article>`;
  }).join("");
  document.querySelectorAll(".go.quiet[data-v]").forEach(b => b.onclick = () => {
    S.vol = (S.vol === b.dataset.v) ? null : b.dataset.v; drawShelf();
  });
  link(document.getElementById("shelf"));
}

/* repeated --------------------------------------------- */
document.getElementById("repeats").innerHTML = D.duplicates.map((d,i) => `
  <div class="pair">
    <button class="pairhead" data-p="${i}" aria-expanded="false">
      <strong>${esc(d.label)}</strong>
      <span class="tags">${d.logins.map(l => `<span class="tag">${SHORT[l]}</span>`).join("")}</span>
      <span class="rops">${d.ids.length}×</span>
    </button>
    <div class="pairbody" hidden>
      <p>${esc(d.note || "")}</p>
      <div class="chipline">${d.ids.filter(i => byid[i]).map(i =>
        `<button data-id="${i}">${esc(byid[i].name)}</button>`).join("")}</div>
    </div>
  </div>`).join("");
document.querySelectorAll("[data-p]").forEach(b => b.onclick = () => {
  const body = b.nextElementSibling;
  body.hidden = !body.hidden;
  b.setAttribute("aria-expanded", String(!body.hidden));
  link(body);
});

/* menus ------------------------------------------------ */
document.getElementById("menus").innerHTML = Object.values(D.menus).map(m => `
  <div class="card"><h3>${esc(m.label)}</h3>
    <ol>${m.items.map(i => `<li><span>${esc(i)}</span></li>`).join("")}</ol></div>`).join("");
document.getElementById("seq").innerHTML = (D.termsetup || []).map(s =>
  `<tr><td>${s.n}</td><td>${esc(s.act)}</td><td>${esc(s.by)}</td></tr>`).join("");

/* tabs ------------------------------------------------- */
function open_(name){
  ["index","manuals","repeats","menus"].forEach(n => {
    document.getElementById("v-"+n).hidden = n !== name;
    document.getElementById("t-"+n).setAttribute("aria-selected", String(n === name));
  });
}
document.querySelectorAll(".tab").forEach(t => t.onclick = () => open_(t.id.slice(2)));

/* bindings --------------------------------------------- */
document.getElementById("q").oninput = e => { S.q = e.target.value; drawIndex(); };
document.getElementById("cat").onchange = e => { S.cat = e.target.value; drawIndex(); };
document.getElementById("reach").onchange = e => { S.reach = e.target.value; drawIndex(); };
document.getElementById("src").onchange = e => { S.src = e.target.value; drawIndex(); };
document.querySelectorAll("[data-lg]").forEach(b => b.onclick = () => {
  const l = b.dataset.lg;
  S.lg.has(l) ? S.lg.delete(l) : S.lg.add(l);
  b.setAttribute("aria-pressed", String(S.lg.has(l)));
  drawIndex();
});
document.getElementById("clear").onclick = () => {
  S = {q:"", lg:new Set(), cat:"", reach:"", src:"", pick:S.pick, vol:S.vol};
  document.getElementById("q").value = "";
  ["cat","reach","src"].forEach(i => document.getElementById(i).value = "");
  document.querySelectorAll("[data-lg]").forEach(b => b.setAttribute("aria-pressed","false"));
  drawIndex();
};
document.addEventListener("keydown", e => {
  if (e.key !== "ArrowDown" && e.key !== "ArrowUp") return;
  if (document.activeElement && document.activeElement.tagName === "INPUT") return;
  const rows = [...document.querySelectorAll(".row")];
  if (!rows.length) return;
  const at = rows.findIndex(r => r.dataset.id === S.pick);
  const next = e.key === "ArrowDown" ? Math.min(at + 1, rows.length - 1) : Math.max(at - 1, 0);
  e.preventDefault();
  S.pick = rows[at < 0 ? 0 : next].dataset.id;
  drawIndex(); drawRead();
  document.querySelector('.row[aria-current="true"]')?.scrollIntoView({block:"nearest"});
});

drawIndex(); drawRead(); drawShelf();
</script>
</body>
</html>
"""

io.open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(
    HTML.replace("__DATA__", DATA).replace("__LOCAL__", "true" if LOCAL else "false"))
print("site written:", os.path.join(OUT, "index.html"), len(HTML) + len(DATA), "bytes",
      "| local" if LOCAL else "| web")
