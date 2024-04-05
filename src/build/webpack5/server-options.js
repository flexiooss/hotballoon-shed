'use strict'

const CONFIG = require('./config')

module.exports = {
allowedHosts: 'all',
  hot: false,
  host: CONFIG.host,
  port: CONFIG.port,
  historyApiFallback: true,
  client: {
      logging: 'info',
      overlay: true
    },
  compress: true,
  server: 'https'
}

