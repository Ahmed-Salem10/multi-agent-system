import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// أثناء التطوير: أي طلب على /ai بيتحوّل للباك اند (FastAPI) على بورت 8000
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/ai": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});
