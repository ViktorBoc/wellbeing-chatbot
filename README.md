# Wellbeing Chatbot (Streamlit + OpenAI)

> **Empatický wellbeing chatbot v slovenčine** na podporu psychohygieny, zvládanie stresu/úzkosti a bezpečné smerovanie k odbornej pomoci v kríze.
> ⚠️ **Upozornenie:** Toto nie je zdravotná starostlivosť ani terapia. Pri akútnom ohrození volaj **112**.

---

## ✨ Funkcie

* **Empatická konverzácia (SK)** – krátke, praktické, láskavé odpovede.
* **Krátkodobá pamäť** konverzácie v rámci relácie (žiadne ukladanie na disk/DB).
* **Rozšírená krízová detekcia** (SK/EN + bežné formulácie aj slang) → **bezpečný krízový banner a lokálna odpoveď bez modelu** pri náznaku sebapoškodzovania/samovražedných myšlienok (viď nižšie „Bezpečnostná vetva bez modelu“).
* **Psychoedukácia a techniky:** dýchanie (4-7-8, box 4-4-4-4, predĺžený výdych), uzemnenie 5-4-3-2-1, krátka svalová relaxácia (PMR), mikro-kroky, jemná kognitívna práca (etiketovanie myšlienok, reframing), tipy pre spánok.
* **Nastaviteľná „Kreativita (temperature)“** – ovplyvňuje rozmanitosť a štýl odpovedí.

---

### 🎛️ Kreativita (temperature)

* **0.0–0.2** – veľmi konzervatívne, strohé a konzistentné odpovede.
* **0.4–0.7** – vyvážené a prirodzené (predvolené: **0.6**).
* **0.8–1.0** – tvorivejšie a pestrejšie, no občas menej konzistentné.

> Čím vyššia hodnota, tým viac model „riskuje“ s formuláciou a variáciami; nižšie hodnoty sú prísnejšie a predvídateľnejšie.

---

## 🧠 Ako agent odpovedá

### Štýl komunikácie

* Láskavý, rešpektujúci, **neodsudzujúci** tón; normalizácia prežívania.
* **Jedna otázka naraz**, krátke odseky/odrážky, jasné kroky.
* **Zrkadlenie pocitov** („znie to, že…“, „chápem, že je to ťažké“).

### Rotácia techník

* Agent **neopakuje stále to isté** – **strieda** dychové cvičenia, uzemnenie, behaviorálne a kognitívne tipy podľa nápovedí v texte používateľa (príznaky úzkosti, vyčerpanie, problémy so spánkom atď.).

### Postup pri náznakoch krízy (SAFE-T / NICE / APA / MHFA – prispôsobené chatu)

1. **Bezpečnosť:** zistí, či je používateľ v bezprostrednom ohrození; ak áno, odporučí **112**, zapojenie dôveryhodnej osoby a odstránenie prostriedkov z dosahu.
2. **Citlivé dopytovanie:** myšlienky/plán/úmysel/časovanie/prostriedky, minulé pokusy; **ochranné faktory** (ľudia, hodnoty, záväzky).
3. **Úroveň rizika → intervencia:**

   * **Vysoké:** naliehavo 112/urgent, zostať v chate, konkrétne kroky, zapojiť ďalšiu osobu.
   * **Stredné:** bezpečnostný plán (signály → coping → ľudia/miesta → linky → odstránenie prostriedkov), krízová linka.
   * **Nízke:** psychoedukácia + malé kroky; jemné odporúčanie kontaktovať odborníka.
4. **Formát odpovede:** uznanie → 1–3 kroky na mieru (striedané techniky) → jemná otázka na ďalší krok → ak riziko, **linky pomoci**.

### Hranice

* **Žiadne diagnózy/lekárske pokyny.**
* **Bez návodov** na sebapoškodzovanie.
* Pri dlhodobých ťažkostiach či zhoršení **odporúča odborníka** (psychológ/psychiater).

---

## 🧰 Technický prehľad

* **UI:** Streamlit (`st.chat_message`, `st.chat_input`), single-page aplikácia.
* **Pamäť:** `st.session_state.messages` – **iba počas relácie** (po refrese sa vymaže).
* **Model:** OpenAI Chat Completions (model nastaviteľný cez `OPENAI_MODEL`).
* **Krízová detekcia:** rozsiahly regulárny výraz (SK/EN + slang).
* **Vstupná moderácia:** `omni-moderation-latest` pred volaním modelu. Ak moderácia alebo regex zachytia self-harm, prechádza sa na **bezpečnostnú vetvu bez modelu**.

### 🔒 Bezpečnostná vetva bez modelu

* **Brána:** `if moderation_selfharm(user_input) or in_crisis(user_input): …`
* **Správanie:** **nevolá sa model**; aplikácia **lokálne** zobrazí chybový badge + **SK krízový banner** a stručnú podpornú správu (112, linky pomoci, okamžité kroky).
* **Cieľ:** minimalizovať riziko nevhodného generovania a dať používateľovi jasný, bezpečný postup.

---

## 🆘 Kontakty na pomoc (Slovensko)

* **112 – tiesňové volanie** (bezprostredné ohrozenie).
* **Linka dôvery Nezábudka:** **0800 800 566** (24/7).
* **Krízová linka pomoci (IPčko):** **0800 500 333** · chat: **krizovalinkapomoci.sk**, **ipcko.sk**.
* **Linka detskej istoty:** **116 111**.

---

## 📚 Metodické východiská (konceptuálne)

* **WHO – LIVE LIFE**: rámec prevencie samovrážd (intervencie, postvencia, bezpečnostné plány).
* **SAMHSA – SAFE-T**: 5 krokov hodnotenia rizika a intervencií.
* **NICE**: odporúčania k identifikácii rizika a starostlivosti v komunite.
* **APA**: posudzovanie a manažment samovražedného správania.
* **Mental Health First Aid (MHFA)**: zásady prvej psychologickej pomoci.

> README sumarizuje princípy týchto rámcov prispôsobené pre chatbot; **nie sú to priame citácie**.

---

## ⚖️ Limity a etika

* Chatbot je **podporný nástroj**, nie zdravotná starostlivosť.
* Neposkytuje diagnózy, medicínske pokyny ani podrobné návody na sebapoškodenie.
* Pri náznaku rizika **nevolá model** a okamžite **smeruje na odbornú/krízovú pomoc** (viď „Bezpečnostná vetva bez modelu“).
* Obsah konverzácie sa **neperzistuje** mimo aktuálnej relácie.


---
## 🧩 Code overview (EN)

- **Configuration block (top of file)**  
  Loads environment variables, reads `OPENAI_API_KEY` and `OPENAI_MODEL`, creates an OpenAI client and sets Streamlit page config. If the key is missing, the app stops with an error.

- **`CRISIS_PATTERNS`**  
  Big regex detecting suicidality / self-harm phrases in Slovak, Czech and English (including slang and typical formulations).

- **`SK_CRISIS_BANNER`**  
  Markdown text for the crisis banner with Slovak helplines and simple immediate safety steps.

- **`FEELING_HINTS`**  
  Regex catching emotional / problem-related language (feeling sad, anxious, stressed, exhausted, etc.), plus context words like work, school, relationship, debts.

- **`GENERIC_REQUEST_HINTS`**  
  Regex for short but clear user requests where extra context is not needed (e.g. “napíš mi niečo pekné”, “povedz mi vtip”, “vytvor …”).

- **`QUESTION_WORDS`**  
  Regex for common question words (čo, ako, ake, kde, kedy, prečo, koľko, kto, aký, ktorý…), tolerant to some missing diacritics.

- **`has_context(text)`**  
  Decides if a single user message has enough information to respond with a wellbeing-style answer:  
  - Emotional/problem language → `True`  
  - Clear request via `GENERIC_REQUEST_HINTS` → `True`  
  - Short question (≥ 3 words and contains a question word or “?”) → `True`  
  - Otherwise, messages with ≥ 5 words are treated as having some context.

- **`history_has_context()`**  
  Scans `st.session_state.messages` for any user message that `has_context` returns `True` for.  
  Used to distinguish “beginning of conversation, still no context” vs. “we already know what’s going on”.

- **`in_crisis(text)`**  
  Simple wrapper that returns `True` if `CRISIS_PATTERNS` matches the input.

- **`moderation_selfharm(text)`**  
  Calls `omni-moderation-latest` and returns `True` if moderation marks any self-harm/suicide category.  
  On failure falls back to `False` so that regex-based `in_crisis` can still work.

- **`SYSTEM_PROMPT`**  
  Large instruction block defining the wellbeing persona, communication style, safety triage, response format and ethical boundaries (no diagnoses, no self-harm instructions).

- **`ai_reply(messages, temperature)`**  
  Calls `client.chat.completions.create(...)` with the full conversation and returns the assistant’s reply text.  
  On exception it returns a human-readable error message.

- **Streamlit UI section**  
  - Sets title and caption.  
  - Sidebar slider controls the OpenAI temperature.  
  - Initializes `st.session_state.messages` with system prompt and greeting.  
  - Renders conversation history (excluding the system message).  
  - Reads new user input via `st.chat_input`.  
  - On new input:
    1. Appends user message to history and displays it.  
    2. If `moderation_selfharm` or `in_crisis` → show crisis banner and a fixed supportive message (no model call).  
    3. Else if there is still no context (`not history_has_context()` and `not has_context(user_input)`) → send the static clarification asking for more context.  
    4. Else → call `ai_reply` and show the model-generated wellbeing response.  
  - Shows a footer disclaimer about non-clinical nature and emergency contact.

