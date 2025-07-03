/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#0080ff',
        'primary-hover': '#0066cc',
        'accent': '#00d4ff',
        'accent-hover': '#00b8e6',
        'dark': '#0a0a0a',
        'dark-secondary': '#111',
        'dark-tertiary': '#1a1a1a',
        'border': '#333',
        'text-primary': '#e0e0e0',
        'text-secondary': '#888',
        'text-tertiary': '#666'
      }
    },
  },
  plugins: [],
}