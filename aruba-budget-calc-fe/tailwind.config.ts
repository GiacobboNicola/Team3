import type { Config } from 'tailwindcss';

export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],

	theme: {
		extend: {
			colors: {
				primary: 'rgb(0, 99, 175)',
				input: '#0099CE'
			}
		}
	},

	plugins: []
} satisfies Config;
