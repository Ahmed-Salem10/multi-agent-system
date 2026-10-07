// قراءة SSE من endpoint بتاع POST (EventSource العادي بيدعم GET بس)
const BASE = import.meta.env.VITE_API_URL || "";

export async function streamChat({ question, history, signal, onEvent }) {
  const res = await fetch(`${BASE}/ai/chat/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, history }),
    signal,
  });

  if (!res.ok || !res.body) {
    throw new Error(`Server responded with ${res.status}`);
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder("utf-8");
  let buffer = "";

  const dispatch = (block) => {
    let event = "message";
    const dataLines = [];
    for (const line of block.split("\n")) {
      if (line.startsWith("event:")) event = line.slice(6).trim();
      else if (line.startsWith("data:")) dataLines.push(line.slice(5).trimStart());
    }
    if (!dataLines.length) return;
    try {
      onEvent(event, JSON.parse(dataLines.join("\n")));
    } catch {
      /* تجاهل أي chunk مش JSON */
    }
  };

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true }).replace(/\r\n/g, "\n");

    let idx;
    while ((idx = buffer.indexOf("\n\n")) !== -1) {
      dispatch(buffer.slice(0, idx));
      buffer = buffer.slice(idx + 2);
    }
  }
  if (buffer.trim()) dispatch(buffer);
}
