/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        border: "var(--border)",
        background: "var(--background)",
        foreground: "var(--foreground)",
        card: "var(--card)",
        primary: "var(--primary)",
        secondary: "var(--secondary)",
        muted: "var(--muted)",
        "muted-foreground": "var(--muted-foreground)",
        accent: "var(--accent)",
        ring: "var(--ring)",
        cyber: {
          blue: "#00d4ff",
          dark: "#0a0e27",
          card: "#151932",
          accent: "#ff0055",
        },
        "cyber-blue": "var(--cyber-blue)",
        "cyber-accent": "var(--cyber-accent)",
        "cyber-dark": "var(--cyber-dark)",
        "cyber-card": "var(--cyber-card)",
      },
      animation: {
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "glow": "glow 2s ease-in-out infinite alternate",
      },
      keyframes: {
        glow: {
          "0%": { boxShadow: "0 0 5px rgb(0 212 255 / 0.5)" },
          "100%": { boxShadow: "0 0 20px rgb(0 212 255 / 0.8)" },
        },
      },
    },
  },
  plugins: [],
};
