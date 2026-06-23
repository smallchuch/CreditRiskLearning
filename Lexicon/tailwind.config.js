/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        brandNavy: "#2C3E50",
        brandOrange: "#F49D1E",
        brandTeal: "#1BB89A",
        brandTealDark: "#27A28A",
      },
    },
  },
  plugins: [],
};
