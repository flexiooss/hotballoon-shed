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
      {
        test: /\.(png|jpe?g|gif|svg|woff2?|eot|ttf|otf|wav)(\?.*)?$/,
        type: 'asset'
      }
    ]
  },
  resolveLoader: {
    modules: [CONFIG.vendors_path]
  }
}
