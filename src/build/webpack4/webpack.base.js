'use strict'

const CONFIG = require('./config')
const path = require('path')
//const babelOptions = require('../babel/getBabelConfig')
const fs = require('fs')

module.exports = {
  entry: CONFIG.entry,
  output: {
    path: CONFIG.dist_path,
    filename: '[name].[hash].js'
  },
  plugins: [ ],
  module: {
    rules: [
//      {
//        test: /\.js$/,
//        loader: 'babel-loader',
//        options: babelOptions
//      },
      {
        test: /\.worker\.js$/,
        loader: 'worker-loader',
        options: {
          name: '[name].[hash].js'
        }
      },
      {
        test: /\.(png|jpe?g|gif|svg|woff2?|eot|ttf|otf|wav)(\?.*)?$/,
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
    modules: [CONFIG.vendors_path]
  }
}
