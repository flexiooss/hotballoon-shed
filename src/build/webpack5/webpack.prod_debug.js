'use strict'

const path = require('path')
const webpack = require('webpack')

const {WebpackManifestPlugin} = require('webpack-manifest-plugin')
const WorkboxPlugin = require('workbox-webpack-plugin')
const WebpackPwaManifest = require('webpack-pwa-manifest')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const HtmlMinimizerPlugin = require("html-minimizer-webpack-plugin");
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin')

const webpackBase = require('./webpack.base')
const CONFIG = require('./config')

const isVerbose = process.argv[2] === '-v'
const entries = process.argv[3].split(',')
const html_template = process.argv[4]
const dist_path = process.argv[5]
const manifestConfig = process.argv[6]
/**
 * @type {boolean}
 */
const inspect = process.argv[7] === '1'
const parsedManifestConfig = JSON.parse(manifestConfig)
entries.unshift(path.resolve(__dirname, './runtime.js'))
webpackBase.entry.app = entries
webpackBase.mode = 'development'
webpackBase.devtool = 'eval'
webpackBase.devtool = 'inline-source-map'
webpackBase.devtool = 'nosources-source-map'
webpackBase.output.crossOriginLoading = 'anonymous'
webpackBase.output.path = dist_path+'/debug'
webpackBase.output.publicPath = '/debug'
webpackBase.output.clean = true
webpackBase.stats = {errorDetails: true}
// webpackBase.target = 'browserslist: > 0.5%, last 3 versions, Firefox ESR, not dead'
webpackBase.target = 'web'

if (isVerbose) {
  console.log('_________________ PWA MANIFEST _________________')
  console.log(parsedManifestConfig)
}


webpackBase.plugins.push(
  new webpack.DefinePlugin({
    'window.__DEVELOPMENT__': JSON.stringify(false)
  }),
  new WebpackPwaManifest({
    filename: 'manifest.json',
    inject: true,
    fingerprints: true,
    ios: false,
    publicPath: null,
    includeDirectory: true,
    name: parsedManifestConfig.name+' [debug]',
    short_name: parsedManifestConfig.short_name+' [debug]',
    description: parsedManifestConfig.description,
    crossorigin: parsedManifestConfig.crossorigin,
    display: parsedManifestConfig.display,
    theme_color: parsedManifestConfig.theme_color,
    background_color: parsedManifestConfig.background_color,
    orientation: parsedManifestConfig.orientation,
    start_url: parsedManifestConfig.start_url,
    icons: [
      {
        src: path.resolve(__dirname, '../html/assets/icon.png'),
        sizes: [96, 128, 192, 256, 384, 512, 1024]
      }
    ]
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
      inject: true,
      scriptLoading: 'defer',
      meta: {
        viewport: 'width=device-width, initial-scale=1, shrink-to-fit=no',
        charset: 'utf-8'
      },
      favicon: path.resolve(__dirname, '../html/assets/favicon.ico')
    }
  ),
  new WorkboxPlugin.GenerateSW({
    maximumFileSizeToCacheInBytes: 5 * 1024 * 1024,
    clientsClaim: true,
    skipWaiting: true
  }),
  new WebpackManifestPlugin({fileName: 'files-manifest.json'}),
)

if (inspect) {
  webpackBase.plugins.push(
    new BundleAnalyzerPlugin()
  )
}

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