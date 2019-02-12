'use strict'
const path = require('path')
const babelOptions = require('../babel/getBabelConfig')
const CONFIG = require('../webpack4/config')

const webpackBase = {
  entry: CONFIG.entry,
  plugins: [],

  module: {
    rules: [
      {
        test: /\.js$/,
        loader: 'cache-loader',
        options: {
          cacheDirectory: path.resolve('/tmp/hotballoon-shed/cache')
        }
      },
      {
        enforce: 'pre',
        test: /\.js$/,
        exclude: /node_modules/,
        loader: 'eslint-loader',
        options: {
          'root': true,
          'parser': 'babel-eslint',
          'parserOptions': {
            'sourceType': 'module'
          },
          'extends': 'standard',
          'plugins': ['html'],
          'rules': {
            'no-unused-vars': ['warn', {
              'vars': 'local',
              'args': 'none',
              'ignoreRestSiblings': false
            }],
            'arrow-parens': 0,
            'generator-star-spacing': 0,
            'no-debugger': 0,
            'no-new': 0,
            'space-before-function-paren': ['error', {
              'anonymous': 'never',
              'named': 'never',
              'asyncArrow': 'never'
            }]
          }
        }
      },
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
          loader: 'pathname-loader',
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
