const path = require('path')

module.exports = {
  entry: {
    app: []
  },
  host: 'localhost',
  port: 8080,
  html: true,
  dist_url: '/',
  stylelint: './src/css/**/*.css',
  refresh: ['../src/index.html', 'index.html', '../dist/index.html'],
  dist_path: path.resolve(__dirname, '../dist'),
  root_path: path.resolve(__dirname, '../'),
  template_html: path.resolve(__dirname, '../src/index.html'),
  https: true
}
