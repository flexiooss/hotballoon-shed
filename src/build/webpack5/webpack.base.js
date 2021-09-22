const CONFIG = require('./config')

module.exports = {
  entry: CONFIG.entry,
  output: {
    path: CONFIG.dist_path,
    publicPath: '',
    filename: '[name].[fullhash].js',
    assetModuleFilename: 'assets/[hash][ext][query]'
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
