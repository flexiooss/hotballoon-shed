const path = require('path')

module.exports = {
  entry: {
    app: []
  },
  host: 'localhost',
  port: 8080,
  dist_path: path.resolve('./dist'),
  root_path: path.resolve(),
  https: true,
  vendors_path: path.resolve(__dirname, '../../../node_modules')
}
