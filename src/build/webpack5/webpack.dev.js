'use strict'

const webpackBase = require('./webpack.base')
const webpack = require('webpack')
const babelOptions = require('../babel/getBabelConfig')

const CONFIG = require('./config')
const path = require('path')

webpackBase.output.clean = true
webpackBase.devtool = 'eval'
//webpackBase.devtool = false
webpackBase.stats = {errorDetails: true}
webpackBase.mode = 'development'

webpackBase.optimization={
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        apiClient: {
        test: /\/node_modules\/@flexio-corp\/.*-client/,
        name: 'api-client',
        reuseExistingChunk: true,
        priority: 1
      },
      oss: {
        test: /[\\/]node_modules[\\/]@flexio-oss/,
        name: 'oss',
        reuseExistingChunk: true,
      },
      corp: {
        test: /[\\/]node_modules[\\/]@flexio-corp/,
        name: 'corp',
        reuseExistingChunk: true,
      },
      tinymce: {
        test: /[\\/]node_modules[\\/]tinymce/,
        name: 'tinymce',
      },
      },
    },
    runtimeChunk: 'single',
    minimize: false,
  }

webpackBase.plugins.push(
  new webpack.DefinePlugin({
    '__DEVELOPMENT__': JSON.stringify(true),
    '__ASSERT__': JSON.stringify(true),
    '__DEBUG__': JSON.stringify(true),
  })
)
//webpackBase.target = 'browserslist: > 0.5%, last 2 versions, Firefox ESR, not dead' //will break HMR on  "webpack-dev-server": "^3.11.2"
webpackBase.target = 'web'
webpackBase.module.rules.push(

  {
    test: /\.(png|jpe?g|gif|svg|woff2?|eot|ttf|otf|wav|wasm)(\?.*)?$/,
    type: 'asset'
  },

 {
    test: /\/[\d\w_-]+\.txt\.css$/,
    loader: 'css-loader',
        options: {
          modules: false,
          exportType: 'string',
          importLoaders: 1,
          sourceMap:false
        }
  },
  {
    test: /\/[\d\w_-]+\.module\.css$/,
    use: [
      'style-loader',
      {
        loader: 'css-loader',
        options: {
          modules: true,
          importLoaders: 1
        }
      }
    ]
  },

  {
    test: /\/[\d\w_-]+\.css$/,
    use: [
      'style-loader',
      {
        loader: 'css-loader',
        options: {
          modules: false
        }
      }
    ]
  }
)

module.exports = webpackBase
