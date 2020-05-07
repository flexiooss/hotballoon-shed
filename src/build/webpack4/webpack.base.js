'use strict'

const CONFIG = require('./config')
const path = require('path')
//const babelOptions = require('../babel/getBabelConfig')
const fs = require('fs')

module.exports = {
  entry: CONFIG.entry,
  output: {
    path: CONFIG.dist_path,
    filename: '[name].[contenthash].js'
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
        test: /\.(png|jpe?g|gif|svg|woff2?|eot|ttf|otf|wav)(\?.*)?$/,
        use: [{
          loader: 'url-loader',
          options: {
            limit: 10
          }
        }]
      },
//      {
//        test: /\.worker\.js$/,
//        use: {
//        loader: 'worker-loader' ,
//          options: {
//            name: '[name].[contenthash].js'
//          }
//        }
//      }
    ]
  },
  resolveLoader: {
    modules: [CONFIG.vendors_path]
  }
}
