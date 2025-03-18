/** @type {import('tailwindcss').Config} */
const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  darkMode: 'class',
  content: [
    "./core/templates/**/*.html",
    './templates/**/*.html',
    './node_modules/flowbite/**/*.js'
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
      typography: ({ theme }) => ({
        orange: {
          css: {
            '--tw-format-body': theme('colors.orange[500]'),
            '--tw-format-headings': theme('colors.orange[900]'),
            '--tw-format-lead': theme('colors.orange[500]'),
            '--tw-format-links': theme('colors.orange[600]'),
            '--tw-format-bold': theme('colors.orange[900]'),
            '--tw-format-counters': theme('colors.orange[500]'),
            '--tw-format-bullets': theme('colors.orange[500]'),
            '--tw-format-hr': theme('colors.orange[200]'),
            '--tw-format-quotes': theme('colors.orange[900]'),
            '--tw-format-quote-borders': theme('colors.orange[300]'),
            '--tw-format-captions': theme('colors.orange[700]'),
            '--tw-format-code': theme('colors.orange[900]'),
            '--tw-format-code-bg': theme('colors.orange[50]'),
            '--tw-format-pre-code': theme('colors.orange[100]'),
            '--tw-format-pre-bg': theme('colors.orange[900]'),
            '--tw-format-th-borders': theme('colors.orange[300]'),
            '--tw-format-td-borders': theme('colors.orange[200]'),
            '--tw-format-th-bg': theme('colors.orange[50]'),
            '--tw-format-invert-body': theme('colors.orange[200]'),
            '--tw-format-invert-headings': theme('colors.white'),
            '--tw-format-invert-lead': theme('colors.orange[300]'),
            '--tw-format-invert-links': theme('colors.white'),
            '--tw-format-invert-bold': theme('colors.white'),
            '--tw-format-invert-counters': theme('colors.orange[400]'),
            '--tw-format-invert-bullets': theme('colors.orange[600]'),
            '--tw-format-invert-hr': theme('colors.orange[700]'),
            '--tw-format-invert-quotes': theme('colors.pink[100]'),
            '--tw-format-invert-quote-borders': theme('colors.orange[700]'),
            '--tw-format-invert-captions': theme('colors.orange[400]'),
            '--tw-format-invert-code': theme('colors.white'),
            '--tw-format-invert-pre-code': theme('colors.orange[300]'),
            '--tw-format-invert-pre-bg': 'rgb(0 0 0 / 50%)',
            '--tw-format-invert-th-borders': theme('colors.orange[600]'),
            '--tw-format-invert-td-borders': theme('colors.orange[700]'),
            '--tw-format-invert-th-bg': theme('colors.orange[700]'),
          },
        },
      }),
      colors: {
        primary: {
          50: 'rgb(var(--color-primary-50) / <alpha-value>)',
          100: 'rgb(var(--color-primary-100) / <alpha-value>)',
          200: 'rgb(var(--color-primary-200) / <alpha-value>)',
          300: 'rgb(var(--color-primary-300) / <alpha-value>)',
          400: 'rgb(var(--color-primary-400) / <alpha-value>)',
          500: 'rgb(var(--color-primary-500) / <alpha-value>)',
          600: 'rgb(var(--color-primary-600) / <alpha-value>)',
          700: 'rgb(var(--color-primary-700) / <alpha-value>)',
          800: 'rgb(var(--color-primary-800) / <alpha-value>)',
          900: 'rgb(var(--color-primary-900) / <alpha-value>)',
        },
      },
    },
  },
  plugins: [
    require('flowbite/plugin'),
    require('flowbite-typography'),
  ],
}

