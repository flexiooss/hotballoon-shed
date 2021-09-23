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

const babelOptions = require('../babel/getBabelConfig')
const webpackBase = require('./webpack.base')
const CONFIG = require('./config')

const isVerbose = process.argv[2] === '-v'
const entries = process.argv[3].split(',')
const html_template = process.argv[4]
const dist_path = process.argv[5]
const manifestConfig = process.argv[6]
const parsedManifestConfig = JSON.parse(manifestConfig)

webpackBase.entry.app = entries
webpackBase.mode = 'production'
webpackBase.devtool = false
webpackBase.output.crossOriginLoading = 'anonymous'
webpackBase.output.path = dist_path
webpackBase.output.clean = true
webpackBase.stats = {errorDetails: true}
webpackBase.target = 'browserslist: > 0.5%, last 3 versions, Firefox ESR, not dead'

if (isVerbose) {
  console.log('_________________ PWA MANIFEST _________________')
  console.log(parsedManifestConfig)
}

webpackBase.optimization = {
  minimize: true,
  splitChunks: {
    chunks: 'all',
    maxSize: 5000000,
    cacheGroups: {
      flexioClient: {
        test: /\/node_modules\/@flexio-corp\/.*-client\/.*\.js/,
        name: 'api-client',
        chunks: 'all',
        reuseExistingChunk: true,
        priority: 0
      },
      flexio: {
        test: /[\\/]node_modules[\\/]((@flexio-corp\/.*-bundle)|@flexio-oss)\/.*\.js/,
        name: 'corpjs',
        chunks: 'all',
        reuseExistingChunk: true,
      },
      styles: {
        name: 'styles',
        type: 'css/mini-extract',
        // For webpack@4
        test: /\.css$/,
        chunks: 'all',
        enforce: true
      }
    }
  },
  minimizer: [
    `...`,
    new CssMinimizerPlugin(),
    new HtmlMinimizerPlugin()
  ]
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
    name: parsedManifestConfig.name,
    short_name: parsedManifestConfig.short_name,
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
    linkType:false,
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
  // new SriPlugin({
  //   hashFuncNames: ['sha256', 'sha384']
  // }),
  new WorkboxPlugin.GenerateSW({
    maximumFileSizeToCacheInBytes: 5 * 1024 * 1024
  }),
  new WebpackManifestPlugin({fileName: 'files-manifest.json'}),
  // new BundleAnalyzerPlugin()
)

webpackBase.module.rules.push(
  {
    test: /\.(png|jpe?g|gif|svg|woff2?|eot|ttf|otf|wav)(\?.*)?$/,
    type: 'asset/resource'
  },
  {
    test: /\.js$/,
    loader: 'babel-loader',
    options: babelOptions
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