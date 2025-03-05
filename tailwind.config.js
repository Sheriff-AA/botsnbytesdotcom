/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: ['./templates/**/*.html'],
  theme: {
    extend: {
      fontFamily: {
				poly: ['"poly"', "serif"],
			},
    },
  },
  plugins: [
    function({ addVariant }) {
			addVariant('firefox', ':-moz-any(&)')
		}
  ],
}

