// Enquiry endpoint for hstarchitects.com.
//
// One request does both halves of the job: the enquiry is written to Supabase so
// it is never lost, and it is emailed to the studio so someone actually sees it.
//
// There is no third-party mail service and nothing to pay for. The mail goes out
// over SMTP from the studio's own mailbox, using a Google app password that lives
// only in Vercel's environment variables. Sender and recipient are the same
// account, so no domain has to be verified and no reputation has to be warmed up.
//
// Deliberately dependency-free: no package.json, no node_modules, no install step
// at deploy. The static site at the repo root keeps shipping exactly as it did.
//
// Environment variables (Vercel -> Project -> Settings -> Environment Variables):
//   SMTP_USER    the Gmail address that sends, e.g. hstarchitects.dev@gmail.com
//   SMTP_PASS    a Google app password for that account, 16 characters  [secret]
//   ENQUIRY_TO   where enquiries land                    (default: SMTP_USER)
//   SMTP_HOST    (default smtp.gmail.com)
//   SMTP_PORT    (default 465, implicit TLS)
//
// Without SMTP_USER and SMTP_PASS the endpoint still stores the enquiry and
// reports that it could not email it. A misconfiguration on our side must never
// be the visitor's problem.
//
// Meta Conversions API (optional; scope these to Production only):
//   META_PIXEL_ID         the pixel / dataset ID, same as SITE["meta_pixel_id"]
//   META_CAPI_TOKEN       Events Manager -> dataset -> Settings -> Conversions
//                         API -> Generate access token                [secret]
//   META_TEST_EVENT_CODE  only while testing, from the Test events tab; remove
//                         it afterwards, since test events are not counted live
//   META_GRAPH_VERSION    (default v26.0)
// Without the first two the Meta step is skipped. It can never fail an enquiry,
// and never delays one by more than META_TIMEOUT_MS.

const tls = require("tls");
const crypto = require("crypto");

// The same publishable values already shipped to every visitor in
// assets/js/config.js, so nothing here is secret. Overridable by env.
const SUPABASE_URL = process.env.SUPABASE_URL || "https://mhfempltoebztrvybidb.supabase.co";
const SUPABASE_KEY = process.env.SUPABASE_ANON_KEY || "sb_publishable_n0lmxgelzVR3py-ZOTDuCQ_O991Dxlr";

// Deliver to the sending mailbox itself rather than to info@hstarchitects.com.
// That address forwards through ImprovMX straight back to this same Gmail, and
// Gmail silently drops a message arriving with a Message-ID it just sent out.
// ImprovMX works around it by rewriting the Message-ID and re-signing with its
// own DKIM key, which breaks DMARC alignment and gets the notification filed as
// spam or phishing. Skipping the round trip avoids all of that. Set ENQUIRY_TO
// explicitly once enquiries should reach a mailbox other than the sender's.
const MAIL_TO = process.env.ENQUIRY_TO || process.env.SMTP_USER || "info@hstarchitects.com";
const SMTP_HOST = process.env.SMTP_HOST || "smtp.gmail.com";
const SMTP_PORT = Number(process.env.SMTP_PORT || 465);

const CRLF = "\r\n";
const LIMITS = { name: 120, email: 160, phone: 40, service: 80, budget: 60, message: 4000, source_page: 200 };

// Campaign parameters the browser may send with an enquiry (see site.js). Only
// these keys are kept, each value cut to 200 characters, so the column cannot
// be used to store anything else.
const ATTR_KEYS = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "utm_id",
  "fbclid", "gclid", "landing", "referrer"];

function cleanAttribution(a) {
  if (!a || typeof a !== "object" || Array.isArray(a)) return null;
  const out = {};
  let any = false;
  for (const k of ATTR_KEYS) {
    const v = a[k];
    if (typeof v === "string" && v.trim()) { out[k] = v.trim().slice(0, 200); any = true; }
  }
  return any ? out : null;
}

/* ---------------------------------------------------------------- helpers */

function str(v, max) {
  if (typeof v !== "string") return null;
  const t = v.trim();
  return t ? t.slice(0, max) : null;
}

// Headers must not carry raw newlines; that is how header injection works.
function headerSafe(v) {
  return String(v).replace(/[\r\n]+/g, " ").trim();
}

// RFC 2047, so an Arabic or accented name survives in the subject line.
function encodeHeader(v) {
  const s = headerSafe(v);
  if (/^[ -~]*$/.test(s)) return s;
  return "=?UTF-8?B?" + Buffer.from(s, "utf8").toString("base64") + "?=";
}

/* ------------------------------------------------------------------- SMTP */

// A minimal SMTP client. Implicit TLS on 465 rather than STARTTLS on 587,
// because it removes a whole negotiation step and Gmail supports both.
function sendMail({ user, pass, to, replyTo, subject, text }) {
  return new Promise((resolve, reject) => {
    const socket = tls.connect({ host: SMTP_HOST, port: SMTP_PORT, servername: SMTP_HOST });
    socket.setEncoding("utf8");
    socket.setTimeout(15000);

    let buffer = "";
    const ready = [];    // replies that arrived before anything asked for them
    const waiting = [];  // askers that got there before their reply
    let settled = false;

    const finish = (err) => {
      if (settled) return;
      settled = true;
      try { socket.destroy(); } catch (_) { /* already gone */ }
      if (err) reject(err); else resolve();
    };

    socket.on("timeout", () => finish(new Error("SMTP timeout")));
    socket.on("error", finish);
    socket.on("close", () => finish(new Error("SMTP connection closed early")));

    socket.on("data", (chunk) => {
      buffer += chunk;
      // A reply may span several lines. Continuation lines put a hyphen after
      // the code ("250-STARTTLS"); the last one puts a space ("250 OK").
      for (;;) {
        const at = buffer.search(/^\d{3} .*$/m);
        if (at === -1) break;
        const nl = buffer.indexOf("\n", at);
        if (nl === -1) break;
        const reply = buffer.slice(0, nl + 1);
        buffer = buffer.slice(nl + 1);
        const parsed = { code: Number(reply.slice(at, at + 3)), text: reply.trim() };
        if (waiting.length) waiting.shift()(parsed);
        else ready.push(parsed);
      }
    });

    const expect = (codes) => new Promise((ok, bad) => {
      const check = (r) => {
        if (codes.indexOf(r.code) !== -1) ok(r.text);
        else bad(new Error("SMTP " + r.code + ": " + r.text.slice(0, 200)));
      };
      if (ready.length) check(ready.shift());
      else waiting.push(check);
    });

    const say = (line) => { socket.write(line + CRLF); };

    const message = [
      "From: " + encodeHeader("HST Architects website") + " <" + user + ">",
      "To: <" + to + ">",
      // omitted for a phone-only lead rather than printed as "<null>"
      replyTo ? "Reply-To: <" + headerSafe(replyTo) + ">" : null,
      "Subject: " + encodeHeader(subject),
      "MIME-Version: 1.0",
      'Content-Type: text/plain; charset="utf-8"',
      "Content-Transfer-Encoding: base64",
      "",
      // base64 sidesteps dot-stuffing and the 998-character line limit at once
      Buffer.from(text, "utf8").toString("base64").replace(/(.{76})/g, "$1" + CRLF),
    ].filter(function (h) { return h !== null; }).join(CRLF);

    (async () => {
      try {
        await expect([220]);
        say("EHLO hstarchitects.com");
        await expect([250]);
        say("AUTH LOGIN");
        await expect([334]);
        say(Buffer.from(user, "utf8").toString("base64"));
        await expect([334]);
        say(Buffer.from(pass, "utf8").toString("base64"));
        await expect([235]);
        say("MAIL FROM:<" + user + ">");
        await expect([250]);
        say("RCPT TO:<" + to + ">");
        await expect([250, 251]);
        say("DATA");
        await expect([354]);
        socket.write(message + CRLF + "." + CRLF);
        await expect([250]);
        say("QUIT");
        // The server closing now is the expected ending, not a failure. end()
        // rather than destroy() so the peer sees a clean FIN instead of a reset.
        settled = true;
        try { socket.end(); } catch (_) { /* already gone */ }
        resolve();
      } catch (e) {
        finish(e);
      }
    })();
  });
}

/* ----------------------------------------------------- Meta Conversions API */

// The server-side twin of the browser pixel's Lead. Same event_name, same
// event_id, so Meta keeps one of the pair. It recovers leads whose browser event
// was blocked, and carries hashed contact details for matching to the ad.

const META_GRAPH_VERSION = process.env.META_GRAPH_VERSION || "v26.0";
const META_TIMEOUT_MS = 2500;
const SITE_ORIGIN = "https://hstarchitects.com";
// Same list as the GA consent defaults in tools/layout.py. The second line of
// defence behind the browser's time-zone check, using Vercel's IP country.
const EUROPE = new Set(["AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR",
  "HU", "IE", "IT", "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE",
  "IS", "LI", "NO", "GB", "CH"]);

function sha256(v) {
  return crypto.createHash("sha256").update(v, "utf8").digest("hex");
}

// Meta: trim, lowercase.
function normEmail(v) {
  return v ? v.trim().toLowerCase() : null;
}

// Meta: digits only, with country code, no leading zeros. The audience is in
// the UAE, so a number typed in local form (050..., 04...) is taken as UAE and
// given 971; "+971 050..." loses the stray trunk zero. Anything else is sent as
// typed, digits only. The UAE default is our assumption, not Meta's rule.
function normPhone(v) {
  if (!v) return null;
  const raw = v.trim();
  let d = raw.replace(/\D/g, "");
  if (!d) return null;
  if (raw.charAt(0) === "+") { /* already carries its country code */ }
  else if (d.startsWith("00")) d = d.slice(2);
  else if (d.startsWith("0")) d = "971" + d.slice(1);
  else if (/^5\d{8}$/.test(d)) d = "971" + d;
  if (d.startsWith("9710")) d = "971" + d.slice(4);
  d = d.replace(/^0+/, "");
  return d.length >= 8 && d.length <= 15 ? d : null;
}

// Meta: lowercase, no punctuation, UTF-8 for non-Latin script. The form has one
// name field, so the first word becomes fn and the last word ln.
function normNamePart(v) {
  if (!v) return null;
  const s = v.normalize("NFC").toLowerCase().replace(/[\p{P}\p{S}]/gu, "").trim();
  return s || null;
}
function splitName(full) {
  const parts = String(full || "").trim().split(/\s+/).filter(Boolean);
  return {
    fn: normNamePart(parts[0]),
    ln: parts.length > 1 ? normNamePart(parts[parts.length - 1]) : null,
  };
}

function readCookie(req, name) {
  const parts = String(req.headers.cookie || "").split(";");
  for (const p of parts) {
    const i = p.indexOf("=");
    if (i > 0 && p.slice(0, i).trim() === name) return p.slice(i + 1).trim();
  }
  return null;
}
// _fbp and _fbc go to Meta exactly as stored: never hashed, never re-cased.
function clickCookie(req, name) {
  const v = readCookie(req, name);
  return v && v.length <= 500 && /^fb\.\d\.\d{10,13}\.\S+$/.test(v) ? v : null;
}

// Never throws, never takes longer than META_TIMEOUT_MS.
async function sendMetaLead(req, payload, row) {
  const pixel = process.env.META_PIXEL_ID;
  const token = process.env.META_CAPI_TOKEN;
  const testCode = process.env.META_TEST_EVENT_CODE;
  if (!pixel || !token) return;
  // belt and braces behind scoping the env vars to Production
  if (process.env.VERCEL_ENV && process.env.VERCEL_ENV !== "production" && !testCode) return;
  // only when the browser was allowed to run the pixel (production, not Europe)
  if (payload.meta_consent !== true) return;
  // no id means no deduplication against the browser Lead, so send nothing
  const eventId = typeof payload.event_id === "string" && /^[A-Za-z0-9._:-]{8,100}$/.test(payload.event_id)
    ? payload.event_id : null;
  if (!eventId) return;
  const country = String(req.headers["x-vercel-ip-country"] || "").toUpperCase();
  if (EUROPE.has(country)) return;

  const ua = String(req.headers["user-agent"] || "");
  if (!ua) return;   // required by Meta for website events
  const ip = String(req.headers["x-forwarded-for"] || req.headers["x-real-ip"] || "").split(",")[0].trim();

  const user = { client_user_agent: ua };
  if (ip) user.client_ip_address = ip;
  const em = normEmail(row.email);
  const ph = normPhone(row.phone);
  const name = splitName(row.name);
  if (em) user.em = [sha256(em)];
  if (ph) user.ph = [sha256(ph)];
  if (name.fn) user.fn = [sha256(name.fn)];
  if (name.ln) user.ln = [sha256(name.ln)];
  const fbp = clickCookie(req, "_fbp");
  const fbc = clickCookie(req, "_fbc");
  if (fbp) user.fbp = fbp;
  if (fbc) user.fbc = fbc;

  // built from the path only, so it always sits on the verified domain
  const path = row.source_page && /^\/[A-Za-z0-9\-._~\/]*$/.test(row.source_page) ? row.source_page : "/";
  const body = {
    data: [{
      event_name: "Lead",
      event_time: Math.floor(Date.now() / 1000),
      event_id: eventId,
      action_source: "website",
      event_source_url: SITE_ORIGIN + path,
      user_data: user,
      // mirrors the browser Lead exactly; never the message, never the budget
      custom_data: {
        content_name: "Website enquiry",
        content_category: row.service || "Not specified",
      },
    }],
  };
  if (testCode) body.test_event_code = testCode;

  // the token rides in the query string as in Meta's examples; never log this URL
  const url = "https://graph.facebook.com/" + META_GRAPH_VERSION + "/" + encodeURIComponent(pixel) +
    "/events?access_token=" + encodeURIComponent(token);
  const ctrl = new AbortController();
  const timer = setTimeout(function () { ctrl.abort(); }, META_TIMEOUT_MS);
  try {
    const r = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal: ctrl.signal,
    });
    if (!r.ok) console.error("[enquiry] meta capi HTTP " + r.status, (await r.text()).slice(0, 300));
  } catch (e) {
    console.error("[enquiry] meta capi failed", String(e && e.message ? e.message : e).slice(0, 200));
  } finally {
    clearTimeout(timer);
  }
}

/* ------------------------------------------------------- no-JS form posts */

// The forms carry method="post" action="/api/enquiry/", so a submission made
// before site.js has attached its handler (slow connection) or without it
// (script blocked) arrives here url-encoded instead of turning into a GET that
// would put the visitor's details in the address bar. Such a visitor needs a
// page back, not JSON: success goes to the thanks page, a refusal gets a short
// page saying why, with a way back to the form.
const FORM_PAGES = ["/contact/", "/consultation/"];

function htmlEsc(s) {
  return String(s).replace(/[&<>"']/g, function (c) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
  });
}

function refusalPage(message, back) {
  return '<!doctype html><html lang="en"><head><meta charset="utf-8">' +
    '<meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">' +
    "<title>Your enquiry was not sent | HST Architects</title></head>" +
    '<body style="font:16px/1.6 system-ui,sans-serif;max-width:34rem;margin:4rem auto;padding:0 1rem;color:#16202b">' +
    '<h1 style="font-size:1.4rem">Your enquiry was not sent</h1>' +
    "<p>" + htmlEsc(message) + "</p>" +
    '<p><a href="' + htmlEsc(back) + '">Back to the form</a>, or call ' +
    '<a href="tel:+971503999314">+971 50 399 9314</a>.</p></body></html>';
}

/* ----------------------------------------------------------------- handler */

module.exports = async (req, res) => {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Use POST." });
  }

  const native = /application\/x-www-form-urlencoded/i.test(String((req.headers && req.headers["content-type"]) || ""));
  const reply = function (code, body) {
    if (!native) return res.status(code).json(body);
    if (code === 200) {
      res.setHeader("Location", "/consultation/thanks/");
      return res.status(303).end();
    }
    const from = payload && typeof payload === "object" ? str(payload.source_page, 200) : null;
    res.setHeader("Content-Type", "text/html; charset=utf-8");
    return res.status(code).send(refusalPage(body.error, FORM_PAGES.indexOf(from) !== -1 ? from : "/contact/"));
  };

  let payload = req.body;
  if (typeof payload === "string") {
    try { payload = JSON.parse(payload); } catch (_) { payload = null; }
  }
  if (!payload || typeof payload !== "object") {
    return reply(400, { error: "Expected a JSON body." });
  }

  // The honeypot is a field no human can see. Answer as though it worked, so a
  // bot learns nothing from the response, and drop the submission on the floor.
  if (str(payload.company, 200)) return reply(200, { ok: true });

  const row = {
    name: str(payload.name, LIMITS.name),
    email: str(payload.email, LIMITS.email),
    phone: str(payload.phone, LIMITS.phone),
    service: str(payload.service, LIMITS.service),
    budget: str(payload.budget, LIMITS.budget),
    message: str(payload.message, LIMITS.message),
    source_page: str(payload.source_page, LIMITS.source_page),
  };

  if (!row.name) return reply(400, { error: "A name is required." });
  // The contact page asks for an email; the ads landing page asks for a phone
  // number first and makes email optional. Either way there must be one way
  // back to the person, and an email that is given must look like one.
  if (row.email && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(row.email)) {
    return reply(400, { error: "Please check the email address, or leave it blank." });
  }
  const phoneDigits = (row.phone || "").replace(/\D/g, "");
  if (!row.email && (phoneDigits.length < 8 || phoneDigits.length > 15)) {
    return reply(400, { error: "Please leave a phone number or an email address." });
  }
  // The landing page makes the note optional; site.js composes a message when
  // it is short, and this does the same for a form posted without site.js.
  if (row.source_page === "/consultation/" && (!row.message || row.message.length < 10)) {
    const base = "Consultation request from the landing page" + (row.service ? " (" + row.service + ")" : "") + ".";
    row.message = row.message ? base + " Note: " + row.message : base;
  }
  if (!row.message || row.message.length < 10) {
    return reply(400, { error: "Please say a little about the project." });
  }

  const attr = cleanAttribution(payload.attribution);

  // 1. Store it. Losing the enquiry is the only real failure, so this decides
  //    the status code and the email is best-effort on top.
  const insert = function (body) {
    return fetch(SUPABASE_URL.replace(/\/$/, "") + "/rest/v1/enquiries", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        apikey: SUPABASE_KEY,
        Prefer: "return=minimal",
      },
      body: JSON.stringify(body),
    });
  };
  let stored = false;
  let storeError = null;
  try {
    let r = await insert(attr ? Object.assign({}, row, { attribution: attr }) : row);
    if (!r.ok && attr && r.status === 400) {
      // Until supabase/migrations/0002_attribution.sql adds the column,
      // PostgREST rejects the unknown field. Store the enquiry without it rather
      // than lose it; the campaign still reaches the studio in the email.
      const why = await r.text();
      if (/attribution/i.test(why)) r = await insert(row);
      else storeError = "HTTP 400 " + why.slice(0, 200);
    }
    stored = r.ok;
    if (!r.ok && !storeError) storeError = "HTTP " + r.status + " " + (await r.text()).slice(0, 200);
  } catch (e) {
    storeError = String(e).slice(0, 200);
  }

  // 1b. Tell Meta, in parallel with the email so it adds no time. Only once the
  //     enquiry is safely stored; if storage failed it waits to see whether the
  //     email got through instead.
  let meta = stored ? sendMetaLead(req, payload, row) : null;

  // 2. Email it.
  let emailed = false;
  let emailError = null;
  const user = process.env.SMTP_USER;
  const pass = process.env.SMTP_PASS;
  if (user && pass) {
    const lines = [
      "Name:    " + row.name,
      row.email ? "Email:   " + row.email : "Email:   (not given)",
      row.phone ? "Phone:   " + row.phone : null,
      phoneDigits.length >= 8 ? "WhatsApp: https://wa.me/" + phoneDigits : null,
      row.service ? "Service: " + row.service : null,
      row.budget ? "Budget:  " + row.budget : null,
      row.source_page ? "Page:    https://hstarchitects.com" + row.source_page : null,
      attr ? "Source:  " + [attr.utm_source, attr.utm_medium, attr.utm_campaign].filter(Boolean).join(" / ") +
        (attr.fbclid ? " (Meta ad click)" : attr.gclid ? " (Google ad click)" : "") : null,
      attr && attr.utm_content ? "Ad:      " + attr.utm_content : null,
      attr && attr.landing ? "Landed:  https://hstarchitects.com" + attr.landing : null,
      "",
      row.message,
      "",
      "--",
      "Sent by the enquiry form on hstarchitects.com. Reply to answer the sender directly.",
    ].filter(Boolean);
    try {
      await sendMail({
        user: user,
        pass: pass,
        to: MAIL_TO,
        replyTo: row.email,   // may be null for a phone-only lead; see sendMail
        subject: (row.source_page === "/consultation/" ? "Consultation request from " : "Website enquiry from ") + row.name,
        text: lines.join("\n"),
      });
      emailed = true;
    } catch (e) {
      emailError = String(e && e.message ? e.message : e).slice(0, 200);
    }
  } else {
    emailError = "SMTP_USER / SMTP_PASS not set";
  }

  // Awaited rather than left dangling: a Vercel function is not guaranteed to
  // keep running after it responds unless waitUntil() from @vercel/functions is
  // used, and this file stays dependency-free. Bounded by META_TIMEOUT_MS and it
  // never rejects, so the visitor's answer cannot be lost to it.
  if (!meta && emailed) meta = sendMetaLead(req, payload, row);
  if (meta) await meta;

  if (!stored && !emailed) {
    console.error("[enquiry] lost", { storeError: storeError, emailError: emailError });
    return reply(502, { error: "Could not record that enquiry." });
  }
  if (!stored) console.error("[enquiry] not stored", storeError);
  if (!emailed) console.error("[enquiry] not emailed", emailError);

  return reply(200, { ok: true, stored: stored, emailed: emailed });
};
