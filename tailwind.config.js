/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx}", 
    "./src/components/**/*.{js,ts,jsx,tsx}", 
  ],
  theme: {
    extend: {
      colors: {
        primary: "#4A90E2", // Cool blue
        secondary: "#50E3C2", // Teal green
        accent: "#F5A623", // Vibrant orange
        background: "#F9FAFB", // Light gray
        text: "#1A202C", // Dark gray
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
      },
    },
  },
  plugins: [],
};
