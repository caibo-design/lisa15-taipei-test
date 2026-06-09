const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY,
  { auth: { persistSession: false } }
);

const DEFAULT_LIMIT = 50;
const MAX_LIMIT = 100;

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Cache-Control', 's-maxage=10, stale-while-revalidate=30');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'GET') {
    return res.status(405).json({ ok: false, error: 'method not allowed' });
  }

  const rawLimit = Number(req.query.limit);
  const limit = Number.isInteger(rawLimit) && rawLimit > 0
    ? Math.min(rawLimit, MAX_LIMIT)
    : DEFAULT_LIMIT;

  // 取 Top N
  const { data, error } = await supabase
    .from('scores')
    .select('id, nickname, score, peak_max, seat_name, created_at')
    .order('peak_max', { ascending: false })
    .order('score', { ascending: false })
    .order('created_at', { ascending: true })
    .limit(limit);

  if (error) {
    console.error('leaderboard error', error);
    return res.status(500).json({ ok: false, error: 'db error' });
  }

  // 總筆數（給「在 1234 人裡排第 N」用）
  const { count: total } = await supabase
    .from('scores')
    .select('id', { count: 'exact', head: true });

  // 如果有指定 myId，補上玩家自己的名次
  const myId = typeof req.query.myId === 'string' ? req.query.myId : null;
  let me = null;
  if (myId) {
    const { data: myRow } = await supabase
      .from('scores')
      .select('id, nickname, score, peak_max, seat_name, created_at')
      .eq('id', myId)
      .maybeSingle();
    if (myRow) {
      const { count: higherPeak } = await supabase
        .from('scores')
        .select('id', { count: 'exact', head: true })
        .gt('peak_max', myRow.peak_max);
      const { count: samePeakHigherScore } = await supabase
        .from('scores')
        .select('id', { count: 'exact', head: true })
        .eq('peak_max', myRow.peak_max)
        .gt('score', myRow.score);
      me = {
        rank: (higherPeak ?? 0) + (samePeakHigherScore ?? 0) + 1,
        nickname: myRow.nickname,
        score: myRow.score,
        peakMax: myRow.peak_max,
        seatName: myRow.seat_name,
        createdAt: myRow.created_at
      };
    }
  }

  res.status(200).json({
    ok: true,
    total: total ?? 0,
    entries: (data || []).map((r, i) => ({
      rank: i + 1,
      id: r.id,
      nickname: r.nickname,
      score: r.score,
      peakMax: r.peak_max,
      seatName: r.seat_name,
      createdAt: r.created_at
    })),
    me
  });
};
