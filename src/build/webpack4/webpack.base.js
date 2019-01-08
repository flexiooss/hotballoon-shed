'use strict'

const CONFIG = require('./config')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const path = require('path')
const babelOptions = require('../babel/babel-options')
const fs = require('fs')

if (fs.existsSync(path.resolve('./build/babel-options.js'))) {
  const customBabelOptions = require(path.resolve('./build/babel-options.js'))
  Object.assign(babelOptions, customBabelOptions)
}

module.exports = {
  entry: CONFIG.entry,
  output: {
    path: CONFIG.dist_path,
    filename: '[name].[hash].js'
  },
  plugins: [
    new HtmlWebpackPlugin(
      {
        filename: 'index.html',
        template: CONFIG.template_html,
        inject: true
      }
    )
  ],
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
    modules: ['node_modules', CONFIG.vendors_path]
  }
}
