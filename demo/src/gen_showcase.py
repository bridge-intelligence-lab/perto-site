#!/usr/bin/env python3
"""Build one showcase page per congregation from a replay JSON.

Usage: gen_showcase.py <replay-CODE.json> <editorial-CODE.json> <out.html>

The replay JSON is the simulator's export: one entry per persona with its full timeline
(member inbound, Perto replies, morning words, weekly cards, onboarding turns). Reply text
is rendered verbatim; this script never edits it. Selection happens in the editorial file.

The editorial file picks the personas and carries the human-written blurbs:
{
  "lang": "pt-BR" | "en",
  "title": "...", "lede": "...", "description": "...",
  "qr_svg": "path to qr svg", "deep_link": "https://wa.me/...",
  "faces_dir": "optional dir with <stem>.jpg",
  "generated_on": "2026-10-03"  (optional: the footer's date; defaults to the run's),
  "pilot_note": {"lead": "...", "text": "..."}  (optional extra line in the pilot box),
  "personas": [ {"key": "BRVN26:p078", "stem": "tiago", "display_name": "Tiago",
                 "role": "47 anos · cabeleireiro", "chips": ["..."],
                 "facts": [["Em casa", "..."], ...], "story": "...", "status": "...",
                 "notice": "..."  (optional: one sentence, in our words, on what to notice),
                 "events": ["2026-10-09T21:22:00", "2026-10-09T21:24:00 inbound", ...]
                   (optional whitelist of timeline events by UTC "at"; a bare timestamp
                    shows every event at that minute, "<at> <kind>" only that kind),
                 "days": ["2026-10-04", ...]  (optional: restrict which sim days to show),
                 "hide_kinds": ["weekly_card"] (optional; this is the default) } ]
}

`qr_svg` and `faces_dir` are resolved against the current working directory, so run this
from the repository root with the paths the editorial files carry.
"""
from __future__ import annotations

import base64
import html
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

STR = {
    "pt-BR": {
        "eyebrow": "Perto · demonstração com personagens fictícios",
        "warn": "Nada aqui é de gente real. Os três personagens foram inventados por um programa de computador para testar o Perto. As respostas do Perto, sim, são de verdade: são exatamente o que ele responderia a você.",
        "chat_morning": "Palavra da manhã",
        "chat_card": "Cartão da semana",
        "voice": "áudio transcrito",
        "crisis": "resposta de cuidado",
        "where": "Onde a conversa está",
        "notice": "O que reparar",
        "how_h": "Como funciona",
        "how": [
            "Você manda uma mensagem à noite, texto ou áudio, do jeito que estiver.",
            "O Perto responde em segundos: uma palavra pastoral curta e um versículo conferido letra por letra na Bíblia. Nunca um versículo sozinho numa hora difícil.",
            "De manhã, no horário que você escolheu, chega uma palavra para o dia, ligada ao que você trouxe na véspera.",
            "O que você escreve é seu. Ninguém da igreja lê. APAGAR remove tudo, PAUSAR silencia.",
        ],
        "try_h": "Experimente na {church}",
        "try_p": "Abra o WhatsApp pelo link ou aponte a câmera para o código. A primeira mensagem já vem pronta, com o código da igreja.",
        "try_btn": "Abrir no WhatsApp",
        "pilot": "O Perto está em fase piloto. Durante o piloto, o Rodrigo (quem constrói o Perto) pode ler as conversas para melhorar as respostas. Nunca a igreja. APAGAR remove tudo na hora.",
        "qr_alt": "QR do WhatsApp da igreja",
        "crisis_line": "Em crise, agora: CVV 188",
        "footer_src": "Conversas geradas em {date} com o modelo {model}. Horários de {tz}.",
        "footer_faces": "Retratos: iniciais, não fotos. Nenhuma pessoa real.",
        "footer_faces_ai": "Rostos gerados por inteligência artificial. Nenhuma pessoa real.",
        "privacy": "Política de privacidade",
        "privacy_href": "/privacidade.html",
        "home_href": "/",
        "nav": [("/", "Início"), ("/igrejas.html", "Para igrejas"), ("/privacidade.html", "Privacidade"), ("/en/", "English")],
        "weekday": ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"],
        "month": ["", "jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"],
        "verse_pat": r"\(?((?:[1-3]\s?)?[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]+(?:\s[A-Za-záéíóúâêôãõç]+)?\s\d{1,3}:\d{1,3}(?:[-–]\d{1,3})?)\)?",
    },
    "en": {
        "eyebrow": "Perto · a demo with fictional characters",
        "warn": "Nobody here is real. The three characters were invented by a computer program to test Perto. Perto's replies, though, are genuine: they are exactly what it would say to you.",
        "chat_morning": "Morning word",
        "chat_card": "Weekly card",
        "voice": "voice note, transcribed",
        "crisis": "care reply",
        "where": "Where the conversation stands",
        "notice": "What to notice",
        "how_h": "How it works",
        "how": [
            "You send a message in the evening, text or voice, however you are.",
            "Perto answers in seconds: a short pastoral word and a verse checked word for word against the Bible. Never a verse alone on a hard night.",
            "In the morning, at the hour you chose, a word for the day arrives, tied to what you brought the night before.",
            "What you write is yours. Nobody at the church reads it. DELETE removes everything, PAUSE goes quiet.",
        ],
        "try_h": "Try it at {church}",
        "try_p": "Open WhatsApp from the link or point your camera at the code. The first message comes pre-filled with the church code.",
        "try_btn": "Open in WhatsApp",
        "pilot": "Perto is in a pilot. During the pilot, Rodrigo (who builds Perto) may read conversations to improve the replies. Never the church. DELETE removes everything at once.",
        "qr_alt": "The church's WhatsApp QR",
        "crisis_line": "In crisis, right now: call or text 988",
        "footer_src": "Conversations generated on {date} with the {model} model. Times in {tz}.",
        "footer_faces": "Portraits are initials, not photos. No real person.",
        "footer_faces_ai": "Faces generated by AI. No real person.",
        "privacy": "Privacy policy",
        "privacy_href": "/en/privacy.html",
        "home_href": "/en/",
        "nav": [("/en/", "Home"), ("/en/churches.html", "For churches"), ("/en/privacy.html", "Privacy"), ("/", "Português")],
        "weekday": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "month": ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "verse_pat": r"\(?((?:[1-3]\s?)?[A-Z][a-z]+(?:\s[A-Za-z]+)?\s\d{1,3}:\d{1,3}(?:[-–]\d{1,3})?)\)?",
    },
}

PALETTE = ["#1f5e46", "#8a3b1f", "#2f4f8a", "#6b4a8a", "#a3651a", "#2e6e6e", "#7a2f4a"]

CSS = """
:root{--bg:#f7f5f0;--panel:#fff;--ink:#1f2a24;--muted:#5d6b63;--line:#e2ded5;--accent:#1f5e46;--accent-ink:#fff;--accent-soft:#e4efe8;--warn-bg:#fff4cf;--warn-ink:#5a4300;--chat:#ece7dc;--out:#d9f5c9;--in:#fff;--serif:"Lora",Georgia,"Times New Roman",serif;--sans:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#11161a;--panel:#181f24;--ink:#e8ebe9;--muted:#a3ada7;--line:#2a333a;--accent:#6fbf95;--accent-ink:#0c1a13;--accent-soft:#1b2b24;--warn-bg:#3a2f08;--warn-ink:#ffe08a;--chat:#0e1317;--out:#1f3b22;--in:#222b31}}
:root[data-theme="dark"]{--bg:#11161a;--panel:#181f24;--ink:#e8ebe9;--muted:#a3ada7;--line:#2a333a;--accent:#6fbf95;--accent-ink:#0c1a13;--accent-soft:#1b2b24;--warn-bg:#3a2f08;--warn-ink:#ffe08a;--chat:#0e1317;--out:#1f3b22;--in:#222b31}
*{box-sizing:border-box}html{color-scheme:light dark}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 var(--sans);padding-inline:16px}
a{color:var(--accent);text-underline-offset:3px}
.wrap{max-width:68ch;margin:0 auto;padding-block:24px 64px}
header.site{display:flex;align-items:baseline;justify-content:space-between;gap:12px;flex-wrap:wrap;padding-block:8px 28px}
.brand{font:600 22px/1 var(--serif);color:var(--ink);text-decoration:none}.brand small{font:400 13px/1 var(--sans);color:var(--muted);margin-left:8px}
nav.site{display:flex;gap:16px;font-size:15px}nav.site a{color:var(--muted);text-decoration:none}
h1{font:600 clamp(28px,6vw,40px)/1.15 var(--serif);margin:0 0 12px;text-wrap:balance}
h2{font:600 24px/1.25 var(--serif);margin:40px 0 10px;text-wrap:balance}
p,li{max-width:68ch}.lead{font-size:19px;color:var(--muted);margin-top:0}
.eyebrow{font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);font-weight:700;margin-bottom:8px}
.warn{background:var(--warn-bg);color:var(--warn-ink);padding:12px 16px;border-radius:10px;font-size:15px;margin:16px 0 28px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:16px;overflow:hidden;margin:28px 0}
.card-head{display:grid;grid-template-columns:88px 1fr;gap:16px;padding:18px;align-items:center}
.avatar{width:88px;height:88px;border-radius:50%;display:grid;place-items:center;font:600 34px/1 var(--serif);color:#fff;letter-spacing:.02em}
.card-head img{width:88px;height:88px;border-radius:50%;object-fit:cover;display:block}
.who{display:grid;gap:4px;min-width:0}.who .name{font:600 26px/1.1 var(--serif)}.who .role{color:var(--muted)}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:4px}.chip{font-size:13px;padding:2px 9px;border-radius:999px;background:var(--accent-soft);color:var(--accent);font-weight:600}
.facts{display:grid;grid-template-columns:1fr 1fr;gap:10px 14px;padding:0 18px 16px}
.fact b{display:block;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}.fact span{font-size:16px}
@media (max-width:480px){.facts{grid-template-columns:1fr}}
.story{padding:0 18px 16px;font-size:16px;margin:0}
.notice{padding:0 18px 16px;font-size:16px;margin:0}.notice b{display:block;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.status{margin:0 18px 16px;padding:10px 12px;border-radius:10px;background:var(--accent-soft);font-size:15px}
.chat{background:var(--chat);padding:14px 12px;display:grid;gap:8px}
.day{font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-weight:700;text-align:center;margin:10px 0 4px}
.msg{max-width:86%;padding:8px 12px;border-radius:12px;font-size:15.5px;line-height:1.45;box-shadow:0 1px 0 rgba(0,0,0,.06);white-space:pre-line;position:relative}
.msg.out{background:var(--out);justify-self:end;border-bottom-right-radius:3px}
.msg.in{background:var(--in);justify-self:start;border-bottom-left-radius:3px}
.msg .t{display:block;font-size:11.5px;color:var(--muted);text-align:right;margin-top:3px}
.msg .tag{display:inline-block;font-size:11px;letter-spacing:.05em;text-transform:uppercase;color:var(--accent);font-weight:700;margin-bottom:4px}
.msg .verse{font:italic 15.5px/1.45 var(--serif);color:var(--accent)}
.steps{counter-reset:step;list-style:none;padding:0;margin:16px 0;display:grid;gap:12px}
.steps li{counter-increment:step;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 16px 14px 56px;position:relative}
.steps li::before{content:counter(step);position:absolute;left:16px;top:14px;width:28px;height:28px;border-radius:50%;background:var(--accent);color:var(--accent-ink);font:600 15px/28px var(--sans);text-align:center}
.try{display:grid;grid-template-columns:150px 1fr;gap:20px;align-items:center;background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:18px;margin-top:16px}
.try svg{width:150px;height:150px;background:#fff;border-radius:10px;padding:6px}
@media (max-width:480px){.try{grid-template-columns:1fr;justify-items:center;text-align:center}}
.cta{display:inline-block;background:var(--accent);color:var(--accent-ink);text-decoration:none;font-weight:600;padding:12px 18px;border-radius:10px;margin-top:8px}
.pilot{font-size:14px;color:var(--muted);margin-top:12px}
footer.site{margin-top:56px;padding-top:20px;border-top:1px solid var(--line);font-size:14px;color:var(--muted);display:flex;flex-wrap:wrap;gap:8px 20px}
footer.site a{color:inherit}
"""


def esc(s: str) -> str:
    return html.escape(s or "", quote=False)


def initials(name: str) -> str:
    parts = [p for p in re.split(r"\s+", name.strip()) if p]
    return (parts[0][0] + (parts[-1][0] if len(parts) > 1 else "")).upper()


def fmt_day(d: datetime, S) -> str:
    wd = S["weekday"][d.weekday()]
    if S is STR["pt-BR"]:
        return f"{wd}, {d.day} de {S['month'][d.month]}"
    return f"{wd}, {S['month'][d.month]} {d.day}"


def render_text(text: str, S) -> str:
    """Escape, then set a scripture quote line (one ending in a reference) in the verse face."""
    out = []
    for line in (text or "").split("\n"):
        e = esc(line)
        if re.search(S["verse_pat"] + r"\s*\.?\s*$", line) and len(line) > 20:
            e = f'<span class="verse">{e}</span>'
        out.append(e)
    return "\n".join(out)


def qr_accessible(svg: str, S) -> str:
    """Give the inline QR a viewBox (so it scales) and an accessible name, if it lacks them."""
    m = re.match(r'<svg\b[^>]*?\bwidth="(\d+)"\s+height="(\d+)"', svg)
    if not m or "viewBox" in svg[: m.end() + 200]:
        return svg
    w, h = m.groups()
    attrs = f' viewBox="0 0 {w} {h}" role="img" aria-label="{esc(S["qr_alt"])}"'
    return svg[: m.end()] + attrs + svg[m.end() :]


def build(replay: dict, ed: dict) -> str:
    S = STR[ed["lang"]]
    cong = replay["congregation"]
    tz = ZoneInfo(cong.get("timezone") or ("America/Sao_Paulo" if ed["lang"] == "pt-BR" else "America/Toronto"))
    by_key = {p["persona_key"]: p for p in replay["personas"]}
    faces = Path(ed.get("faces_dir", "")) if ed.get("faces_dir") else None
    cards = []
    used_faces = 0
    for i, pe in enumerate(ed["personas"]):
        p = by_key[pe["key"]]
        name = pe.get("display_name") or p["member"].get("name") or p["profile"].get("first_name")
        face = faces / f"{pe['stem']}.jpg" if faces else None
        if face and face.exists():
            b64 = base64.b64encode(face.read_bytes()).decode()
            used_faces += 1
            av = f'<img src="data:image/jpeg;base64,{b64}" alt="">'
        else:
            av = f'<div class="avatar" style="background:{PALETTE[i % len(PALETTE)]}" aria-hidden="true">{esc(initials(name))}</div>'
        chips = "".join(f'<span class="chip">{esc(c)}</span>' for c in pe.get("chips", []))
        facts = "".join(f'<div class="fact"><b>{esc(k)}</b><span>{esc(v)}</span></div>' for k, v in pe.get("facts", []))
        # timeline → chat bubbles grouped by local day
        hide = set(pe.get("hide_kinds", ["weekly_card"]))
        only_days = set(pe.get("days", []))
        only_ats = set(pe.get("events", []))  # explicit whitelist of timeline "at" values
        bubbles, last_day = [], None
        for ev in p["timeline"]:
            if ev["kind"] in hide or ev["kind"] == "system":
                continue
            if only_ats and ev["at"] not in only_ats and f'{ev["at"]} {ev["kind"]}' not in only_ats:
                continue
            at = datetime.fromisoformat(ev["at"]).replace(tzinfo=ZoneInfo("UTC")).astimezone(tz)
            day = at.date().isoformat()
            if only_days and day not in only_days:
                continue
            if day != last_day:
                bubbles.append(f'<div class="day">{esc(fmt_day(at, S))}</div>')
                last_day = day
            side = "out" if ev["kind"] in ("inbound", "command") else "in"
            tag = ""
            if ev["kind"] == "morning_word":
                tag = f'<span class="tag">{S["chat_morning"]}</span>\n'
            elif ev["kind"] == "weekly_card":
                tag = f'<span class="tag">{S["chat_card"]}</span>\n'
            elif ev["kind"] == "inbound" and (ev.get("intent") or {}).get("voice"):
                tag = f'<span class="tag">🎙 {S["voice"]}</span>\n'
            elif ev["kind"] == "reply" and ev.get("was_crisis"):
                tag = f'<span class="tag">{S["crisis"]}</span>\n'
            text = (pe.get("overrides") or {}).get(ev["at"], ev["text"])
            bubbles.append(
                f'<div class="msg {side}">{tag}{render_text(text, S)}'
                f'<span class="t">{at.strftime("%H:%M")}</span></div>'
            )
        cards.append(
            f'<section class="card" id="{esc(pe["stem"])}">'
            f'<div class="card-head">{av}<div class="who"><div class="name">{esc(name)}</div>'
            f'<div class="role">{esc(pe.get("role", ""))}</div><div class="chips">{chips}</div></div></div>'
            f'<div class="facts">{facts}</div>'
            f'<p class="story">{esc(pe.get("story", ""))}</p>'
            + (f'<p class="notice"><b>{S["notice"]}</b>{esc(pe["notice"])}</p>' if pe.get("notice") else "")
            + (f'<div class="status"><b>{S["where"]}:</b> {esc(pe["status"])}</div>' if pe.get("status") else "")
            + f'<div class="chat">{"".join(bubbles)}</div></section>'
        )
    qr = Path(ed["qr_svg"]).read_text() if ed.get("qr_svg") else ""
    qr = re.sub(r"<\?xml[^>]*>\s*", "", qr)
    qr = qr_accessible(qr, S)
    nav = "".join(f'<a href="{h}">{esc(t)}</a>' for h, t in S["nav"])
    pn = ed.get("pilot_note") or {}
    pilot_note = (
        f'<p class="pilot"><strong>{esc(pn["lead"])}</strong> {esc(pn.get("text", ""))}</p>\n    '
        if pn.get("lead") else ""
    )
    how = "".join(f"<li>{esc(x)}</li>" for x in S["how"])
    run = replay.get("run", {})
    gen_date = (ed.get("generated_on") or run.get("generated_on") or run.get("ended_sim_time") or "")[:10]
    footer_src = S["footer_src"].format(date=gen_date, model=run.get("perto_model", "claude-sonnet-5"), tz=cong.get("city", ""))
    return f"""<!doctype html>
<html lang="{ed['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(ed['title'])}</title>
<meta name="description" content="{esc(ed.get('description', ''))}">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,500;0,600;1,400&display=swap">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header class="site">
  <a class="brand" href="{S['home_href']}">Perto <small>perto.life</small></a>
  <nav class="site">{nav}</nav>
</header>
<main>
  <div class="eyebrow">{esc(S['eyebrow'])}</div>
  <h1>{esc(ed['title'])}</h1>
  <p class="lead">{esc(ed['lede'])}</p>
  <div class="warn">{esc(S['warn'])}</div>
  {"".join(cards)}
  <h2>{esc(S['how_h'])}</h2>
  <ol class="steps">{how}</ol>
  <h2>{esc(S['try_h'].format(church=cong['name']))}</h2>
  <p>{esc(S['try_p'])}</p>
  <div class="try">{qr}<div><p style="margin:0 0 4px"><strong>{esc(cong['name'])}</strong> · {esc(cong.get('city', ''))}</p>
    <a class="cta" href="{esc(ed['deep_link'])}" target="_blank" rel="noopener">{esc(S['try_btn'])}</a>
    {pilot_note}<p class="pilot">{esc(S['pilot'])}</p></div></div>
</main>
<footer class="site">
  <span>© 2026 Bridge Intelligence Inc.</span>
  <a href="{S['privacy_href']}">{esc(S['privacy'])}</a>
  <span>{esc(footer_src)}</span>
  <span>{esc(S['footer_faces_ai'] if used_faces else S['footer_faces'])}</span>
  <span><strong>{esc(S['crisis_line'])}</strong></span>
</footer>
</div>
</body>
</html>
"""


if __name__ == "__main__":
    replay = json.loads(Path(sys.argv[1]).read_text())
    ed = json.loads(Path(sys.argv[2]).read_text())
    Path(sys.argv[3]).write_text(build(replay, ed))
    print("wrote", sys.argv[3], Path(sys.argv[3]).stat().st_size, "bytes")
