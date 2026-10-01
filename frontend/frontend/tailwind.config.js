/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["IBM Plex Mono", "ui-monospace", "monospace"],
      },
      colors: {
        base: {
          bg: "#0F1419",
          surface: "#161B22",
          surface2: "#1C232C",
          border: "#2A313C",
          text: "#E6E8EB",
          subtext: "#8B95A1",
          muted: "#5B6472",
        },
        tier: {
          low: "#5A9B7C",
          lowBg: "#17241D",
          medium: "#C9A227",
          mediumBg: "#241F13",
          high: "#C06B57",
          highBg: "#261815",
        },
        accent: "#4E8CD9",
      },
      borderRadius: {
        sm: "4px",
        DEFAULT: "6px",
      },
    },
  },
  plugins: [],
};
