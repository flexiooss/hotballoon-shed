'use strict'

const webpack = require('webpack')
// const webpackBase = require('../webpack4/webpack.base')
const babelOptions = require('../babel/getBabelConfig')
const CONFIG = require('../webpack4/config')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

const webpackBase = {
  entry: CONFIG.entry,
  plugins: [],

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
    modules: ['node_modules', CONFIG.vendors_path]
  }
}

// const path = require('path')

// CONFIG.entry.app = [
//   path.resolve('./src/js/_before.js'),
//   path.resolve('./src/js/bootstrap.js'),
//   path.resolve('./src/js/_after.js')
// ]
// webpackBase.output.globalObject = 'this'

// webpackBase.devtool = 'cheap-module-eval-source-map'

webpackBase.mode = 'development'


//
// webpackBase.module.rules.push(
//   {
//     test: /\.css$/,
//     use: [
//       MiniCssExtractPlugin.loader,
//       {
//         loader: 'css-loader',
//         options: {
//           modules: true,
//           importLoaders: 1,
//           localIdentName: '[sha1:hash:hex:4]'
//         }
//       },
//       {
//         loader: 'css-media-queries-loader',
//         options: CONFIG.mediaqueries
//       }
//     ]
//   }
// )
//
// webpackBase.module.rules.push(
//   {
//     test: /\.css$/,
//     use: [
//       'style-loader',
//       {
//         loader: 'css-loader',
//         options: {
//           modules: true,
//           importLoaders: 1,
//           localIdentName: '[local]'
//         }
//       },
//       {
//         loader: 'css-media-queries-loader',
//         options: CONFIG.mediaqueries
//       }
//     ]
//   }
// )

module.exports = webpackBase
