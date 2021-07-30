'use strict'

const CONFIG = require('./config')

module.exports = {
  contentBase: CONFIG.dist_path,
  hot: true,
  host: CONFIG.host,
  port: CONFIG.port,
  historyApiFallback: true,
  https: CONFIG.https,
  clientLogLevel: 'info',
  stats: {
    colors: true
  }
}
