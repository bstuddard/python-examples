// @ts-check
import { defineConfig } from 'astro/config';

import sitemap from '@astrojs/sitemap';

import svelte from '@astrojs/svelte';

import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  // site: 'https://stargazers.club', Add here when domain is established
  integrations: [
    sitemap(), 
    svelte()
  ],

  vite: {
    plugins: [tailwindcss()],
    resolve: {
      alias: {
        $lib: '/src/lib'
      }
    }
  }
});