import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import { streamChat } from "./sse.js";

/* ------------------------------------------------------------------ */
/* ثوابت: الـ agents اللي في الجراف                                      */
/* ------------------------------------------------------------------ */
const AGENTS = [
  { id: "supervisor", name: "Supervisor", icon: "👑", color: "#ffd44d" },
  { id: "rag", name: "RAG", icon: "📚", color: "#4dd2ff" },
  { id: "research", name: "Research", icon: "🌐", color: "#3dffb0" },
  { id: "analysis", name: "Analysis", icon: "🔬", color: "#c58cff" },
  { id: "final", name: "Final", icon: "⚡", color: "#ff8a5c" },
];

const SUGGESTIONS = [
  "ما هو أكبر كوكب في المجموعة الشمسية؟",
  "Can humans live on Mars?",
  "لخّص لي المستندات اللي رفعتها",
  "What are the latest space missions?",
];

const initialAgents = () =>
  Object.fromEntries(AGENTS.map((a) => [a.id, { status: "idle", ms: null }]));

let nextId = 1;
const uid = () => `m${nextId++}`;

// أي شكل للـ source (string / dict / غيره) يتحوّل لنص آمن للعرض
function normalizeSource(s) {
  if (typeof s === "string") return s;
  if (s && typeof s === "object") {
    return String(
      s.url || s.source || s.file || s.filename || s.title || s.name || JSON.stringify(s)
    );
  }
  return String(s ?? "");
}

function normalizeList(list) {
  if (!Array.isArray(list)) return [];
  return Array.from(new Set(list.map(normalizeSource).filter(Boolean)));
}

/* ------------------------------------------------------------------ */
/* Logo                                                                */
/* ------------------------------------------------------------------ */
function Bolt({ size = 28 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 64 64" aria-hidden="true">
      <defs>
        <linearGradient id="boltg" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#fff3b0" />
          <stop offset="0.5" stopColor="#ffd44d" />
          <stop offset="1" stopColor="#ff9d00" />
        </linearGradient>
      </defs>
      <path fill="url(#boltg)" d="M36 4 14 36h14l-4 24 26-34H35z" />
    </svg>
  );
}

/* ------------------------------------------------------------------ */
/* Pipeline: عرض حي لشغل الـ agents                                     */
/* ------------------------------------------------------------------ */
function Pipeline({ agents }) {
  return (
    <div className="pipeline" aria-label="Agents pipeline">
      {AGENTS.map((a, i) => {
        const s = agents[a.id] || { status: "idle", ms: null };
        return (
          <div key={a.id} className="pipe-item">
            <div
              className={`node ${s.status}`}
              style={{ "--c": a.color }}
              title={a.name}
            >
              <span className="node-icon">{a.icon}</span>
              <span className="node-name">{a.name}</span>
              {s.status === "running" && <span className="spinner" />}
              {s.status === "done" && s.ms != null && (
                <span className="node-ms">{(s.ms / 1000).toFixed(1)}s</span>
              )}
              {s.status === "done" && s.ms == null && (
                <span className="node-ms">✓</span>
              )}
            </div>
            {i < AGENTS.length - 1 && <span className="link" />}
          </div>
        );
      })}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* رسالة                                                               */
/* ------------------------------------------------------------------ */
function Message({ m }) {
  if (m.role === "user") {
    return (
      <div className="row user">
        <div className="bubble user-bubble" dir="auto">
          {m.content}
        </div>
      </div>
    );
  }

  return (
    <div className="row bot">
      <div className="avatar">
        <Bolt size={22} />
      </div>
      <div className="bot-col">
        <Pipeline agents={m.agents} />

        <div className={`bubble bot-bubble ${m.error ? "has-error" : ""}`} dir="auto">
          {m.content ? (
            <div className="md">
              <ReactMarkdown>{m.content}</ReactMarkdown>
            </div>
          ) : !m.error ? (
            <div className="thinking">
              <span className="dot" />
              <span className="dot" />
              <span className="dot" />
              <span className="thinking-text">
                {m.statusText || "ZUES is thinking…"}
              </span>
            </div>
          ) : null}

          {m.streaming && m.content && <span className="caret" />}
          {m.error && <div className="error-box">⚠ {m.error}</div>}
        </div>

        {m.toolsUsed?.length > 0 && (
          <div className="chips">
            {m.toolsUsed.map((t) => (
              <span key={t} className="chip tool">
                ⚙ {t}
              </span>
            ))}
          </div>
        )}

        {m.sources?.length > 0 && (
          <div className="sources">
            <div className="sources-title">Sources</div>
            <div className="chips">
              {m.sources.map((raw, i) => {
                const s = String(raw);
                const isUrl = /^https?:\/\//i.test(s);
                return isUrl ? (
                  <a
                    key={i}
                    className="chip src"
                    href={s}
                    target="_blank"
                    rel="noreferrer"
                    title={s}
                  >
                    🔗 {s.replace(/^https?:\/\/(www\.)?/, "").slice(0, 38)}
                  </a>
                ) : (
                  <span key={i} className="chip src" title={s}>
                    📄 {s.slice(0, 38)}
                  </span>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* App                                                                 */
/* ------------------------------------------------------------------ */
export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const abortRef = useRef(null);
  const endRef = useRef(null);
  const taRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages]);

  // تحديث رسالة معيّنة
  const patch = (id, fn) =>
    setMessages((prev) => prev.map((m) => (m.id === id ? fn(m) : m)));

  const autoGrow = (el) => {
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 160) + "px";
  };

  async function send(text) {
    const question = (text ?? input).trim();
    if (!question || busy) return;

    // التاريخ: آخر الرسائل المكتملة (السيرفر بياخد آخر 6)
    const history = messages
      .filter((m) => m.content && !m.error)
      .slice(-6)
      .map((m) => ({ role: m.role === "user" ? "user" : "assistant", content: m.content }));

    const botId = uid();
    setMessages((prev) => [
      ...prev,
      { id: uid(), role: "user", content: question },
      {
        id: botId,
        role: "assistant",
        content: "",
        streaming: true,
        agents: initialAgents(),
        sources: [],
        toolsUsed: [],
        statusText: "Supervisor is planning…",
      },
    ]);
    setInput("");
    requestAnimationFrame(() => autoGrow(taRef.current));
    setBusy(true);

    const controller = new AbortController();
    abortRef.current = controller;

    const setAgent = (m, id, status, ms = null) => ({
      ...m,
      agents: { ...m.agents, [id]: { status, ms: ms ?? m.agents[id]?.ms ?? null } },
    });

    try {
      await streamChat({
        question,
        history,
        signal: controller.signal,
        onEvent: (event, data) => {
          if (event === "start") {
            patch(botId, (m) => setAgent(m, "supervisor", "running"));
          } else if (event === "tool_start") {
            patch(botId, (m) => {
              let n = setAgent(m, "supervisor", "done");
              n = setAgent(n, data.agent, "running");
              return { ...n, statusText: `${data.label} is working…` };
            });
          } else if (event === "tool_end") {
            patch(botId, (m) => {
              let n = setAgent(m, data.agent, "done", data.duration_ms);
              // الـ supervisor هيرجع يقرر الخطوة اللي بعدها
              n = setAgent(n, "supervisor", "running");
              return { ...n, statusText: "Supervisor is deciding the next step…" };
            });
          } else if (event === "token") {
            patch(botId, (m) => {
              let n = m;
              if (m.agents.final.status !== "running") {
                n = setAgent(n, "supervisor", "done");
                n = setAgent(n, "final", "running");
              }
              return { ...n, content: n.content + String(data.text ?? "") };
            });
          } else if (event === "done") {
            patch(botId, (m) => {
              const finished = Object.fromEntries(
                AGENTS.map((a) => {
                  const cur = m.agents[a.id];
                  const used =
                    a.id === "supervisor" ||
                    a.id === "final" ||
                    cur.status === "done";
                  return [a.id, { ...cur, status: used ? "done" : "idle" }];
                })
              );
              const trace = Array.isArray(data.trace) ? data.trace : [];
              const t = trace.find((x) => x && x.agent === "final");
              if (t) finished.final.ms = t.duration_ms ?? null;
              return {
                ...m,
                agents: finished,
                streaming: false,
                sources: normalizeList(data.sources),
                toolsUsed: normalizeList(data.tools_used),
              };
            });
          } else if (event === "error") {
            patch(botId, (m) => ({
              ...m,
              streaming: false,
              error: data.message || "Something went wrong",
            }));
          }
        },
      });
    } catch (e) {
      if (e.name === "AbortError") {
        patch(botId, (m) => ({ ...m, streaming: false, error: m.content ? null : "Stopped." }));
      } else {
        patch(botId, (m) => ({
          ...m,
          streaming: false,
          error: `Can't reach the server. ${e.message}`,
        }));
      }
    } finally {
      // لو الستريم خلص من غير done (انقطاع)
      patch(botId, (m) => ({ ...m, streaming: false }));
      setBusy(false);
      abortRef.current = null;
    }
  }

  const stop = () => abortRef.current?.abort();
  const reset = () => {
    abortRef.current?.abort();
    setMessages([]);
    setInput("");
    setBusy(false);
  };

  const onKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  };

  const empty = messages.length === 0;

  return (
    <div className="app">
      <div className="bg" aria-hidden="true">
        <span className="orb o1" />
        <span className="orb o2" />
        <span className="orb o3" />
        <span className="grid" />
      </div>

      <header className="topbar">
        <div className="brand">
          <span className="brand-bolt">
            <Bolt size={30} />
          </span>
          <div>
            <h1 className="brand-name">
              ZUES <span>AI</span>
            </h1>
            <p className="brand-tag">Multi-Agent Intelligence</p>
          </div>
        </div>
        <button className="ghost" onClick={reset} disabled={empty && !busy}>
          + New chat
        </button>
      </header>

      <main className="chat">
        {empty ? (
          <section className="hero">
            <div className="hero-bolt">
              <Bolt size={86} />
            </div>
            <h2>
              Command a <span className="grad">team of agents</span>
            </h2>
            <p className="hero-sub">
              ZUES يوجّه سؤالك بين وكلاء متخصصين: قاعدة المعرفة، البحث على الإنترنت،
              التحليل، ثم الإجابة النهائية — وأنت تشوف كل خطوة لحظة بلحظة.
            </p>

            <div className="hero-pipeline">
              <Pipeline agents={initialAgents()} />
            </div>

            <div className="suggestions">
              {SUGGESTIONS.map((s) => (
                <button key={s} className="suggest" dir="auto" onClick={() => send(s)}>
                  {s}
                </button>
              ))}
            </div>
          </section>
        ) : (
          <div className="thread">
            {messages.map((m) => (
              <Message key={m.id} m={m} />
            ))}
            <div ref={endRef} />
          </div>
        )}
      </main>

      <footer className="composer-wrap">
        <div className="composer">
          <textarea
            ref={taRef}
            value={input}
            rows={1}
            dir="auto"
            placeholder="اسأل ZUES أي حاجة…  |  Ask ZUES anything…"
            onChange={(e) => {
              setInput(e.target.value);
              autoGrow(e.target);
            }}
            onKeyDown={onKeyDown}
          />
          {busy ? (
            <button className="send stop" onClick={stop} title="Stop">
              ■
            </button>
          ) : (
            <button
              className="send"
              onClick={() => send()}
              disabled={!input.trim()}
              title="Send"
            >
              <Bolt size={22} />
            </button>
          )}
        </div>
        <p className="hint">Enter للإرسال · Shift+Enter سطر جديد</p>
      </footer>
    </div>
  );
}
