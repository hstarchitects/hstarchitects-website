/* ============================================================================
   HST Architects, site behaviour
   Theme, navigation, reveal, accordion, project filters, contact form.
   ========================================================================= */
(function () {
  "use strict";

  var doc = document;
  var root = doc.documentElement;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- measurement -------------------------------------------------- */
  // Every helper below is a no-op unless its tag actually loaded, so local
  // previews, Vercel previews and visitors the tags skip send nothing.

  // Meta: window.HST_META is set by the head snippet (tools/layout.py), true
  // only on the production host for visitors outside Europe.
  function metaOn() {
    return window.HST_META === true && typeof window.fbq === "function";
  }
  function metaTrack(name, params, eventId) {
    if (!metaOn()) return;
    try {
      if (eventId) window.fbq("track", name, params || {}, { eventID: eventId });
      else window.fbq("track", name, params || {});
    } catch (e) {}
  }
  function gaEvent(name, params) {
    if (typeof window.gtag !== "function") return;
    try { window.gtag("event", name, params || {}); } catch (e) {}
  }
  // One id per conversion, shared by the browser pixel and the server-side
  // Conversions API call, so Meta counts the pair once.
  function newEventId() {
    try { if (window.crypto && crypto.randomUUID) return crypto.randomUUID(); } catch (e) {}
    return "ev-" + Date.now().toString(36) + "-" + Math.random().toString(36).slice(2, 12);
  }

  // Campaign attribution. An ad click lands with utm_* and a click id; the
  // visitor may read three pages before they enquire, so the parameters are kept
  // for the tab and sent with the enquiry, which is how the studio learns which
  // advert produced it. The latest tagged landing wins and replaces the whole
  // record: that is the click that brought the person back, and it is what
  // Meta's own _fbc cookie reflects, so the two never disagree. An untagged page
  // view leaves the record alone.
  var ATTR_KEYS = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "utm_id", "fbclid", "gclid"];
  function attribution() {
    try { return JSON.parse(sessionStorage.getItem("hst_attr") || "null"); } catch (e) { return null; }
  }
  (function () {
    var q;
    try { q = new URL(window.location.href).searchParams; } catch (e) { return; }
    var found = {}, any = false;
    ATTR_KEYS.forEach(function (k) {
      var v = q.get(k);
      if (v) { found[k] = v.slice(0, 200); any = true; }
    });
    if (!any) return;
    found.landing = window.location.pathname;
    if (doc.referrer) {
      try { found.referrer = new URL(doc.referrer).hostname; } catch (e) {}
    }
    try { sessionStorage.setItem("hst_attr", JSON.stringify(found)); } catch (e) {}
  })();

  // _fbc fallback. The pixel writes this cookie itself from ?fbclid= when it
  // loads; this only matters when fbevents.js is blocked, so /api/enquiry can
  // still attribute the lead to the ad click. Format per Meta:
  // fb.<subdomainIndex>.<creation time in ms>.<fbclid>, fbclid unmodified.
  (function () {
    if (window.HST_META !== true) return;
    var id = null;
    try { id = new URL(window.location.href).searchParams.get("fbclid"); } catch (e) {}
    if (!id || !/^[A-Za-z0-9_-]{8,500}$/.test(id)) return;
    var m = doc.cookie.match(/(?:^|;\s*)_fbc=([^;]+)/);
    if (m && m[1].slice(-id.length) === id) return;
    doc.cookie = "_fbc=fb.1." + Date.now() + "." + id +
      "; max-age=7776000; path=/; SameSite=Lax; Secure";
  })();

  // Contact: taps on phone, WhatsApp and email. Once per channel per page view,
  // so a double tap is not two contacts.
  var contacted = {};
  doc.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest('a[href^="tel:"], a[href^="https://wa.me/"], a[href^="mailto:"]');
    if (!a) return;
    var href = a.getAttribute("href");
    var method = href.indexOf("tel:") === 0 ? "phone" : href.indexOf("mailto:") === 0 ? "email" : "whatsapp";
    if (contacted[method]) return;
    contacted[method] = true;
    metaTrack("Contact", { contact_method: method });
    gaEvent("contact_click", { method: method });
  });

  /* ---------- theme ------------------------------------------------------ */
  function applyTheme(t) {
    root.setAttribute("data-theme", t);
    try { localStorage.setItem("hst-theme", t); } catch (e) {}
    var m = doc.querySelector('meta[name="theme-color"]');
    if (m) m.setAttribute("content", t === "dark" ? "#0E1620" : "#F1EDE4");
    doc.querySelectorAll("[data-theme-toggle]").forEach(function (b) {
      b.setAttribute("aria-label", t === "dark" ? "Switch to light theme" : "Switch to dark theme");
      b.setAttribute("aria-pressed", String(t === "dark"));
    });
  }

  doc.addEventListener("click", function (e) {
    var t = e.target.closest("[data-theme-toggle]");
    if (!t) return;
    applyTheme(root.getAttribute("data-theme") === "dark" ? "light" : "dark");
  });

  // sync with the OS while the visitor has made no explicit choice
  var mq = window.matchMedia("(prefers-color-scheme: dark)");
  (mq.addEventListener ? mq.addEventListener.bind(mq, "change") : mq.addListener.bind(mq))(function (e) {
    var stored = null;
    try { stored = localStorage.getItem("hst-theme"); } catch (err) {}
    if (!stored) applyTheme(e.matches ? "dark" : "light");
  });

  /* ---------- header hide on scroll -------------------------------------- */
  var header = doc.querySelector(".header");
  if (header) {
    var last = 0, ticking = false;
    window.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var y = window.scrollY;
        if (y > last && y > 320) header.classList.add("is-hidden");
        else header.classList.remove("is-hidden");
        last = y;
        ticking = false;
      });
    }, { passive: true });
  }

  /* ---------- mobile drawer ---------------------------------------------- */
  var drawer = doc.getElementById("drawer");
  function setDrawer(open) {
    if (!drawer) return;
    drawer.classList.toggle("is-open", open);
    drawer.setAttribute("aria-hidden", String(!open));
    doc.body.style.overflow = open ? "hidden" : "";
    var btn = doc.querySelector("[data-drawer-open]");
    if (btn) btn.setAttribute("aria-expanded", String(open));
    if (open) { var f = drawer.querySelector("a, button"); if (f) f.focus(); }
  }
  doc.addEventListener("click", function (e) {
    if (e.target.closest("[data-drawer-open]")) { setDrawer(true); return; }
    if (e.target.closest("[data-drawer-close]")) { setDrawer(false); return; }
    if (drawer && drawer.classList.contains("is-open") && e.target.closest(".drawer__nav a")) setDrawer(false);
  });
  doc.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && drawer && drawer.classList.contains("is-open")) setDrawer(false);
  });

  /* ---------- reveal on scroll ------------------------------------------- */
  var items = doc.querySelectorAll(".reveal");
  if (!items.length) { /* nothing */ }
  else if (reduced || !("IntersectionObserver" in window)) {
    items.forEach(function (n) { n.classList.add("is-in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.06 });
    items.forEach(function (n) { io.observe(n); });
  }

  /* ---------- FAQ accordion ---------------------------------------------- */
  doc.querySelectorAll(".faq__q").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var item = btn.closest(".faq__item");
      var panel = item.querySelector(".faq__a");
      var open = item.classList.contains("is-open");
      // close siblings within the same list
      item.parentElement.querySelectorAll(".faq__item.is-open").forEach(function (o) {
        if (o === item) return;
        o.classList.remove("is-open");
        o.querySelector(".faq__q").setAttribute("aria-expanded", "false");
        o.querySelector(".faq__a").style.height = "0px";
      });
      item.classList.toggle("is-open", !open);
      btn.setAttribute("aria-expanded", String(!open));
      panel.style.height = open ? "0px" : panel.scrollHeight + "px";
    });
  });
  window.addEventListener("resize", function () {
    doc.querySelectorAll(".faq__item.is-open .faq__a").forEach(function (p) {
      p.style.height = p.scrollHeight + "px";
    });
  });

  /* ---------- project filters -------------------------------------------- */
  var filterBar = doc.querySelector("[data-filters]");
  if (filterBar) {
    var thumb = filterBar.querySelector(".filters__thumb");

    // move the glass indicator under whichever segment is active
    function moveThumb(btn, animate) {
      if (!thumb || !btn) return;
      var br = filterBar.getBoundingClientRect();
      var r = btn.getBoundingClientRect();
      // getBoundingClientRect includes the capsule's own border, but the thumb is
      // positioned inside the padding box, so subtract it or every stop is off by 1px
      var bcs = getComputedStyle(filterBar);
      var bl = parseFloat(bcs.borderLeftWidth) || 0;
      var bt = parseFloat(bcs.borderTopWidth) || 0;
      if (!animate) thumb.style.transition = "none";
      thumb.style.width = r.width + "px";
      thumb.style.height = r.height + "px";
      thumb.style.transform = "translate(" + (r.left - br.left - bl) + "px," +
                              (r.top - br.top - bt - (parseFloat(getComputedStyle(thumb).top) || 0)) + "px)";
      thumb.style.opacity = "1";
      if (!animate) {
        // force a reflow so the suppressed transition does not leak into the next move
        void thumb.offsetWidth;
        thumb.style.transition = "";
      }
    }

    filterBar.addEventListener("click", function (e) {
      var b = e.target.closest(".filter");
      if (!b) return;
      var val = b.dataset.filter;
      filterBar.querySelectorAll(".filter").forEach(function (f) {
        f.classList.toggle("is-active", f === b);
        f.setAttribute("aria-pressed", String(f === b));
      });
      moveThumb(b, true);
      doc.querySelectorAll("[data-cat]").forEach(function (card) {
        var show = val === "all" || card.dataset.cat === val;
        card.style.display = show ? "" : "none";
      });
      var url = new URL(window.location);
      if (val === "all") url.searchParams.delete("filter"); else url.searchParams.set("filter", val);
      history.replaceState(null, "", url);
    });
    var pre = new URL(window.location).searchParams.get("filter");
    if (pre) {
      var target = filterBar.querySelector('.filter[data-filter="' + CSS.escape(pre) + '"]');
      if (target) target.click();
    }

    // place the indicator once fonts have settled, and keep it in step on resize
    var settle = function () { moveThumb(filterBar.querySelector(".filter.is-active"), false); };
    settle();
    if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(settle);
    window.addEventListener("resize", settle);
  }

  /* ---------- back to top -------------------------------------------------- */
  var toTop = doc.querySelector("[data-to-top]");
  if (toTop) {
    toTop.hidden = false;
    var onScroll = function () {
      toTop.classList.toggle("is-in", window.scrollY > window.innerHeight * 0.6);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    toTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: reduced ? "auto" : "smooth" });
    });
  }

  /* ---------- horizontal rail buttons ------------------------------------ */
  doc.querySelectorAll("[data-rail]").forEach(function (nav) {
    var rail = doc.getElementById(nav.dataset.rail);
    if (!rail) return;
    nav.addEventListener("click", function (e) {
      var b = e.target.closest("button");
      if (!b) return;
      var step = rail.firstElementChild ? rail.firstElementChild.offsetWidth + 20 : 320;
      rail.scrollBy({ left: b.dataset.dir === "next" ? step : -step, behavior: reduced ? "auto" : "smooth" });
    });
  });

  /* ---------- contact form ----------------------------------------------- */
  var form = doc.getElementById("contact-form");
  if (form) {
    var status = doc.getElementById("form-status");
    var submit = form.querySelector('[type="submit"]');

    function fail(field, msg) {
      var w = field.closest(".field");
      w.classList.add("field--error");
      var e = w.querySelector(".field__err");
      if (e) {
        if (msg) e.textContent = msg;
        // give the message an id and point the input at it so screen readers read it
        if (!e.id) e.id = (field.id || field.name) + "-err";
        field.setAttribute("aria-describedby", e.id);
      }
      field.setAttribute("aria-invalid", "true");
    }
    function clear(field) {
      var w = field.closest(".field");
      w.classList.remove("field--error");
      field.removeAttribute("aria-invalid");
      field.removeAttribute("aria-describedby");
    }
    form.querySelectorAll("input, textarea, select").forEach(function (f) {
      f.addEventListener("input", function () { clear(f); });
    });

    function validate() {
      var ok = true;
      var name = form.elements.name, email = form.elements.email, message = form.elements.message;
      if (!name.value.trim()) { fail(name, "Please tell us your name."); ok = false; }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email.value.trim())) { fail(email, "Please enter a valid email address."); ok = false; }
      if (message.value.trim().length < 12) { fail(message, "A sentence or two about the project helps us reply properly."); ok = false; }
      return ok;
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      status.className = "form__status";
      if (form.elements.company && form.elements.company.value) return; // honeypot
      if (!validate()) {
        status.textContent = "Please check the highlighted fields.";
        status.classList.add("is-err");
        var bad = form.querySelector(".field--error input, .field--error textarea");
        if (bad) bad.focus();
        return;
      }

      var eventId = newEventId();
      var attr = attribution();
      var payload = {
        name: form.elements.name.value.trim(),
        email: form.elements.email.value.trim(),
        phone: (form.elements.phone && form.elements.phone.value.trim()) || null,
        service: (form.elements.service && form.elements.service.value) || null,
        budget: (form.elements.budget && form.elements.budget.value) || null,
        message: form.elements.message.value.trim(),
        source_page: window.location.pathname,
        // passed through so the endpoint can enforce the trap too, for anything
        // that posts to it directly rather than through this form
        company: (form.elements.company && form.elements.company.value) || "",
        // the same id goes to the browser Lead below and to the server's
        // Conversions API call, which only runs when the pixel may run here
        event_id: eventId,
        meta_consent: window.HST_META === true,
        attribution: attr
      };   // created_at is set by the database, not the client

      submit.disabled = true;
      var original = submit.querySelector("span") ? submit.querySelector("span").textContent : submit.textContent;
      if (submit.querySelector("span")) submit.querySelector("span").textContent = "Sending…";

      send(payload).then(function () {
        // Conversions fire only once the enquiry is safely recorded. Neither
        // carries the name, email, phone or message.
        metaTrack("Lead", {
          content_name: "Website enquiry",
          content_category: payload.service || "Not specified"
        }, eventId);
        gaEvent("generate_lead", {
          lead_source: (attr && attr.utm_source) || "direct",
          lead_service: payload.service || "not specified",
          lead_budget: payload.budget || "not specified",
          form_page: window.location.pathname
        });
        form.reset();
        status.textContent = "Thank you. Your enquiry has reached the studio and we will be in touch.";
        status.classList.add("is-ok");
      }).catch(function (err) {
        console.error("[hst] enquiry failed", err);
        var mail = doc.querySelector('a[href^="mailto:"]');
        var tel = doc.querySelector('a[href^="tel:"]');
        status.innerHTML = "We could not send that from the site. Please email " +
          (mail ? mail.outerHTML : "the studio") + " or call " + (tel ? tel.outerHTML : "us") + " instead.";
        status.classList.add("is-err");
      }).finally(function () {
        submit.disabled = false;
        if (submit.querySelector("span")) submit.querySelector("span").textContent = original;
        status.scrollIntoView({ block: "nearest", behavior: reduced ? "auto" : "smooth" });
      });
    });
  }

  /* ---------- enquiry transport (shared by both forms) ------------------- */
  // The endpoint stores the enquiry AND emails the studio, so it is the path
  // that actually reaches a human. If it is unreachable we still write to the
  // database directly, which is what the site did before it existed: the
  // enquiry is captured either way, it just may wait for someone to look.
  function send(payload) {
      // trailing slash on purpose: vercel.json sets trailingSlash, so the bare
      // path answers 308 and every submission would pay for an extra round trip
      return fetch("/api/enquiry/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      }).then(function (r) {
        if (r.ok) return;
        if (r.status >= 400 && r.status < 500) {
          // our own validation talking; a second attempt would say the same
          return r.json().catch(function () { return {}; }).then(function (b) {
            var e = new Error(b.error || "HTTP " + r.status);
            e.final = true;
            throw e;
          });
        }
        throw new Error("HTTP " + r.status);
      }).catch(function (err) {
        if (err && err.final) throw err;
        console.warn("[hst] enquiry endpoint unavailable, writing direct", err);
        return direct(payload);
      });
    }

    function direct(payload) {
      var cfg = window.HST_CONFIG || {};
      if (!cfg.supabaseUrl || !cfg.supabaseAnonKey) {
        return Promise.reject(new Error("Backend not configured"));
      }
      return fetch(cfg.supabaseUrl.replace(/\/$/, "") + "/rest/v1/enquiries", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "apikey": cfg.supabaseAnonKey,
          "Authorization": "Bearer " + cfg.supabaseAnonKey,
          "Prefer": "return=minimal"
        },
        // the endpoint accepts the honeypot field, the table does not
        body: JSON.stringify({
          name: payload.name, email: payload.email, phone: payload.phone,
          service: payload.service, budget: payload.budget,
          message: payload.message, source_page: payload.source_page
        })
      }).then(function (r) {
        if (!r.ok) return r.text().then(function (t) { throw new Error("HTTP " + r.status + " " + t); });
      });
    }

  /* ---------- consultation landing (/consultation/) ---------------------- */
  // Phone-first: name and a mobile number are all it asks for. Success goes to
  // /consultation/thanks/, which fires the conversion once from a one-time
  // token, so a reload or a shared thanks link never double-counts.
  function normPhone(v) {
    var s = String(v || "").trim().replace(/[\s().-]/g, "");
    if (/^00/.test(s)) s = "+" + s.slice(2);
    else if (/^971\d{8,9}$/.test(s)) s = "+" + s;
    else if (/^0\d{8,9}$/.test(s)) s = "+971" + s.slice(1);
    else if (/^5\d{8}$/.test(s)) s = "+971" + s;
    var d = s.replace(/\D/g, "");
    if (d.length < 8 || d.length > 15) return null;
    return (s.charAt(0) === "+" ? "+" : "") + d;
  }

  var lp = doc.getElementById("consultation-form");
  if (lp) {
    var lpStatus = lp.querySelector(".form__status");
    var lpSubmit = lp.querySelector('[type="submit"]');
    var more = lp.querySelector("[data-form-more]");
    var WA_BASE = "Hello HST Architects, I would like to arrange a consultation";
    var WA_TAIL = ". (Sent from hstarchitects.com/consultation)";

    // The optional fields stay folded on every screen. Opened by default on a
    // laptop they pushed the submit button below the fold, and fewer visible
    // fields is what gets a paid visitor to finish.

    function lpFail(field, msg) {
      var w = field.closest(".field");
      w.classList.add("field--error");
      var e = w.querySelector(".field__err");
      if (e) { if (msg) e.textContent = msg; field.setAttribute("aria-describedby", e.id); }
      field.setAttribute("aria-invalid", "true");
    }
    lp.querySelectorAll("input, textarea").forEach(function (f) {
      f.addEventListener("input", function () {
        var w = f.closest(".field");
        if (w) w.classList.remove("field--error");
        f.removeAttribute("aria-invalid");
      });
    });

    // choosing a service also tailors every WhatsApp link on the page
    function setService(title) {
      lp.querySelectorAll('input[name="service"]').forEach(function (r) { r.checked = (r.value === title); });
      var text = WA_BASE + (title && title !== "Multiple / not sure" ? " about " + title : "") + WA_TAIL;
      doc.querySelectorAll('a[href^="https://wa.me/"]').forEach(function (a) {
        a.href = a.href.split("?")[0] + "?text=" + encodeURIComponent(text);
      });
    }
    lp.addEventListener("change", function (e) {
      if (e.target.name === "service") setService(e.target.value);
    });
    // ?service=<key> preselects, so an ad group per discipline lands ready
    try {
      var key = new URL(window.location.href).searchParams.get("service");
      var preSvc = key && lp.querySelector('input[name="service"][data-key="' + key.replace(/[^a-z-]/g, "") + '"]');
      if (preSvc) setService(preSvc.value);
    } catch (e) {}

    function toForm() {
      var card = doc.getElementById("enquire");
      if (card) card.scrollIntoView({ block: "start", behavior: reduced ? "auto" : "smooth" });
      var n = doc.getElementById("lp-name");
      if (n) setTimeout(function () { n.focus({ preventScroll: true }); }, reduced ? 0 : 450);
    }
    doc.querySelectorAll("[data-focus-form], [data-dock-cta]").forEach(function (a) {
      a.addEventListener("click", function (e) { e.preventDefault(); toForm(); });
    });
    doc.querySelectorAll("[data-pick-service]").forEach(function (b) {
      b.addEventListener("click", function () { setService(b.getAttribute("data-pick-service")); toForm(); });
    });

    lp.addEventListener("submit", function (e) {
      e.preventDefault();
      lpStatus.className = "form__status";
      lpStatus.textContent = "";
      if (lp.elements.company && lp.elements.company.value) return; // honeypot

      var name = lp.elements.name, phone = lp.elements.phone, email = lp.elements.email;
      var ok = true;
      if (!name.value.trim()) { lpFail(name, "Please tell us your name."); ok = false; }
      var ph = normPhone(phone.value);
      if (!ph) { lpFail(phone, "Please enter a mobile or WhatsApp number we can reach you on."); ok = false; }
      var em = email.value.trim();
      if (em && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(em)) {
        if (more) more.open = true;
        lpFail(email, "Please check the email address, or leave it blank."); ok = false;
      }
      if (!ok) {
        lpStatus.textContent = "Please check the highlighted fields.";
        lpStatus.classList.add("is-err");
        var bad = lp.querySelector(".field--error input, .field--error textarea");
        if (bad) bad.focus();
        return;
      }

      var svcInput = lp.querySelector('input[name="service"]:checked');
      var svc = svcInput ? svcInput.value : "";
      var note = lp.elements.message.value.trim();
      // the table needs a message of ten characters or more
      var base = "Consultation request from the landing page" + (svc ? " (" + svc + ")" : "") + ".";
      var message = note.length >= 10 ? note : (note ? base + " Note: " + note : base);
      var eventId = newEventId();

      var payload = {
        name: name.value.trim(),
        email: em || null,
        phone: ph,
        service: svc || null,
        budget: null,
        message: message,
        source_page: window.location.pathname,
        company: (lp.elements.company && lp.elements.company.value) || "",
        event_id: eventId,
        meta_consent: window.HST_META === true,
        attribution: attribution()
      };

      lpSubmit.disabled = true;
      var label = lpSubmit.querySelector("span");
      var original = label ? label.textContent : "";
      if (label) label.textContent = "Sending…";

      send(payload).then(function () {
        // a one-time token for the thanks page, which fires the conversion
        var lead = { eid: eventId, service: svc, first: (payload.name.split(/\s+/)[0] || "").slice(0, 40) };
        var stored = false;
        try { sessionStorage.setItem("hst_lead", JSON.stringify(lead)); stored = true; } catch (err) {}
        if (!stored) fireLead(lead);
        window.location.assign("/consultation/thanks/");
      }).catch(function (err) {
        console.error("[hst] consultation request failed", err);
        if (err && err.final) {
          lpStatus.textContent = err.message;
        } else {
          lpStatus.innerHTML = "We could not send that from the site. Please call " +
            '<a href="tel:+971503999314">+971 50 399 9314</a> or message us on WhatsApp instead.';
        }
        lpStatus.classList.add("is-err");
        lpSubmit.disabled = false;
        if (label) label.textContent = original;
      });
    });
  }

  function fireLead(l) {
    metaTrack("Lead", { content_name: "Consultation request", content_category: l.service || "Not specified" }, l.eid);
    var a = attribution();
    gaEvent("generate_lead", {
      lead_source: (a && a.utm_source) || "direct",
      lead_service: l.service || "not specified",
      form_page: "/consultation/"
    });
  }

  // thanks page: fire once, then forget the token
  if (doc.body.classList.contains("lp--thanks")) {
    var lead = null;
    try { lead = JSON.parse(sessionStorage.getItem("hst_lead") || "null"); sessionStorage.removeItem("hst_lead"); } catch (e) {}
    if (lead) {
      // the pixel may still be loading; fbq queues calls until it arrives
      fireLead(lead);
      var slot = doc.querySelector("[data-lead-name]");
      if (slot && lead.first) slot.textContent = ", " + lead.first;
    }
  }

  // mobile dock: out of the way until the hero actions scroll off, and away
  // again while the form is on screen or being typed into
  var dock = doc.querySelector("[data-dock]");
  var heroCta = doc.querySelector("[data-hero-cta]");
  var formCard = doc.getElementById("enquire");
  if (dock && heroCta && "IntersectionObserver" in window) {
    var heroGone = false, formSeen = false, typing = false;
    var paint = function () { dock.classList.toggle("is-in", heroGone && !formSeen && !typing); };
    new IntersectionObserver(function (en) { heroGone = !en[0].isIntersecting; paint(); }).observe(heroCta);
    if (formCard) new IntersectionObserver(function (en) { formSeen = en[0].intersectionRatio >= 0.25; paint(); },
      { threshold: [0, 0.25, 0.5] }).observe(formCard);
    if (lp) {
      lp.addEventListener("focusin", function () { typing = true; paint(); });
      lp.addEventListener("focusout", function () { typing = false; paint(); });
    }
  }

  /* ---------- current year ------------------------------------------------ */
  doc.querySelectorAll("[data-year]").forEach(function (n) { n.textContent = new Date().getFullYear(); });
})();
