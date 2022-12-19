'use strict'

const path = require('path')
const webpack = require('webpack')
const babelOptions = require('../babel/getBabelConfig')

const UglifyJsPlugin = require('uglifyjs-webpack-plugin')
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin')
const Terser = require('terser')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

const webpackBase = require('./webpack.base')
const CONFIG = require('./config')

//const entries = process.argv[3].split(',')
const entries = JSON.parse(process.argv[3])

const html_template = process.argv[4]
const dist_path = process.argv[5]

webpackBase.entry = entries

webpackBase.mode = 'production'
webpackBase.devtool = false
webpackBase.output.crossOriginLoading = 'anonymous'
webpackBase.output.path = dist_path
webpackBase.output.filename = 'bundle.js'

webpackBase.optimization = {

  minimizer: [
   new UglifyJsPlugin({
     uglifyOptions: {
          output: {
            comments: false,
//      TODO: check this for tinymce
          "ascii_only": true
        }
      },
      sourceMap: true,
      minify(file, sourceMap) {
        const uglifyJsOptions = {
          output: {
              comments: false,
  //      TODO: check this for tinymce
            "ascii_only": true
          }
        }

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
  new webpack.DefinePlugin({
    '__DEVELOPMENT__': JSON.stringify(false),
    '__ASSERT__': JSON.stringify(false),
    '__DEBUG__': JSON.stringify(false)
  }),
  new MiniCssExtractPlugin({
    filename: '[name].[hash].css',
    chunkFilename: '[id].[hash].css'
  })
)

webpackBase.module.rules.push(
      {
        test: /\.js$/,
        loader: 'babel-loader',
        options: babelOptions
      },
  {
    test: /\.css$/,
    use: [
      'style-loader',
      MiniCssExtractPlugin.loader,
      {
        loader: 'css-loader',
        options: {
          modules: true,
          importLoaders: 1,
          localIdentName: '[local]',
            sourceMap:false,
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
