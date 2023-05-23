'use strict'

const CONFIG = require('./config')

module.exports = {
  contentBase: CONFIG.dist_path,
  hot: false,
  client: false,
  webSocketServer: false
  host: CONFIG.host,
  port: CONFIG.port,
  historyApiFallback: true,
  https: CONFIG.https,
  clientLogLevel: 'info',
  compress: true,
  stats: {
    colors: true
  }
}
