'use strict'

const CONFIG = require('./config')

module.exports = {
  allowedHosts: 'all',
  host: CONFIG.host,
  port: CONFIG.port,
  historyApiFallback: true,
  compress: true,
  server: 'https'
}

