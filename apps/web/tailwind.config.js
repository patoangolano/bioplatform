/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: {
          base: "#0A0E14",
          surface: "#121823",
          "surface-2": "#1A2332",
        },
        border: {
          DEFAULT: "#243043",
        },
        text: {
          primary: "#E6EDF3",
          muted: "#8B98A9",
        },
        accent: {
          DEFAULT: "#00E599",
          dim: "#0FB888",
        },
        cyan: {
          secondary: "#22D3EE",
        },
        danger: "#F87171",
        warning: "#FBBF24",
        base: {
          A: "#3DDC84",
          C: "#38BDF8",
          G: "#FBBF24",
          T: "#F87171",
          U: "#F87171",
        },
        prov: {
          observation: "#22D3EE",
          inference: "#00E599",
          hypothesis: "#FBBF24",
        },
      },
      fontFamily: {
        display: ['"Sora"', "system-ui", "sans-serif"],
        sans: ['"Inter"', "system-ui", "sans-serif"],
        mono: ['"JetBrains Mono"', "ui-monospace", "monospace"],
      },
      borderRadius: {
        xl: "12px",
      },
      boxShadow: {
        glow: "0 0 0 1px rgba(0,229,153,0.35), 0 0 24px -2px rgba(0,229,153,0.45)",
        "glow-sm": "0 0 16px -4px rgba(0,229,153,0.4)",
      },
      keyframes: {
        scanner: {
          "0%": { transform: "translateX(-110%)" },
          "100%": { transform: "translateX(110%)" },
        },
        "fade-slide": {
          "0%": { opacity: "0", transform: "translateY(8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        pulseDot: {
          "0%,100%": { opacity: "1" },
          "50%": { opacity: "0.35" },
        },
      },
      animation: {
        scanner: "scanner 3.2s ease-in-out infinite",
        "fade-slide": "fade-slide 0.45s ease-out both",
        pulseDot: "pulseDot 1.8s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};
