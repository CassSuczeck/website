# Page generator for the Safe Travels site. Edit the content here, run `python3 _tools/build.py`, and commit the regenerated HTML.
import os, html
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
CALC = 'https://tools.besafetravels.com/calculator/'
TEL = 'tel:+19089863415'
SMS = 'sms:+19089863415'
WARRANTY = '/warranty/'
PREVIEW = True  # launch: set to False (drops the site-wide noindex; pages built with noindex=True keep theirs)
MAPS = 'https://www.google.com/maps/d/viewer?mid=1zVy3tcZjMJs6Td0ImW-RaEHxchd74Ag'
# Website form receiver (Apps Script /exec URL; code: CassSuczeck/calculator apps-script/website-receiver.gs).
# Empty = not deployed yet: the forms validate, then tell people to call instead of pretending to send.
FORMS_ENDPOINT = ''

NAV = [('Services', '/services/'), ('Calculator', '/calculator/'), ('Reviews', '/reviews/'),
       ('Appointments', '/appointments/'), ('Contact', '/contact/'), ('About', '/about/'), ('FAQ', '/faq/')]

LD = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"AutoRepair","name":"Safe Travels Mobile Repair","legalName":"Be Safe Travels LLC",
 "url":"https://besafetravels.com/","logo":"https://besafetravels.com/assets/logo.png","telephone":"+1-908-986-3415","email":"info@besafetravels.com",
 "address":{"@type":"PostalAddress","addressLocality":"Port Monmouth","addressRegion":"NJ","postalCode":"07758","addressCountry":"US"},
 "areaServed":["Monmouth County, NJ","Middlesex County, NJ"],
 "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":"08:30","closes":"17:00"}]}
</script>'''

def page(path, title, desc, body, active=None, extra_head='', noindex=False):
    canon = 'https://besafetravels.com' + path
    nav = '\n'.join(
        '      <li><a href="%s"%s>%s</a></li>' % (h, ' aria-current="page"' if n == active else '', n) for n, h in NAV)
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<!-- PREVIEW: at launch set PREVIEW = False and remove the preview banner -->
{'<meta name="robots" content="noindex, nofollow">' if PREVIEW or noindex else ''}
<link rel="canonical" href="{canon}">
<link rel="icon" type="image/png" href="/assets/favicon.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Montserrat:wght@700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
{extra_head}{LD if path == '/' else ''}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site">
  <div class="preview-banner">Preview of the new besafetravels.com. The live site is unchanged.</div>
  <div class="wrap">
    <a class="logo" href="/"><picture><source srcset="/assets/logo.webp" type="image/webp"><img src="/assets/logo.png" width="224" height="48" alt="Safe Travels Mobile Repair, home"></picture></a>
    <nav class="main" aria-label="Main">
      <ul>
{nav}
      </ul>
    </nav>
    <a class="btn" href="/appointments/">Schedule a call</a>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site">
  <div class="wrap">
    <div class="cols">
      <div>
        <h2>Safe Travels Mobile Repair</h2>
        <p>Mobile auto repair based in Port Monmouth, NJ 07758. We come to your home or work across Monmouth County and nearby towns.</p>
        <p><a href="/#where-we-work">Towns we serve</a> · <a href="/cars-we-work-on/">Cars we work on</a> · <a href="/our-tools/">Our tools</a></p>
      </div>
      <div>
        <h2>Contact</h2>
        <p><a href="{TEL}">(908) 986-3415</a> (call or <a href="{SMS}">text</a>)</p>
        <p><a href="mailto:info@besafetravels.com">info@besafetravels.com</a></p>
      </div>
      <div>
        <h2>Hours</h2>
        <p>Calls: 7am to 8pm</p>
        <p>Visits: 8:30am to 5pm, Monday to Saturday</p>
      </div>
    </div>
    <p class="legal">&copy; 2026 Be Safe Travels LLC. All rights reserved. · <a href="/warranty/">Warranty</a> · <a href="/terms-and-conditions/">Terms</a> · <a href="/privacy-policy/">Privacy policy</a></p>
  </div>
</footer>
<aside class="callbar" aria-label="Call or text us">
  <a class="btn" href="{TEL}">Call (908) 986-3415</a>
  <a class="btn alt" href="{SMS}">Text us</a>
</aside>
</body>
</html>
'''
    d = os.path.join(OUT, path.strip('/'))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w').write(doc)

# Shared submit helper for the site's forms. Apps Script can't answer a CORS preflight, so this is a "simple"
# request (text/plain body with JSON inside), which still lets the page read the reply, same as the calculator.
FORMS_JS = """<script>
(function(){
  var ENDPOINT = '%s', OPENED = Date.now(), PHONE = '<a href="tel:+19089863415">(908) 986-3415</a>';
  window.stSend = function(form, payload, okHtml){
    var st = form.querySelector('[role=status]'), btn = form.querySelector('button[type=submit]');
    function say(cls, html){ st.className = 'msg ' + cls; st.innerHTML = html; }
    if (!ENDPOINT) { say('err', 'This is a preview: the form isn’t connected yet. Please call or text ' + PHONE + '.'); return; }
    payload.website = form.querySelector('.trap input').value; // bot trap: people never see this field
    payload.elapsed = Date.now() - OPENED;                     // bots post instantly; the server checks this too
    payload.page = location.pathname;
    var label = btn.textContent; btn.disabled = true; btn.textContent = 'Sending…';
    var ctl = window.AbortController ? new AbortController() : null, timer = ctl && setTimeout(function(){ ctl.abort(); }, 15000);
    fetch(ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, signal: ctl ? ctl.signal : undefined, body: JSON.stringify(payload) })
      .then(function(res){ return res.json(); })
      .then(function(b){
        if (!b || b.result !== 'success') throw new Error((b && b.message) || 'Not saved');
        form.reset(); say('ok', okHtml); btn.textContent = label; btn.disabled = false;
      })
      .catch(function(){ say('err', 'We couldn’t send this. Please try again, or call us at ' + PHONE + '.'); btn.disabled = false; btn.textContent = label; })
      .then(function(){ if (timer) clearTimeout(timer); });
  };
})();
</script>""" % FORMS_ENDPOINT

BTNS = f'''<div class="btn-row">
      <a class="btn" href="{CALC}">Get my estimate</a>
      <a class="btn" href="/appointments/">Schedule a call</a>
      <a class="btn" href="{TEL}">Call (908) 986-3415</a>
    </div>'''

TOWNS = ('Middletown, Holmdel, Hazlet, Keyport, Keansburg, Union Beach, Matawan, Aberdeen, Atlantic Highlands, Highlands, '
         'Rumson, Red Bank, Little Silver, Shrewsbury, Monmouth Beach, Colts Neck, Tinton Falls, Eatontown, Long Branch, Deal, '
         'Ocean Township, Asbury Park, Neptune, Belmar, Wall, Marlboro, Manalapan, Englishtown, Freehold, Old Bridge, '
         'Spotswood, East Brunswick, North Brunswick, New Brunswick, Sayreville, South Amboy, Perth Amboy, Woodbridge, '
         'Metuchen, and Edison')
def town_url(t): return '/mobile-mechanic-%s-nj/' % t.lower().replace(' ', '-')
_t = [t.strip() for t in TOWNS.replace(' and ', ' ').split(',')]
TOWNS_LINKED = ', '.join('<a href="%s">%s</a>' % (town_url(t), t) for t in _t[:-1]) + ', and <a href="%s">%s</a>' % (town_url(_t[-1]), _t[-1])

R_EC = ('Safe Travels was fantastic. They fixed our Volvo XC90 driver’s side visor for $150 less than the dealership and saved us a long wait at the service center. They showed up on time, completed the repair in minutes (less than 15 minutes), and clearly knew exactly what they were doing. Great value, super convenient, and very professional. Highly recommend.',
        'E.C. (Google), sun visor replacement on a Volvo XC90')
R_CW = ('They came to our work location and we didn’t have to drop off the car. Their estimate was quite reasonable, especially given the age of the vehicle and number of issues we were previously enduring. They kept us informed every step of the way. Our car is now running better than it had in almost a decade.',
        'C.W. (Nextdoor), multiple repairs on a Scion xB Release Series 2.0')
R_CH = ('What exceptional service I was provided. So convenient I didn’t have to drive anywhere to leave my vehicle and arrange a ride. Service was provided right outside. Neat, clean, efficient and cost friendly.',
        'C.H. (Google), Jeep Cherokee')
R_DP = ('They did a wonderful job, very courteous and prompt. I loved the way they explained what work was being done and why. Thank you!',
        'D.P. (Nextdoor), tow hitch install on a Chevy Bolt EV')
R_HC = ('I didn’t know it was possible! I always wanted a dash cam but I thought they all required the 12v jack--since I always have a phone charger plugged in, I figured that was the end of the story. But Feather was able to install a dash cam so that it’s hard-wired into the car’s electrical supply, with all the wires hidden neatly behind the trim as if it came from the factory like that. The dash cam just WORKS while I’m driving, and I don’t have to do a thing. A+, 10/10, would recommend to anyone!',
        'Feather’s spouse, Nextbase 622GW dash cam install on a 2019 Honda Civic hatchback')

def review(r):
    return f'''<div class="card"><blockquote class="review"><p>“{r[0]}”</p><footer>{r[1]}</footer></blockquote></div>'''

# ---------------- Home ----------------
page('/', 'Mobile Mechanic in Monmouth County, NJ | Safe Travels',
     'Mobile auto repair at your home or work in Monmouth County and nearby towns, NJ. Free phone consultation; same-day visits often available.',
f'''<section class="hero">
  <div class="wrap">
    <h1>Mobile auto repair in Monmouth County, NJ</h1>
    <p class="lede">We come to your home or work. No shop visit, no towing, no waiting room.</p>
    {BTNS}
    <p class="trust">Fully insured · Written estimate before any work · <a href="{WARRANTY}">Warranty on our work</a></p>
    <p class="small">Prefer to text? <a href="{SMS}">(908) 986-3415</a></p>
  </div>
</section>
<section>
  <div class="wrap narrow">
    <h2>Car care that’s transparent, professional, and convenient</h2>
    <p>Whether you’re juggling school drop-off, a packed work schedule, or getting ready for a road trip, we bring maintenance, diagnostics, repairs, and accessory installs to your driveway. No surprise charges: you get a written estimate before any work begins. On business days, we return every voicemail the same day and can often schedule a diagnostic visit the same day too.</p>
  </div>
</section>
<section class="tint">
  <div class="wrap grid2">
    <div>
      <h2>What we fix</h2>
      <ul class="checks">
        <li>Brakes: pads, rotors, and full brake jobs</li>
        <li>Batteries, alternators, and charging problems</li>
        <li>Check engine lights and no-starts</li>
        <li>Belts, pulleys, and suspension</li>
        <li>Small fixes: bulbs, mirrors, door latches, plus sun visor repair</li>
        <li>Dash cams, tow hitches, and other accessories</li>
        <li>Pre-purchase and multipoint inspections</li>
      </ul>
      <p><a href="/services/">See all services</a></p>
    </div>
    <div>
      <h2>How pricing works</h2>
      <ul class="checks">
        <li><strong>Free phone consultation:</strong> tell us what’s going on, and we’ll give you our best read and a ballpark price.</li>
        <li><strong>Repairs and on-site diagnostics:</strong> $159.99 per hour, one-hour minimum. Diagnostic time is credited toward the repair if you go ahead.</li>
        <li><strong>Small jobs</strong> (a bulb, a mirror): $25 trip fee plus parts and mileage ($1 per mile, round trip, from Port Monmouth), or bundle a few to reach the one-hour minimum and we waive the trip fee and mileage.</li>
      </ul>
      <p><a href="{CALC}">Get a ballpark price for your car</a> · <a href="/faq/">Pricing questions</a></p>
    </div>
  </div>
</section>
<section>
  <div class="wrap grid2">
    <div>
      <h2 id="where-we-work">Where we work</h2>
      <p>We come to you in {TOWNS_LINKED}.</p>
      <p>Don’t see your town? Call or text <a href="{TEL}">(908) 986-3415</a>.</p>
    </div>
    <a class="map" href="{MAPS}"><picture><source type="image/webp" srcset="/assets/service-area-map-490.webp 490w, /assets/service-area-map.webp 1050w" sizes="(max-width: 760px) 92vw, 490px"><img src="/assets/service-area-map.jpg" width="1050" height="1020" loading="lazy" alt="Map of the Safe Travels Mobile Repair service area, about a 30-minute drive from Middletown, NJ: from Woodbridge and Edison south through New Brunswick, East Brunswick, Old Bridge, Marlboro, Manalapan, Freehold, Holmdel, Middletown, Red Bank and Long Branch to Asbury Park, Neptune and Belmar. Opens the interactive map."></picture></a>
  </div>
</section>
<section class="tint">
  <div class="wrap">
    <h2>What customers say</h2>
    <div class="cards">
      {review(R_EC)}
      {review(R_CW)}
      {review(R_CH)}
    </div>
    <p style="margin-top:18px"><a href="/reviews/">Read more reviews</a></p>
  </div>
</section>
<section>
  <div class="wrap">
    <h2>Ready when you are</h2>
    <div class="btn-row">
      <a class="btn" href="{CALC}">Get my estimate</a>
      <a class="btn alt" href="/appointments/">Schedule a call</a>
    </div>
  </div>
</section>''')

# ---------------- Services ----------------
def svc(title, price, intro, items_title, items, why, extra=''):
    li = ''.join(f'<li>{i}</li>' for i in items)
    wy = ''.join(f'<li>{w}</li>' for w in why)
    return f'''<article class="service">
      <h2>{title}</h2>
      <p class="price">{price}</p>
      {intro}
      {f'<h3>{items_title}</h3><ul class="checks">{li}</ul>' if items else ''}
      {extra}
      <h3>Why choose us</h3>
      <ul class="checks">{wy}</ul>
      <a class="btn alt" href="/appointments/">Schedule a consultation</a>
    </article>'''

page('/services/', 'Mobile Auto Repair Services, Middletown NJ | Safe Travels',
     'Mobile auto repair at your home or work in Monmouth County and nearby towns, NJ: quick fixes, inspections and dash cam installs.',
f'''<section>
  <div class="wrap narrow">
    <h1>Services</h1>
    <p class="lede">Prices are starting prices. Same-day availability on business days in most cases: we return voicemails the same day and can often fit in a diagnostic visit the same day too.</p>
    <div class="btn-row"><a class="btn" href="{CALC}">Get my estimate</a><a class="btn alt" href="/appointments/">Schedule a consultation</a></div>
    <div class="card" style="margin:8px 0 12px;">
      <h2 style="font-size:21px;">Facing a big repair on an older car?</h2>
      <p>Our free tool compares the cost of fixing your car with the cost of trading it in for a newer one, in about two minutes.</p>
      <a class="btn alt" href="https://tools.besafetravels.com/fix-or-trade/" target="_blank" rel="noopener">Fix it, or trade it in?<span class="sr-only"> (opens in a new tab)</span></a>
    </div>
    {svc('Common Repairs &amp; Quick Fixes', 'Free phone consult · $159.99/hr (1-hour min.) · Small jobs from $25 + parts',
         '<p><em>We handle the small jobs that are easy to put off but annoying to live with, done at your home or office, no shop visit needed.</em></p><p>Covers: brakes, belts &amp; pulleys, door latches &amp; handles, hood or tailgate that won’t stay open, headlights, taillights, side mirrors, license plate lights, interior lights, and other bulb replacements.</p><p><strong>Sun visor repair</strong> (flapping, won’t stay up, or a visor light that’s stopped working) is priced on its own: about $160 to $500, part included.</p>',
         'How pricing works',
         ['<strong>Free phone consultation:</strong> tell us what’s going on, and we’ll give you our best read and a ballpark price.',
          '<strong>One small job</strong> (a bulb, a mirror, a plate light): $25 trip fee, plus parts and mileage ($1 per mile, round trip, from Port Monmouth).',
          '<strong>Several small jobs:</strong> bundle them to reach the one-hour minimum ($159.99), and we waive the trip fee and mileage.',
          '<strong>Repairs and on-site diagnostics</strong> (like brakes or belts): $159.99 per hour, one-hour minimum. Diagnostic time is credited toward the repair if you go ahead.'],
         ['Small jobs handled quickly, without a shop appointment', 'Quality parts and a clear diagnosis before any work', 'One trip covers multiple small fixes at once'])}
    {svc('Pre-Purchase Inspection', '$59.99',
         '<p class="small">Trip fee and mileage may apply for locations more than a 30-minute drive away.</p><p>Buying a used car? We meet you where the car is, at the seller’s driveway or the lot, and check it over before you commit, so you know what you’re buying.</p>',
         'What we check',
         ['Computer scan for stored and pending trouble codes, plus readiness monitors (they show whether codes were cleared recently)',
          'Engine and transmission: leaks, fluid level and condition, belts and hoses',
          'Brakes, tires (tread and age), suspension and steering', 'Battery and charging system',
          'Rust underneath: frame, subframe and brake lines (New Jersey road salt makes this worth a look)',
          'Lights, wipers, and signs of past body or flood repair', 'A short test drive, when the seller allows it'],
         ['We come to the car; no need to bring it to a shop', 'An independent second opinion before you sign', 'Ask us anything on the spot'],
         '<p><strong>What you get:</strong> a plain-language summary of what we found, what needs attention soon, and what can wait, so you can decide, or ask the seller about price.</p><p class="small"><em>Ask the seller’s permission first; dealerships usually allow an outside inspection on their lot.</em></p>')}
    {svc('Multipoint Vehicle Inspection', '$99.99',
         '<p class="small">Trip fee and mileage may apply for locations more than a 30-minute drive away.</p><p>A full check-up for the car you already drive, at your home or work. We look it over from top to bottom and tell you what’s in good shape, what needs attention soon, and what can wait.</p>',
         'What we check',
         ['Computer scan for trouble codes', 'Fluids: oil, coolant, brake, transmission and power-steering, plus any leaks',
          'Brakes: pads, rotors and lines', 'Tires: tread, wear pattern and pressure', 'Battery and charging system test',
          'Belts, hoses, suspension and steering', 'Lights, wipers and horn', 'Rust underneath: frame, subframe and brake lines'],
         ['Good before a road trip, before winter, after buying a car, or when you’re deciding whether to fix it or trade it in', 'One visit, at your home or work'],
         '<p><strong>What you get:</strong> a prioritized list (now / soon / later) with a price for anything you’d like us to fix.</p><p class="small"><em>This is a mechanical check-up, not the NJ MVC state inspection.</em></p>')}
    {svc('Privacy Upgrades', '$159.99 per hour, one-hour minimum, plus parts',
         '<p>Many newer cars send driving data, such as location, speed, and braking, back to the manufacturer. If you’d rather keep that data private, we can disable it.</p>',
         'We offer',
         ['<strong>DCM (Data Communication Module) removal or bypass:</strong> disables the module that reports your vehicle’s data.',
          '<strong>Cellular antenna bypass:</strong> disconnects the vehicle’s cellular connection so data can’t be transmitted even if the module is left in place.'],
         ['Done correctly, without affecting unrelated systems (infotainment, Bluetooth, and speakers often share wiring with these modules)', 'Clear explanation of what’s being disabled and why'])}
    {svc('Dash Cam, Camera &amp; Custom Electrical Installs', '$159.99 per hour, one-hour minimum, plus parts',
         '<p>Clean, hardwired installs for cameras, lighting, and custom electrical add-ons: no dangling cords, and done properly through your vehicle’s electrical system.</p>',
         'We install',
         ['Dash cams (hardwired, no cigarette-lighter plugs)', 'Backup and rear cameras, rearview screens', 'Winches', 'LED lights and rock lights', 'Custom electrical installs for other accessories'],
         ['Hardwired for a clean look, with no visible cords or loose wiring', 'Installed by a technician who understands your vehicle’s electrical system, not just the accessory', 'One trip covers multiple add-ons at once'])}
  </div>
</section>''', 'Services')

# ---------------- Calculator ----------------
page('/calculator/', 'Repair Cost Estimate | Safe Travels Mobile Repair',
     'Get a ballpark price for common car repairs from Safe Travels Mobile Repair, the mobile mechanic that comes to you in Monmouth County, NJ.',
f'''<section class="hero">
  <div class="wrap narrow">
    <h1>What will my repair cost?</h1>
    <p class="lede">Get a ballpark price for common repairs in about a minute.</p>
    <div class="btn-row"><a class="btn" href="{CALC}">Get my estimate</a></div>
  </div>
</section>''', 'Calculator')

# ---------------- Reviews ----------------
page('/reviews/', 'Customer Reviews | Safe Travels Mobile Repair, Middletown NJ',
     'See what customers say about Safe Travels Mobile Repair’s on-site auto diagnostics, repairs, and dash cam installs across Monmouth County, NJ.',
f'''<section>
  <div class="wrap">
    <h1>Customer reviews</h1>
    <p class="lede">Real recommendations from our customers.</p>
    <div class="cards">
      {review(R_EC)}
      {review(R_CW)}
      {review(R_CH)}
      {review(R_DP)}
      {review(R_HC)}
    </div>
  </div>
</section>''', 'Reviews')

# ---------------- Appointments ----------------
page('/appointments/', 'Book a Mobile Mechanic Visit | Safe Travels Mobile Repair',
     'Book a phone consult or on-site repair with Safe Travels Mobile Repair, serving Middletown, NJ and surrounding Monmouth County towns.',
f'''<section>
  <div class="wrap narrow">
    <h1>Schedule a phone consult</h1>
    <p class="lede">Can’t wait for a slot? On business days, we return voicemails the same day and can often fit in a same-day diagnostic visit. Just call or text <a href="{TEL}">(908) 986-3415</a>.</p>
    <iframe title="Book a phone consultation with Safe Travels (Calendly)" src="https://calendly.com/besafetravelsllc/consultation?hide_event_type_details=1&amp;hide_gdpr_banner=1" style="width:100%;height:760px;border:0;border-radius:12px;background:#fff" loading="lazy"></iframe>
    <p class="small">Calendar not loading? <a href="https://calendly.com/besafetravelsllc/consultation">Open the booking page</a>.</p>
  </div>
</section>''', 'Appointments')

# ---------------- Contact ----------------
page('/contact/', 'Contact Safe Travels Mobile Repair | Middletown, NJ',
     'Text or call (908) 986-3415 to book a mobile mechanic in Middletown, Red Bank & Monmouth County, NJ. We come to your home or workplace.',
f'''<section>
  <div class="wrap grid2">
    <div>
      <h1>Contact us</h1>
      <p class="lede">On business days, we return every voicemail the same day.</p>
      <p><strong>Call or text:</strong> <a href="{TEL}">(908) 986-3415</a></p>
      <p><strong>Email:</strong> <a href="mailto:info@besafetravels.com">info@besafetravels.com</a></p>
      <p><strong>Hours:</strong> calls 7am to 8pm; visits 8:30am to 5pm, Monday to Saturday.</p>
      <p>Want a price first? <a href="{CALC}">Get my estimate</a>.</p>
    </div>
    <form class="card" id="contact" novalidate>
      <h2>Send us a message</h2>
      <div class="field"><label for="c-name">Name (required)</label><input id="c-name" name="name" autocomplete="name" required></div>
      <div class="field"><label for="c-phone">Phone (required)</label><input id="c-phone" name="phone" type="tel" autocomplete="tel" required></div>
      <div class="field"><label for="c-email">Email (optional)</label><input id="c-email" name="email" type="email" autocomplete="email"></div>
      <div class="field"><label for="c-vehicle">Vehicle: year, make and model (required)</label><input id="c-vehicle" name="vehicle" placeholder="e.g. 2015 Honda Accord" required></div>
      <div class="field"><label for="c-town">Town where the car is (required)</label><input id="c-town" name="town" list="c-towns" autocomplete="address-level2" required><datalist id="c-towns">{''.join('<option value="%s">' % t for t in _t)}</datalist></div>
      <div class="field"><label for="c-msg">What’s going on with the car? (required)</label><textarea id="c-msg" name="message" placeholder="e.g. grinding noise when braking, check engine light on" required></textarea></div>
      <div class="trap" aria-hidden="true"><label for="c-web">Leave this empty</label><input id="c-web" name="website" tabindex="-1" autocomplete="off"></div>
      <div id="c-status" role="status" aria-live="polite"></div>
      <p class="small">By sending this, you agree Safe Travels may call or text you about your request. Message and data rates may apply. Reply STOP to opt out. See our <a href="/privacy-policy/">privacy policy</a>.</p>
      <button class="btn" type="submit">Send message</button>
    </form>
  </div>
</section>
{FORMS_JS}
<script>
(function(){{
  var f = document.getElementById('contact'), st = document.getElementById('c-status');
  function say(cls, t){{ st.className = 'msg ' + cls; st.textContent = t; }}
  f.addEventListener('submit', function(e){{
    e.preventDefault();
    var el = f.elements, v = function(n){{ return el[n].value.trim(); }};
    var name = v('name'), phone = v('phone'), email = v('email'), vehicle = v('vehicle'), town = v('town'), msg = v('message');
    if (!name || phone.replace(/\\D/g,'').length < 10 || !vehicle || !town || !msg) {{ say('err', 'Please add your name, a phone number with at least 10 digits, your vehicle, your town, and what’s going on with the car.'); return; }}
    if (email && !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)) {{ say('err', 'Please check your email address, or leave it blank.'); return; }}
    stSend(f, {{ form: 'contact', name: name, phone: phone, email: email, vehicle: vehicle, town: town, message: msg }},
      'Message sent. We’ll call or text you soon. Need us sooner? Call <a href="{TEL}">(908) 986-3415</a>.');
  }});
}})();
</script>''', 'Contact')

# ---------------- About ----------------
page('/about/', 'About Us | Safe Travels Mobile Repair, Middletown NJ',
     'Family-owned mobile auto repair founded by Feather Waters, a technician since 2010, serving Middletown, Red Bank, Holmdel and Hazlet, NJ.',
f'''<section>
  <div class="wrap narrow">
    <h1>Who we are</h1>
    <figure class="founder"><picture><source type="image/webp" srcset="/assets/feather-480.webp 480w, /assets/feather-800.webp 800w" sizes="(max-width: 760px) 92vw, 320px"><img src="/assets/feather.jpg" width="800" height="800" alt="Feather Waters, founder of Safe Travels Mobile Repair, in a Safe Travels work shirt"></picture><figcaption>Feather Waters, founder and technician</figcaption></figure>
    <p class="lede">Safe Travels Mobile Repair is a family-owned mobile auto repair service based in Middletown, NJ, that brings expert and honest auto care to you, on your schedule, so your car and life stay on track.</p>
    <p>We proudly serve drivers within about 30 minutes of Middletown, including Red Bank, Holmdel, and Hazlet.</p>
    <p>Founded by Feather Waters, a seasoned technician who has worked on vehicles since 2010, we specialize in on-site car diagnostics, vehicle inspections, and mobile car repairs that fit your schedule and lifestyle. Feather’s expertise spans from passenger cars to heavy-duty equipment, like semis and excavators. Whether you need a pre-purchase car inspection, help with a check engine light, or a solution for slow-moving windows or electrical issues, she’ll get to the root of the problem and explain it clearly before any work begins.</p>
    <p>Because Feather knows how disruptive car trouble can be, Safe Travels returns every voicemail the same day on business days and, in many cases, can schedule a diagnostic visit the same day.</p>
    <ul class="checks">
      <li>Serving 07758 and surrounding areas</li>
      <li>Mobile safety inspections</li>
      <li>Car diagnostics</li>
      <li>Dash cam and backup camera installation</li>
      <li><a href="/cars-we-work-on/">Cars we work on</a></li>
    </ul>
    <div class="btn-row"><a class="btn" href="/contact/">Contact us</a><a class="btn alt" href="{CALC}">Get my estimate</a></div>
  </div>
</section>''', 'About')


# ---------------- Town pages ----------------
# One page per town in "Where we work". Intros use only plain, checkable facts; Feather reviews them before launch.
# (name, county, intro)
TOWN_PAGES = [
  ('Middletown', 'Monmouth', 'Our home base is Port Monmouth, part of Middletown Township, so Middletown is the area we cover most often. We work in Port Monmouth, Belford, Leonardo, Lincroft and the rest of the township.'),
  ('Holmdel', 'Monmouth', 'Holmdel borders Middletown and is a short drive from our base in Port Monmouth.'),
  ('Hazlet', 'Monmouth', 'Hazlet borders Middletown and is one of the closest towns to our base in Port Monmouth.'),
  ('Keyport', 'Monmouth', 'Keyport is a Bayshore borough a short drive west of our base in Port Monmouth.'),
  ('Keansburg', 'Monmouth', 'Keansburg is a Bayshore borough right next to Port Monmouth, so it’s one of the closest towns we serve.'),
  ('Union Beach', 'Monmouth', 'Union Beach is a Bayshore borough on Raritan Bay, a short drive west of our base in Port Monmouth.'),
  ('Matawan', 'Monmouth', 'Matawan is a short drive west of our base in Port Monmouth, along the Bayshore.'),
  ('Aberdeen', 'Monmouth', 'Aberdeen Township, including Cliffwood and Strathmore, is a short drive west of our base in Port Monmouth.'),
  ('Atlantic Highlands', 'Monmouth', 'Atlantic Highlands sits on Sandy Hook Bay, a short drive east of our base in Port Monmouth.'),
  ('Highlands', 'Monmouth', 'Highlands sits at the foot of the bridge to Sandy Hook, a short drive east of our base in Port Monmouth.'),
  ('Rumson', 'Monmouth', 'Rumson sits between the Navesink and Shrewsbury rivers, within our usual service area.'),
  ('Red Bank', 'Monmouth', 'Red Bank is a short drive from our base in Port Monmouth. If you work downtown, we can fix your car in your work lot while you’re at your desk.'),
  ('Little Silver', 'Monmouth', 'Little Silver, just southeast of Red Bank, is within our usual service area.'),
  ('Shrewsbury', 'Monmouth', 'Shrewsbury, just south of Red Bank, is within our usual service area.'),
  ('Monmouth Beach', 'Monmouth', 'Monmouth Beach, on the ocean just north of Long Branch, is within our service area.'),
  ('Colts Neck', 'Monmouth', 'Colts Neck is within our usual service area. On a farm or a long driveway, we come to wherever the car is parked.'),
  ('Tinton Falls', 'Monmouth', 'Tinton Falls is within our usual service area, at your home or at work.'),
  ('Eatontown', 'Monmouth', 'Eatontown is within our usual service area, at your home or at work.'),
  ('Long Branch', 'Monmouth', 'Long Branch, on the oceanfront, is within our service area.'),
  ('Deal', 'Monmouth', 'Deal, on the oceanfront just south of Long Branch, is within our service area.'),
  ('Ocean Township', 'Monmouth', 'Ocean Township, including Oakhurst and Wanamassa, is within our service area.'),
  ('Asbury Park', 'Monmouth', 'Asbury Park, on the shore, is within our service area.'),
  ('Neptune', 'Monmouth', 'Neptune Township, including Ocean Grove, is within our service area, just south of Asbury Park.'),
  ('Belmar', 'Monmouth', 'Belmar, on the shore, is at the southern edge of our service area.'),
  ('Wall', 'Monmouth', 'Wall Township is at the southern edge of our service area.'),
  ('Marlboro', 'Monmouth', 'Marlboro is within our service area, west of Holmdel.'),
  ('Manalapan', 'Monmouth', 'Manalapan, southwest of Marlboro, is at the western edge of our service area.'),
  ('Englishtown', 'Monmouth', 'Englishtown, a small borough surrounded by Manalapan, is at the western edge of our service area.'),
  ('Freehold', 'Monmouth', 'Freehold Borough, the Monmouth County seat, and the nearby parts of Freehold Township are at the southwestern edge of our service area.'),
  ('Old Bridge', 'Middlesex', 'Old Bridge, just over the Middlesex County line, is within our service area.'),
  ('Spotswood', 'Middlesex', 'Spotswood, a borough next to East Brunswick, is within our service area.'),
  ('East Brunswick', 'Middlesex', 'East Brunswick, along the New Jersey Turnpike in Middlesex County, is within our service area.'),
  ('North Brunswick', 'Middlesex', 'North Brunswick, just southwest of New Brunswick, is at the western edge of our service area.'),
  ('New Brunswick', 'Middlesex', 'New Brunswick, the Middlesex County seat on the Raritan River, is at the western edge of our service area.'),
  ('Sayreville', 'Middlesex', 'Sayreville, including Parlin and Morgan, is within our service area in Middlesex County.'),
  ('South Amboy', 'Middlesex', 'South Amboy, on Raritan Bay across the river from Perth Amboy, is within our service area in Middlesex County.'),
  ('Perth Amboy', 'Middlesex', 'Perth Amboy, at the mouth of the Raritan River, is within our service area in Middlesex County.'),
  ('Woodbridge', 'Middlesex', 'Woodbridge Township, including Iselin, Colonia, Fords and Avenel, is within our service area in Middlesex County.'),
  ('Metuchen', 'Middlesex', 'Metuchen, a borough surrounded by Edison, is within our service area.'),
  ('Edison', 'Middlesex', 'Edison Township is within our service area in Middlesex County.'),
]
for town, county, p1 in TOWN_PAGES:
    p2 = 'Distances beyond a 30-minute drive add $1 per mile, round trip; call and we’ll tell you before we book.' if 'edge' in p1 else 'We come to your driveway or work lot, so you don’t lose a day to the shop.'
    page(town_url(town), f'Mobile Mechanic in {town}, NJ | Safe Travels',
         f'Mobile auto repair at your home or work in {town}, NJ: diagnostics, brakes, inspections and quick fixes. Free consult. Call (908) 986-3415.',
f"""<section>
  <div class="wrap narrow">
    <h1>Mobile mechanic in {town}, NJ</h1>
    <p class="lede">Safe Travels Mobile Repair comes to you in {town}. No shop visit, no towing, no waiting room.</p>
    <p>{p1} {p2}</p>
    <h2>What we do in {town}</h2>
    <ul class="checks">
      <li>Check engine lights and on-site diagnostics</li>
      <li>Brake pads, rotors and full brake jobs</li>
      <li>Pre-purchase inspections ($59.99) and multipoint inspections ($99.99)</li>
      <li>Bulbs, mirrors, latches and other quick fixes, plus sun visor repair</li>
      <li>Dash cam, backup camera and tow hitch installs</li>
    </ul>
    <p><a href="/services/">See all services and prices</a> · <a href="/cars-we-work-on/">Cars we work on</a></p>
    <h2>How pricing works</h2>
    <p>The phone consultation is free. Repairs and on-site diagnostics are $159.99 per hour with a one-hour minimum, plus parts, and diagnostic time is credited toward the repair. You get a written estimate before any work begins.</p>
    {BTNS}
  </div>
</section>""")

# ---------------- Cars we work on (makes; keep in sync with the calculator's BRAND_TIER) ----------------
def makes(*m): return ', '.join(m)
page('/cars-we-work-on/', 'Cars We Work On: Makes & Years | Safe Travels',
     'Mobile repair for domestic, Japanese, Korean and European cars, model year 1996 and newer, plus Maserati. See which makes we service in Monmouth County.',
f"""<section>
  <div class="wrap narrow">
    <h1>Cars we work on</h1>
    <p class="lede">We work on most gas and hybrid cars, SUVs, trucks and vans from model year 1996 on, domestic and imported.</p>
    <h2>American</h2>
    <p>{makes('Buick','Cadillac','Chevrolet','Chrysler','Dodge','Ford','GMC','Hummer','Jeep','Lincoln','Mercury','Oldsmobile','Plymouth','Pontiac','Ram','Saturn')}</p>
    <h2>Japanese and Korean</h2>
    <p>{makes('Acura','Genesis','Honda','Hyundai','Infiniti','Isuzu','Kia','Lexus','Mazda','Mitsubishi','Nissan','Scion','Subaru','Suzuki','Toyota')}</p>
    <h2>European</h2>
    <p>{makes('Alfa Romeo','Audi','BMW','Fiat','Jaguar','Land Rover','Maserati','Mercedes-Benz','Mini','Porsche','Saab','Smart','Volkswagen','Volvo')}</p>
    <p class="small">For imported makes, work varies a lot from model to model, so we confirm the price after a look.</p>
    <h2>Where we refer you to a specialist</h2>
    <ul class="checks">
      <li><strong>Electric vehicles:</strong> we do tow hitch and accessory installs, and in some cases brakes, suspension and interior work. For anything else, we’ll point you to a shop that does.</li>
      <li><strong>Cars older than model year 1996</strong>, before standard OBD-II diagnostics.</li>
      <li><strong>Exotics</strong> such as Ferrari, Lamborghini, Bentley, Rolls-Royce, Aston Martin, McLaren and Lotus, and Maserati’s MC20 and MCPura.</li>
    </ul>
    <p>Not sure about your car? Call or text <a href="{TEL}">(908) 986-3415</a>.</p>
    {BTNS}
  </div>
</section>""")

# ---------------- Our Tools (to-do 16; copy from calculator repo docs/brands-page-draft.md, names only, no logos) ----------------
page('/our-tools/', 'Professional Tools & Factory Diagnostics | Safe Travels',
     'Safe Travels Mobile Repair brings shop-grade tools, professional scan tools and factory service software to your driveway in Monmouth County, NJ.',
f"""<section>
  <div class="wrap narrow">
    <h1>The tools we bring to your driveway</h1>
    <p class="lede">A mobile mechanic is only as good as the tools in the van. We carry the same professional brands you’d find in a well-equipped shop, plus the diagnostic software that lets us read your car the way its maker intended.</p>
    <h2>Hand tools and storage</h2>
    <p>Snap-on · Matco · Gearwrench · OTC · Knipex · Craftsman · Kobalt · Husky</p>
    <h2>Power tools</h2>
    <p>Milwaukee · DEWALT</p>
    <h2>Scan tools and diagnostics</h2>
    <p>Autel · Topdon · TEXA · Nexiq</p>
    <p>From a check engine light to a module that needs programming, professional scan tools let us find the cause instead of guessing, so you pay for the repair you need.</p>
    <h2>Factory service information and software</h2>
    <p>When a job needs the manufacturer’s own procedures or software, we use it:</p>
    <ul class="checks">
      <li><strong>BMW Group:</strong> BMW, BMW Motorrad and MINI</li>
      <li><strong>Audi:</strong> erWin and ODIS</li>
      <li><strong>Volkswagen:</strong> erWin and ODIS</li>
      <li><strong>General Motors Europe:</strong> Chevrolet, Opel, Vauxhall and GM Korea vehicles</li>
      <li><strong>Honda</strong></li>
      <li><strong>Jaguar</strong></li>
      <li><strong>Maserati</strong> (TechInfo)</li>
      <li><strong>Mercedes-Benz</strong></li>
      <li><strong>Saab</strong></li>
    </ul>
    <h2>Secure Gateway access</h2>
    <p>Many newer vehicles lock their diagnostic port behind a security gateway. We’re registered with <strong>AutoAuth</strong>, so we can unlock it and work on those vehicles properly.</p>
    <h2>And more</h2>
    <p>This list grows as we take on new jobs. Not sure we can work on your vehicle? See <a href="/cars-we-work-on/">Cars we work on</a>, or call us at <a href="{TEL}">(908) 986-3415</a> and ask.</p>
    {BTNS}
    <p class="small">Brand names are trademarks of their respective owners. Their use here describes the tools and software we use and doesn’t imply endorsement or sponsorship.</p>
  </div>
</section>""")

# ---------------- FAQ ----------------
def q(qq, a): return f'<details><summary>{qq}</summary><div class="answer"><p>{a}</p></div></details>'
page('/faq/', 'FAQ: Pricing & Service Area | Safe Travels Mobile Repair',
     'How mobile repair pricing works at Safe Travels: free phone consults, on-site diagnostics, small-job fees, service area and hours.',
f'''<section>
  <div class="wrap narrow">
    <h1>Frequently asked questions</h1>
    <p class="lede">Can’t find your answer? Call us at <a href="{TEL}">(908) 986-3415</a>. Calls are answered from 7am to 8pm.</p>
    <h2 style="margin-top:28px">Pricing</h2>
    {q('Is the diagnosis free?', 'The phone consultation is. Call us, describe the problem, and we’ll tell you what we think it is and roughly what it costs. If we need to come out and test the car, on-site diagnostics are $159.99 per hour with a one-hour minimum, credited toward the repair if you go ahead.')}
    {q('Is there a minimum charge?', 'Yes. Repairs have a one-hour labor minimum ($159.99), plus parts. There are two exceptions. Oil changes start at $80 plus parts. A single small job, like a bulb or a wiper, is a $25 trip fee plus parts and mileage ($1 per mile, round trip, from Port Monmouth).')}
    {q('Can you come out for something small, like a headlight bulb?', 'Yes. A single small job is a $25 trip fee, plus parts and mileage ($1 per mile, round trip, from our base in Port Monmouth). If you have a few small things, bundle them: once the work reaches the one-hour minimum, the trip fee and mileage are waived.')}
    {q('How do I get a price before you come out?', f'Use our <a href="{CALC}">repair cost estimator</a> for a ballpark price in about a minute, or call us. Before we begin any work, you’ll receive a written estimate.')}
    {q('Why does the price depend on my car?', 'Age, size, and make change how long a job takes. An older or larger vehicle, or one with a more complex layout, usually takes more labor. Our estimator adjusts for that, and we confirm the price once we see the car.')}
    {q('Can there be additional charges after the estimate?', 'Sometimes. Once work begins, a repair can turn out to need more than the first estimate covered, for example an engine wash. We only do an engine wash as part of a larger repair, when the job needs it. Added work and its price can come up any time between your first estimate and the finished job, and prices for it can change. Before we go over your written estimate, we always ask for your OK in writing.')}
    <h2 style="margin-top:36px">Service and scheduling</h2>
    {q('Where do you work?', 'At your home or office, within about 30 minutes of Middletown and Port Monmouth, NJ (07758). Not sure if you’re in range? Call and ask. Beyond 30 minutes (drive time by Google Maps), we charge $1 per mile, round trip, for the whole trip.')}
    {q('What are your hours?', 'We answer calls from 7am to 8pm. On-site visits are from 8:30am to 5pm, Monday to Saturday. If that doesn’t work for your schedule, we can arrange an after-hours visit for an additional fee.')}
    {q('Do you do oil changes?', 'Sometimes. An oil change is usually best done on a lift, so we generally recommend your dealer or an independent shop with lifts. In some cases, we can do it in your driveway, starting at $80 plus parts. Ask us when you call, and we’ll tell you if yours is one of them.')}
    {q('What vehicles do you work on?', 'Most gas and hybrid cars, SUVs, trucks, and vans, domestic and imported, including Maserati, from model year 1996 on.')}
    {q('Do you work on electric vehicles?', 'Only some jobs: tow hitch installs, accessory installs, and, in some cases, brakes, suspension, and interior work. For anything else, call us, and we’ll refer you to a shop that does.')}
    {q('Do you work on older cars?', 'Yes, any gas or hybrid vehicle from model year 1996 on, when standard diagnostic systems (OBD-II) arrived. For cars older than 1996, call us, and we’ll refer you to a shop that specializes in them.')}
    {q('Do you work on exotic cars?', 'Some exotic cars need a specialty shop; for example, Ferrari, Lamborghini, Rolls-Royce, and Maserati’s MC20. Call us, and we’ll refer you to a specialty shop.')}
    {q('How do I book?', f'<a href="/appointments/">Schedule a call</a>, <a href="{SMS}">text</a>, or call us at <a href="{TEL}">(908) 986-3415</a>.')}
  </div>
</section>''', 'FAQ')

# Follows the live Squarespace privacy policy (Chrome capture 2026-10-24), changed only where the new site works
# differently: GitHub hosts it, no Squarespace cookies/statistics, no reCAPTCHA, no Weglot, forms go to our Google Sheet.
# If the launch site adds analytics, a language menu or a new form service, update "What's collected automatically"
# and "Who else handles it". Owner and, ideally, an NJ attorney review the wording before launch.
page('/privacy-policy/', 'Privacy Policy | Safe Travels Mobile Repair',
     'What Safe Travels Mobile Repair collects on this website, by phone and by text, why, and how to ask us to delete it. We never sell your information.',
f'''<section><div class="wrap narrow">
<h1>Privacy policy</h1>
<p class="lede">Be Safe Travels LLC, doing business as Safe Travels Mobile Repair (“we”, “us”), runs this website and our tools at tools.besafetravels.com. We collect only what we need to answer you and fix your car. We never sell your information.</p>
<h2>What we collect</h2>
<h3>What you give us</h3>
<ul>
<li><strong>Forms on this site:</strong> the contact form asks for your name, phone number, email, your vehicle, your town, and what’s going on with it. The forms on our <a href="/terms-and-conditions/">Terms and Conditions</a> page ask for your first and last name and record that you agreed.</li>
<li><strong>Repair estimate calculator and “Fix it, or trade it in?” tool</strong> (tools.besafetravels.com): if you ask us to contact you, your name, phone, email, your vehicle and the estimate. If you enter a VIN, your browser sends it to the U.S. government’s free NHTSA vehicle lookup to find the year, make and model.</li>
<li><strong>Booking:</strong> what you enter when you schedule a call through Calendly.</li>
<li><strong>Calls and texts:</strong> your phone number and what you tell us.</li>
</ul>
<h3>What’s collected automatically</h3>
<ul>
<li><strong>Hosting:</strong> GitHub, which hosts this website and our tools, logs visits like any web host (for example your IP address, browser, and the pages requested).</li>
<li><strong>Fonts:</strong> this site loads its fonts from Google Fonts, so Google receives your IP address when the fonts load.</li>
<li><strong>Booking page:</strong> our booking page shows Calendly’s scheduler, which may set its own cookies.</li>
<li><strong>Spam protection:</strong> our forms use a hidden field and a timing check to tell people from bots. They don’t track you.</li>
</ul>
<p>This site itself doesn’t set cookies or keep visitor statistics. We don’t take payments on this website, and we don’t ask for Social Security, driver’s license or card numbers here.</p>
<h2>How we use it</h2>
<p>To answer your request, give you a price, schedule and do the work, follow up about that work, honor our warranty, and keep the site working and free of spam. We don’t send marketing texts.</p>
<h2>Who else handles it</h2>
<p>We don’t sell your information or share it for advertising. A few services help us run the business and handle it for us, not for their own marketing:</p>
<ul>
<li><strong>GitHub:</strong> hosts this website and tools.besafetravels.com.</li>
<li><strong>Google:</strong> our business email, the spreadsheet where form and tool requests arrive, Google Fonts, and Google Voice (our business phone line, for calls and texts).</li>
<li><strong>Calendly:</strong> booking.</li>
<li>The software we use for estimates and invoices.</li>
<li><strong>Carfax:</strong> after a repair, we report the vehicle’s service record (VIN, mileage and the work done) to Carfax’s vehicle history, without your name or contact details.</li>
</ul>
<p>We may also share information if the law requires it, or to protect our rights or someone’s safety.</p>
<h2 id="texts">Calls and texts</h2>
<p>When you text us, or give us your number on a form and agree to be contacted, we may call or text you about your request: replies, estimates, scheduling, arrival times, and follow-up on the work. How often depends on the job. Message and data rates may apply. Reply STOP to stop texts, or HELP for help. Agreeing to texts is not a condition of buying anything from us.</p>
<p>We never sell or share your mobile number or your text consent with anyone for their marketing.</p>
<h2>Cookies: your choices</h2>
<p>This site doesn’t set cookies itself. Calendly’s scheduler on our booking page may; you can block or clear cookies in your browser settings. Blocking some cookies may stop the scheduler from working.</p>
<h2>How long we keep it</h2>
<p>As long as we need it to do the work, stand behind it, and keep the business, tax and repair records the law requires. Then we delete it.</p>
<h2>Keeping it safe</h2>
<p>We limit who can see your information and use services with secure (HTTPS) connections. No website is perfectly secure, so please don’t send sensitive details like card numbers by form, email or text.</p>
<h2>Children</h2>
<p>This site is for adults. We don’t knowingly collect information from children under 13.</p>
<h2>Your choices</h2>
<p>To see, correct, or delete what we have about you, call or text <a href="{TEL}">(908) 986-3415</a> or email <a href="mailto:info@besafetravels.com">info@besafetravels.com</a>. We’ll answer within 30 days. We may need to keep some records the law requires.</p>
<h2>Changes</h2>
<p>If we change this policy, we’ll post the new version here with a new date.</p>
<p class="small">Be Safe Travels LLC · Port Monmouth, NJ 07758 · <a href="{TEL}">(908) 986-3415</a> · <a href="mailto:info@besafetravels.com">info@besafetravels.com</a><br>Last updated: October 2026</p>
</div></section>''')

# ---------------- Warranty and Terms: follow the LIVE Squarespace pages (Feather, 2026-10-24) ----------------
# Text copied word for word from besafetravels.com/warranty and /terms-and-conditions (Chrome capture
# "live-warranty-terms-text-2026-10-24", Drive). The live Terms differ slightly from the printed "BST T&C 07.30.2026"
# (e.g. "By signing any document with us"); the live wording wins here. Warranty stays out of search after launch.
TERMS_SOURCE = 'besafetravels.com, captured October 24, 2026'
TERMS_VERSION_ID = 'live-2026-10-24'  # sent with each "I agree"; change when the terms text changes
def agree_form(kind, title):
    # Same fields, checkbox and button as the live Squarespace forms. Posts through stSend (FORMS_JS).
    statement = f'I have read and agree to the {title}. I understand that submitting a service request does not authorize work on my vehicle.'
    k = kind[0]
    return f'''<form class="card agree" id="agree-{kind}" data-terms="{kind}" novalidate>
  <h3>Agree to the {title}</h3>
  <fieldset><legend>Name (required)</legend>
    <div class="field"><label for="{k}-first">First Name</label><input id="{k}-first" name="first" autocomplete="given-name" required></div>
    <div class="field"><label for="{k}-last">Last Name</label><input id="{k}-last" name="last" autocomplete="family-name" required></div>
  </fieldset>
  <div class="field check"><input type="checkbox" id="{k}-ok" name="ok" required><label for="{k}-ok">{html.escape(statement)}</label></div>
  <div class="trap" aria-hidden="true"><label for="{k}-web">Leave this empty</label><input id="{k}-web" name="website" tabindex="-1" autocomplete="off"></div>
  <div role="status" aria-live="polite"></div>
  <button class="btn" type="submit">I agree</button>
</form>'''
AGREE_JS = '''<script>
(function(){
  document.querySelectorAll('form.agree').forEach(function(f){
    f.addEventListener('submit', function(e){
      e.preventDefault();
      var st = f.querySelector('[role=status]'), first = f.elements.first.value.trim(), last = f.elements.last.value.trim(), ok = f.elements.ok;
      if (!first || !last || !ok.checked) { st.className = 'msg err'; st.textContent = 'Please add your first and last name and tick the box.'; return; }
      stSend(f, { form: 'terms', terms: f.dataset.terms, first: first, last: last, accepted: true,
                  statement: ok.labels[0].textContent, version: '%s' },
        'Thank you, ' + first.replace(/[<>&"]/g, '') + '. Your agreement is recorded.');
    });
  });
})();
</script>''' % TERMS_VERSION_ID
WEBSITE_TERMS = [
 ('b', 'These Website Terms apply to your use of this website and to service requests you submit through it. They do not, by themselves, authorize us to inspect, diagnose, repair, or perform other work on your vehicle.'),
 ('p', 'By checking the box labeled “I agree to the Website Terms” or otherwise affirmatively accepting these Terms when submitting a service request, you agree that:'),
 ('lp', 'Service requests are not repair authorization.', 'A request for an appointment, estimate, inspection, or service does not authorize us to begin work.'),
 ('lp', 'We will obtain separate authorization before work begins.', 'Before performing chargeable diagnostic or repair work, we will provide the applicable estimate or price and obtain your authorization in the manner required by law. Any authorization will be limited to the work and price or maximum amount you approve.'),
 ('lp', 'Additional work requires additional approval.', 'We will not perform work beyond the authorized scope or charge more than the authorized amount without obtaining your further approval, except as permitted by law.'),
 ('lp', 'You must be authorized to approve the work.', 'You represent that you own the vehicle or are authorized by its owner to request and approve the services.'),
 ('lp', 'Website information is not a final estimate.', 'Any prices, descriptions, availability, or timing shown on the website are informational unless we expressly confirm them in a written estimate or service authorization.'),
 ('lp', 'Separate service documents control the work.', 'The estimate, repair order, invoice, or other service authorization that you approve for a particular visit governs the scope and price of that service. These Website Terms do not replace that authorization.'),
]
SERVICE_TERMS = [
 ('h3', 'Authorization'),
 ('p', 'By signing any document with us, the undersigned customer (“you” or the “customer”) expressly authorizes Be Safe Travels LLC (“BST”) to perform and provide the services, repairs, and/or upgrades as listed in this Estimate, along with all parts and labor necessary (the “Services”). Customer agrees that BST has gone over the cost of the Services and customer gives express authorization and consent to BST to provide such Services. Customer authorizes BST, at customer’s risk, to operate the vehicle for purposes of testing, inspection, or delivery.'),
 ('h3', 'Limited Warranty; Limitations'),
 ('p', 'Labor is covered by BST’s warranty of 90 days or 3,000 miles, whichever comes first. The aforementioned warranty is limited to the labor set forth on this Estimate only. BST’s performance under the aforementioned warranty shall be limited to, at BST’s sole discretion a) re-repair and/or replacement of parts or b) a refund to Customer of the monies paid under this Estimate. To honor the aforementioned warranty, the vehicle and any faulty parts must be made available to BST for inspection at a time and location designated by BST, at customer’s expense. Customer-supplied parts, customer neglect, misuse, modification, alteration, abuse, unreasonable use, or damage caused by improper maintenance, use of the vehicle for racing or for off-road purposes, and pre-existing conditions are excluded from the aforementioned warranty. Parts are warranted according to manufacturer specifications, and to the extent permitted under said warranty, BST hereby assigns said manufacturer warranty to the undersigned. THE FOREGOING IS BST’S EXCLUSIVE WRITTEN WARRANTY ON LABOR AND STATES CUSTOMER’S EXCLUSIVE REMEDY FOR THAT LABOR. TO THE EXTENT PERMITTED BY LAW, ANY IMPLIED WARRANTIES ARE LIMITED IN DURATION TO THE WARRANTY PERIOD STATED ABOVE. BST DOES NOT DISCLAIM, AND NOTHING IN THESE TERMS DISCLAIMS, ANY IMPLIED WARRANTY THAT MAY NOT BE DISCLAIMED OR LIMITED UNDER THE MAGNUSON-MOSS WARRANTY ACT, 15 U.S.C. § 2301 ET SEQ., OR NEW JERSEY LAW. SOME OF THESE LIMITATIONS MAY NOT APPLY TO CUSTOMER UNDER NEW JERSEY LAW.'),
 ('h3', 'Limitation of Liability'),
 ('p', 'BST’S TOTAL LIABILITY IS LIMITED TO THE COST OF PARTS AND LABOR PROVIDED UNDER THIS ESTIMATE. BST is not responsible for costs of substitute transportation, transportation expenses, compensation for inconvenience or loss of use, the cost of a rental car, reimbursement for time off work, loss of income, towing charges, loss of revenue, legal fees and costs, or any consequential or incidental damages. BST is not responsible for cosmetic damage (such as tool marks, scratches, or wear near bolt heads and components), or secondary issues, failures, or problems that arise as a result of the Services. BST is not liable for damage to the vehicle caused by customer negligence, misuse, damage, wear and tear, or failure to follow maintenance recommendations. BST is not responsible for, or liable for, any claims, damages, costs, expenses, or losses unrelated to the Services provided under this Estimate. BST is not responsible if a manufacturer or third-party warranty is voided as a result of the provision of the Services. Customer agrees that customer is responsible for loss or damage to the vehicle and to articles left in the vehicle, in the event of fire, theft, accident, or other cause beyond BST’s direct control. Notwithstanding the foregoing, nothing in these Terms limits or excludes BST’s liability for personal injury, or for property damage, to the extent caused by BST’s own negligence, gross negligence, recklessness, or willful misconduct; for any liability that may not lawfully be limited or excluded under the New Jersey Consumer Fraud Act, N.J.S.A. 56:8-1 et seq.; or for any other right that may not be waived or limited under New Jersey or federal law. The limitations and exclusions in this section apply only to the maximum extent permitted by New Jersey law.'),
 ('p', 'WARNING. If BST installed any video, navigational, cruise control, or other add-on equipment in Customer’s vehicle, then Customer assumes the risk of any accidents or injuries caused by using any such equipment if such use is not in conformity with the equipment manufacturer\'s safety precautions and recommendations. Further, BST assumes no liability for such accidents or injuries.'),
 ('h3', 'Supplied Parts'),
 ('p', 'All parts supplied by BST are new unless expressly set forth in the Estimate.'),
 ('h3', 'Replaced Parts'),
 ('p', 'Unless Customer requests the return of replaced parts before work is commenced, Customer waives the return of any parts removed or replaced by BST. Parts that are sold on an exchange basis, and parts that BST is required to return to a manufacturer or distributor, are not subject to return. BST need not return parts that, by virtue of their size, weight, or similar factors, are impractical to return.'),
 ('h3', 'Time of Service'),
 ('p', 'Customer acknowledges that the turnaround time varies depending upon the complexity of the work, current workload, and delays beyond our control. Any delay in service estimate time table will not subject BST to any liability.'),
 ('h3', 'Payment'),
 ('p', 'Payment in full is due upon completion of the Services set forth in the Estimate, provided that Customer shall make a 50% deposit upon execution of this Estimate. There are no refunds on installed tires, wheels, discontinued items, or on any special orders. All returned parts are subject to a 15% handling charge. If Customer cancels after executing this Estimate, BST may retain from the deposit the cost of any parts already ordered (subject to the 15% handling charge if returnable, or the full price if non-returnable, discontinued, or special-order) plus the value of any labor already performed, and BST shall refund the balance of the deposit to Customer. Customer agrees that customer has inspected the vehicle and by making final payment on the Estimate, customer acknowledges and agrees that the Services were performed satisfactorily to customer. This acknowledgment does not waive Customer’s rights under BST’s written warranty above, for latent defects not reasonably discoverable on inspection, or under the New Jersey Consumer Fraud Act, N.J.S.A. 56:8-1 et seq.'),
 ('h3', 'Estimate'),
 ('p', 'This Estimate is the written price estimate for the Services for purposes of N.J.A.C. 13:45A-26C.2(a)(3). BST will not perform, and will not charge for, any work or parts in excess of this Estimate until BST has obtained Customer’s authorization for the additional work and cost. If that authorization is given orally, BST will note on the repair order or invoice the date, the time, the name of the person authorizing the additional work, the telephone number called, and the additional parts, labor, and total additional cost, consistent with N.J.A.C. 13:45A-26C.2(a)(6). Customer authorizes BST to contact Customer at the telephone number provided on this Estimate for this purpose.'),
 ('h3', 'Property Access; Permission to Enter; Indemnification'),
 ('p', 'Customer represents and warrants that Customer owns, or has full authority and all permissions and consents necessary, to authorize BST and its personnel to enter and perform the Services at the location where the vehicle is located, including any private property, driveway, parking area, common or shared area, gated or guard-controlled community, condominium or homeowners-association property, apartment or multi-unit complex, employer or commercial lot, and any garage or covered structure (the “Work Location”). Customer grants BST a limited license to enter the Work Location and to move and operate the vehicle as reasonably necessary to perform the Services. Customer is responsible for arranging and providing all access BST needs to reach the vehicle, including gate codes, guard or gatehouse clearance, keys, fobs, parking authorization, and compliance with the rules of any property owner, landlord, or association; and Customer is responsible for any fee, fine, assessment, or penalty that any such third party imposes as a result of BST’s permitted access to or performance at the Work Location, except to the extent arising from BST’s own negligence or willful misconduct. Customer represents that the Work Location is reasonably suitable for the Services and will identify any known condition that could affect the safety of the Services or be susceptible to damage (for example, soft, cracked, sloped, or coated pavement). Customer assumes the risk of, and BST is not responsible for, damage to the surface or condition of the Work Location arising from the ordinary and proper performance of the Services or from pre-existing conditions, except to the extent caused by BST’s negligence. To the fullest extent permitted by law, Customer shall indemnify, defend, and hold harmless BST from any third-party claim, demand, fine, or loss arising out of (a) Customer’s lack of authority or permission to grant access to the Work Location, or (b) BST’s access to or presence at the Work Location at Customer’s direction; provided that this indemnity does not extend to any claim to the extent it arises from BST’s own negligence, recklessness, or willful misconduct, or from personal injury or property damage caused by BST.'),
 ('h3', 'Vehicle Immobilization; Duration of Service'),
 ('p', 'Customer acknowledges that performance of the Services requires BST to disassemble the vehicle and to render it immobilized and inoperable, and that the vehicle, the immediate work area, and BST’s service vehicle will be occupied and in use during the agreed service hours as needed to complete the Services. Customer further acknowledges that the vehicle may remain immobilized and inoperable beyond the estimated completion time, including for one or more days, for reasons including parts availability, back-ordered, delayed, or non-conforming parts, supplier and shipping delays, the discovery of additional necessary work, and weather or site conditions. Customer accepts that risk, and any claim for loss of use, substitute transportation, or delay is governed by the Limitation of Liability section above. BST will notify Customer as soon as reasonably practicable if BST expects the vehicle to remain inoperable overnight or longer, and will take reasonable steps to leave the vehicle in a secured condition when BST is not on site.'),
 ('h3', 'Exclusive Access During Service'),
 ('p', 'From the time BST begins the Services until BST notifies Customer that the vehicle has been returned to operable condition and released, the vehicle and the immediate work area are an active work site presenting risks that may include raised, jacked, or unsupported loads, removed or partially secured components, hot surfaces, open or pressurized systems, exposed fluids, and electrical hazards. For safety and to protect the integrity of the Services, Customer agrees that only BST personnel shall touch, enter, start, move, operate, work on, or otherwise access the vehicle or the work area, and Customer shall not permit any other person, including any other repairer or contractor, to do so. Customer assumes the risk of any injury, loss, or damage arising from access to the vehicle or the work area in breach of this section, and Customer shall reimburse BST for the reasonable cost of any re-inspection, re-work, replacement parts, and labor at BST’s standard rates made necessary by that access. If Customer wishes to retrieve an item from the vehicle while the Services are in progress, Customer shall ask BST, and BST will accommodate the request if BST determines it can be done safely; BST may decline or defer the request until the vehicle is in a safe condition. This section is a safety and work-quality covenant only. It does not transfer ownership or possession of the vehicle to BST, does not give BST any right to retain or detain the vehicle, and does not limit Customer’s right to direct BST to stop work, in which case BST will return the vehicle to operable condition to the extent reasonably practicable and Customer shall pay for parts and labor furnished through that time.'),
 ('h3', 'No Custody; Personal Property and Items in the Vehicle'),
 ('p', 'Except while BST personnel are physically present and performing the Services, BST does not have and does not accept custody, possession, or control of the vehicle, and BST is not a bailee of the vehicle or of its contents. The vehicle remains at a location selected by and under the control of Customer. Customer shall remove all personal property from the vehicle before the Services begin. BST is not responsible for the loss, theft, or disappearance of personal property, parts, components, tools, or other items from the vehicle or the work area, except to the extent caused by the negligence or intentional acts of BST or BST’s personnel.'),
 ('h3', 'Fines, Penalties, and Charges During the Service Period'),
 ('p', 'From the time Customer authorizes the Services until BST releases the vehicle, Customer is responsible for any fine, penalty, ticket, assessment, towing charge, storage charge, or similar cost imposed by any municipality, association, landlord, property owner, or other third party arising from the presence, condition, immobilization, or inoperability of the vehicle at the Work Location, except to the extent caused by BST’s negligence or by BST’s unreasonable delay in performing the Services. Customer is responsible for confirming that the vehicle may remain at the Work Location in an inoperable condition for the expected duration of the Services, and for obtaining any permission required from any property owner, landlord, or association.'),
 ('h3', 'Dispute Resolution'),
 ('p', 'Any disputes arising from this agreement shall be resolved in accordance with New Jersey law, with venue in Monmouth County, New Jersey.'),
 ('lp', 'Photo Release:', 'Customer irrevocably gives BST the right and license to photograph, record, and/or video the customer’s vehicle and the immediate work area (collectively, the “Photos”), and to edit, use, and reproduce such Photos, in whole or in part, in print or electronically, for BST’s business purposes, including marketing, advertising, promotion, portfolio, training, and documentation of the Services, on a perpetual and worldwide basis (collectively, the “Rights”). The Rights include, without limitation, using the Photos with other images, graphics, and text, and altering or modifying the Photos by traditional or digital photographic techniques including creating composite, blurred, or distorted representations, retouching, and changing color, perspective, foreground, size, shape, context, or background. Customer agrees that all rights in each Photo, photograph, recording, or video taken by or on behalf of BST, including all copyrights, are BST\'s exclusive property. Customer grants the Rights only as to the vehicle and as to areas that Customer has authority to permit BST to photograph. BST will not publish any Photo in which Customer or any other individual is personally identifiable without that person’s separate written consent, will obscure the vehicle’s license plate and vehicle identification number in any Photo that BST publishes, and will not publish any Photo that identifies the street address of the Work Location. To the fullest extent permitted by applicable law, Customer waives claims against BST for violation of the right of privacy or publicity arising from BST’s authorized and lawful use of the Photos as permitted by this section; provided that this section shall not be applied to waive any right or remedy that may not lawfully be waived by Customer under New Jersey law.'),
 ('lp', 'Severability; New Jersey Savings Clause:', 'If any provision of these Terms is held void, unenforceable, or inapplicable, that provision shall be enforced to the maximum extent permitted and the remaining provisions shall remain in full force. No provision of these Terms is intended to, and no provision shall be applied to, waive, limit, or disclaim any right or remedy that a consumer has under New Jersey law that may not lawfully be waived, limited, or disclaimed, including rights under the New Jersey Consumer Fraud Act, N.J.S.A. 56:8-1 et seq., the Truth-in-Consumer Contract, Warranty and Notice Act, N.J.S.A. 56:12-14 et seq., and the automotive-repair regulations at N.J.A.C. 13:45A-26C.1 et seq. To the extent any limitation of liability, exclusion, disclaimer, or indemnity in these Terms would otherwise be void or unenforceable as applied to a New Jersey consumer, it does not apply to Customer in New Jersey.'),
 ('lp', 'Entire Agreement; Modifications:', 'This Estimate, including these Terms, is the entire agreement between BST and Customer regarding the Services and supersedes all prior discussions and understandings. These Terms may be modified only in a writing signed by BST. Customer may sign this Estimate electronically, and an electronic, scanned, or photocopied signature shall have the same force and effect as an original.'),
]
NOTICE = ['When a motor vehicle is physically presented during normal working hours and, in any event before work begins, a written estimated price stated either:<ol type="A"><li>PRICE NOT TO EXCEED $..., and given without charge; or</li><li>As an exact figure broken down as to parts and labor. This establishment has the right to charge you for this diagnostic service, although if you then have the repair done here, you will not be charged twice for any part of such charge necessary to make the repair.</li><li>As an exact figure to complete a specific repair.</li></ol>',
          'For your protection, you may waive your right to an estimate only by signing a written waiver.',
          'Require that this establishment not start work on your vehicle until you sign an authorization stating the nature of the repair or problem and the odometer reading of your vehicle if you physically present the vehicle here during normal working hours.',
          'A detailed invoice stating charges for parts and labor separately and whether any new, rebuilt, reconditioned or used parts have been supplied.',
          'The replaced parts, if requested before work is commenced, unless their size, weight or similar factors make return of the parts impractical.',
          'A written copy of the guaranty.”']
def anchor(h): return h.lower().replace(';','').replace(',','').replace(':','').replace(' ','-')
def blocks(items):
    out = []
    for it in items:
        k = it[0]
        if k in ('h2', 'h3'): out.append(f'<{k} id="{anchor(it[1])}">{html.escape(it[1])}</{k}>')
        elif k == 'b': out.append(f'<p><strong>{html.escape(it[1])}</strong></p>')
        elif k == 'lp': out.append(f'<p><strong>{html.escape(it[1])}</strong> {html.escape(it[2])}</p>')
        else: out.append(f'<p>{html.escape(it[1])}</p>')
    return '\n'.join(out)
TERMS_TOC = ''.join(f'<li><a href="#{anchor(t)}">{html.escape(t)}</a></li>' for k, t, *_ in SERVICE_TERMS if k == 'h3')

page('/warranty/', 'Our Warranty | Safe Travels Mobile Repair, Monmouth County, NJ',
     'Labor on every Safe Travels repair is covered for 90 days or 3,000 miles, whichever comes first. Here’s what’s covered and how to use it.',
f'''<section><div class="wrap narrow">
<h1>Our warranty</h1>
<p class="lede">We stand behind our work. If something we fixed isn’t right, call or text us, and we’ll make it right.</p>
<h2>What’s covered</h2>
<p><strong>Labor: 90 days or 3,000 miles</strong>, whichever comes first, from the day we finish the job.</p>
<p>It covers the labor listed on your written estimate.</p>
<p>Parts carry their manufacturer’s warranty, and we pass that warranty on to you.</p>
<h2>How we make it right</h2>
<p>If covered work isn’t right, we’ll look at the car first. Then, at our choice, we’ll either:</p>
<ul>
<li>redo the repair, or replace the part, or</li>
<li>refund what you paid for that work.</li>
</ul>
<h2>Coming back to you</h2>
<p>Within about 30 minutes of Port Monmouth: no charge for us to come back for a warranty repair.</p>
<p>Farther away: mileage of $1 per mile, round trip, from Port Monmouth.</p>
<p>We’ll set a time that works for both of us. Please have the car and any part that failed available when we arrive.</p>
<h2>What isn’t covered</h2>
<ul>
<li>Parts you supplied yourself</li>
<li>Damage from neglect, misuse, abuse, accidents, or racing or off-road use</li>
<li>Work changed, modified, or repaired by someone else after our visit</li>
<li>Problems from skipped or improper maintenance</li>
<li>Problems the car already had that weren’t part of the job</li>
</ul>
<h2>How to use your warranty</h2>
<ol>
<li>Call or text <a href="{TEL}">(908) 986-3415</a>, or email <a href="mailto:info@besafetravels.com">info@besafetravels.com</a>.</li>
<li>Tell us what’s happening and when we did the work (your invoice helps).</li>
<li>We’ll set up a visit, check the car, and make it right.</li>
</ol>
<h2>The fine print</h2>
<p>The full warranty terms are in the Terms and Conditions on <a href="/terms-and-conditions/">this website</a>. Nothing on this page, or in those terms, takes away any right you have under New Jersey or federal law.</p>
</div></section>''', noindex=True)

page('/terms-and-conditions/', 'Terms and Conditions | Safe Travels Mobile Repair',
     'Website terms and the service terms and conditions for Safe Travels Mobile Repair, including our warranty and the customer notice required in New Jersey.',
f'''<section><div class="wrap narrow">
<h1>Terms and conditions</h1>
<nav aria-label="Sections"><ul class="toc"><li><a href="#website-terms">Website Terms and Service Authorization</a></li><li><a href="#service-terms">Service Terms and Conditions</a></li>{TERMS_TOC}<li><a href="#customer-notice">Required Posting Pursuant to N.J.A.C. 13:45A-26C.2(a)(11)</a></li></ul></nav>
<div class="legal-text">
<h2 id="website-terms">Website Terms and Service Authorization</h2>
{blocks(WEBSITE_TERMS)}
</div>
{agree_form('website', 'Website Terms')}
<div class="legal-text">
<h2 id="service-terms">Service Terms and Conditions</h2>
{blocks(SERVICE_TERMS)}
<h3 id="customer-notice">Required Posting Pursuant to N.J.A.C. 13:45A-26C.2(a)(11)</h3>
<p>“A CUSTOMER OF THIS ESTABLISHMENT IS ENTITLED TO:</p>
<ol>{''.join(f'<li>{n}</li>' for n in NOTICE)}</ol>
</div>
{agree_form('services', 'Services Terms')}
<p class="small">Be Safe Travels LLC, Port Monmouth, NJ 07758. Text as on {TERMS_SOURCE}.</p>
</div></section>
{FORMS_JS}
{AGREE_JS}''')

# ---------------- Promotions (DRAFT 2026-10-24, to-do 14; not linked yet, Feather reviews first) ----------------
# Every offer here is a standing price or policy, so nothing needs an end date. A dated offer must state its dates
# and terms on the page. Wording: calm and specific, no "deals", no countdowns, no pressure, no knocking anyone.
PROMO_END = 'November 24, 2026'  # community offers: one month from Oct 24, 2026 (Feather)
def offer(title, price, body, terms, h='h2'):
    return f'''<article class="card offer">
      <{h}>{title}</{h}>
      {f'<p class="price">{price}</p>' if price else ''}
      <p>{body}</p>
      <p class="small">{terms}</p>
    </article>'''
page('/promotions/', 'Promotions | Safe Travels Mobile Repair, Monmouth County, NJ',
     'Ways to get more from a Safe Travels visit: one consolidated appointment for small jobs, a winter readiness review, pre-purchase inspections and a free first conversation.',
f'''<section class="hero">
  <div class="wrap narrow">
    <h1>Promotions</h1>
    <p class="lede">A few considered ways to get more from each visit. We come to your driveway or office lot, so the car gets our attention while your day carries on.</p>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="cards offers">
      {offer('The consolidated visit', 'Trip fee and mileage waived',
             'Save the small things for one appointment: a bulb, a wiper, a mirror, a door latch. Once the work reaches our one-hour minimum ($159.99), we waive the $25 trip fee and the mileage.',
             'Ongoing. Parts are extra. A single small job on its own is a $25 trip fee plus parts and mileage ($1 per mile, round trip, from Port Monmouth).')}
      {offer('Winter readiness review', '$99.99',
             'Before the cold settles in, a hands-on multipoint inspection of the main systems: engine, transmission and axles; brakes, including the parking brake; tires; suspension; and safety systems. Includes an OBD-II scan when time on site allows, photos, and written technician notes, so you can plan any work on your own schedule.',
             'Flat price. A trip fee and mileage may apply beyond a 30-minute drive. Any repair is quoted separately, in writing, before work begins.')}
      {offer('Before you buy', '$59.99',
             'Considering a used car? We meet you at the seller’s driveway or the dealer’s lot and inspect it before you commit, so you know what you’re buying.',
             'Flat price. A trip fee and mileage may apply beyond a 30-minute drive.')}
      {offer('A first conversation, on us', 'Free',
             'Tell us what you’re hearing, feeling or seeing. We’ll give you our honest read and a ballpark price by phone, before anyone drives anywhere.',
             f'Calls answered 7am to 8pm. On-site diagnostics are $159.99 per hour, one-hour minimum, credited toward the repair if you go ahead.')}
    </div>
  </div>
</section>
<section class="tint" id="community">
  <div class="wrap">
    <h2>Community offers, through {PROMO_END}</h2>
    <p class="lede">For our neighbors. No coupon, code or proof: mention the offer when you book, and we take your word for it.</p>
    <div class="cards">
      {offer('For MSK patients, caregivers and families', '50% off your visit',
             'If you’re a patient at Memorial Sloan Kettering (MSK), or caring for one, or family of one: half off your service visit. One less thing to arrange.',
             f'Through {PROMO_END}. Off the visit’s final price before tax, parts and labor, whether it’s an inspection or a repair.', 'h3')}
      {offer('For Friendly Dental patients, caregivers and families', '10% off your visit',
             'If you, someone you care for, or someone in your family is a patient of Friendly Dental: 10% off your service visit.',
             f'Through {PROMO_END}. Off the visit’s final price before tax, parts and labor, whether it’s an inspection or a repair.', 'h3')}
      {offer('For Joint Physical Therapy patients, caregivers and families', '10% off your visit',
             'If you, someone you care for, or someone in your family is a patient of Joint Physical Therapy: 10% off your service visit.',
             f'Through {PROMO_END}. Off the visit’s final price before tax, parts and labor, whether it’s an inspection or a repair.', 'h3')}
    </div>
    <h3 style="margin-top:28px">How these offers work</h3>
    <ul class="checks">
      <li>Mention the offer when you book. There’s no coupon or code, and we will never ask for proof of a diagnosis, treatment, appointment or family connection.</li>
      <li>However you heard about it, from a friend, our website, or our service vehicle, we’ll honor it through {PROMO_END}.</li>
      <li>The offer comes off the final price of your service visit, before tax, whether it’s an inspection or a repair. You still get a written estimate before any work begins, with the offer shown on it.</li>
    </ul>
    <p class="small">Offers valid through {PROMO_END}. Terms and conditions apply; subject to change without notice. Safe Travels Mobile Repair isn’t affiliated with, sponsored by or endorsed by Memorial Sloan Kettering, Friendly Dental or Joint Physical Therapy; these offers are our own.</p>
  </div>
</section>
<section>
  <div class="wrap narrow">
    <h2>Every visit, the same way</h2>
    <ul class="checks">
      <li>A written estimate before any work begins.</li>
      <li>Diagnostic time credited toward the repair.</li>
      <li>Labor covered for 90 days or 3,000 miles. <a href="/warranty/">Our warranty</a></li>
    </ul>
    <div class="btn-row">
      <a class="btn" href="/appointments/">Schedule a call</a>
      <a class="btn alt" href="{CALC}">Get my estimate</a>
    </div>
  </div>
</section>''')

open(os.path.join(OUT, 'robots.txt'), 'w').write('# Preview: keep search engines out until launch\nUser-agent: *\nDisallow: /\n')
page('/_404/', 'Page not found | Safe Travels Mobile Repair', 'Page not found.',
f'''<section><div class="wrap narrow"><h1>Page not found</h1><p class="lede">That page doesn’t exist or has moved.</p>
<div class="btn-row"><a class="btn" href="/">Go to the home page</a><a class="btn alt" href="{TEL}">Call (908) 986-3415</a></div></div></section>''')
os.replace(os.path.join(OUT,'_404','index.html'), os.path.join(OUT,'404.html')); os.rmdir(os.path.join(OUT,'_404'))
print('built')
