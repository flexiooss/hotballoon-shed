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

webpackBase.entry.app = entries

webpackBase.mode = 'production'
webpackBase.devtool = false
webpackBase.output.crossOriginLoading = 'anonymous'
webpackBase.output.path = dist_path
webpackBase.output.filename = 'bundle.js'

webpackBase.optimization = {

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
    })
  ]
}

webpackBase.plugins.push(
  new webpack.DefinePlugin({
    'window.__DEVELOPMENT__': JSON.stringify(false)
  })
)



module.exports = webpackBase
