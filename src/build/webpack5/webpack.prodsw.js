'use strict'

const path = require('path')
const webpack = require('webpack')

const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

const babelOptions = require('../babel/getBabelConfig')
const webpackBase = require('./webpack.base')
const CONFIG = require('./config')

const isVerbose = process.argv[2] === '-v'
//const entries = process.argv[3].split(',')
const entries = JSON.parse(process.argv[3])
const html_template = process.argv[4]
const dist_path = process.argv[5]
/**
 * @type {boolean}
 */
const inspect = process.argv[6] === '1'
//entries.unshift(path.resolve(__dirname, './runtime.js'))
//webpackBase.entry.app = entries
webpackBase.entry = entries
webpackBase.mode = 'production'
webpackBase.devtool = false
webpackBase.output.path = dist_path
webpackBase.stats = {errorDetails: true}
// webpackBase.target = 'browserslist: > 0.5%, last 3 versions, Firefox ESR, not dead'
//webpackBase.target = 'web'
webpackBase.output.clean=false

webpackBase.optimization = {
  minimize: true,
    runtimeChunk: {
      name: (entrypoint) => {
        if (entrypoint.name === "service-worker") {
          return null;
        }

        return `runtime-${entrypoint.name}`
      }
    },
  splitChunks: {
    chunks(chunk) {
        return chunk.name !== "boot" && chunk.name !== "service-worker";
    }
  }
}

webpackBase.plugins.push(
  new webpack.DefinePlugin({
    '__DEVELOPMENT__': JSON.stringify(false),
     '__ASSERT__': JSON.stringify(false),
    '__DEBUG__': JSON.stringify(false)
  }),
)

if (inspect) {
  webpackBase.plugins.push(
    new BundleAnalyzerPlugin()
  )
}

webpackBase.module.rules.push(
  {
    test: /\.js$/,
    loader: 'babel-loader',
    options: babelOptions.prod
  },
)

module.exports = webpackBase
