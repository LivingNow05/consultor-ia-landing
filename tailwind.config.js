/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    "./templates/**/*.html",
    "./dist/**/*.html",
    "./*.py",
    "./*.html"
  ],
  theme: {
    extend: {
      colors: {
        'brand': '#18181b',
        'brand-light': '#f4f4f5',
        'accent': '#2563eb',
        'success': '#10b981',
        'gray-1': '#18181b',
        'gray-2': '#52525b',
        'gray-card': '#ffffff',
        'gray-border': '#e4e4e7',
      },
      fontFamily: {
        body: ['"Inter"', 'sans-serif'],
        header: ['"Playfair Display"', 'serif'],
      }
    }
  },
  plugins: [],
}
