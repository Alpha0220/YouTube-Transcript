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
        primary: {
          DEFAULT: '#007AFF',
          hover: '#0051D5',
          foreground: '#FFFFFF',
        },
        background: '#F5F5F7',
        foreground: '#1D1D1F',
        card: {
          DEFAULT: '#FFFFFF',
          foreground: '#1D1D1F',
        },
        secondary: {
          DEFAULT: '#F5F5F7',
          foreground: '#1D1D1F',
        },
        muted: {
          DEFAULT: '#F5F5F7',
          foreground: '#86868B',
        },
        border: '#E5E5E7',
        input: '#F5F5F7',
        ring: '#007AFF',
        destructive: {
          DEFAULT: '#FF3B30',
          foreground: '#FFFFFF',
        },
        success: '#34C759',
      },
      borderRadius: {
        DEFAULT: '0.75rem',
      },
    },
  },
  plugins: [],
}
export default config

