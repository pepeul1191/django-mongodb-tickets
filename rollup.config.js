import svelte from 'rollup-plugin-svelte';
import commonjs from '@rollup/plugin-commonjs';
import terser from '@rollup/plugin-terser';
import resolve from '@rollup/plugin-node-resolve';
import css from 'rollup-plugin-css-only';
import copy from 'rollup-plugin-copy';
import babel from 'rollup-plugin-babel';

const production = !process.env.ROLLUP_WATCH;

const Vendor = {
  input: 'src/entries/vendor.js',
  output: {
    sourcemap: true,
    format: 'iife',
    name: 'vendor',
    file: production ? 'static/dist/vendor.min.js' : 'static/dist/vendor.js',
    globals: {
      'axios': 'axios',
      'bootstrap': 'bootstrap'
    }
  },
  plugins: [
    svelte({
      compilerOptions: {
        dev: !production
      }
    }),

    css({
      output: 'vendor.min.css',
      minify: true
    }),

    resolve({
      browser: true,
      dedupe: ['svelte'],
      exportConditions: ['svelte']
    }),

    commonjs(),

    production && terser(),

    copy({
      hook: 'writeBundle',
      targets: [
        {
          src: 'node_modules/font-awesome/fonts/*',
          dest: 'static/fonts/'
        }
      ]
    })
  ],
  watch: {
    clearScreen: false
  }
};

const App = {
  input: 'src/entries/app.js',
  output: {
    file: 'static/dist/app.js',
    format: 'iife'
  },
  plugins: [
    resolve(),
    commonjs(),
    babel({
      exclude: 'node_modules/**',
      presets: ['@babel/preset-env']
    }),
    terser()
  ]
};

export default [App, Vendor, ];