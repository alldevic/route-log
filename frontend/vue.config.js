const path = require('path');

module.exports = {
  css: {
    loaderOptions: {
      sass: {
        data: '',
      },
      scss: {
        data: '@import "@/styles/abstracts/_variables.scss";',
      },
    },
  },
  configureWebpack: {
    resolve: {
      extensions: ['.ts', '.js'],
      alias: {
        '@': path.resolve(__dirname, 'src/'),
        'typings': path.resolve(__dirname, 'typings/'),
        'styles': path.resolve(__dirname, 'src/styles/'),
      },
    },
    module: {
      rules: [
        {
          test: /\.pug$/,
          oneOf: [
            { resourceQuery: /^\?vue/, use: ['pug-plain-loader'] },
            { use: ['raw-loader', 'pug-plain-loader'] },
          ],
        },
      ],
    },
  },
};
