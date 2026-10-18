// 画面の動き（フロントエンド）。ボタンを押したら、APIにデータを依頼する。
const list = document.getElementById("list");
const form = document.getElementById("form");
const titleInput = document.getElementById("title");
const message = document.getElementById("message");

async function load() {
  const res = await fetch("/api/items");
  const { items } = await res.json();
  list.replaceChildren(
    ...items.map((item) => {
      const li = document.createElement("li");
      const span = document.createElement("span");
      span.textContent = item.title;
      const button = document.createElement("button");
      button.textContent = "削除";
      button.addEventListener("click", async () => {
        await fetch(`/api/items/${item.id}`, { method: "DELETE" });
        load();
      });
      li.append(span, button);
      return li;
    }),
  );
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  message.textContent = "";
  const res = await fetch("/api/items", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ title: titleInput.value }),
  });
  if (!res.ok) {
    const { error } = await res.json();
    message.textContent = error;
    return;
  }
  titleInput.value = "";
  load();
});

load();
