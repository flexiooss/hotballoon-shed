'use strict'
const path = require('path')
const babelOptions = require('../babel/getBabelConfig')
const CONFIG = require('../webpack4/config')

const webpackBase = {
  entry: CONFIG.entry,
  plugins: [],
  performance: {
    hints: false
  },
  optimization: {
    removeAvailableModules: false,
    removeEmptyChunks: false,
    splitChunks: false
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        use:[
        {
          loader: 'cache-loader',
          options: {
            cacheDirectory: path.resolve('/tmp/hotballoon-shed/cache')
          }
        },
        {
          loader: 'babel-loader',
          options: babelOptions
        }
        ],
        include: /node_modules/
      },
//      {
//        enforce: 'pre',
//        test: /\.js$/,
//        exclude: /node_modules/,
//        loader: 'eslint-loader',
//        options: {
//          'root': true,
//          'parser': 'babel-eslint',
//          'parserOptions': {
//            'sourceType': 'module'
//          },
//          'extends': 'standard',
//          'plugins': ['html'],
//          'rules': {
//            'no-unused-vars': ['warn', {
//              'vars': 'local',
//              'args': 'none',
//              'ignoreRestSiblings': false
//            }],
//            'arrow-parens': 0,
//            'generator-star-spacing': 0,
//            'no-debugger': 0,
//            'no-new': 0,
//            'space-before-function-paren': ['error', {
//              'anonymous': 'never',
//              'named': 'never',
//              'asyncArrow': 'never'
//            }]
//          }
//        }
//      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        options: babelOptions,
        exclude: /node_modules/
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
    modules: [CONFIG.vendors_path]
  }
}
webpackBase.mode = 'development'
//webpackBase.target= 'node'

module.exports = webpackBase
