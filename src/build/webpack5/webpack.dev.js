'use strict'

const webpackBase = require('./webpack.base')
const webpack = require('webpack')
const babelOptions = require('../babel/getBabelConfig')

const CONFIG = require('./config')
const path = require('path')
const StyleLintPlugin = require('stylelint-webpack-plugin')
const CircularDependencyPlugin = require('circular-dependency-plugin')

webpackBase.output.clean = true
webpackBase.devtool = 'eval-cheap-module-source-map'
webpackBase.devtool = 'eval'
webpackBase.stats = {errorDetails: true}
webpackBase.mode = 'development'

webpackBase.plugins.push(
  new webpack.DefinePlugin({
    'window.__DEVELOPMENT__': JSON.stringify(true),
    'window.__ASSERT__': JSON.stringify(true),
    'window.__DEBUG__': JSON.stringify(true),
  }),
  new CircularDependencyPlugin(),
  new StyleLintPlugin(),
)
//webpackBase.target = 'browserslist: > 0.5%, last 2 versions, Firefox ESR, not dead' //will break HMR on  "webpack-dev-server": "^3.11.2"
webpackBase.target = 'web'
webpackBase.module.rules.push(
  {
    test: /\.(png|jpe?g|gif|svg|woff2?|eot|ttf|otf|wav)(\?.*)?$/,
    type: 'asset'
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
