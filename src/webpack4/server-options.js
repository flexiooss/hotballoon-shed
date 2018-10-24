'use strict'

const CONFIG = require('./config')
const webpackDev = require('./webpack.dev')

module.exports = {
  index: '',
  contentBase: CONFIG.dist_path,
  hot: true,
  host: CONFIG.host,
  port: CONFIG.port,
  historyApiFallback: true,
  https: CONFIG.https,
  clientLogLevel: 'info',
  open: webpackDev.output.publicPath,
  stats: {
    colors: true
  }
}
