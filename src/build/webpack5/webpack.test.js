'use strict'
const path = require('path')
const babelOptions = require('../babel/getBabelConfig')
const CONFIG = require('./config')

const webpackBase = {
  entry: CONFIG.entry,
  plugins: [],
  performance: {
    hints: false
  },
  mode:'development',
  target: "node",
  optimization: {
    removeAvailableModules: false,
    removeEmptyChunks: false,
    splitChunks: false
  },
  cache: {
    type: 'filesystem',
    cacheDirectory: path.resolve('/tmp/hotballoon-shed/cache')
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        loader: 'babel-loader',
        options: babelOptions.test,
        exclude: /node_modules/
      },
      {
        test: /\.(css|png|jpe?g|gif|svg|woff2?|eot|ttf|otf|wav)(\?.*)?$/,
        type: 'asset'
      }
    ]
  },
  resolveLoader: {
    modules: [CONFIG.vendors_path]
  }
}

module.exports = webpackBase
