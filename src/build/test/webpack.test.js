'use strict'

const babelOptions = require('../babel/getBabelConfig')
const CONFIG = require('../webpack4/config')

const webpackBase = {
  entry: CONFIG.entry,
  plugins: [],

  module: {
    rules: [
      {
        test: /\.js$/,
        loader: 'babel-loader',
        options: babelOptions
      },
      {
        test: /\.worker\.js$/,
        loader: 'worker-loader',
        options: {
          name: '[name].[hash].js'
        }
      },
      {
        test: /\.(css|png|jpe?g|gif|svg|woff2?|eot|ttf|otf|wav)(\?.*)?$/,
        use: [{
          loader: 'url-loader',
          query: {
            limit: 10
          }
        }]
      }
    ]
  },
  resolveLoader: {
    modules: ['node_modules', CONFIG.vendors_path]
  }
}
webpackBase.mode = 'development'

module.exports = webpackBase
