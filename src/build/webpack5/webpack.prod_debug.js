'use strict'

const path = require('path')
const webpack = require('webpack')

const {WebpackManifestPlugin} = require('webpack-manifest-plugin')
//const WorkboxPlugin = require('workbox-webpack-plugin')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const HtmlMinimizerPlugin = require("html-minimizer-webpack-plugin");
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin')

const webpackBase = require('./webpack.base')
const CONFIG = require('./config')

const isVerbose = process.argv[2] === '-v'
//const entries = process.argv[3].split(',')
const entries = JSON.parse(process.argv[3])

const html_template = process.argv[4]
const dist_path = process.argv[5]
//entries.unshift(path.resolve(__dirname, './runtime.js'))
//webpackBase.entry.app = entries
webpackBase.entry = entries
webpackBase.mode = 'development'
webpackBase.devtool = 'inline-source-map'
webpackBase.output.crossOriginLoading = 'anonymous'
webpackBase.output.path = dist_path+'/debug'
//webpackBase.output.publicPath = '/debug'
webpackBase.output.clean = true
webpackBase.stats = {errorDetails: true}
// webpackBase.target = 'browserslist: > 0.5%, last 3 versions, Firefox ESR, not dead'
webpackBase.target = 'web'

webpackBase.plugins.push(
  new webpack.DefinePlugin({
    '__DEVELOPMENT__': JSON.stringify(false),
    '__ASSERT__': JSON.stringify(true),
    '__DEBUG__': JSON.stringify(true)
  }),
  new MiniCssExtractPlugin({
    filename: "[name].[contenthash].css",
    chunkFilename: "[id].[contenthash].css",
    linkType: false,
    attributes: {
      rel: "preload",
      as: "style",
      onLoad: "this.onload=null;this.rel='stylesheet'"
    }
  }),
  new HtmlWebpackPlugin(
    {
      filename: 'index.html',
      template: html_template,
      inject: 'body',
      scriptLoading: 'defer',
      meta: {
        viewport: 'width=device-width, initial-scale=1, shrink-to-fit=no',
        charset: 'utf-8'
      },
      favicon: path.resolve(__dirname, '../html/assets/favicon.ico'),
      excludeChunks:['service-worker']
    }
  ),
//  new WorkboxPlugin.GenerateSW({
//    maximumFileSizeToCacheInBytes: 5 * 1024 * 1024,
//    clientsClaim: true,
//    skipWaiting: true
//  }),
  new WebpackManifestPlugin({fileName: 'files-manifest.json'}),
)

webpackBase.module.rules.push(
  {
    test: /\.(png|jpe?g|gif|svg|woff2?|eot|ttf|otf|wav)(\?.*)?$/,
    type: 'asset/resource'
  },
  {
    test: /\.module\.css$/,
    use: [
      MiniCssExtractPlugin.loader,
      {
        loader: 'css-loader',
        options: {
          modules: true,
          importLoaders: 1,
          sourceMap: false,
        }
      }
    ]
  },
  {
    test: /\/[\d\w_-]+\.css$/,
    use: [
      MiniCssExtractPlugin.loader,
      {
        loader: 'css-loader',
        options: {
          modules: false
        }
      },
    ]
  }
)

module.exports = webpackBase
