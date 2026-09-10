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
//   ENQUIRY_TO   where enquiries land          (default info@hstarchitects.com)
//   SMTP_HOST    (default smtp.gmail.com)
//   SMTP_PORT    (default 465, implicit TLS)
//
// Without SMTP_USER and SMTP_PASS the endpoint still stores the enquiry and
// reports that it could not email it. A misconfiguration on our side must never
// be the visitor's problem.

const tls = require("tls");

// The same publishable values already shipped to every visitor in
// assets/js/config.js, so nothing here is secret. Overridable by env.
const SUPABASE_URL = process.env.SUPABASE_URL || "https://mhfempltoebztrvybidb.supabase.co";
const SUPABASE_KEY = process.env.SUPABASE_ANON_KEY || "sb_publishable_n0lmxgelzVR3py-ZOTDuCQ_O991Dxlr";

const MAIL_TO = process.env.ENQUIRY_TO || "info@hstarchitects.com";
const SMTP_HOST = process.env.SMTP_HOST || "smtp.gmail.com";
const SMTP_PORT = Number(process.env.SMTP_PORT || 465);

const CRLF = "\r\n";
const LIMITS = { name: 120, email: 160, phone: 40, service: 80, budget: 60, message: 4000, source_page: 200 };

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
      "Reply-To: <" + headerSafe(replyTo) + ">",
      "Subject: " + encodeHeader(subject),
      "MIME-Version: 1.0",
      'Content-Type: text/plain; charset="utf-8"',
      "Content-Transfer-Encoding: base64",
      "",
      // base64 sidesteps dot-stuffing and the 998-character line limit at once
      Buffer.from(text, "utf8").toString("base64").replace(/(.{76})/g, "$1" + CRLF),
    ].join(CRLF);

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

/* ----------------------------------------------------------------- handler */

module.exports = async (req, res) => {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Use POST." });
  }

  let payload = req.body;
  if (typeof payload === "string") {
    try { payload = JSON.parse(payload); } catch (_) { payload = null; }
  }
  if (!payload || typeof payload !== "object") {
    return res.status(400).json({ error: "Expected a JSON body." });
  }

  // The honeypot is a field no human can see. Answer as though it worked, so a
  // bot learns nothing from the response, and drop the submission on the floor.
  if (str(payload.company, 200)) return res.status(200).json({ ok: true });

  const row = {
    name: str(payload.name, LIMITS.name),
    email: str(payload.email, LIMITS.email),
    phone: str(payload.phone, LIMITS.phone),
    service: str(payload.service, LIMITS.service),
    budget: str(payload.budget, LIMITS.budget),
    message: str(payload.message, LIMITS.message),
    source_page: str(payload.source_page, LIMITS.source_page),
  };

  if (!row.name) return res.status(400).json({ error: "A name is required." });
  if (!row.email || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(row.email)) {
    return res.status(400).json({ error: "A valid email address is required." });
  }
  if (!row.message || row.message.length < 10) {
    return res.status(400).json({ error: "Please say a little about the project." });
  }

  // 1. Store it. Losing the enquiry is the only real failure, so this decides
  //    the status code and the email is best-effort on top.
  let stored = false;
  let storeError = null;
  try {
    const r = await fetch(SUPABASE_URL.replace(/\/$/, "") + "/rest/v1/enquiries", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        apikey: SUPABASE_KEY,
        Authorization: "Bearer " + SUPABASE_KEY,
        Prefer: "return=minimal",
      },
      body: JSON.stringify(row),
    });
    stored = r.ok;
    if (!r.ok) storeError = "HTTP " + r.status + " " + (await r.text()).slice(0, 200);
  } catch (e) {
    storeError = String(e).slice(0, 200);
  }

  // 2. Email it.
  let emailed = false;
  let emailError = null;
  const user = process.env.SMTP_USER;
  const pass = process.env.SMTP_PASS;
  if (user && pass) {
    const lines = [
      "Name:    " + row.name,
      "Email:   " + row.email,
      row.phone ? "Phone:   " + row.phone : null,
      row.service ? "Service: " + row.service : null,
      row.budget ? "Budget:  " + row.budget : null,
      row.source_page ? "Page:    https://hstarchitects.com" + row.source_page : null,
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
        replyTo: row.email,
        subject: "Website enquiry from " + row.name,
        text: lines.join("\n"),
      });
      emailed = true;
    } catch (e) {
      emailError = String(e && e.message ? e.message : e).slice(0, 200);
    }
  } else {
    emailError = "SMTP_USER / SMTP_PASS not set";
  }

  if (!stored && !emailed) {
    console.error("[enquiry] lost", { storeError: storeError, emailError: emailError });
    return res.status(502).json({ error: "Could not record that enquiry." });
  }
  if (!stored) console.error("[enquiry] not stored", storeError);
  if (!emailed) console.error("[enquiry] not emailed", emailError);

  return res.status(200).json({ ok: true, stored: stored, emailed: emailed });
};
