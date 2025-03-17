/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    "./core/templates/**/*.html",
  ],
  theme: {
    extend: {
      maxHeight: {
        '0': '0',
        xl: '36rem',
      },
      fontFamily: {
        sans: ['Inter', ...defaultTheme.fontFamily.sans],
      },
    },
  },
  plugins: [
    // require("daisyui")
  ],
}

