/* ============================================================================
   HST Architects — site behaviour
   Theme, navigation, reveal, accordion, project filters, contact form.
   ========================================================================= */
(function () {
  "use strict";

  var doc = document;
  var root = doc.documentElement;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

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
    filterBar.addEventListener("click", function (e) {
      var b = e.target.closest(".filter");
      if (!b) return;
      var val = b.dataset.filter;
      filterBar.querySelectorAll(".filter").forEach(function (f) {
        f.classList.toggle("is-active", f === b);
        f.setAttribute("aria-pressed", String(f === b));
      });
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

      var payload = {
        name: form.elements.name.value.trim(),
        email: form.elements.email.value.trim(),
        phone: (form.elements.phone && form.elements.phone.value.trim()) || null,
        service: (form.elements.service && form.elements.service.value) || null,
        budget: (form.elements.budget && form.elements.budget.value) || null,
        message: form.elements.message.value.trim(),
        source_page: window.location.pathname
      };   // created_at is set by the database, not the client

      submit.disabled = true;
      var original = submit.querySelector("span") ? submit.querySelector("span").textContent : submit.textContent;
      if (submit.querySelector("span")) submit.querySelector("span").textContent = "Sending…";

      send(payload).then(function () {
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

    function send(payload) {
      var cfg = window.HST_CONFIG || {};
      if (cfg.supabaseUrl && cfg.supabaseAnonKey) {
        return fetch(cfg.supabaseUrl.replace(/\/$/, "") + "/rest/v1/enquiries", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "apikey": cfg.supabaseAnonKey,
            "Authorization": "Bearer " + cfg.supabaseAnonKey,
            "Prefer": "return=minimal"
          },
          body: JSON.stringify(payload)
        }).then(function (r) {
          if (!r.ok) return r.text().then(function (t) { throw new Error("HTTP " + r.status + " " + t); });
        });
      }
      return Promise.reject(new Error("Backend not configured"));
    }
  }

  /* ---------- current year ------------------------------------------------ */
  doc.querySelectorAll("[data-year]").forEach(function (n) { n.textContent = new Date().getFullYear(); });
})();
