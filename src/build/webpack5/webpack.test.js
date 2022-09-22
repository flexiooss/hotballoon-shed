'use strict'
const path = require('path')
const babelOptions = require('../babel/getBabelConfig')
const CONFIG = require('./config')
const webpack = require('webpack')

const webpackBase = {
  entry: CONFIG.entry,
  plugins: [
   new webpack.DefinePlugin({
    '__DEVELOPMENT__': JSON.stringify(true),
     '__ASSERT__': JSON.stringify(true),
    '__DEBUG__': JSON.stringify(true)
  })
  ],
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
};

module.exports = webpackBase
