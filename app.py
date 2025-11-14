import os
import re

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL") or st.secrets.get("OPENAI_MODEL", "gpt-4o")

if not OPENAI_API_KEY:
    st.error("❗ Chýba OPENAI_API_KEY. Pridaj ho do .env alebo ako systémovú premennú a spusti appku znova.")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)
st.set_page_config(page_title="Wellbeing Chatbot", page_icon="🫶", layout="centered")

CRISIS_PATTERNS = re.compile(
    r"""(
        # SLOVENSKY – všeobecné samovražedné vyjadrenia
        \bsamovra[žz]d(?:[auyieo]*|n[ée]|\s*my[šs]lienky?)\b|
        \b(chcem|idem|pl[aá]nujem)\s*(sa\s*)?zabi[tť]\b|
        \b(zabijem|odstr[aá]nim)\s*(sa)?\b|
        \bukon[čc]i[ťt]\s*(so\s*)?(svoj[iy]m?\s*)?životom\b|
        \bkon[čc][ií]m\s*so\s*životom\b|
        \b(nechcem|nechce\s*sa\s*mi)\s*ž[ií]ť\b|
        \bživot\s*(už)?\s*nem[aá]\s*zmysel\b|
        \b(už|uz)\s*to\s*(pre\s*mňa\s*)?nem[aá]\s*zmysel\b|
        \bskon[čc]i[ťt]\s*to(nie)?\s*nav[žz]dy\b|
        \burobi[ťt]\s*konec?\b|\bsprav[ií]m\s*konec?\b|
        \bchcem\s*od[ií]s[ťt]\s*nav[žz]dy\b|\bvymaza[ťt]\s*sa\b|

        # SLOVENSKY – sebapoškodzovanie / metódy (iba na DETEKCIU, nie návody)
        \b(rez[aá]m|reza[ťt]|poreza[ťt])\s*(sa|si)\b|
        \bporeza[ťt]\s*si\s*(žily|zily)\b|
        \bobesi[ťt]\s*(sa)?\b|\bobes[iy]m\s*(sa)?\b|
        \bsko[čc][ií]m?\s*(z|pod)\s*(okna|balk[óo]na?|mosta|vlak|auto|autobus)\b|
        \b(pred[aá]vkov[aá]?[ťt]|prejes[ťt]\s*sa\s*liekmi|otr[aá]vi[ťt])\s*(sa)?\b|
        \b(utopi[ťt]|utop[iy]m)\s*(sa)?\b|
        \bubl[ií]?[žz]i[ťt]\s*(si|sa)\b|\bchcem\s*si\s*ubl[ií]žiť\b|

        # Česky – časté preklepy/slang
        \bsebezni[čc]uj|sebepo[šs]kozov[aá]n[ií]\b|
        \bchci\s*zab[ií]t\s*se\b|\bskon[čc]it\s*se\s*životem\b|

        # Anglicky
        \bi\s*(want|wanna)\s*die\b|
        \bi'?m\s*going\s*to\s*kill\s*myself\b|
        \bkill\s*myself\b|\bhang\s*myself\b|
        \bend\s*my\s*life\b|\bend\s*it\s*all\b|
        \bno\s*(reason|point)\s*to\s*live\b|\bi\s*don'?t\s*want\s*to\s*live\b|
        \bsuicide\b|\bself\s*-?\s*harm\b
    )""",
    re.IGNORECASE | re.VERBOSE,
)

SK_CRISIS_BANNER = (
    "**🔴 Ak si v bezprostrednom ohrození, hneď volaj 112.**\n\n"
    "**Overené kontakty (Slovensko):**\n"
    "- **Linka dôvery Nezábudka:** **0800 800 566** (24/7)\n"
    "- **Krízová linka pomoci (IPčko):** **0800 500 333** · chat: **https://krizovalinkapomoci.sk** · **https://ipcko.sk**\n"
    "- **Linka detskej istoty:** **116 111** (nonstop, bezplatne)\n"
    "- Ak si mimo SR: **https://findahelpline.com**\n\n"
    "**Čo môžeš spraviť hneď teraz:**\n"
    "1. Ak máš pri sebe nebezpečné veci alebo lieky, **daj ich preč z dosahu** alebo popros niekoho spoľahlivého, aby ich odložil.\n"
    "2. **Zavolaj niekomu, komu dôveruješ** (priateľ/ka, rodina) – zostaň s niekým alebo nech niekto zostane s tebou.\n"
    "3. Skús krátko **spomaliť dych** (napr. box 4-4-4-4 alebo 4-7-8) a **uzemnenie 5-4-3-2-1**.\n"
    "4. Ak sa pocity stupňujú, **kontaktuj hneď odbornú pomoc** (linky vyššie) alebo **112**.\n\n"
    "_Nie si na to sám/sama. Spoločné kroky sú bezpečnejšie._"
)


FEELING_HINTS = re.compile(
    r"""(
        # Priame pomenovanie stavu/pocitu
        c[íi]tim|c[iy]tim|
        som\s+(smutn[ýa]|nahnevan[ýa]|vystresovan[ýa]|na[šs]tvan[ýa]|frustrovan[ýa]|
             vyhoren[ýa]|pr[aá]zdn[ýa]|na\s*dne|bez\s*energie|apatick[ýa])|
        m[aá]m\s+(úzkosť|uzkost|stres|paniku|panick[ýy]\s*z[aá]chvat|strach|depresiu|nervy|
                 probl[eé]m|starosti|n[áa]valy\s*úzkosti)|
        tr[aá]pi\s*ma|bol[ií]\s*ma\s*srdce|zle\s*sp[íi]m|nesp[íi]m|bud[ií]m\s*sa|
        c[íi]tim\s*sa\s*(s[aá]m|osamelo|vinn[ýy]|hanb[íi]m\s*sa)|
        pla[čc]em|rozpla[čc]e\s*ma|m[áa]m\s*chu[ťt]\s*plaka[ťt]|
        # Kontextové stresory (indície)
        (v\s*pr[aá]ci|v\s*robote|v\s*škole|na\s*vysokej|vo\s*vz[ťt]ahu|rodina|rozchod|rozvod|
         konflikty|dlhy|peniaze|samota|vy[čc]erpan[ýa])
    )""",
    re.IGNORECASE | re.VERBOSE,
)

GENERIC_REQUEST_HINTS = re.compile(
    r"""(
        # priame požiadavky typu "napíš/povedz/ukáž/daj mi ..."
        \bnap[íi]š\s+mi\b|
        \bpovedz\s+mi\b|
        \buk[aá]ž\s+mi\b|
        \bdaj\s+mi\b|
        \bgeneruj\b|
        \bvytvor\b|

        # typické "napíš mi niečo pekné/milé/motivačné"
        \bnap[íi]š\s+mi\s+nie[čc]o\s+(pekne|pekné|milé|pozit[ií]vne|motiva[čc]n[eé])\b|
        \bnap[íi]š\s+mi\s+(vtip|afirm[áa]ciu|b[aá]se[nň])\b
    )""",
    re.IGNORECASE | re.VERBOSE,
)

QUESTION_WORDS = re.compile(
    r"\b(čo|co|ako|ake|kde|kedy|pre[čc]o|ko[ľl]ko|kto|ak[eyýaé]|ktor[eyýaé])\b",
    re.IGNORECASE,
)

def has_context(text: str) -> bool:
    """Je v texte náznak pocitov/problému, alebo je to jasná požiadavka/otázka?"""
    t = (text or "").strip()
    if not t:
        return False

    if FEELING_HINTS.search(t):
        return True

    if GENERIC_REQUEST_HINTS.search(t):
        return True

    tokens = t.split()

    if QUESTION_WORDS.search(t) or "?" in t:
        return len(tokens) >= 3

    return len(tokens) >= 5

def history_has_context() -> bool:
    """Prešla už konverzácia bodom, kde používateľ poskytol kontext?"""
    for m in st.session_state.messages:
        if m.get("role") == "user" and has_context(m.get("content", "")):
            return True
    return False

def in_crisis(text: str) -> bool:
    return bool(CRISIS_PATTERNS.search(text or ""))

def moderation_selfharm(text: str) -> bool:
    """
    Vráti True, ak moderácia naznačuje self-harm/suicidálne riziko.
    Používa omni-moderation-latest.
    """
    try:
        mod = client.moderations.create(
            model="omni-moderation-latest",
            input=text
        )
        res = mod.results[0]
        cat = res.categories or {}

        return any([
            cat.get("self-harm", False),
            cat.get("self-harm/intent", False),
            cat.get("self-harm/instructions", False),
            cat.get("suicide", False),
        ])
    except Exception:
        return False


SYSTEM_PROMPT = """
Si empatický wellbeing sprievodca v SLOVENČINE. Nie si terapia ani urgentná zdravotná starostlivosť.
Neposkytuješ diagnózy, medicínske pokyny ani návody na sebapoškodzovanie. Tvoj cieľ: bezpečne podporiť
psychohygienu a zvládanie (stres, úzkosť, smútok, vyčerpanie), a pri riziku zrozumiteľne smerovať na odbornú/krízovú pomoc.

# 0) KOMUNIKAČNÝ ŠTÝL
- Láskavý, rešpektujúci, neodsudzujúci tón. Zrkadli pocity („znie to, že…“, „chápem, že je to ťažké“).
- Jedna otázka naraz. Krátke odseky/odrážky. Jednoduchý jazyk. Žiadne moralizovanie.
- Normalizuj bežné prežívanie (napr. „veľa ľudí má v takýchto situáciách úzkosť – nie si v tom sám/sama“).

# 1) KONTEXT NA PRVOM MIESTE
- Ak je vstup krátky alebo nejasný (bez emócií/problému): najprv stručne uznaj a polož 1 jemnú otázku
  na doplnenie („Čo sa presne stalo?“ / „Ako sa v tom cítiš?“). Zatiaľ nedávaj konkrétne rady.
- Keď kontext máš, prejdina odporúčania.

# 2) REPERTOÁR PODPORY (rotuj; vždy uveď krátke „prečo“)
- Dych: 4–7–8, box 4–4–4–4, predĺžený výdych.
- Uzemnenie: 5–4–3–2–1, pomenovanie 5 zmyslov, orientácia v priestore.
- Svalová relaxácia (krátka PMR): čelo, ramená, čeľusť, dlane.
- Kognitívne: pomenovanie myšlienok („mám myšlienku, že…“), jemný reframe, plánovanie starostí.
- Behaviorálne: mikro-úloha (2–5 min), hydratácia/jedlo, svetlo/pohyb, kontakt s blízkym.
- Emócie: „urge surfing“, dych do brucha, chladenie tváre.
- Spánok: hygiena spánku, zníženie stimulácie, večerný rituál, „parking lot“ na starosti.
- Komunikácia: I-statements, stanovovanie hraníc, jemné prosby o podporu.
- Podpora a zmysel: drobné kroky k spojeniu s ľuďmi/komunitou, pripomenutie hodnôt.

# 3) TRIÁŽ A BEZPEČNOSŤ (princípy SAFE-T / NICE / APA / MHFA – prispôsobené chatu)
- Pri náznakoch rizika sa zameraj na: myšlienky, plán/úmysel, prostriedky, časovanie, minulé pokusy,
  ochranné faktory (ľudia/hodnoty/zodpovednosti), aktuálnu bezpečnosť.
- Nikdy nepopisuj spôsoby sebapoškodzovania. Nezdieľaj „návody“.
- Ak je prítomné akútne riziko alebo neistota: jasne odporuč 112/krízové linky, odstránenie nebezpečných
  predmetov z dosahu, zapojenie dôveryhodnej osoby, zostať s niekým.
- Ak riziko nie je akútne: pracuj s bezpečnostným mini-plánom (signály → coping → ľudia/miesta → linky pomoci → odstránenie prostriedkov).
- Vždy ostaň podporný a konkrétny; radšej malé, uskutočniteľné kroky než dlhé zoznamy.

# 4) FORMÁT ODPOVEDE (keď už je kontext)
1) Uznanie + krátke zhrnutie (1–2 vety).
2) 1–3 malé kroky na mieru (odrážky), každý s jednou vetou „prečo to môže pomôcť“.
3) Na záver pridaj krátku **pozvánku v oznamovacej vete**, nie priamu otázku.
   - Príklad: „Ak chceš, daj mi vedieť, čo z toho by si chcel vyskúšať ako prvé a môžeme to spolu viac rozobrať alebo naplánovať.“
   - Vyhýbaj sa prázdnym otázkam typu „Čo myslíš, čo by ti teraz najviac pomohlo?“.
4) Ak zaznie riziko: pripoj blok s kontaktmi/112 a bezpečnostnými krokmi (bez opisov metód).

# 5) HRANICE A ETIKA
- Žiadne diagnózy ani lekárske/liekové rady. Povzbuď kontaktovať psychológa/psychiatra pri dlhších či zhoršených ťažkostiach.
- Rešpektuj anonymitu; nevyžaduj citlivé detaily. Nemanipuluj, netlač.
"""

def ai_reply(messages, temperature: float = 0.6) -> str:
    """Volá OpenAI Chat Completions a vráti text odpovede."""
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            temperature=temperature,
            messages=messages,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return (
            "Ospravedlňujem sa, nastal problém s generovaním odpovede. Skús to prosím znova "
            f"alebo skontroluj konfiguráciu API. (Detail: {e})"
        )

st.title("🫶 Wellbeing Chatbot")
st.caption("Podporný, empatický a praktický sprievodca psychohygienou. Nenahrádza odbornú starostlivosť.")

with st.sidebar:
    st.subheader("⚙️ Nastavenia")
    temperature = st.slider("Kreativita (temperature)", 0.0, 1.0, 0.6, 0.1)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "assistant",
            "content": (
                "Ahoj, som tvoj wellbeing sprievodca. Ako ti dnes môžem pomôcť?\n"
                "Ak chceš, kľudne jednou–dvomi vetami napíš, čo sa deje alebo ako sa cítiš."
            ),
        },
    ]

for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message("assistant" if msg["role"] == "assistant" else "user"):
        st.markdown(msg["content"])

user_input = st.chat_input("Napíš, s čím chceš pomôcť…")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    if moderation_selfharm(user_input) or in_crisis(user_input):
        with st.chat_message("assistant"):
            st.error("Vyzerá to, že prežívaš niečo veľmi ťažké.")
            st.markdown(SK_CRISIS_BANNER)
        st.session_state.messages.append({
            "role": "assistant",
            "content": (
                "Som tu, aby som ťa podporil/a. Ak si v akútnom ohrození, volaj 112.\n"
                "Linky pomoci: Nezábudka 0800 800 566 · Krízová linka pomoci 0800 500 333 · ipcko.sk · 116 111 (deti/mladí)."
            ),
        })

    elif not history_has_context() and not has_context(user_input):
        clarify = (
            "Zatiaľ som od teba zachytil len veľmi krátku správu, z ktorej neviem pochopiť, čo sa deje. "
            "Aby som ti vedel reálne pomôcť, potrebujem trochu viac kontextu – skús mi v jednej až dvoch vetách "
            "napísať, čo sa aktuálne deje alebo ako sa v tom cítiš."
        )
        with st.chat_message("assistant"):
            st.markdown(clarify)
        st.session_state.messages.append({"role": "assistant", "content": clarify})

    else:
        reply = ai_reply(st.session_state.messages, temperature=temperature)
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

st.markdown("---")
st.caption(
    "Tento chatbot je informačný a podporný. Nenahrádza zdravotnú ani psychoterapeutickú starostlivosť.\n"
    "Pri výraznom zhoršení alebo akútnom riziku kontaktuj 112/krízovú linku."
)
