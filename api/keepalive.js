// Keeps the Free-plan Supabase project from pausing.
//
// Supabase pauses a Free project after a week without enough database activity,
// and says a few requests a day is typically enough. The exact threshold is not
// published, so each run makes three real PostgREST queries, spaced out.
//
// Called twice a day by Vercel Cron (see "crons" in vercel.json) and every six
// hours by a GitHub Actions schedule, so a failure in either one alone does not
// let the project pause. The queries are read-only and return nothing, because
// row-level security hides enquiries from the publishable key, so the endpoint
// is safe to leave callable. If CRON_SECRET is set in Vercel it is enforced.
//
// Dependency-free like api/enquiry.js: no package.json, no install step.

const SUPABASE_URL = (process.env.SUPABASE_URL || "https://mhfempltoebztrvybidb.supabase.co").replace(/\/$/, "");
// The same publishable value already shipped to every visitor in assets/js/config.js.
const SUPABASE_KEY = process.env.SUPABASE_ANON_KEY || "sb_publishable_n0lmxgelzVR3py-ZOTDuCQ_O991Dxlr";

function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }

async function read(i) {
  const started = Date.now();
  try {
    const r = await fetch(SUPABASE_URL + "/rest/v1/enquiries?select=id&limit=1", {
      headers: { apikey: SUPABASE_KEY },
      signal: AbortSignal.timeout(8000),
    });
    return { n: i, status: r.status, ms: Date.now() - started };
  } catch (e) {
    return { n: i, status: 0, ms: Date.now() - started, error: String(e && e.message ? e.message : e).slice(0, 120) };
  }
}

module.exports = async (req, res) => {
  const secret = process.env.CRON_SECRET;
  if (secret && req.headers.authorization !== "Bearer " + secret) {
    return res.status(401).json({ error: "Unauthorised." });
  }

  const reads = [];
  for (let i = 1; i <= 3; i++) {
    reads.push(await read(i));
    if (i < 3) await sleep(1500);
  }
  const ok = reads.every(function (r) { return r.status === 200; });
  if (!ok) console.error("[keepalive] Supabase not answering", reads);

  // 200 either way so Vercel does not retry-storm a paused project; the body and
  // the log say whether it worked.
  return res.status(200).json({ ok: ok, reads: reads, at: new Date().toISOString() });
};
