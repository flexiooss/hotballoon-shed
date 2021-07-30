const CONFIG = require('./config')

module.exports = {
  entry: CONFIG.entry,
  output: {
    path: CONFIG.dist_path,
    filename: '[name].[fullhash].js'
  },
  plugins: [],
  module: {
    rules: [

    ]
  },
  resolveLoader: {
    modules: [CONFIG.vendors_path]
  }
}
