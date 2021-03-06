'use strict'

const webpackBase = require('./webpack.base')
const webpack = require('webpack')
const babelOptions = require('../babel/getBabelConfig')

const CONFIG = require('./config')
const path = require('path')
const StyleLintPlugin = require('stylelint-webpack-plugin')
const CircularDependencyPlugin = require('circular-dependency-plugin')

webpackBase.output.globalObject = 'this'

webpackBase.devtool = 'cheap-module-eval-source-map'

webpackBase.mode = 'development'

webpackBase.plugins.push(
  new webpack.DefinePlugin({
    'window.__DEVELOPMENT__': JSON.stringify(true),
    'window.__ASSERT__': JSON.stringify(true),
    'window.__DEBUG__': JSON.stringify(true),
    'process.env.NODE_ENV': JSON.stringify('development')
  }),
  new webpack.NamedModulesPlugin(),
  new webpack.HotModuleReplacementPlugin(),
  new webpack.NoEmitOnErrorsPlugin(),
  new CircularDependencyPlugin(),
  new StyleLintPlugin()
)

webpackBase.module.rules.push(
  {
        test: /\.js$/,
        loader: 'babel-loader',
        options: babelOptions
      },{
    test: /\.css$/,
    use: [
      'style-loader',
      {
        loader: 'css-loader',
        options: {
          modules: true,
          importLoaders: 1,
          localIdentName: '[local]',
            sourceMap:true,
            camelCase:true
        }
      },
//      {
//        loader: 'css-media-queries-loader',
//        options: CONFIG.mediaqueries
//      }
    ]
  }
)

module.exports = webpackBase
