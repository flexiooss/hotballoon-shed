'use strict'

const path = require('path')
const webpack = require('webpack')
// const ExtractTextPlugin = require('extract-text-webpack-plugin')
// const UglifyJsPlugin = require('uglifyjs-webpack-plugin')
const CleanWebpackPlugin = require('clean-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

const webpackBase = require('./webpack.base')
const CONFIG = require('./config')

CONFIG.entry.app = ['babel-polyfill', './src/js/bootstrap.js']

webpackBase.devtool = false
webpackBase.mode = 'production'
webpackBase.devtool = false

webpackBase.optimization = {
  // minimizer: [
  //   new UglifyJsPlugin({
  //     test: /\.js(\?.*)?$/i,
  //     cache: false,
  //     sourceMap: true,
  //     extractComments: false,
  //     uglifyOptions: {
  //       compress: true
  //     }
  //   })
  // ],
  splitChunks: {
    cacheGroups: {
      styles: {
        name: 'styles',
        test: /\.css$/,
        chunks: 'all',
        enforce: true
      }
    }
  }
}

webpackBase.plugins.push(
  new CleanWebpackPlugin([CONFIG.dist_path + '/*'], {
    root: path.resolve(),
    verbose: true,
    watch: true
  }),
  new webpack.DefinePlugin({
    'window.__DEVELOPPEMENT__': JSON.stringify(false)
    // 'process.env.NODE_ENV': JSON.stringify('production')
  }),
  new MiniCssExtractPlugin({
    filename: '[name].[hash].css',
    chunkFilename: '[id].[hash].css'
  })
)

webpackBase.module.rules.push({
  test: /\.css$/,
  use: [
    MiniCssExtractPlugin.loader,
    'css-loader'
  ]
})

// webpackBase.module.rules.forEach(function(rule, k) {
//   if ('.css'.match(rule.test)) {
//     rule.use.shift()
//     webpackBase.module.rules[k].use = ExtractTextPlugin.extract({
//       fallback: 'style-loader',
//       use: [{
//         loader: rule.use[0].loader,
//         options: {
//           minimize: true
//         }
//       }]
//     })
//   }
// })

module.exports = webpackBase
