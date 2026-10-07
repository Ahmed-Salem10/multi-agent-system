import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import "./App.css";

// بدل الشاشة الفاضية: لو حصل crash نعرض سببه
class ErrorBoundary extends React.Component {
  state = { error: null };

  static getDerivedStateFromError(error) {
    return { error };
  }

  componentDidCatch(error, info) {
    console.error("ZUES AI crashed:", error, info);
  }

  render() {
    if (!this.state.error) return this.props.children;
    return (
      <div style={{ padding: 32, color: "#eef0ff", fontFamily: "sans-serif", maxWidth: 760, margin: "0 auto" }}>
        <h2 style={{ color: "#ffd44d" }}>⚡ ZUES AI — حصل خطأ في الواجهة</h2>
        <pre
          style={{
            whiteSpace: "pre-wrap",
            background: "rgba(255,255,255,0.06)",
            padding: 16,
            borderRadius: 12,
            direction: "ltr",
            textAlign: "left",
          }}
        >
          {String(this.state.error?.stack || this.state.error)}
        </pre>
        <button
          onClick={() => window.location.reload()}
          style={{ padding: "10px 18px", borderRadius: 10, border: "none", cursor: "pointer", fontWeight: 700 }}
        >
          Reload
        </button>
      </div>
    );
  }
}

createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </React.StrictMode>
);
