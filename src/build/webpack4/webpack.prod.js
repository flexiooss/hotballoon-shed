'use strict'

const path = require('path')
const webpack = require('webpack')
const UglifyJsPlugin = require('uglifyjs-webpack-plugin')
const CleanWebpackPlugin = require('clean-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const LinkStylesheetHtmlWebpackPlugin = require('link-stylesheet-html-webpack-plugin')

const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin')
const Terser = require('terser')
const SriPlugin = require('webpack-subresource-integrity')
const HtmlWebpackPlugin = require('html-webpack-plugin')

const webpackBase = require('./webpack.base')
const CONFIG = require('./config')

const entries = process.argv[3].split(',')
const html_template = process.argv[4]
const dist_path = process.argv[5]

entries.unshift(path.resolve(__dirname, '../../../node_modules/babel-polyfill'))
webpackBase.entry.app = entries

webpackBase.devtool = false
webpackBase.mode = 'production'
webpackBase.devtool = false
webpackBase.output.crossOriginLoading = 'anonymous'
webpackBase.output.path = dist_path

webpackBase.optimization = {
  splitChunks: {
    chunks: 'all'
  },
  minimizer: [
    new UglifyJsPlugin({
      sourceMap: true,
      minify(file, sourceMap) {
        const uglifyJsOptions = {}

        if (sourceMap) {
          uglifyJsOptions.sourceMap = {
            content: sourceMap
          }
        }

        return Terser.minify(file, uglifyJsOptions)
      }
    }),
    new OptimizeCSSAssetsPlugin({
      cssProcessorPluginOptions: {
        preset: ['default', {discardComments: {removeAll: true}}]
      }
    })
  ]
}

webpackBase.plugins.push(
new HtmlWebpackPlugin(
      {
        filename: 'index.html',
        template: html_template,
        inject: true
      }
    ),
  new CleanWebpackPlugin([dist_path + '/*'], {
    root: path.resolve(),
    verbose: true,
    watch: true
  }),
  new webpack.DefinePlugin({
    'window.__DEVELOPMENT__': JSON.stringify(false)
  }),
  new MiniCssExtractPlugin({
    filename: '[name].[hash].css',
    chunkFilename: '[id].[hash].css'
  }),
  new SriPlugin({
    hashFuncNames: ['sha256', 'sha384']
  })
  // new LinkStylesheetHtmlWebpackPlugin()
)

webpackBase.module.rules.push(
  {
    test: /\.css$/,
    use: [
      MiniCssExtractPlugin.loader,
      {
        loader: 'css-loader',
        options: {
          modules: true,
          importLoaders: 1,
          localIdentName: '[sha1:hash:hex:4]',
                        camelCase:true

        }
      },
      {
        loader: 'css-media-queries-loader',
        options: CONFIG.mediaqueries
      }
    ]
  }
)

module.exports = webpackBase
