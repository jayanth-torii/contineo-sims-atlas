# -*- coding: utf-8 -*-
"""Build the Contineo SIMS Atlas site from features.json.

    python build/site.py [outdir] [--local]

--local emits the copy that sits beside the PDFs, with working manual links.
Interface follows Material Design 3: neutral tonal palette, MD3 shape and
state layers, a bottom navigation bar and full-screen detail view on phones.
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
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><rect width='16' height='16' rx='4' fill='%231b1b19'/><rect x='3.4' y='4' width='9.2' height='1.5' rx='.75' fill='%23fff'/><rect x='3.4' y='7.3' width='9.2' height='1.5' rx='.75' fill='%23fff'/><rect x='3.4' y='10.6' width='5.4' height='1.5' rx='.75' fill='%23908f89'/></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Roboto+Mono:wght@400;500&display=swap">
<style>
/* Material Design 3, monochrome. Neutral tonal surfaces carry the hierarchy
   instead of colour; shape, state layers and the MD3 type scale do the rest.
   Phones get a bottom navigation bar and a full-screen detail view. */
:root{
  /* MD3 colour roles — light */
  --primary:#1b1b19; --on-primary:#ffffff; --primary-container:#dfded8; --on-primary-container:#191915;
  --surface:#fdfcfa; --on-surface:#1b1b19; --surface-variant:#e4e3dc; --on-surface-variant:#46463f;
  --s-lowest:#ffffff; --s-low:#f7f6f2; --s-container:#f2f1ec; --s-high:#ecebe6; --s-highest:#e6e5e0;
  --outline:#77766f; --outline-variant:#c8c7c0; --scrim:rgba(0,0,0,.4);
  /* MD3 shape scale */
  --r-xs:4px; --r-s:8px; --r-m:12px; --r-l:16px; --r-xl:28px; --r-full:999px;
  /* MD3 elevation */
  --e1:0 1px 2px rgba(0,0,0,.30),0 1px 3px 1px rgba(0,0,0,.15);
  --e2:0 1px 2px rgba(0,0,0,.30),0 2px 6px 2px rgba(0,0,0,.15);
  --e3:0 4px 8px 3px rgba(0,0,0,.15),0 1px 3px rgba(0,0,0,.30);
  --f:"Roboto",system-ui,-apple-system,"Segoe UI",sans-serif;
  --f-mono:"Roboto Mono",ui-monospace,Consolas,monospace;
  color-scheme:light;
}
@media (prefers-color-scheme:dark){ :root:not([data-theme="light"]){
  --primary:#e6e5e0; --on-primary:#1b1b19; --primary-container:#3c3b37; --on-primary-container:#e6e5e0;
  --surface:#131311; --on-surface:#e6e5e0; --surface-variant:#46463f; --on-surface-variant:#c8c7c0;
  --s-lowest:#0e0e0c; --s-low:#1b1b19; --s-container:#1f1f1d; --s-high:#2a2a27; --s-highest:#353532;
  --outline:#918f88; --outline-variant:#46463f; --scrim:rgba(0,0,0,.6);
  color-scheme:dark; } }
:root[data-theme="light"]{
  --primary:#1b1b19; --on-primary:#ffffff; --primary-container:#dfded8; --on-primary-container:#191915;
  --surface:#fdfcfa; --on-surface:#1b1b19; --surface-variant:#e4e3dc; --on-surface-variant:#46463f;
  --s-lowest:#ffffff; --s-low:#f7f6f2; --s-container:#f2f1ec; --s-high:#ecebe6; --s-highest:#e6e5e0;
  --outline:#77766f; --outline-variant:#c8c7c0; --scrim:rgba(0,0,0,.4); color-scheme:light; }
:root[data-theme="dark"]{
  --primary:#e6e5e0; --on-primary:#1b1b19; --primary-container:#3c3b37; --on-primary-container:#e6e5e0;
  --surface:#131311; --on-surface:#e6e5e0; --surface-variant:#46463f; --on-surface-variant:#c8c7c0;
  --s-lowest:#0e0e0c; --s-low:#1b1b19; --s-container:#1f1f1d; --s-high:#2a2a27; --s-highest:#353532;
  --outline:#918f88; --outline-variant:#46463f; --scrim:rgba(0,0,0,.6); color-scheme:dark; }

*{box-sizing:border-box}
body{margin:0;background:var(--surface);color:var(--on-surface);font-family:var(--f);
  font-size:16px;line-height:1.5;-webkit-font-smoothing:antialiased;-webkit-tap-highlight-color:transparent}
button{font:inherit;color:inherit;background:none;border:0}
:focus-visible{outline:3px solid var(--primary);outline-offset:2px}
.wrap{max-width:1380px;margin:0 auto;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}

/* MD3 type scale */
.t-display{font-size:36px;line-height:44px;font-weight:400;letter-spacing:0}
.t-headline{font-size:24px;line-height:32px;font-weight:400;letter-spacing:0}
.t-title-l{font-size:22px;line-height:28px;font-weight:400}
.t-title-m{font-size:16px;line-height:24px;font-weight:500;letter-spacing:.15px}
.t-title-s{font-size:14px;line-height:20px;font-weight:500;letter-spacing:.1px}
.t-body-l{font-size:16px;line-height:24px;letter-spacing:.5px}
.t-body-m{font-size:14px;line-height:20px;letter-spacing:.25px}
.t-body-s{font-size:12px;line-height:16px;letter-spacing:.4px}
.t-label-l{font-size:14px;line-height:20px;font-weight:500;letter-spacing:.1px}
.t-label-m{font-size:12px;line-height:16px;font-weight:500;letter-spacing:.5px}
.t-label-s{font-size:11px;line-height:16px;font-weight:500;letter-spacing:.5px}
.mono{font-family:var(--f-mono);font-variant-numeric:tabular-nums}

/* MD3 state layer */
.state{position:relative;overflow:hidden;isolation:isolate}
.state::after{content:"";position:absolute;inset:0;background:currentColor;opacity:0;
  transition:opacity .12s;pointer-events:none;z-index:-1}
.state:hover::after{opacity:.08}
.state:active::after{opacity:.12}

/* ── top app bar ─────────────────────────────── */
.appbar{position:sticky;top:env(safe-area-inset-top,0px);z-index:20;background:var(--surface);
  border-bottom:1px solid var(--outline-variant)}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);
  z-index:21;background:var(--surface)}
.appbar .inner{display:flex;align-items:center;gap:12px;min-height:64px;padding-block:8px}
.appbar h1{margin:0;font-size:22px;line-height:28px;font-weight:500;letter-spacing:0;flex:1 1 auto;min-width:0}
.appbar h1 small{display:block;font-size:12px;line-height:16px;font-weight:400;letter-spacing:.4px;
  color:var(--on-surface-variant);font-family:var(--f-mono)}
.iconbtn{width:48px;height:48px;border-radius:var(--r-full);display:grid;place-items:center;cursor:pointer;
  color:var(--on-surface-variant);flex:none}
.iconbtn[aria-pressed="true"]{background:var(--primary-container);color:var(--on-primary-container)}
.themeset{display:flex;gap:2px;flex:none}

/* ── hero / figures ──────────────────────────── */
.hero{padding-block:22px 6px}
.hero p{margin:10px 0 0;max-width:62ch;color:var(--on-surface-variant)}
.figs{display:grid;grid-template-columns:repeat(auto-fit,minmax(118px,1fr));gap:8px;margin-top:20px}
.figcard{background:var(--s-container);border-radius:var(--r-m);padding:14px}
.figcard b{display:block;font-size:28px;line-height:34px;font-weight:400;font-variant-numeric:tabular-nums}
.figcard span{display:block;margin-top:4px;color:var(--on-surface-variant)}

/* ── desktop tabs ────────────────────────────── */
.tabs{display:flex;gap:0;border-bottom:1px solid var(--outline-variant);margin-top:20px;overflow-x:auto;
  scrollbar-width:none}
.tabs::-webkit-scrollbar{display:none}
.tab{flex:1 1 0;min-width:112px;min-height:48px;padding:0 16px;cursor:pointer;color:var(--on-surface-variant);
  border-bottom:3px solid transparent;display:flex;align-items:center;justify-content:center;gap:8px;
  white-space:nowrap}
.tab[aria-selected="true"]{color:var(--primary);border-bottom-color:var(--primary)}
.tab b{font-weight:500;font-family:var(--f-mono);font-size:12px}

/* ── search + chips ──────────────────────────── */
.filters{display:flex;flex-direction:column;gap:12px;padding-block:16px;position:sticky;
  top:calc(env(safe-area-inset-top,0px) + 64px);background:var(--surface);z-index:15}
.searchbar{display:flex;align-items:center;gap:12px;height:56px;background:var(--s-high);
  border-radius:var(--r-xl);padding:0 18px}
.searchbar svg{flex:none;color:var(--on-surface-variant)}
.searchbar input{flex:1 1 auto;min-width:0;background:none;border:0;color:var(--on-surface);font:inherit;
  font-size:16px;outline:0}
.searchbar input::placeholder{color:var(--on-surface-variant)}
.chiprow{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;padding-bottom:2px}
.chiprow::-webkit-scrollbar{display:none}
.chip{min-height:32px;border-radius:var(--r-s);border:1px solid var(--outline);padding:0 14px;cursor:pointer;
  display:inline-flex;align-items:center;gap:6px;color:var(--on-surface-variant);white-space:nowrap;flex:none}
.chip[aria-pressed="true"]{background:var(--primary-container);color:var(--on-primary-container);
  border-color:transparent;padding-left:8px}
.chip .tick{display:none}
.chip[aria-pressed="true"] .tick{display:block}
.selects{display:flex;gap:8px;flex-wrap:wrap}
select{flex:1 1 150px;min-width:0;height:48px;background:var(--s-high);border:0;border-radius:var(--r-xs);
  color:var(--on-surface);font:inherit;font-size:14px;padding:0 12px}
.tally{color:var(--on-surface-variant);display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.textbtn{min-height:40px;border-radius:var(--r-full);padding:0 14px;cursor:pointer;color:var(--primary);
  font-weight:500;font-size:14px}

/* ── panes ───────────────────────────────────── */
.panes{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,460px);gap:24px;align-items:start;
  padding-bottom:56px}

/* ── index list ──────────────────────────────── */
.group{margin-top:20px}
.group:first-child{margin-top:4px}
.grouphead{display:flex;align-items:center;gap:8px;padding:8px 4px;color:var(--on-surface-variant)}
.grouphead b{font-family:var(--f-mono);font-size:12px;font-weight:500}
.items{background:var(--s-low);border-radius:var(--r-m);overflow:hidden}
.item{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:14px;align-items:center;width:100%;
  text-align:left;min-height:64px;padding:10px 16px;cursor:pointer;
  border-bottom:1px solid var(--outline-variant);color:var(--on-surface)}
.item:last-child{border-bottom:0}
.item[aria-current="true"]{background:var(--primary-container);color:var(--on-primary-container)}
.avatar{width:40px;height:40px;border-radius:var(--r-full);background:var(--s-highest);display:grid;
  place-items:center;font-family:var(--f-mono);font-size:11px;font-weight:500;color:var(--on-surface-variant);
  flex:none}
.item[aria-current="true"] .avatar{background:var(--primary);color:var(--on-primary)}
.itemtext{min-width:0}
.itemtext .hl{font-weight:500;background:var(--primary-container);border-radius:2px}
.item[aria-current="true"] .hl{background:var(--surface)}
.itemsub{color:var(--on-surface-variant);margin-top:2px;display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.item[aria-current="true"] .itemsub{color:var(--on-primary-container)}
.badge{border:1px solid var(--outline-variant);border-radius:var(--r-xs);padding:0 5px;font-family:var(--f-mono);
  font-size:11px;line-height:17px}
.trail{display:flex;align-items:center;gap:10px;color:var(--on-surface-variant);flex:none}
.item[aria-current="true"] .trail{color:var(--on-primary-container)}
.empty{background:var(--s-low);border-radius:var(--r-m);padding:28px 18px;color:var(--on-surface-variant)}

/* ── detail ──────────────────────────────────── */
.sheet{position:sticky;top:calc(env(safe-area-inset-top,0px) + 80px);background:var(--s-low);
  border-radius:var(--r-l);max-height:calc(100vh - 110px);display:flex;flex-direction:column;overflow:hidden}
.sheetbar{display:none;align-items:center;gap:8px;padding:8px 8px 8px 4px;background:var(--s-low);
  border-bottom:1px solid var(--outline-variant);flex:none}
.sheetbar h2{margin:0;font-size:16px;line-height:24px;font-weight:500;flex:1 1 auto;min-width:0;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.read{padding:22px;overflow:auto;min-width:0}
.read .over{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.read h2.title{margin:12px 0 0;font-size:24px;line-height:32px;font-weight:400;letter-spacing:0;
  text-wrap:balance}
.lead{margin:12px 0 0;color:var(--on-surface-variant)}
.sect{margin-top:24px}
.secthead{display:flex;justify-content:space-between;align-items:baseline;gap:10px;color:var(--on-surface-variant);
  margin-bottom:10px}
.paths{display:flex;flex-direction:column;gap:8px}
.pathrow{display:flex;gap:10px;align-items:flex-start;background:var(--s-container);border-radius:var(--r-s);
  padding:10px 12px}
.pathrow .who{font-family:var(--f-mono);font-size:11px;font-weight:500;background:var(--primary);
  color:var(--on-primary);border-radius:var(--r-xs);padding:2px 6px;flex:none}
.pathrow code{font-family:var(--f-mono);font-size:13px;color:var(--on-surface-variant);overflow-wrap:anywhere;
  line-height:1.45}
ol.ops{list-style:none;margin:0;padding:0;counter-reset:o}
ol.ops li{counter-increment:o;display:grid;grid-template-columns:26px minmax(0,1fr);gap:10px;
  padding:9px 0;border-bottom:1px solid var(--outline-variant);color:var(--on-surface-variant)}
ol.ops li:last-child{border-bottom:0}
ol.ops li::before{content:counter(o,decimal-leading-zero);font-family:var(--f-mono);font-size:11px;
  color:var(--outline);padding-top:3px}
.callout{margin-top:18px;background:var(--primary-container);color:var(--on-primary-container);
  border-radius:var(--r-m);padding:14px 16px}
.links{display:flex;flex-wrap:wrap;gap:8px}
.links button,.links a{min-height:40px;border:1px solid var(--outline);border-radius:var(--r-s);padding:8px 12px;
  cursor:pointer;color:var(--on-surface);text-decoration:none;text-align:left;font-size:14px}
.rank{display:flex;flex-direction:column}
.rankrow{display:grid;grid-template-columns:minmax(0,1fr) auto auto;gap:14px;padding:10px 0;
  border-bottom:1px solid var(--outline-variant);align-items:baseline}
.rankrow span:not(:first-child){font-family:var(--f-mono);font-size:13px;color:var(--on-surface-variant)}

/* ── manuals ─────────────────────────────────── */
.shelf{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:12px;margin-top:16px;
  padding-bottom:56px}
.vol{background:var(--s-low);border-radius:var(--r-m);padding:16px;display:flex;flex-direction:column;gap:10px;
  min-width:0}
.vol h3{margin:0;font-size:16px;line-height:24px;font-weight:500}
.vol p{margin:0;color:var(--on-surface-variant)}
.volmeta{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.acts{display:flex;flex-wrap:wrap;gap:8px;margin-top:auto;padding-top:6px}
.filled{min-height:40px;border-radius:var(--r-full);background:var(--primary);color:var(--on-primary);
  padding:0 20px;display:inline-flex;align-items:center;gap:8px;cursor:pointer;font-weight:500;font-size:14px;
  text-decoration:none}
.tonal{min-height:40px;border-radius:var(--r-full);background:var(--s-highest);color:var(--on-surface);
  padding:0 18px;display:inline-flex;align-items:center;gap:8px;cursor:pointer;font-weight:500;font-size:14px}

/* ── attach + pdf viewer ─────────────────────── */
.attach{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:14px;padding:14px 16px;
  background:var(--s-low);border-radius:var(--r-m)}
.attach p{margin:0;flex:1 1 240px;min-width:0;color:var(--on-surface-variant)}
.pdfwrap{position:fixed;inset:0;z-index:60;background:var(--s-lowest);display:flex;flex-direction:column;
  visibility:hidden;opacity:0;transition:opacity .18s ease,visibility .18s ease}
.pdfwrap.open{visibility:visible;opacity:1}
.pdfbar{display:flex;align-items:center;gap:8px;background:var(--s-container);
  border-bottom:1px solid var(--outline-variant);
  padding:calc(8px + env(safe-area-inset-top,0px)) max(8px,env(safe-area-inset-right,0px)) 8px
          max(8px,env(safe-area-inset-left,0px))}
.pdfbar h2{margin:0;font-size:16px;line-height:22px;font-weight:500;flex:1 1 auto;min-width:0;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.iconbtn{width:48px;height:48px;min-width:48px;border-radius:var(--r-full);display:inline-flex;
  align-items:center;justify-content:center;cursor:pointer;color:var(--on-surface);text-decoration:none}
.pdfbody{flex:1 1 auto;min-height:0;position:relative;background:var(--s-lowest)}
.pdfbody iframe{width:100%;height:100%;border:0;display:block}
.pdfnote{padding:10px max(12px,env(safe-area-inset-left,0px))
         calc(10px + env(safe-area-inset-bottom,0px)) max(12px,env(safe-area-inset-right,0px));
  background:var(--s-container);border-top:1px solid var(--outline-variant);
  color:var(--on-surface-variant);display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.pdfnote a{color:var(--on-surface);text-underline-offset:3px}

/* ── repeated + menus ────────────────────────── */
.stack{display:flex;flex-direction:column;gap:8px;margin-top:16px;padding-bottom:56px}
.pair{background:var(--s-low);border-radius:var(--r-m);overflow:hidden}
.pairhead{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:12px;align-items:center;width:100%;
  text-align:left;min-height:64px;padding:12px 16px;cursor:pointer}
.pairbody{padding:0 16px 16px;color:var(--on-surface-variant)}
.pairbody p{margin:0 0 12px}
.menugrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px;margin-top:16px}
.menu{background:var(--s-low);border-radius:var(--r-m);padding:16px;min-width:0}
.menu h3{margin:0 0 10px;font-size:14px;line-height:20px;font-weight:500;font-family:var(--f-mono);
  padding-bottom:8px;border-bottom:1px solid var(--outline-variant)}
.menu ol{list-style:none;margin:0;padding:0;counter-reset:m}
.menu li{counter-increment:m;display:grid;grid-template-columns:22px minmax(0,1fr);gap:8px;padding:6px 0;
  color:var(--on-surface-variant);border-bottom:1px solid var(--outline-variant);font-size:14px}
.menu li:last-child{border-bottom:0}
.menu li::before{content:counter(m,decimal-leading-zero);font-family:var(--f-mono);font-size:11px;
  color:var(--outline);padding-top:2px}
.seqwrap{overflow-x:auto;margin-top:14px;border-radius:var(--r-m);background:var(--s-low)}
table.seq{border-collapse:collapse;width:100%;min-width:420px;font-size:14px}
table.seq th{background:var(--primary);color:var(--on-primary);text-align:left;padding:12px 14px;
  font-size:12px;font-weight:500;letter-spacing:.5px}
table.seq td{padding:11px 14px;border-bottom:1px solid var(--outline-variant);color:var(--on-surface-variant)}
table.seq td:first-child{font-family:var(--f-mono);width:44px}
.note{color:var(--on-surface-variant);margin:14px 0 0;max-width:72ch}
footer{border-top:1px solid var(--outline-variant);padding-block:22px;margin-top:8px;
  color:var(--on-surface-variant);max-width:76ch}

/* ── bottom navigation bar (phones) ──────────── */
.navbar{display:none}
@media (max-width:1020px){
  .panes{grid-template-columns:1fr;gap:0}
  .tabs{display:none}
  .appbar .inner{min-height:56px}
  .appbar h1{font-size:18px;line-height:22px}
  /* the whole filter block sticky would swallow a third of the screen:
     keep only the search bar pinned, let the rest scroll away */
  .filters{position:static;gap:10px;padding-block:12px}
  .searchbar{position:sticky;top:calc(env(safe-area-inset-top,0px) + 56px);z-index:15;height:52px}
  .figs{grid-template-columns:repeat(auto-fit,minmax(96px,1fr));gap:6px;margin-top:14px}
  .figcard{padding:10px 12px;border-radius:var(--r-s)}
  .figcard b{font-size:22px;line-height:26px}
  .hero{padding-block:14px 2px}
  .hero p{font-size:14px;line-height:20px;letter-spacing:.25px}
  .selects{gap:6px}
  select{height:44px;flex:1 1 128px}
  main{padding-bottom:calc(84px + env(safe-area-inset-bottom,0px))}
  .shelf,.stack,.panes{padding-bottom:12px}

  .navbar{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:30;background:var(--s-container);
    border-top:1px solid var(--outline-variant);
    padding:12px max(8px,env(safe-area-inset-left,0px)) calc(16px + env(safe-area-inset-bottom,0px))
            max(8px,env(safe-area-inset-right,0px))}
  .dest{flex:1 1 0;min-width:0;display:flex;flex-direction:column;align-items:center;gap:4px;cursor:pointer;
    color:var(--on-surface-variant);padding:0}
  .dest .pill{width:64px;height:32px;border-radius:var(--r-full);display:grid;place-items:center;
    transition:background .15s}
  .dest[aria-selected="true"] .pill{background:var(--primary-container);color:var(--on-primary-container)}
  .dest[aria-selected="true"]{color:var(--on-surface)}
  .dest span{font-size:12px;line-height:16px;font-weight:500;letter-spacing:.5px;
    max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}

  /* full-screen detail */
  .sheet{position:fixed;inset:0;z-index:40;border-radius:0;max-height:none;background:var(--surface);
    transform:translateY(100%);transition:transform .22s ease;visibility:hidden}
  .sheet.open{transform:none;visibility:visible}
  .sheetbar{display:flex;padding-top:calc(8px + env(safe-area-inset-top,0px))}
  .read{padding:18px max(16px,env(safe-area-inset-left,0px))
        calc(32px + env(safe-area-inset-bottom,0px)) max(16px,env(safe-area-inset-right,0px))}
  body.locked{overflow:hidden}
}
@media (prefers-reduced-motion:reduce){ *{transition:none!important} }
</style>
</head>
<body>

<header class="appbar">
  <div class="wrap inner">
    <h1>Contineo SIMS Atlas<small>ncet-sims.contineo.in</small></h1>
    <div class="themeset" role="group" aria-label="Colour theme">
      <button class="iconbtn state" data-th="light" title="Light" aria-pressed="false"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4.3"/><path d="M12 2v2.2M12 19.8V22M2 12h2.2M19.8 12H22M4.9 4.9l1.6 1.6M17.5 17.5l1.6 1.6M19.1 4.9l-1.6 1.6M6.5 17.5l-1.6 1.6"/></svg></button>
      <button class="iconbtn state" data-th="auto" title="Match the system" aria-pressed="true"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2.6" y="4.2" width="18.8" height="13" rx="2"/><path d="M8.5 20.2h7"/></svg></button>
      <button class="iconbtn state" data-th="dark" title="Dark" aria-pressed="false"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 14.6A8.6 8.6 0 0 1 9.4 4 8.6 8.6 0 1 0 20 14.6z"/></svg></button>
    </div>
  </div>
</header>

<main class="wrap">

<section class="hero">
  <p class="t-body-l">Every function in the student ERP, the login it lives in, and every operation
  available once you are there. Built from three walkthrough recordings and nineteen Contineo user manuals.</p>
  <div class="figs" id="figs"></div>
</section>

<div class="tabs" role="tablist">
  <button class="tab state t-title-s" role="tab" id="t-index" aria-selected="true">Capabilities <b id="c1"></b></button>
  <button class="tab state t-title-s" role="tab" id="t-manuals" aria-selected="false">Manuals <b id="c4"></b></button>
  <button class="tab state t-title-s" role="tab" id="t-repeats" aria-selected="false">Repeated <b id="c2"></b></button>
  <button class="tab state t-title-s" role="tab" id="t-menus" aria-selected="false">Menus <b id="c3"></b></button>
</div>

<section id="v-index" role="tabpanel" aria-labelledby="t-index">
  <div class="filters">
    <div class="searchbar">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4.2-4.2"/></svg>
      <input id="q" type="search" placeholder="Search capabilities and operations" aria-label="Search capabilities">
    </div>
    <div class="chiprow" role="group" aria-label="Filter by login" id="lg"></div>
    <div class="selects">
      <select id="cat" aria-label="Filter by area"><option value="">Every area</option></select>
      <select id="reach" aria-label="Filter by reach">
        <option value="">Any reach</option>
        <option value="solo">Only one login</option>
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
    </div>
    <div class="tally t-body-m"><span id="tally"></span>
      <button class="textbtn state" id="clear" type="button">Reset filters</button></div>
  </div>
  <div class="panes">
    <div id="index"></div>
    <div class="sheet" id="sheet">
      <div class="sheetbar">
        <button class="iconbtn state" id="back" aria-label="Back to the list"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M11 18l-6-6 6-6"/></svg></button>
        <h2 id="sheettitle">Detail</h2>
      </div>
      <div class="read" id="read" aria-live="polite"></div>
    </div>
  </div>
</section>

<section id="v-manuals" role="tabpanel" aria-labelledby="t-manuals" hidden>
  <p class="note t-body-m" id="manhint"></p>
  <div class="attach">
    <p class="t-body-m" id="attachmsg"></p>
    <input type="file" id="pickfiles" accept="application/pdf,.pdf" multiple hidden>
    <button class="filled state" id="attachbtn" type="button">Attach the manual PDFs</button>
  </div>
  <div class="shelf" id="shelf"></div>
</section>

<section id="v-repeats" role="tabpanel" aria-labelledby="t-repeats" hidden>
  <p class="note t-body-m">Thirty-nine jobs that more than one login can do. Each is a decision for a
  rebuild: keep the duplication on purpose, or collapse it.</p>
  <div class="stack" id="repeats"></div>
</section>

<section id="v-menus" role="tabpanel" aria-labelledby="t-menus" hidden>
  <p class="note t-body-m">Every menu, transcribed from the screen, spelling and all &mdash; including
  &ldquo;Calender Of Events&rdquo;, which the product has always misspelt.</p>
  <div class="menugrid" id="menus"></div>
  <h3 class="t-title-m" style="margin:26px 0 0">The term setup sequence</h3>
  <div class="seqwrap"><table class="seq"><thead><tr><th>#</th><th>Activity</th><th style="width:170px">Owner</th></tr></thead>
  <tbody id="seq"></tbody></table></div>
  <div style="height:56px"></div>
</section>

<footer class="t-body-m" id="foot"></footer>
</main>

<div class="pdfwrap" id="pdfwrap" role="dialog" aria-modal="true" aria-labelledby="pdftitle">
  <div class="pdfbar">
    <button class="iconbtn state" id="pdfclose" type="button" aria-label="Close the manual"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M11 18l-6-6 6-6"/></svg></button>
    <h2 id="pdftitle"></h2>
    <a class="iconbtn state" id="pdftab" target="_blank" rel="noopener" aria-label="Open in a new tab"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg></a>
  </div>
  <div class="pdfbody" id="pdfbody"></div>
  <p class="pdfnote t-body-s" id="pdfnote"></p>
</div>

<nav class="navbar" role="tablist" aria-label="Sections">
  <button class="dest state" data-dest="index" aria-selected="true">
    <span class="pill"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h10"/></svg></span><span>Capabilities</span></button>
  <button class="dest state" data-dest="manuals" aria-selected="false">
    <span class="pill"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M8 7h8"/></svg></span><span>Manuals</span></button>
  <button class="dest state" data-dest="repeats" aria-selected="false">
    <span class="pill"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="8.5" y="8.5" width="12" height="12" rx="2"/><path d="M15.5 4.5h-11v11"/></svg></span><span>Repeated</span></button>
  <button class="dest state" data-dest="menus" aria-selected="false">
    <span class="pill"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3.5" y="3.5" width="7" height="7" rx="1.6"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.6"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.6"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.6"/></svg></span><span>Menus</span></button>
</nav>

<script>
const D = __DATA__;
const LOCAL = __LOCAL__;
const LOGINS = ["DC","FAC","HOD","SPOC","CNS","SP","IQAC"];
const LNAME = {DC:"Department Coordinator",FAC:"Faculty / Staff",HOD:"HOD",SPOC:"SPOC",
               CNS:"Counsellor",SP:"Student / Parent portal",IQAC:"IQAC Head"};
const SHORT = {DC:"DC",FAC:"FAC",HOD:"HOD",SPOC:"SPOC",CNS:"CNS",SP:"S/P",IQAC:"IQAC"};
const STATE = {live:"In use",partial:"Partly built",unused:"Present, unused",listed:"Listed, never opened"};
const EVID = {video:"Seen in a recording",manual:"Documented in a manual only",both:"Recording and manual"};
const F = D.features, M = D.manuals || [];
const byid = {}, byman = {};
F.forEach(f => byid[f.id] = f);
M.forEach(m => byman[m.id] = m);
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const nops = f => (f.ops || []).length;
const phone = () => window.matchMedia("(max-width:1020px)").matches;

/* theme ------------------------------------------------ */
const root = document.documentElement;
function theme(t){
  if (t === "auto") root.removeAttribute("data-theme"); else root.setAttribute("data-theme", t);
  try { localStorage.setItem("sims-theme", t); } catch(e) {}
  document.querySelectorAll("[data-th]").forEach(b =>
    b.setAttribute("aria-pressed", String(b.dataset.th === t)));
}
let saved = "auto";
try { saved = localStorage.getItem("sims-theme") || "auto"; } catch(e) {}
theme(saved);
document.querySelectorAll("[data-th]").forEach(b => b.onclick = () => theme(b.dataset.th));

/* figures ---------------------------------------------- */
const totalOps = F.reduce((a,f) => a + nops(f), 0);
const menuN = Object.values(D.menus).reduce((a,m) => a + m.items.length, 0);
document.getElementById("figs").innerHTML = [
  [F.length,"capabilities"],[totalOps,"operations"],["7","logins"],
  [M.length,"manuals read"],[D.duplicates.length,"repeated jobs"],[menuN,"menu entries"]
].map(([n,l]) => `<div class="figcard"><b>${n}</b><span class="t-label-m">${l}</span></div>`).join("");
document.getElementById("c1").textContent = F.length;
document.getElementById("c2").textContent = D.duplicates.length;
document.getElementById("c3").textContent = Object.keys(D.menus).length;
document.getElementById("c4").textContent = M.length;
document.getElementById("foot").innerHTML =
  `Internal requirement capture for Nagarjuna College of Engineering and Technology. Seven logins are
   mapped; Admission and Examination were never issued, so they stay unmapped. The Contineo user manuals
   are the vendor’s confidential documents and are not republished here.`;

/* filters ---------------------------------------------- */
const TICK = `<svg class="tick" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M4.5 12.5l5 5 10-11"/></svg>`;
document.getElementById("lg").innerHTML = LOGINS.map(l =>
  `<button class="chip state t-label-l" data-lg="${l}" aria-pressed="false" title="${esc(LNAME[l])}">${TICK}${SHORT[l]}</button>`).join("");
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
  return esc(text.slice(0,i)) + '<span class="hl">' + esc(text.slice(i, i + S.q.length)) +
         "</span>" + esc(text.slice(i + S.q.length));
}

function drawIndex(){
  const list = F.filter(hit), groups = [];
  list.forEach(f => {
    let g = groups.find(x => x.cat === f.cat);
    if (!g) groups.push(g = {cat:f.cat, rows:[]});
    g.rows.push(f);
  });
  document.getElementById("index").innerHTML = list.length ? groups.map(g => `
    <section class="group">
      <div class="grouphead"><span class="t-title-s">${esc(g.cat)}</span><b>${g.rows.length}</b></div>
      <div class="items">
        ${g.rows.map(f => `
          <button class="item state" data-id="${f.id}" aria-current="${S.pick === f.id}">
            <span class="avatar">${f.id.replace("F","")}</span>
            <span class="itemtext">
              <span class="t-body-l">${mark(f.name)}</span>
              <span class="itemsub t-body-s">${f.logins.slice(0,3).map(l =>
                `<span class="badge">${SHORT[l]}</span>`).join("")}${
                f.logins.length > 3 ? `<span class="badge">+${f.logins.length - 3}</span>` : ""}
                <span>${esc(STATE[f.status])}</span></span>
            </span>
            <span class="trail"><span class="mono t-body-s">${nops(f)}</span>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 6l6 6-6 6"/></svg></span>
          </button>`).join("")}
      </div>
    </section>`).join("")
    : `<div class="empty t-body-l">Nothing matches those filters.</div>`;
  document.getElementById("tally").textContent =
    `${list.length} of ${F.length} · ${list.reduce((a,f)=>a+nops(f),0)} operations`;
  document.querySelectorAll(".item").forEach(r => r.onclick = () => pickOne(r.dataset.id));
}

function pickOne(id){
  S.pick = id; drawIndex(); drawRead();
  if (phone()) openSheet();
}
function openSheet(){
  document.getElementById("sheet").classList.add("open");
  document.body.classList.add("locked");
  document.getElementById("read").scrollTop = 0;
  document.getElementById("back").focus();
}
function closeSheet(){
  document.getElementById("sheet").classList.remove("open");
  document.body.classList.remove("locked");
}
document.getElementById("back").onclick = closeSheet;
document.addEventListener("keydown", e => {
  if (e.key !== "Escape") return;
  if (pdfOpen()) closePdf(); else closeSheet();
});

function drawRead(){
  const el = document.getElementById("read"), f = byid[S.pick];
  document.getElementById("sheettitle").textContent = f ? f.name : "Detail";
  if (!f){
    const rank = LOGINS.map(l => ({l, n:F.filter(x => x.logins.includes(l)).length,
      o:F.filter(x => x.logins.includes(l)).reduce((a,x)=>a+nops(x),0)})).sort((a,b) => b.n - a.n);
    el.innerHTML = `
      <div class="t-label-m" style="color:var(--on-surface-variant)">START HERE</div>
      <h2 class="title">Seven logins, ${F.length} capabilities</h2>
      <p class="lead t-body-m">Choose any row to read what that screen does, the exact menu path in each
      login that has it, and every operation available once you are inside.</p>
      <div class="sect"><div class="secthead"><span class="t-title-s">Capabilities per login</span>
        <span class="t-label-m">OPS</span></div>
        <div class="rank">${rank.map(r => `<div class="rankrow"><span class="t-body-m">${esc(LNAME[r.l])}</span>
          <span>${r.n}</span><span>${r.o}</span></div>`).join("")}</div></div>
      <div class="callout t-body-m">Admission and Examination are missing because the vendor never issued
      those logins. They sit at either end of the student life-cycle; everything between them is here.</div>`;
    return;
  }
  const kin = F.filter(o => o.id !== f.id &&
      ((f.dup && o.dup === f.dup) || (o.cat === f.cat && o.logins.some(l => f.logins.includes(l))))).slice(0,6);
  el.innerHTML = `
    <div class="over">
      <span class="badge">${f.id}</span><span class="badge">${esc(f.cat)}</span>
      <span class="badge">${esc(STATE[f.status])}</span>
      <span class="badge">${esc(EVID[f.src] || f.src)}</span>
    </div>
    <h2 class="title">${esc(f.name)}</h2>
    <p class="lead t-body-l">${esc(f.desc)}</p>
    <div class="sect"><div class="secthead"><span class="t-title-s">Where to find it</span>
      <span class="t-label-m">${f.logins.length} ${f.logins.length === 1 ? "LOGIN" : "LOGINS"}</span></div>
      <div class="paths">${f.logins.map(l => `
        <div class="pathrow"><span class="who">${SHORT[l]}</span><code>${esc((f.path||{})[l] || "—")}</code></div>`).join("")}
      </div></div>
    ${nops(f) ? `<div class="sect"><div class="secthead"><span class="t-title-s">What you can do here</span>
      <span class="t-label-m mono">${nops(f)}</span></div>
      <ol class="ops t-body-m">${f.ops.map(o => `<li><span>${esc(o)}</span></li>`).join("")}</ol></div>` : ""}
    ${f.note ? `<div class="callout t-body-m">${esc(f.note)}</div>` : ""}
    ${(f.man||[]).length ? `<div class="sect"><div class="secthead"><span class="t-title-s">Documented in</span></div>
      <div class="links">${f.man.filter(i => byman[i]).map(i =>
        `<button class="state" data-pdf="${i}">${esc(byman[i].title)} · ${byman[i].pages}pp</button>
         <button class="state" data-man="${i}">What it covers</button>`).join("")}</div></div>` : ""}
    ${kin.length ? `<div class="sect"><div class="secthead"><span class="t-title-s">Nearby</span></div>
      <div class="links">${kin.map(o => `<button class="state" data-id="${o.id}">${esc(o.name)}</button>`).join("")}</div></div>` : ""}`;
  link(el);
}

function link(el){
  el.querySelectorAll("[data-id]").forEach(b => b.onclick = () => {
    go("index"); pickOne(b.dataset.id);
    if (!phone()) document.querySelector('.item[aria-current="true"]')?.scrollIntoView({block:"center"});
  });
  el.querySelectorAll("[data-pdf]").forEach(b => b.onclick = () => openPdf(b.dataset.pdf));
  el.querySelectorAll("[data-man]").forEach(b => b.onclick = () => {
    closeSheet(); go("manuals"); S.vol = b.dataset.man; drawShelf();
    document.querySelector(`.vol[data-v="${S.vol}"]`)?.scrollIntoView({block:"center"});
  });
}

/* manuals ---------------------------------------------- */
document.getElementById("manhint").textContent =
  "Nineteen manuals, 387 pages, every step folded into the capabilities below.";

/* the PDFs themselves ----------------------------------- */
const FILES = new Map();                 /* normalised filename -> File        */
const BLOBS = new Map();                 /* manual id          -> object URL   */
const norm = s => String(s).toLowerCase().replace(/\.pdf$/, "")
  .replace(/\(\d+\)$/, "").replace(/[^a-z0-9]/g, "");
let wanted = null;

function manUrl(m){
  if (BLOBS.has(m.id)) return BLOBS.get(m.id);
  const f = FILES.get(norm(m.file));
  if (f){ const u = URL.createObjectURL(f); BLOBS.set(m.id, u); return u; }
  return LOCAL ? encodeURIComponent(m.file) : null;
}
const nAttached = () => M.filter(m => BLOBS.has(m.id) || FILES.has(norm(m.file))).length;

function drawAttach(){
  const n = nAttached();
  const msg = document.getElementById("attachmsg");
  const btn = document.getElementById("attachbtn");
  if (n){
    msg.textContent = n + " of " + M.length + " manuals attached — they open here. "
      + "Nothing was uploaded; the files never leave this browser, and the attachment clears on reload.";
    btn.textContent = n < M.length ? "Attach the rest" : "Attach more";
  } else if (LOCAL){
    msg.textContent = "This copy sits in the same folder as the PDFs, so every manual opens straight away.";
    btn.textContent = "Attach PDFs from elsewhere";
  } else {
    msg.textContent = "The manuals are Contineo’s and are not served from this site. "
      + "Point this page at your own copies once — select all nineteen, or drop the folder here — "
      + "and every manual opens inside the page. Nothing is uploaded.";
    btn.textContent = "Attach the manual PDFs";
  }
}

function openPdf(id){
  const m = byman[id];
  if (!m) return;
  const url = manUrl(m);
  if (!url){ wanted = id; go("manuals"); drawAttach();
    document.getElementById("pickfiles").click(); return; }
  closeSheet();
  document.getElementById("pdftitle").textContent = m.title;
  document.getElementById("pdftab").href = url;
  document.getElementById("pdfbody").innerHTML =
    '<iframe src="' + url + '#view=FitH" title="' + esc(m.title) + '"></iframe>';
  document.getElementById("pdfnote").innerHTML =
    esc(m.file) + " · " + m.pages + " pages. Nothing showing? "
    + '<a href="' + url + '" target="_blank" rel="noopener">Open it in a new tab</a>.';
  document.getElementById("pdfwrap").classList.add("open");
  document.body.classList.add("locked");
  document.getElementById("pdfclose").focus();
}
function closePdf(){
  document.getElementById("pdfwrap").classList.remove("open");
  document.getElementById("pdfbody").innerHTML = "";
  if (!document.getElementById("sheet").classList.contains("open"))
    document.body.classList.remove("locked");
}
const pdfOpen = () => document.getElementById("pdfwrap").classList.contains("open");
document.getElementById("pdfclose").onclick = closePdf;

function take(list){
  for (const f of list) if (/\.pdf$/i.test(f.name)) FILES.set(norm(f.name), f);
  drawAttach(); drawShelf(); drawRead();
  if (wanted){ const id = wanted; wanted = null;
    if (manUrl(byman[id])) openPdf(id); }
}
document.getElementById("attachbtn").onclick = () => document.getElementById("pickfiles").click();
document.getElementById("pickfiles").addEventListener("change", e => {
  take(e.target.files); e.target.value = "";
});
const drop = document.getElementById("v-manuals");
["dragenter","dragover"].forEach(n => drop.addEventListener(n, e => {
  e.preventDefault(); e.dataTransfer.dropEffect = "copy";
}));
drop.addEventListener("drop", e => { e.preventDefault(); take(e.dataTransfer.files); });

function drawShelf(){
  document.getElementById("shelf").innerHTML = M.map(m => {
    const open = S.vol === m.id;
    return `<article class="vol" data-v="${m.id}">
      <div class="volmeta"><span class="badge">${m.id}</span><span class="badge">${m.pages} pages</span>
        ${m.logins.map(l => `<span class="badge">${SHORT[l]}</span>`).join("")}
        ${m.conf ? `<span class="badge">confidential</span>` : ""}</div>
      <h3>${esc(m.title)}</h3>
      <p class="t-body-m">${esc(m.sum)}</p>
      ${open ? `<div class="sect" style="margin-top:2px"><div class="secthead">
        <span class="t-title-s">Documents</span><span class="t-label-m mono">${m.covers.length}</span></div>
        <div class="links">${m.covers.filter(i => byid[i]).map(i =>
          `<button class="state" data-id="${i}">${esc(byid[i].name)}</button>`).join("")}</div></div>` : ""}
      <div class="acts">
        <button class="filled state" type="button" data-pdf="${m.id}">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5"/></svg>Open the PDF</button>
        <button class="tonal state" data-v="${m.id}">${open ? "Hide" : "What it covers"}</button>
      </div>
    </article>`;
  }).join("");
  document.querySelectorAll(".tonal[data-v]").forEach(b => b.onclick = () => {
    S.vol = (S.vol === b.dataset.v) ? null : b.dataset.v; drawShelf();
  });
  link(document.getElementById("shelf"));
}

/* repeated --------------------------------------------- */
document.getElementById("repeats").innerHTML = D.duplicates.map((d,i) => `
  <div class="pair">
    <button class="pairhead state" data-p="${i}" aria-expanded="false">
      <span><span class="t-body-l">${esc(d.label)}</span>
        <span class="itemsub t-body-s">${d.logins.map(l => `<span class="badge">${SHORT[l]}</span>`).join("")}</span></span>
      <span class="trail"><span class="mono t-body-s">${d.ids.length}×</span></span>
    </button>
    <div class="pairbody t-body-m" hidden>
      <p>${esc(d.note || "")}</p>
      <div class="links">${d.ids.filter(i => byid[i]).map(i =>
        `<button class="state" data-id="${i}">${esc(byid[i].name)}</button>`).join("")}</div>
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
  <div class="menu"><h3>${esc(m.label)}</h3>
    <ol>${m.items.map(i => `<li><span>${esc(i)}</span></li>`).join("")}</ol></div>`).join("");
document.getElementById("seq").innerHTML = (D.termsetup || []).map(s =>
  `<tr><td>${s.n}</td><td>${esc(s.act)}</td><td>${esc(s.by)}</td></tr>`).join("");

/* navigation ------------------------------------------- */
function go(name){
  ["index","manuals","repeats","menus"].forEach(n => {
    document.getElementById("v-"+n).hidden = n !== name;
    document.getElementById("t-"+n).setAttribute("aria-selected", String(n === name));
  });
  document.querySelectorAll("[data-dest]").forEach(b =>
    b.setAttribute("aria-selected", String(b.dataset.dest === name)));
  if (name !== "index") closeSheet();
}
document.querySelectorAll(".tab").forEach(t => t.onclick = () => go(t.id.slice(2)));
document.querySelectorAll("[data-dest]").forEach(b => b.onclick = () => {
  go(b.dataset.dest); window.scrollTo({top:0, behavior:"smooth"});
});

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
  const rows = [...document.querySelectorAll(".item")];
  if (!rows.length) return;
  const at = rows.findIndex(r => r.dataset.id === S.pick);
  const next = e.key === "ArrowDown" ? Math.min(at + 1, rows.length - 1) : Math.max(at - 1, 0);
  e.preventDefault();
  S.pick = rows[at < 0 ? 0 : next].dataset.id;
  drawIndex(); drawRead();
  document.querySelector('.item[aria-current="true"]')?.scrollIntoView({block:"nearest"});
});

drawIndex(); drawRead(); drawShelf(); drawAttach();
</script>
</body>
</html>
"""

io.open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(
    HTML.replace("__DATA__", DATA).replace("__LOCAL__", "true" if LOCAL else "false"))
print("site written:", os.path.join(OUT, "index.html"), len(HTML) + len(DATA), "bytes",
      "| local" if LOCAL else "| web")
