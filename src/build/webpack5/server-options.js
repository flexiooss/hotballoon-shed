'use strict'

const CONFIG = require('./config')

module.exports = {
allowedHosts: 'all',
//  contentBase: CONFIG.dist_path,
  hot: false,
  host: CONFIG.host,
  port: CONFIG.port,
  historyApiFallback: true,
//  https: CONFIG.https,
  client: {
      logging: 'info',
      overlay: true
    },
  compress: true,
//  stats: {
//    colors: true
//  },
  server: 'https'
}

const ex = {
  allowedHosts: 'all',
  contentBase: '/home/thomas/workspaces/ui/bundles/component-commons-bundle/js-tinymce-common/tmp_dist',
  hot: false,
  host: '0.0.0.0',
  port: 8080,
  historyApiFallback: true,
  client: { logging: 'info', overlay: true },
  compress: true,
  stats: { colors: true },
  server: 'https',
  static: { publicPath: '/' }
}

