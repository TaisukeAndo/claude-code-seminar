// API（バックエンド）。/api/ で始まるURLへの依頼だけがここに来る。
// それ以外のURLは、public/ の画面（HTML・CSS・JavaScript）がそのまま返される。
// items の例は、要件に合わせて書き換える。

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json; charset=utf-8" },
  });

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const { pathname } = url;

    if (!pathname.startsWith("/api/")) {
      return env.ASSETS.fetch(request);
    }

    if (pathname === "/api/health" && request.method === "GET") {
      return json({ ok: true, environment: env.ENVIRONMENT ?? "local" });
    }

    // 一覧の取得
    if (pathname === "/api/items" && request.method === "GET") {
      const { results } = await env.DB.prepare(
        "SELECT id, title, created_at FROM items ORDER BY id DESC",
      ).all();
      return json({ items: results });
    }

    // 登録
    if (pathname === "/api/items" && request.method === "POST") {
      let body;
      try {
        body = await request.json();
      } catch {
        return json({ error: "JSONの形式が正しくありません" }, 400);
      }
      const title = typeof body.title === "string" ? body.title.trim() : "";
      if (!title) return json({ error: "題名を入力してください" }, 400);
      if (title.length > 200) return json({ error: "題名は200文字以内にしてください" }, 400);
      const result = await env.DB.prepare("INSERT INTO items (title) VALUES (?)")
        .bind(title)
        .run();
      return json({ id: result.meta.last_row_id, title }, 201);
    }

    // 削除
    const match = pathname.match(/^\/api\/items\/(\d+)$/);
    if (match && request.method === "DELETE") {
      const result = await env.DB.prepare("DELETE FROM items WHERE id = ?")
        .bind(Number(match[1]))
        .run();
      if (result.meta.changes === 0) return json({ error: "データが見つかりません" }, 404);
      return json({ deleted: Number(match[1]) });
    }

    return json({ error: "見つかりません" }, 404);
  },
};
