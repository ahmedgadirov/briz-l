import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        mint: {
          DEFAULT: '#3EB489',
          light: '#5fc4a0',
          dark: '#2A8B6B',
        },
        clinic: {
          primary: '#3EB489',
          secondary: '#2A8B6B',
          accent: '#142850',
        },
      },
      fontFamily: {
        sans: ['var(--font-inter)', 'system-ui', 'sans-serif'],
        display: ['var(--font-space-grotesk)', 'system-ui', 'sans-serif'],
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        glow: {
          '0%': { boxShadow: '0 0 20px rgba(62, 180, 137, 0.3)' },
          '100%': { boxShadow: '0 0 40px rgba(62, 180, 137, 0.6)' },
        },
      },
    },
  },
  plugins: [],
}
export default config