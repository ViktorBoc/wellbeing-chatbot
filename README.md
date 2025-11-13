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
