/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./docs/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        'astro-blue': 'rgba(24, 21, 68)',
      },
    },
  },
}