'use strict'

const CONFIG = require('./config')

module.exports = {
allowedHosts: 'all',
  hot: true,
  liveReload: false,
  host: CONFIG.host,
  port: CONFIG.port,
  historyApiFallback: true,
//  client: {
//      logging: 'info',
//      overlay: false,
//      webSocketTransport: 'sockjs'
//    },
  compress: true,
  server: 'https'
}

