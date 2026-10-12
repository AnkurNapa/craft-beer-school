"""Seasonal dressing. Oktoberfest runs until the Brewing Fundamentals batch starts;
the date check below switches everything off by itself after that. To retire it,
empty MASCOT and OKT in pages_a.py."""

UNTIL = "2026-10-18T00:00:00+05:30"

HAT = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 42'%3E"
       "%3Cpath d='M44 25 C50 14 54 8 60 2 C58 10 54 18 47 26Z' fill='%23f3ead2' stroke='%237a5a2b' stroke-width='1'/%3E"
       "%3Cellipse cx='32' cy='35' rx='30' ry='6' fill='%23264d32'/%3E"
       "%3Cpath d='M15 35 C15 16 21 7 32 7 C43 7 49 16 49 35Z' fill='%23356b45'/%3E"
       "%3Cpath d='M15.5 27 H48.5 V32 H15.5Z' fill='%238a5a2b'/%3E"
       "%3Ccircle cx='22' cy='29.5' r='2.2' fill='%23e3a33b'/%3E%3C/svg%3E")

# Runs in <head> so the decorations are on before first paint.
GATE = """<script>try{if(new Date()<new Date('UNTIL')&&!localStorage.getItem('cbs-okt-off'))document.documentElement.classList.add('okt')}catch(e){if(new Date()<new Date('UNTIL'))document.documentElement.classList.add('okt')}</script>""".replace("UNTIL", UNTIL)

# A beer mug in a Bavarian hat that strolls along the bottom of every page and
# links to the enrol form. Closing it is remembered on this browser.
MASCOT = """
<style>
.okt body{overflow-x:clip}
.okt-mascot{display:none}
.okt .okt-mascot{display:block;position:fixed;left:0;bottom:12px;z-index:55;width:64px;animation:okt-walk 26s linear infinite alternate}
.okt-mascot a{display:block;animation:okt-turn 52s steps(1) infinite}
.okt-mascot svg{display:block;width:64px;height:auto;animation:okt-bob .5s ease-in-out infinite alternate;filter:drop-shadow(0 4px 6px rgba(59,36,20,.25))}
.okt-mascot .leg-a{animation:okt-step .5s ease-in-out infinite alternate;transform-origin:18px 66px}
.okt-mascot .leg-b{animation:okt-step .5s ease-in-out infinite alternate-reverse;transform-origin:34px 66px}
.okt-mascot button{position:absolute;top:-6px;right:-6px;width:20px;height:20px;border-radius:50%;border:0;background:#3b2414;color:#fff;font-size:13px;line-height:20px;padding:0;cursor:pointer;opacity:0;transition:opacity .2s}
.okt-mascot button::before{content:"\\00d7"}
.okt-mascot:hover button,.okt-mascot button:focus-visible{opacity:1}
.okt-mascot a:focus-visible{outline:3px solid #2f7fc6;outline-offset:4px;border-radius:8px}
.okt-music{display:none}
.okt .okt-music{display:block;position:fixed;right:14px;bottom:14px;z-index:56;width:44px;height:44px;border-radius:50%;border:2px solid #e0912f;background:#3b2414;color:#fbf3e2;font-size:20px;line-height:40px;padding:0;cursor:pointer;box-shadow:0 4px 10px rgba(59,36,20,.3);transition:transform .15s}
.okt-music::before{content:"\\266B"}
.okt-music[aria-pressed="true"]{background:#e0912f;border-color:#3b2414}
.okt-music[aria-pressed="true"]::before{content:"\\275A\\275A";font-size:12px;letter-spacing:1px}
.okt-music:hover{transform:scale(1.08)}
.okt-music:focus-visible{outline:3px solid #2f7fc6;outline-offset:3px}
@keyframes okt-walk{to{transform:translateX(calc(100vw - 76px))}}
@keyframes okt-turn{50%{transform:scaleX(-1)}}
@keyframes okt-bob{to{transform:translateY(-3px)}}
@keyframes okt-step{from{transform:rotate(-18deg)}to{transform:rotate(18deg)}}
@media(max-width:680px){.okt .okt-music{bottom:78px;right:10px;width:40px;height:40px;line-height:36px}.okt .okt-mascot{bottom:74px;width:38px;animation-duration:18s}.okt-mascot svg{width:38px}.okt-mascot button{opacity:1;width:16px;height:16px;line-height:16px;font-size:11px;top:-4px;right:-8px}@keyframes okt-walk{to{transform:translateX(calc(100vw - 46px))}}}
@media(prefers-reduced-motion:reduce){.okt .okt-mascot,.okt-mascot a,.okt-mascot svg,.okt-mascot .leg-a,.okt-mascot .leg-b{animation:none}.okt .okt-mascot{left:auto;right:16px}}
</style>
<div class="okt-mascot" id="okt-mascot">
  <a href="contact.html?course=Brewing%20Fundamentals#enroll" data-cta="okt-mascot" aria-label="Oktoberfest batch of Brewing Fundamentals starts 17 October: enrol">
    <svg viewBox="0 0 60 80" aria-hidden="true">
      <line class="leg-a" x1="18" y1="66" x2="18" y2="77" stroke="#3b2414" stroke-width="4" stroke-linecap="round"/>
      <line class="leg-b" x1="34" y1="66" x2="34" y2="77" stroke="#3b2414" stroke-width="4" stroke-linecap="round"/>
      <path d="M44 34h5a6 6 0 0 1 6 6v12a6 6 0 0 1-6 6h-5" fill="none" stroke="#7a4a1a" stroke-width="4"/>
      <rect x="8" y="26" width="36" height="42" rx="5" fill="#f0a830" stroke="#7a4a1a" stroke-width="2"/>
      <rect x="13" y="32" width="5" height="30" rx="2.5" fill="#fff" opacity=".35"/>
      <g fill="#fffaf0"><circle cx="13" cy="27" r="6"/><circle cx="22" cy="24" r="7"/><circle cx="32" cy="25" r="6.5"/><circle cx="40" cy="27" r="5"/></g>
      <circle cx="21" cy="42" r="2.4" fill="#3b2414"/><circle cx="33" cy="42" r="2.4" fill="#3b2414"/>
      <path d="M21 50q6 6 12 0" fill="none" stroke="#3b2414" stroke-width="2.2" stroke-linecap="round"/>
      <circle cx="17" cy="48" r="2.5" fill="#e0703a" opacity=".5"/><circle cx="37" cy="48" r="2.5" fill="#e0703a" opacity=".5"/>
      <image href="HAT" x="10" y="0" width="34" height="22"/>
    </svg>
  </a>
  <button type="button" aria-label="Hide the Oktoberfest mascot" onclick="try{localStorage.setItem('cbs-okt-off','1')}catch(e){}document.getElementById('okt-mascot').remove()"></button>
</div>
<button type="button" class="okt-music" id="okt-music" aria-pressed="false" aria-label="Play Oktoberfest music"></button>
<script>
// A home-made oompah loop in C: tuba on beats 1 and 3, brass chords on 2 and 4, a
// polka tune on top. Web Audio only, so nothing to download and no licence.
(()=>{const btn=document.getElementById('okt-music');if(!btn||!(window.AudioContext||window.webkitAudioContext))return;
const E=60/138/2,CH=[[48,52,55],[53,57,60],[55,59,62],[48,52,55],[48,52,55],[53,57,60],[55,59,62],[48,52,55]],
MEL=[67,72,76,72,79,76,72,76,69,72,77,72,81,77,72,77,71,74,79,74,77,74,71,74,72,76,79,76,72,0,72,0,
76,76,79,76,72,72,76,72,77,77,81,77,72,72,77,72,74,79,77,74,71,74,79,74,72,0,67,0,72,0,0,0];
let ctx,out,timer,step=0,at=0;const hz=m=>440*2**((m-69)/12);
function note(m,t,d,type,v){const o=ctx.createOscillator(),g=ctx.createGain();o.type=type;o.frequency.value=hz(m);
g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(v,t+.012);g.gain.exponentialRampToValueAtTime(.001,t+d);
o.connect(g).connect(out);o.start(t);o.stop(t+d+.05)}
function play(i,t){const bar=CH[(i>>3)%8],b=i%8;if(MEL[i%64])note(MEL[i%64],t,E*.9,'sawtooth',.16);
if(b%4==0)note((b?bar[2]:bar[0])-12,t,E*1.6,'triangle',.55);if(b%4==2)bar.forEach(m=>note(m,t,E*.7,'square',.05))}
function tick(){while(at<ctx.currentTime+.25){play(step++,at);at+=E}}
function start(){if(!ctx){ctx=new(window.AudioContext||window.webkitAudioContext)();const lp=ctx.createBiquadFilter();lp.frequency.value=2400;
out=ctx.createGain();out.gain.value=.12;out.connect(lp).connect(ctx.destination)}
ctx.resume();at=ctx.currentTime+.05;timer=setInterval(tick,50);btn.setAttribute('aria-pressed','true');btn.setAttribute('aria-label','Pause Oktoberfest music')}
function stop(){clearInterval(timer);timer=0;if(ctx)ctx.suspend();btn.setAttribute('aria-pressed','false');btn.setAttribute('aria-label','Play Oktoberfest music')}
btn.addEventListener('click',()=>timer?stop():start());
document.addEventListener('visibilitychange',()=>{if(document.hidden&&timer)stop()})})();
</script>
""".replace("UNTIL", UNTIL).replace("HAT", HAT)
