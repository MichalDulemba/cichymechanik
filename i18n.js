(function () {
  const supported = ['pl', 'en'];
  const stored = localStorage.getItem('lang');
  const browser = (navigator.language || '').slice(0, 2).toLowerCase();
  window.LANG = supported.includes(stored) ? stored : (supported.includes(browser) ? browser : 'pl');

  window.I18N = {
    pl: {
      nav_listen:  'Posłuchaj',
      nav_about:   'O mnie',
      nav_contact: 'Kontakt',

      hero_eyebrow: 'Klawiatury mechaniczne · Polska · 2026',
      hero_title:   'Każda klawiatura<br>brzmi <em>inaczej.</em><br>Ta ma brzmieć <em>dobrze.</em>',
      hero_sub:     'Ręcznie montowane klawiatury mechaniczne. Dobieramy switche, smarujemy, testujemy. Posłuchaj zanim kupisz — każdy build ma nagranie.',

      builds_title:          'Dostępne builds',
      builds_count_suffix:   'sztuk',
      filter_sound:          'Głośność',
      filter_all:            'Wszystkie',
      no_results:            'Brak buildów w tej kategorii.',
      card_available:        'dostępna',
      card_play_title:       'Posłuchaj',

      contact_title: 'Kontakt',
      contact_p1:    'Masz pytanie o konkretny build? Chcesz zamówić klawiaturę z własną specyfikacją? Napisz — odpowiadam zwykle tego samego dnia.',
      contact_p2:    'Możemy też porozmawiać o tym który switch będzie dobry do Twojego use case — biuro, dom, gaming, pisanie.',
      contact_note:  'Odpiszę z informacją o dostępności, sposobie płatności i wysyłce.<br>Wysyłam przez InPost — paczkomaty i kurier.',
      form_name:     'Imię',
      form_message:  'Wiadomość',
      form_name_ph:  'Jan',
      form_msg_ph:   'Pytam o AK820 — czy jest dostępna i jak mogę zamówić?',
      form_submit:   'Wyślij wiadomość →',
      form_sending:  'Wysyłanie…',
      form_success:  'Wiadomość wysłana. Odezwę się wkrótce.',
      form_error:    'Coś poszło nie tak. Napisz na kontakt@cichymechanik.pl',
      form_note:     'Możesz też pisać na <a href="mailto:kontakt@cichymechanik.pl" style="color:inherit;">kontakt@cichymechanik.pl</a>',

      footer_listen:   'Posłuchaj',
      footer_about:    'O mnie',
      footer_terms:    'Regulamin',
      footer_location: 'Żory · Śląsk · 2026',

      overlay_back:        '← Wszystkie builds',
      overlay_sounds_like: 'Jak to brzmi',
      overlay_build_video: 'Jak to składam',
      overlay_coming_soon: 'nagranie wkrótce',
      overlay_price_note:  'cena brutto · wysyłka InPost',
      overlay_specs:       'Specyfikacja',
      overlay_ask:         'Pytaj / zamów →',
      overlay_reply:       'Odpowiadam zwykle tego samego dnia.',
      overlay_photo:       '[ zdjęcie ]',
      overlay_ask_prefix:  'Pytam o',
      lightbox_close:      'Zamknij ×',

      kontakt_eyebrow: 'Zapytaj o build',
      kontakt_title:   'Napisz —<br>odpowiadam <em>tego samego dnia.</em>',
      kontakt_sub:     'Pytania o buildy, własna specyfikacja, dobór switcha do Twojego use case.',
      kontakt_p1:      'Masz pytanie o konkretny build? Chcesz zamówić klawiaturę z własną specyfikacją? Napisz — odpowiadam zwykle tego samego dnia.',
      kontakt_p2:      'Możemy też porozmawiać o tym który switch będzie dobry do Twojego use case — biuro, dom, gaming, pisanie.',
      kontakt_note:    'Odpiszę z informacją o dostępności, sposobie płatności i wysyłce.<br>Wysyłam przez InPost — paczkomaty i kurier.',

      omnie_eyebrow:  'O mnie',
      omnie_title:    'Michał.<br>Żory. Śląsk.<br><em>Klawiatura.</em>',
      omnie_p1:       'Na co dzień programista. Maniak AI. Generalista który potrzebuje dobrych klawiatur do pisania promptów. Ślązak — ale taki co lubi jeździć nad morze.',
      omnie_p2:       'Zaczęło się od budzenia domowników waleniem w klawisze o 4 rano. Skończyło na kilkunastu godzinach przy pęsecie, Krytoxie i switchach rozłożonych na całym biurku. Tak to już bywa.',
      omnie_p3:       'Dziś każdy build który wychodzi z warsztatu jest <strong>testowany, nagrywany i opisywany</strong>. Nie wysyłam nic czego sam nie chciałbym używać.',
      photo_caption:  'Standardowy strój roboczy podczas smarowania stabilizatorów.',
      how_i_work:     'Jak pracuję',
      p01_title:      'Dobór komponentów',
      p01_desc:       'Obudowa, płytka, switch — każda kombinacja ma inny charakter dźwięku. Zaczynam od pytania: do czego ma służyć?',
      p02_title:      'Ręczne smarowanie',
      p02_desc:       'Każdy switch osobno. Krytox 205g0 na lineary, 3203 na tactile. Stem rails bez 205g0 — żeby nie niszczyć pad dampening. Zajmuje godziny. Słychać różnicę.',
      p03_title:      'Test i nagranie',
      p03_desc:       'Przed wysyłką — test akustyczny i nagranie. Słyszysz zanim kupisz. Nie ma niespodzianek po otwarciu paczki.',
      stat_builds:    'Builds 2026',
      stat_hours:     'Godzin przy pęsecie',
      stat_recorded:  'Build nagrany',
      stat_shipping:  'Wysyłka InPost',
      why_title:      'Dlaczego to robię',
      why_p1:         'Nie wierzę w "najlepszy switch". Wierzę w <strong>właściwy switch dla konkretnej osoby</strong>. Ktoś kto pisze przez 8 godzin potrzebuje czegoś innego niż gracz który chce najszybszy pretravel na WASD. Dlatego rozmawiam zanim zaproponuję build.',
      why_p2:         'To zaskakujące, że zmiana switcha może pomóc przejść od dźwięku trzaskania drzwiami toitoi, przez stukanie kamyczkami w piaskownicy, do zamykania drzwi w samochodzie za 300 tys.',
      why_p3:         'Klawiatura to jedyna rzecz z którą masz kontakt przez każdą godzinę pracy. Warto żeby brzmiała dobrze.',
      cta_text:       'Pytaj o <em>swój idealny build.</em><br>Odpiszę tego samego dnia.',
      cta_btn:        'Napisz do mnie →',

      dzwieki_eyebrow:       'Porównaj brzmienie',
      dzwieki_title:         'Usłysz zanim<br><em>kupisz.</em>',
      dzwieki_sub:           'Kliknij build, posłuchaj jak brzmi. Każda klawiatura nagrana w tych samych warunkach.',
      dzwieki_panel_eyebrow: 'Test dźwięku',
      dzwieki_select:        'Wybierz build',
      dzwieki_coming_soon:   'Nagranie wkrótce',
    },
    en: {
      nav_listen:  'Listen',
      nav_about:   'About',
      nav_contact: 'Contact',

      hero_eyebrow: 'Mechanical keyboards · Poland · 2026',
      hero_title:   'Every keyboard<br>sounds <em>different.</em><br>This one sounds <em>good.</em>',
      hero_sub:     'Hand-built mechanical keyboards. Custom switches, hand-lubed, tested. Listen before you buy — every build has a recording.',

      builds_title:          'Available builds',
      builds_count_suffix:   'builds',
      filter_sound:          'Sound level',
      filter_all:            'All',
      no_results:            'No builds in this category.',
      card_available:        'available',
      card_play_title:       'Listen',

      contact_title: 'Contact',
      contact_p1:    "Have a question about a specific build? Want to order a keyboard with custom specs? Write me — I usually reply the same day.",
      contact_p2:    "We can also talk about which switch fits your use case — office, home, gaming, typing.",
      contact_note:  "I'll reply with availability, payment details and shipping info.<br>Shipping via InPost — parcel lockers and courier.",
      form_name:     'Name',
      form_message:  'Message',
      form_name_ph:  'John',
      form_msg_ph:   'Asking about the AK820 — is it available and how can I order?',
      form_submit:   'Send message →',
      form_sending:  'Sending…',
      form_success:  "Message sent. I'll get back to you soon.",
      form_error:    'Something went wrong. Write to kontakt@cichymechanik.pl',
      form_note:     'You can also write to <a href="mailto:kontakt@cichymechanik.pl" style="color:inherit;">kontakt@cichymechanik.pl</a>',

      footer_listen:   'Listen',
      footer_about:    'About',
      footer_terms:    'Terms',
      footer_location: 'Żory · Silesia · 2026',

      overlay_back:        '← All builds',
      overlay_sounds_like: 'How it sounds',
      overlay_build_video: 'How I build it',
      overlay_coming_soon: 'recording coming soon',
      overlay_price_note:  'price incl. VAT · InPost shipping',
      overlay_specs:       'Specs',
      overlay_ask:         'Ask / order →',
      overlay_reply:       'I usually reply the same day.',
      overlay_photo:       '[ photo ]',
      overlay_ask_prefix:  'Asking about',
      lightbox_close:      'Close ×',

      kontakt_eyebrow: 'Ask about a build',
      kontakt_title:   'Write —<br>I reply <em>the same day.</em>',
      kontakt_sub:     'Build questions, custom specs, switch advice for your use case.',
      kontakt_p1:      "Have a question about a specific build? Want to order a keyboard with custom specs? Write me — I usually reply the same day.",
      kontakt_p2:      "We can also talk about which switch fits your use case — office, home, gaming, typing.",
      kontakt_note:    "I'll reply with availability, payment details and shipping info.<br>Shipping via InPost — parcel lockers and courier.",

      omnie_eyebrow:  'About me',
      omnie_title:    'Michał.<br>Żory. Silesia.<br><em>Keyboards.</em>',
      omnie_p1:       'Software developer by day. AI nerd. Generalist who needs good keyboards for writing prompts. From Silesia — but the kind who likes going to the seaside.',
      omnie_p2:       "It started with waking up the household banging keys at 4am. Ended with hours hunched over tweezers, Krytox, and switches spread across the entire desk. That's how it goes.",
      omnie_p3:       "Today every build that leaves the workshop is <strong>tested, recorded and documented</strong>. I don't ship anything I wouldn't use myself.",
      photo_caption:  'Standard work attire during stabilizer lubing.',
      how_i_work:     'How I work',
      p01_title:      'Component selection',
      p01_desc:       'Case, PCB, switch — each combination has a different sound character. I start by asking: what is it for?',
      p02_title:      'Hand lubing',
      p02_desc:       "Each switch individually. Krytox 205g0 for linears, 3203 for tactiles. Stem rails without 205g0 — to preserve pad dampening. Takes hours. You can hear the difference.",
      p03_title:      'Test & recording',
      p03_desc:       "Before shipping — acoustic test and recording. You hear it before you buy. No surprises when you open the package.",
      stat_builds:    'Builds 2026',
      stat_hours:     'Hours with tweezers',
      stat_recorded:  'Build recorded',
      stat_shipping:  'InPost shipping',
      why_title:      'Why I do this',
      why_p1:         "I don't believe in \"the best switch\". I believe in <strong>the right switch for a specific person</strong>. Someone who types for 8 hours needs something different from a gamer who wants the fastest pretravel on WASD. That's why I talk before recommending a build.",
      why_p2:         "It's surprising how a switch change can take you from the sound of slamming a porta-potty door, through clicking pebbles in a sandbox, to closing the door of a €300k car.",
      why_p3:         'A keyboard is the only thing you touch every hour of your working day. It should sound good.',
      cta_text:       'Ask about <em>your ideal build.</em><br>I\'ll reply the same day.',
      cta_btn:        'Write to me →',

      dzwieki_eyebrow:       'Compare the sound',
      dzwieki_title:         'Hear it before<br><em>you buy.</em>',
      dzwieki_sub:           'Click a build, listen to how it sounds. Every keyboard recorded under the same conditions.',
      dzwieki_panel_eyebrow: 'Sound test',
      dzwieki_select:        'Select a build',
      dzwieki_coming_soon:   'Recording coming soon',
    }
  };

  window.applyLang = function (lang) {
    const t = window.I18N[lang];
    if (!t) return;
    document.querySelectorAll('[data-t]').forEach(el => {
      const v = t[el.dataset.t];
      if (v !== undefined) el.textContent = v;
    });
    document.querySelectorAll('[data-t-html]').forEach(el => {
      const v = t[el.dataset.tHtml];
      if (v !== undefined) el.innerHTML = v;
    });
    document.querySelectorAll('[data-t-ph]').forEach(el => {
      const v = t[el.dataset.tPh];
      if (v !== undefined) el.placeholder = v;
    });
    document.querySelectorAll('.lang-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.lang === lang);
    });
    document.documentElement.lang = lang;
  };

  window.setLang = function (lang) {
    if (!supported.includes(lang)) return;
    localStorage.setItem('lang', lang);
    window.LANG = lang;
    location.reload();
  };

  document.addEventListener('DOMContentLoaded', function () {
    window.applyLang(window.LANG);
  });
})();
