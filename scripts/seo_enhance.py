from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://ivanromanenko78.github.io"
OG_IMAGE = f"{BASE_URL}/ivan-romanenko.jpg"
TODAY = date.today().isoformat()

LANGS = {
    "pt": {"prefix": "", "html": "pt", "hreflang": "pt", "og": "pt_PT"},
    "en": {"prefix": "en", "html": "en", "hreflang": "en", "og": "en_US"},
    "ua": {"prefix": "uk", "html": "uk", "hreflang": "uk", "og": "uk_UA"},
    "ru": {"prefix": "ru", "html": "ru", "hreflang": "ru", "og": "ru_RU"},
}

PAGES = {
    "home": {
        "source": "index.html",
        "route": "/",
        "kind": "home",
        "titles": {
            "pt": "Ivan Romanenko | Realizador, Videógrafo e Motion Designer em Portugal",
            "en": "Ivan Romanenko | Director, Videographer & Motion Designer in Portugal",
            "ua": "Іван Романенко | Режисер, відеооператор і motion designer у Португалії",
            "ru": "Иван Романенко | Режиссёр, видеооператор и моушен-дизайнер в Португалии",
        },
        "descriptions": {
            "pt": "Realizador, videógrafo, operador de câmara, editor e motion designer em Portugal, com mais de 23 anos de experiência em televisão, publicidade e vídeo.",
            "en": "Film director, videographer, camera operator, editor and motion designer in Portugal with over 23 years of experience in television, advertising and video.",
            "ua": "Режисер, відеооператор, монтажер і motion designer у Португалії з понад 23 роками досвіду в телебаченні, рекламі та відеовиробництві.",
            "ru": "Режиссёр, видеооператор, монтажёр и моушен-дизайнер в Португалии с опытом более 23 лет в телевидении, рекламе и видеопроизводстве.",
        },
    },
    "camera": {
        "source": "camera/index.html",
        "route": "/camera/",
        "kind": "service",
        "service": "Video production, camera operation and editing",
        "titles": {
            "pt": "Videógrafo e Operador de Câmara em Portugal | Ivan Romanenko",
            "en": "Videographer and Camera Operator in Portugal | Ivan Romanenko",
            "ua": "Відеооператор і відеограф у Португалії | Іван Романенко",
            "ru": "Видеооператор и видеограф в Португалии | Иван Романенко",
        },
        "descriptions": {
            "pt": "Filmagem, televisão, publicidade, concertos e edição. Videógrafo disponível em Fundão, Covilhã, Castelo Branco e em todo Portugal.",
            "en": "Filming, television, advertising, concerts and editing. Videographer available in Fundão, Covilhã, Castelo Branco and across Portugal.",
            "ua": "Відеозйомка, телебачення, реклама, концерти та монтаж. Робота у Фундані, Ковільяні, Каштелу-Бранку та по всій Португалії.",
            "ru": "Видеосъёмка, телевидение, реклама, концерты и монтаж. Работа в Фундане, Ковильяне, Каштелу-Бранку и по всей Португалии.",
        },
    },
    "motion": {
        "source": "motion/index.html",
        "route": "/motion/",
        "kind": "service",
        "service": "Motion design, animation and video editing",
        "titles": {
            "pt": "Motion Designer e Editor de Vídeo em Portugal | Ivan Romanenko",
            "en": "Motion Designer and Video Editor in Portugal | Ivan Romanenko",
            "ua": "Motion designer і відеомонтажер у Португалії | Іван Романенко",
            "ru": "Моушен-дизайнер и видеомонтажёр в Португалии | Иван Романенко",
        },
        "descriptions": {
            "pt": "Motion design, animação 2D, edição, composição e publicidade para redes sociais. Trabalho remoto e em Portugal.",
            "en": "Motion design, 2D animation, video editing, compositing and social advertising. Available remotely and in Portugal.",
            "ua": "Motion design, 2D-анімація, відеомонтаж, композитинг і реклама для соцмереж. Віддалено та в Португалії.",
            "ru": "Моушен-дизайн, 2D-анимация, видеомонтаж, композитинг и реклама для соцсетей. Удалённо и в Португалии.",
        },
    },
    "marketing": {
        "source": "marketing/index.html",
        "route": "/marketing/",
        "kind": "service",
        "service": "Digital marketing, Meta Ads and lead generation",
        "titles": {
            "pt": "Especialista em Meta Ads e Marketing Digital | Ivan Romanenko",
            "en": "Meta Ads and Digital Marketing Specialist | Ivan Romanenko",
            "ua": "Спеціаліст з Meta Ads і цифрового маркетингу | Іван Романенко",
            "ru": "Специалист по Meta Ads и цифровому маркетингу | Иван Романенко",
        },
        "descriptions": {
            "pt": "Meta Ads, geração de leads, retargeting, testes criativos e otimização de campanhas para negócios em Portugal e projetos remotos.",
            "en": "Meta Ads, lead generation, retargeting, creative testing and campaign optimization for businesses in Portugal and remote projects.",
            "ua": "Meta Ads, лідогенерація, ретаргетинг, тестування креативів і оптимізація кампаній для бізнесу в Португалії та віддалено.",
            "ru": "Meta Ads, лидогенерация, ретаргетинг, тестирование креативов и оптимизация кампаний для бизнеса в Португалии и удалённо.",
        },
    },
}


def localized_route(route: str, lang: str) -> str:
    prefix = LANGS[lang]["prefix"]
    if not prefix:
        return route
    if route == "/":
        return f"/{prefix}/"
    return f"/{prefix}{route}"


def absolute(route: str) -> str:
    return BASE_URL + route


def alternates(page: dict) -> str:
    rows = []
    for lang, info in LANGS.items():
        rows.append(
            f'<link rel="alternate" hreflang="{info["hreflang"]}" href="{absolute(localized_route(page["route"], lang))}">'
        )
    rows.append(
        f'<link rel="alternate" hreflang="x-default" href="{absolute(page["route"])}">'
    )
    return "\n".join(rows)


def schema_for(page: dict, lang: str) -> dict:
    person = {
        "@type": "Person",
        "@id": f"{BASE_URL}/#person",
        "name": "Ivan Romanenko",
        "url": f"{BASE_URL}/",
        "image": OG_IMAGE,
        "jobTitle": ["Film Director", "Videographer", "Camera Operator", "Video Editor", "Motion Designer"],
        "sameAs": [
            "https://www.facebook.com/profile.php?id=1335770893",
            "https://t.me/videocreator_ivan_romanenko",
        ],
        "knowsLanguage": ["pt", "en", "uk", "ru"],
    }
    website = {
        "@type": "WebSite",
        "@id": f"{BASE_URL}/#website",
        "url": f"{BASE_URL}/",
        "name": "Ivan Romanenko Portfolio",
        "inLanguage": LANGS[lang]["html"],
        "publisher": {"@id": f"{BASE_URL}/#person"},
    }
    professional_service = {
        "@type": "ProfessionalService",
        "@id": f"{BASE_URL}/#professional-service",
        "name": "Ivan Romanenko — Video, Motion & Digital Production",
        "url": f"{BASE_URL}/",
        "image": OG_IMAGE,
        "founder": {"@id": f"{BASE_URL}/#person"},
        "telephone": "+380969248969",
        "areaServed": [
            {"@type": "Country", "name": "Portugal"},
            {"@type": "AdministrativeArea", "name": "Castelo Branco"},
            {"@type": "City", "name": "Fundão"},
            {"@type": "City", "name": "Covilhã"},
        ],
        "serviceType": [
            "Video production",
            "Camera operation",
            "Video editing",
            "Motion design",
            "Digital advertising",
        ],
        "availableLanguage": ["Portuguese", "English", "Ukrainian", "Russian"],
    }
    if page["kind"] == "home":
        return {"@context": "https://schema.org", "@graph": [person, website, professional_service]}

    route = localized_route(page["route"], lang)
    webpage = {
        "@type": "WebPage",
        "@id": f"{absolute(route)}#webpage",
        "url": absolute(route),
        "name": page["titles"][lang],
        "description": page["descriptions"][lang],
        "inLanguage": LANGS[lang]["html"],
        "isPartOf": {"@id": f"{BASE_URL}/#website"},
        "about": {"@id": f"{BASE_URL}/#person"},
    }
    service = {
        "@type": "Service",
        "@id": f"{absolute(route)}#service",
        "name": page["service"],
        "url": absolute(route),
        "description": page["descriptions"][lang],
        "provider": {"@id": f"{BASE_URL}/#person"},
        "areaServed": ["Portugal", "Castelo Branco", "Fundão", "Covilhã"],
    }
    return {"@context": "https://schema.org", "@graph": [person, website, webpage, service]}


def seo_block(page: dict, lang: str) -> str:
    title = page["titles"][lang]
    description = page["descriptions"][lang]
    route = localized_route(page["route"], lang)
    canonical = absolute(route)
    locale = LANGS[lang]["og"]
    schema = json.dumps(schema_for(page, lang), ensure_ascii=False, separators=(",", ":"))
    return f'''<!-- SEO:START -->
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta name="author" content="Ivan Romanenko">
<meta name="theme-color" content="#090b10">
<link rel="canonical" href="{canonical}">
{alternates(page)}
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Ivan Romanenko">
<meta property="og:locale" content="{locale}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:alt" content="Ivan Romanenko — director, videographer and motion designer">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{OG_IMAGE}">
<script type="application/ld+json">{schema}</script>
<!-- SEO:END -->'''


def clean_old_seo(html: str) -> str:
    html = re.sub(r"<!-- SEO:START -->.*?<!-- SEO:END -->", "", html, flags=re.S)
    patterns = [
        r"<title\b[^>]*>.*?</title>",
        r"<meta\s+name=[\"']description[\"'][^>]*>",
        r"<meta\s+name=[\"']robots[\"'][^>]*>",
        r"<meta\s+name=[\"']author[\"'][^>]*>",
        r"<meta\s+name=[\"']theme-color[\"'][^>]*>",
        r"<meta\s+property=[\"']og:[^\"']+[\"'][^>]*>",
        r"<meta\s+name=[\"']twitter:[^\"']+[\"'][^>]*>",
        r"<link\s+rel=[\"']canonical[\"'][^>]*>",
        r"<link\s+rel=[\"']alternate[\"'][^>]*hreflang=[\"'][^\"']+[\"'][^>]*>",
        r"<link\s+rel=[\"']icon[\"'][^>]*>",
    ]
    for pattern in patterns:
        html = re.sub(pattern, "", html, flags=re.I | re.S)
    return html


def set_default_language(html: str, lang: str) -> str:
    html_lang = LANGS[lang]["html"]
    html = re.sub(r"<html\s+lang=[\"'][^\"']+[\"']", f'<html lang="{html_lang}"', html, count=1, flags=re.I)
    html = re.sub(r"<!-- DEFAULT-LANG:START -->.*?<!-- DEFAULT-LANG:END -->", "", html, flags=re.S)
    marker = f"<!-- DEFAULT-LANG:START --><script>window.DEFAULT_LANG='{lang}';</script><!-- DEFAULT-LANG:END -->"
    if "assets/index-i18n.js" in html:
        html = html.replace('<script src="/assets/index-i18n.js"></script>', marker + '<script src="/assets/index-i18n.js"></script>', 1)
    elif re.search(r"window\.DEFAULT_LANG=['\"](?:pt|en|ua|ru)['\"]", html):
        html = re.sub(r"window\.DEFAULT_LANG=['\"](?:pt|en|ua|ru)['\"]", f"window.DEFAULT_LANG='{lang}'", html, count=1)
    elif "window.PAGE_TRANSLATIONS" in html:
        html = html.replace("window.PAGE_TRANSLATIONS", f"window.DEFAULT_LANG='{lang}';window.PAGE_TRANSLATIONS", 1)
    return html


def enhance_html(html: str, page: dict, lang: str) -> str:
    html = clean_old_seo(html)
    block = seo_block(page, lang)
    viewport = re.search(r"<meta\s+name=[\"']viewport[\"'][^>]*>", html, flags=re.I)
    if viewport:
        pos = viewport.end()
        html = html[:pos] + "\n" + block + html[pos:]
    else:
        html = html.replace("<head>", "<head>\n" + block, 1)
    return set_default_language(html, lang)


def update_portfolio_js() -> None:
    path = ROOT / "assets/portfolio.js"
    text = path.read_text(encoding="utf-8")
    anchor = "document.querySelectorAll('.contact-form')"
    idx = text.find(anchor)
    if idx == -1:
        raise RuntimeError("Could not locate contact-form anchor in portfolio.js")
    prefix = r"""(()=>{const translations=window.PAGE_TRANSLATIONS||{};const defaultLang=window.DEFAULT_LANG||'pt';const prefixes={pt:'',en:'/en',ua:'/uk',ru:'/ru'};const htmlLang={pt:'pt',en:'en',ua:'uk',ru:'ru'};function stripLangPath(path){const clean=path.replace(/^\/(en|uk|ru)(?=\/|$)/,'');return clean||'/'}function pathLanguage(path){if(/^\/en(?:\/|$)/.test(path))return'en';if(/^\/uk(?:\/|$)/.test(path))return'ua';if(/^\/ru(?:\/|$)/.test(path))return'ru';return'pt'}function localizedUrl(base,lang){const prefix=prefixes[lang]??'';return(prefix+base).replace(/\/+/g,'/')}const basePath=stripLangPath(location.pathname);const pathLang=pathLanguage(location.pathname);const queryLang=new URLSearchParams(location.search).get('lang');if(queryLang&&Object.prototype.hasOwnProperty.call(prefixes,queryLang)&&queryLang!==pathLang){location.replace(localizedUrl(basePath,queryLang)+location.hash);return}function setLang(lang){if(!translations[lang])lang=defaultLang;document.documentElement.lang=htmlLang[lang]||lang;document.querySelectorAll('[data-i18n]').forEach(el=>{const value=translations[lang]?.[el.dataset.i18n];if(value!==undefined)el.textContent=value});document.querySelectorAll('[data-i18n-html]').forEach(el=>{const value=translations[lang]?.[el.dataset.i18nHtml];if(value!==undefined)el.innerHTML=value});document.querySelectorAll('.lang').forEach(btn=>btn.classList.toggle('active',btn.dataset.lang===lang));document.querySelectorAll('[data-page-link]').forEach(link=>{link.href=localizedUrl(link.dataset.pageLink,lang)});document.querySelectorAll('.brand').forEach(link=>{link.href=localizedUrl('/',lang)});localStorage.setItem('portfolioLang',lang)}document.querySelectorAll('.lang').forEach(btn=>btn.addEventListener('click',()=>{const lang=btn.dataset.lang;location.href=localizedUrl(basePath,lang)+location.hash}));setLang(pathLang||defaultLang);"""
    path.write_text(prefix + text[idx:], encoding="utf-8")


def write_sitemap() -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for page in PAGES.values():
        for lang in LANGS:
            route = localized_route(page["route"], lang)
            lines.append("  <url>")
            lines.append(f"    <loc>{absolute(route)}</loc>")
            lines.append(f"    <lastmod>{TODAY}</lastmod>")
            for alt_lang, info in LANGS.items():
                alt_route = localized_route(page["route"], alt_lang)
                lines.append(f'    <xhtml:link rel="alternate" hreflang="{info["hreflang"]}" href="{absolute(alt_route)}"/>')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{absolute(page["route"])}"/>')
            lines.append("  </url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n",
        encoding="utf-8",
    )


def write_favicon() -> None:
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#090b10"/><path d="M17 15h8v34h-8zM32 15h8l7 19 7-19h8L49 49h-5L32 15z" fill="#a6ff4d"/></svg>'''
    (ROOT / "favicon.svg").write_text(svg, encoding="utf-8")


def main() -> None:
    original = {key: (ROOT / page["source"]).read_text(encoding="utf-8") for key, page in PAGES.items()}
    for key, page in PAGES.items():
        pt_html = enhance_html(original[key], page, "pt")
        (ROOT / page["source"]).write_text(pt_html, encoding="utf-8")
        for lang in ("en", "ua", "ru"):
            output_route = localized_route(page["route"], lang).strip("/")
            output = ROOT / output_route / "index.html" if output_route else ROOT / "index.html"
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(enhance_html(original[key], page, lang), encoding="utf-8")
    update_portfolio_js()
    write_sitemap()
    write_favicon()


if __name__ == "__main__":
    main()
