-- 例の表。要件に合わせて、新しいSQLファイル（0002_...）で表を追加・変更する。
-- 既存のSQLファイルは書き換えない。
CREATE TABLE IF NOT EXISTS items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
