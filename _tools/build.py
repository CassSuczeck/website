# Page generator for the Safe Travels site. Edit the content here, run `python3 _tools/build.py`, and commit the regenerated HTML.
import os, html
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
CALC = 'https://tools.besafetravels.com/calculator/'
TEL = 'tel:+19089863415'
SMS = 'sms:+19089863415'
MAPS = 'https://www.google.com/maps/d/viewer?mid=1zVy3tcZjMJs6Td0ImW-RaEHxchd74Ag'

NAV = [('Services', '/services/'), ('Calculator', '/calculator/'), ('Reviews', '/reviews/'),
       ('Appointments', '/appointments/'), ('Contact', '/contact/'), ('About', '/about/'), ('FAQ', '/faq/')]

LD = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"AutoRepair","name":"Safe Travels Mobile Repair","legalName":"Be Safe Travels LLC",
 "url":"https://besafetravels.com/","logo":"https://besafetravels.com/assets/logo.png","telephone":"+1-908-986-3415","email":"info@besafetravels.com",
 "address":{"@type":"PostalAddress","addressLocality":"Port Monmouth","addressRegion":"NJ","postalCode":"07758","addressCountry":"US"},
 "areaServed":"Monmouth County, NJ",
 "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":"08:30","closes":"17:00"}]}
</script>'''

def page(path, title, desc, body, active=None, extra_head=''):
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
<!-- PREVIEW: remove the robots noindex line and the preview banner at launch -->
<meta name="robots" content="noindex, nofollow">
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
    <p class="legal">&copy; 2026 Be Safe Travels LLC. All rights reserved. · <a href="/privacy/">Privacy policy</a></p>
  </div>
</footer>
</body>
</html>
'''
    d = os.path.join(OUT, path.strip('/'))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w').write(doc)

BTNS = f'''<div class="btn-row">
      <a class="btn" href="{CALC}">Get my estimate</a>
      <a class="btn" href="/appointments/">Schedule a call</a>
      <a class="btn" href="{TEL}">Call (908) 986-3415</a>
    </div>'''

TOWNS = ('Middletown, Holmdel, Hazlet, Keyport, Keansburg, Matawan, Aberdeen, Atlantic Highlands, Highlands, Rumson, '
         'Red Bank, Shrewsbury, Colts Neck, Tinton Falls, Eatontown, Long Branch, Ocean Township, Asbury Park, Wall, '
         'Marlboro, Old Bridge, Sayreville, Perth Amboy, and Woodbridge')
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
    <a class="map" href="{MAPS}"><picture><source type="image/webp" srcset="/assets/service-area-map-490.webp 490w, /assets/service-area-map.webp 920w" sizes="(max-width: 760px) 92vw, 490px"><img src="/assets/service-area-map.jpg" width="920" height="968" loading="lazy" alt="Map of the Safe Travels Mobile Repair service area in New Jersey, from Woodbridge and Perth Amboy south through Sayreville, Old Bridge, Hazlet, Holmdel, Middletown, Red Bank, Rumson, Eatontown and Long Branch to Asbury Park and Wall. Opens the interactive map."></picture></a>
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
     'Mobile auto repair at your home or work in Monmouth County and nearby towns, NJ: quick fixes, inspections, dash cam installs and engine washes.',
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
    {svc('Professional Engine Wash', '$159.99 per hour, one-hour minimum',
         '<p>Restore your engine bay to a clean, like-new condition. Our engine wash is done by experienced technicians who know modern engine bays. We protect electronics and wiring harnesses, use professional-grade degreasers, and make sure no water gets where it shouldn’t.</p>',
         '', [],
         ['Done by technicians, not guesswork', 'Safe for electronic components and harnesses', 'Thorough degreasing', 'Helps long-term upkeep and resale value'])}
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
      <p class="small">By sending this, you agree Safe Travels may call or text you about your request. Message and data rates may apply. Reply STOP to opt out. See our <a href="/privacy/">privacy policy</a>.</p>
      <button class="btn" type="submit">Send message</button>
    </form>
  </div>
</section>
<script>
(function(){{
  // Preview: no endpoint yet. At launch this posts to an Apps Script lead receiver (same pattern as the calculator).
  var ENDPOINT = '';
  var f = document.getElementById('contact'), st = document.getElementById('c-status');
  function say(cls, t){{ st.className = 'msg ' + cls; st.textContent = t; }}
  f.addEventListener('submit', function(e){{
    e.preventDefault();
    var el = f.elements, v = function(n){{ return el[n].value.trim(); }};
    var name = v('name'), phone = v('phone'), email = v('email'), vehicle = v('vehicle'), town = v('town'), msg = v('message');
    if (!name || phone.replace(/\\D/g,'').length < 10 || !vehicle || !town || !msg) {{ say('err', 'Please add your name, a phone number with at least 10 digits, your vehicle, your town, and what’s going on with the car.'); return; }}
    if (email && !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)) {{ say('err', 'Please check your email address, or leave it blank.'); return; }}
    if (!ENDPOINT) {{ say('err', 'This is a preview: the form isn’t connected yet. Please call or text (908) 986-3415.'); return; }}
  }});
}})();
</script>''', 'Contact')

# ---------------- About ----------------
page('/about/', 'About Us | Safe Travels Mobile Repair, Middletown NJ',
     'Family-owned mobile auto repair founded by Feather Waters, a technician with 15+ years’ experience, serving Middletown, Red Bank, Holmdel and Hazlet, NJ.',
f'''<section>
  <div class="wrap narrow">
    <h1>Who we are</h1>
    <figure class="founder"><picture><source type="image/webp" srcset="/assets/feather-480.webp 480w, /assets/feather-800.webp 800w" sizes="(max-width: 760px) 92vw, 320px"><img src="/assets/feather.jpg" width="800" height="800" alt="Feather Waters, founder of Safe Travels Mobile Repair, in a Safe Travels work shirt"></picture><figcaption>Feather Waters, founder and technician</figcaption></figure>
    <p class="lede">Safe Travels Mobile Repair is a family-owned mobile auto repair service based in Middletown, NJ, that brings expert and honest auto care to you, on your schedule, so your car and life stay on track.</p>
    <p>We proudly serve drivers within about 30 minutes of Middletown, including Red Bank, Holmdel, and Hazlet.</p>
    <p>Founded by Feather Waters, a seasoned technician with over 15 years of experience, we specialize in on-site car diagnostics, vehicle inspections, and mobile car repairs that fit your schedule and lifestyle. Feather’s expertise spans from passenger cars to heavy-duty equipment, like semis and excavators. Whether you need a pre-purchase car inspection, help with a check engine light, or a solution for slow-moving windows or electrical issues, she’ll get to the root of the problem and explain it clearly before any work begins.</p>
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
  ('Matawan', 'Monmouth', 'Matawan is a short drive west of our base in Port Monmouth, along the Bayshore.'),
  ('Aberdeen', 'Monmouth', 'Aberdeen Township, including Cliffwood and Strathmore, is a short drive west of our base in Port Monmouth.'),
  ('Atlantic Highlands', 'Monmouth', 'Atlantic Highlands sits on Sandy Hook Bay, a short drive east of our base in Port Monmouth.'),
  ('Highlands', 'Monmouth', 'Highlands sits at the foot of the bridge to Sandy Hook, a short drive east of our base in Port Monmouth.'),
  ('Rumson', 'Monmouth', 'Rumson sits between the Navesink and Shrewsbury rivers, within our usual service area.'),
  ('Red Bank', 'Monmouth', 'Red Bank is a short drive from our base in Port Monmouth. If you work downtown, we can fix your car in your work lot while you’re at your desk.'),
  ('Shrewsbury', 'Monmouth', 'Shrewsbury, just south of Red Bank, is within our usual service area.'),
  ('Colts Neck', 'Monmouth', 'Colts Neck is within our usual service area. On a farm or a long driveway, we come to wherever the car is parked.'),
  ('Tinton Falls', 'Monmouth', 'Tinton Falls is within our usual service area, at your home or at work.'),
  ('Eatontown', 'Monmouth', 'Eatontown is within our usual service area, at your home or at work.'),
  ('Long Branch', 'Monmouth', 'Long Branch, on the oceanfront, is within our service area.'),
  ('Ocean Township', 'Monmouth', 'Ocean Township, including Oakhurst and Wanamassa, is within our service area.'),
  ('Asbury Park', 'Monmouth', 'Asbury Park, on the shore, is at the southern edge of our service area.'),
  ('Wall', 'Monmouth', 'Wall Township is at the southern edge of our service area.'),
  ('Marlboro', 'Monmouth', 'Marlboro is within our service area, west of Holmdel.'),
  ('Old Bridge', 'Middlesex', 'Old Bridge, just over the Middlesex County line, is within our service area.'),
  ('Sayreville', 'Middlesex', 'Sayreville, including Parlin and Morgan, is within our service area in Middlesex County.'),
  ('Perth Amboy', 'Middlesex', 'Perth Amboy, at the mouth of the Raritan River, is at the northern edge of our service area.'),
  ('Woodbridge', 'Middlesex', 'Woodbridge Township, including Iselin, Colonia, Fords and Avenel, is at the northern edge of our service area.'),
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

# DRAFT (compliance check, Oct 13 2026): owner and, ideally, an NJ attorney review wording before launch.
page('/privacy/', 'Privacy policy | Safe Travels Mobile Repair', 'How Safe Travels Mobile Repair collects and uses your information.',
f'''<section><div class="wrap narrow">
<h1>Privacy policy</h1>
<p class="lede">We collect only what we need to answer you and fix your car. We never sell your information.</p>
<h2>What we collect</h2>
<ul>
<li><strong>Contact form and estimate calculator:</strong> your name, phone, email (optional), vehicle, town, and what’s going on with the car.</li>
<li><strong>Booking:</strong> what you enter when you schedule a call through Calendly.</li>
<li><strong>Calls and texts:</strong> your number and what you tell us.</li>
</ul>
<p>We don’t collect Social Security numbers, driver’s license numbers, or card numbers on this website.</p>
<h2>How we use it</h2>
<p>To answer your request, give you a price, schedule and do the work, and follow up about that work. We don’t send marketing texts.</p>
<h2>Who else handles it</h2>
<p>A few services help us run the site: Calendly (booking), Google (fonts on this site and our email and form tools), and Google Voice (our business phone line, for calls and texts). They process your information for us, not for their own marketing. We never sell or share your mobile number or text consent for anyone’s marketing.</p>
<h2 id="texts">Calls and texts</h2>
<p>When you text us or give us your number on a form, we may call or text you about your request: replies, estimates, scheduling, arrival times, and follow-up on the work. How often depends on the job. Message and data rates may apply. Reply STOP to stop texts, or HELP for help.</p>
<h2>Your choices</h2>
<p>To see, correct, or delete what we have about you, call or text <a href="{TEL}">(908) 986-3415</a> or email <a href="mailto:info@besafetravels.com">info@besafetravels.com</a>. Reply STOP to any text to stop texts.</p>
<p class="small">Be Safe Travels LLC, Port Monmouth, NJ 07758. Last updated October 2026.</p>
</div></section>''')

open(os.path.join(OUT, 'robots.txt'), 'w').write('# Preview: keep search engines out until launch\nUser-agent: *\nDisallow: /\n')
page('/_404/', 'Page not found | Safe Travels Mobile Repair', 'Page not found.',
f'''<section><div class="wrap narrow"><h1>Page not found</h1><p class="lede">That page doesn’t exist or has moved.</p>
<div class="btn-row"><a class="btn" href="/">Go to the home page</a><a class="btn alt" href="{TEL}">Call (908) 986-3415</a></div></div></section>''')
os.replace(os.path.join(OUT,'_404','index.html'), os.path.join(OUT,'404.html')); os.rmdir(os.path.join(OUT,'_404'))
print('built')
