'use strict'

const path = require('path')
const webpack = require('webpack')
const UglifyJsPlugin = require('uglifyjs-webpack-plugin')
const CleanWebpackPlugin = require('clean-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin')
const Terser = require('terser')
const LinkStylesheetHtmlWebpackPlugin = require('link-stylesheet-html-webpack-plugin')
const SriPlugin = require('webpack-subresource-integrity')
// const AppCachePlugin = require('appcache-webpack-plugin')
// const MediaQueryPlugin = require('media-query-plugin')

const webpackBase = require('./webpack.base')
const CONFIG = require('./config')

webpackBase.entry.app = ['babel-polyfill', './src/js/bootstrap.js']

webpackBase.devtool = false
webpackBase.mode = 'production'
webpackBase.devtool = false
webpackBase.output.crossOriginLoading = 'anonymous'

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
    ,
    new OptimizeCSSAssetsPlugin({
      cssProcessorPluginOptions: {
        preset: ['default', {discardComments: {removeAll: true}}],
      }
    })
  ]
}

// const cssPrint = new LinkStylesheetHtmlWebpackPlugin({
//   'media': 'print'
// })

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
  }),
  new SriPlugin({
    hashFuncNames: ['sha256', 'sha384']
  })
)

webpackBase.module.rules.push(
  {
    test: /\.css$/,
    use: [
      // {
      //   loader: 'link-stylesheet-html-webpack-plugin',
      // },
      MiniCssExtractPlugin.loader,
      {
        loader: 'css-loader',
        options: {
          modules: true,
          importLoaders: 1,
          localIdentName: '[sha1:hash:hex:4]'
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
