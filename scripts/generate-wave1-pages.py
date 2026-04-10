#!/usr/bin/env python3
from pathlib import Path
import json, html
ROOT = Path(__file__).resolve().parent.parent
batches = json.load((ROOT/'data'/'wave1-batches.json').open(encoding='utf-8'))['batches']
output_dir = ROOT
profession_map = {
    'unternehmensberater': {
        'title': 'Unternehmensberater in {city_label}',
        'h1': 'Landingpage für Unternehmensberater in {city_label}',
        'problem': 'Wenn ein Beratungsangebot fachlich stark ist, online aber noch zu generisch, zu abstrakt oder zu wenig vertrauenswürdig wirkt.',
        'deliverable': 'klare Positionierung, verständlichere Angebotskommunikation, stärkere Landingpage-Struktur und sauberer nächster Schritt',
    },
    'projektmanager': {
        'title': 'Projektmanager in {city_label}',
        'h1': 'Landingpage für Projektmanager in {city_label}',
        'problem': 'Wenn Projekte, Kompetenzen und Leistungen zwar vorhanden sind, online aber noch nicht klar genug in ein überzeugendes Profil übersetzt werden.',
        'deliverable': 'klare Leistungsdarstellung, vertrauenswürdiger Auftritt und stärkere Anfrageführung für projektnahe Dienstleistungen',
    },
    'berater': {
        'title': 'Berater in {city_label}',
        'h1': 'Landingpage für Berater in {city_label}',
        'problem': 'Wenn Beratungsleistungen korrekt beschrieben sind, aber noch nicht schnell genug verständlich, differenzierend oder anschlussfähig wirken.',
        'deliverable': 'verständlicheres Angebot, bessere Website-Texte, saubere Struktur und klarere Conversion-Logik',
    },

    'it-berater': {
        'title': 'IT-Berater in {city_label}',
        'h1': 'Landingpage für IT-Berater in {city_label}',
        'problem': 'Wenn IT-nahe Beratungsleistungen fachlich stark sind, online aber noch nicht verständlich, vertrauenswürdig oder klar genug positioniert werden.',
        'deliverable': 'klare Positionierung, bessere Leistungsdarstellung und stärkere Anfrageführung für IT-nahe Beratungsangebote',
    },
    'ki-berater': {
        'title': 'KI-Berater in {city_label}',
        'h1': 'Landingpage für KI-Berater in {city_label}',
        'problem': 'Wenn KI-Angebote interessant sind, aber online noch zu abstrakt, zu technisch oder zu wenig anschlussfähig für echte Interessenten wirken.',
        'deliverable': 'verständlicheres KI-Angebot, bessere Nutzenkommunikation und klarere Conversion-Logik',
    },
    'interim-manager': {
        'title': 'Interim Manager in {city_label}',
        'h1': 'Landingpage für Interim Manager in {city_label}',
        'problem': 'Wenn Führung auf Zeit, Restrukturierung oder operative Verantwortung online noch nicht klar genug als seriöses Angebot sichtbar wird.',
        'deliverable': 'stärkerer Vertrauensrahmen, klarere Leistungsdarstellung und bessere Anfragefähigkeit für Interim-Management-Angebote',
    },

    'seo-berater': {
        'title': 'SEO-Berater in {city_label}',
        'h1': 'Landingpage für SEO-Berater in {city_label}',
        'problem': 'Wenn SEO-Leistungen fachlich stark sind, online aber noch zu technisch, zu allgemein oder zu wenig vertrauenswürdig wirken.',
        'deliverable': 'klarere Leistungsdarstellung, verständlichere Angebotskommunikation und stärkere Anfrageführung für SEO-nahe Beratungsangebote',
    },
    'hr-berater': {
        'title': 'HR-Berater in {city_label}',
        'h1': 'Landingpage für HR-Berater in {city_label}',
        'problem': 'Wenn HR-, Recruiting- oder People-Themen zwar fachlich kompetent sind, online aber noch nicht klar genug in ein starkes Beratungsangebot übersetzt werden.',
        'deliverable': 'stärkere Positionierung, klarere Nutzenkommunikation und ein vertrauenswürdigerer Auftritt für HR-nahe Beratung',
    },
}
city_labels = {
    'wien':'Wien','graz':'Graz','linz':'Linz','salzburg':'Salzburg','innsbruck':'Innsbruck','klagenfurt':'Klagenfurt','st-poelten':'St. Pölten','wiener-neustadt':'Wiener Neustadt',
    'berlin':'Berlin','duesseldorf':'Düsseldorf','frankfurt':'Frankfurt','hamburg':'Hamburg','hannover':'Hannover','koeln':'Köln','muenchen':'München','stuttgart':'Stuttgart'
}
base_css = """:root{--bg:#040712;--panel:rgba(15,22,40,.84);--line:rgba(140,164,255,.14);--line-strong:rgba(124,156,255,.24);--text:#eef3ff;--muted:#afbadc;--accent:#7c9cff;--accent2:#59e1bf;--shadow:0 28px 80px rgba(0,0,0,.40);--max:1100px}*{box-sizing:border-box}body{margin:0;font-family:Inter,ui-sans-serif,system-ui,sans-serif;color:var(--text);background:radial-gradient(circle at 10% 0%, rgba(124,156,255,.18), transparent 24%),linear-gradient(180deg,#040712 0%,#09101d 42%,#060915 100%)}a{color:inherit;text-decoration:none}.wrap{width:min(calc(100% - 32px),var(--max));margin:0 auto}.nav{position:sticky;top:0;background:rgba(5,8,20,.78);backdrop-filter:blur(18px);border-bottom:1px solid var(--line)}.nav-inner{display:flex;justify-content:space-between;align-items:center;padding:14px 0;gap:16px}.brand{display:flex;gap:12px;align-items:center;font-weight:800}.mark{width:48px;height:48px;border-radius:15px;overflow:hidden;display:grid;place-items:center;background:linear-gradient(135deg, rgba(124,156,255,.16), rgba(89,225,191,.14));border:1px solid rgba(255,255,255,.12);padding:5px}.mark img{width:100%;height:100%;object-fit:contain;border-radius:11px}.hero{padding:62px 0 26px}.panel,.card{background:linear-gradient(180deg, rgba(18,28,51,.88), rgba(10,15,28,.78));border:1px solid var(--line);border-radius:28px;box-shadow:var(--shadow)}.panel{padding:38px}.grid-2,.grid-3{display:grid;gap:18px}.grid-2{grid-template-columns:repeat(2,1fr)}.grid-3{grid-template-columns:repeat(3,1fr)}h1,h2,h3{margin:0 0 14px;line-height:1.04}h1{font-size:clamp(2.8rem,6vw,5rem)}h2{font-size:clamp(1.8rem,3vw,2.5rem)}p,li{color:var(--muted);line-height:1.78}.eyebrow{display:inline-flex;padding:8px 14px;border-radius:999px;border:1px solid rgba(124,156,255,.26);background:rgba(124,156,255,.10);margin-bottom:18px;font-size:.82rem;color:#dce6ff}.card{padding:24px}.cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:18px}.btn{padding:14px 18px;border-radius:14px;font-weight:700;border:1px solid transparent;display:inline-flex;align-items:center;justify-content:center}.primary{background:linear-gradient(135deg,var(--accent),var(--accent2));color:#08111f}.secondary{background:rgba(255,255,255,.03);border-color:var(--line-strong);color:var(--text)}.section{padding:26px 0 12px}.footer{padding:38px 0 60px;text-align:center;color:var(--muted)}@media(max-width:980px){.grid-2,.grid-3{grid-template-columns:1fr}}"""

def page(city, profession):
    city_label = city_labels.get(city, city.replace('-', ' ').title())
    meta = profession_map[profession]
    slug = f'landingpage-{city}-{profession}.html'
    canonical = f'https://bertlclaw.at/{slug}'
    title = f"{meta['title'].format(city_label=city_label)} – BertlClaw"
    desc = f"{meta['title'].format(city_label=city_label)}: klare Landingpage, bessere Website-Texte und stärkere Positionierung für beratungsnahe Angebote in {city_label}."
    h1 = meta['h1'].format(city_label=city_label)
    return f'''<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}" /><link rel="canonical" href="{canonical}" /><meta property="og:title" content="{html.escape(title)}" /><meta property="og:description" content="{html.escape(desc)}" /><meta property="og:type" content="website" /><meta property="og:url" content="{canonical}" /><meta property="og:image" content="https://bertlclaw.at/bertlclaw-assets/og-card.jpg" /><meta name="twitter:card" content="summary_large_image" /><style>{base_css}</style></head><body><nav class="nav"><div class="wrap nav-inner"><div class="brand"><div class="mark"><img src="bertlclaw-assets/logo-main.jpg" alt="BertlClaw Logo" /></div><div>BertlClaw</div></div><div><a href="index.html">← Startseite</a></div></div></nav><header class="hero wrap"><section class="panel"><div class="eyebrow">{html.escape(city_label)} · {profession.replace('-', ' ')} · Landingpage · Positionierung</div><h1>{html.escape(h1)}</h1><p>{html.escape(meta['problem'])}</p><p style="margin:14px 0 0;color:#dce6ff;line-height:1.7;max-width:62ch;">Direktkontakt mit Dominic Reisenbichler, MSc. · ehrliche Einordnung innerhalb von 24–48 Stunden · 2–4 Sätze reichen für den Einstieg.</p><div class="cta"><a class="btn primary" href="kontakt.html#formular" data-track-click="{profession}-hero-contact">Kostenlose Ersteinschätzung anfragen</a><a class="btn secondary" href="erstgespraech.html" data-track-click="{profession}-hero-call">Kostenloses Erstgespräch</a><a class="btn secondary" href="proof.html" data-track-click="{profession}-hero-proof">Proof ansehen</a></div></section></header><main class="wrap"><section class="section"><div class="grid-2"><div class="card"><h2>Wann diese Seite sinnvoll ist</h2><ul><li>wenn dein Angebot online noch nicht klar genug wirkt</li><li>wenn Leistungen zu allgemein oder austauschbar beschrieben sind</li><li>wenn mehr Vertrauen und bessere Anfrageführung gebraucht werden</li><li>wenn eine Landingpage statt allgemeiner Website-Fläche gebraucht wird</li></ul></div><div class="card"><h2>Was BertlClaw dabei liefert</h2><p>{html.escape(meta['deliverable'])}.</p><div class="cta"><a class="btn primary" href="services.html">Leistungen ansehen</a><a class="btn secondary" href="use-cases.html">Anwendungsfälle ansehen</a></div></div></div></section><section class="section"><div class="grid-3"><article class="card"><h3>Klarere Positionierung</h3><p>Weniger generische Selbstbeschreibung, mehr Relevanz und bessere Anschlussfähigkeit für Interessenten.</p></article><article class="card"><h3>Stärkere Landingpage-Struktur</h3><p>Hero, Nutzen, Vertrauenselemente, FAQ und nächster Schritt greifen sauberer ineinander.</p></article><article class="card"><h3>Weniger Reibung vor der Anfrage</h3><p>Keine diffuse Kontaktaufforderung, sondern ein verständlicher nächster Schritt mit klarer Erwartung.</p></article></div></section><section class="section"><div class="card"><h2>Passender nächster Schritt</h2><p>Wenn du unsicher bist, ob genau diese Richtung passt, reicht eine kurze Nachricht. Danach folgt eine ehrliche Einordnung statt Sales-Druck.</p><div class="cta"><a class="btn primary" href="kontakt.html#formular" data-track-click="{profession}-mid-contact">Kostenlose Ersteinschätzung anfragen</a><a class="btn secondary" href="preise.html" data-track-click="{profession}-mid-pricing">Preise ansehen</a><a class="btn secondary" href="faq.html" data-track-click="{profession}-mid-faq">FAQ ansehen</a></div></div></section></main><footer class="footer wrap"><div style="display:flex;justify-content:center;gap:14px;flex-wrap:wrap;margin-bottom:14px;font-size:.92rem;"><a href="index.html">Startseite</a><a href="services.html">Leistungen</a><a href="use-cases.html">Anwendungsfälle</a><a href="impressum.html">Impressum</a><a href="datenschutz.html">Datenschutz</a></div>BertlClaw · {html.escape(meta['title'].format(city_label=city_label))}</footer></body></html>'''

written=[]
first_batch=batches[0] if batches else []
for cluster in first_batch:
    city=cluster['city']
    for path in cluster['paths']:
        slug=path.removeprefix('/landingpage-').removesuffix('.html')
        profession='berater'
        city=slug
        for candidate in sorted(profession_map.keys(), key=len, reverse=True):
            suffix='-' + candidate
            if slug.endswith(suffix):
                profession=candidate
                city=slug[:-len(suffix)]
                break
        # only support the first production professions cleanly
        if profession not in profession_map:
            continue
        content=page(city, profession)
        target=output_dir / path.lstrip('/')
        target.write_text(content, encoding='utf-8')
        written.append(str(target))
print(json.dumps({'written_count':len(written),'sample':written[:20]}, ensure_ascii=False, indent=2))
