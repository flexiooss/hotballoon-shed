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
  dist_path: path.resolve('./dist'),
  root_path: path.resolve(),
  template_html: path.resolve('./src/index.html'),
  https: true,
  mediaqueries: {
    desktop: 'screen min-width(800px)',
    print: 'print'
  }
}
