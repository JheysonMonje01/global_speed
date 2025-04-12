// postcss.config.js
module.exports = {
    plugins: {
      '@tailwindcss/postcss': {}, // <--- este es el nuevo plugin correcto
      autoprefixer: {},
    },
  };
  