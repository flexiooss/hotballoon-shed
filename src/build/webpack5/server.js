'use strict'

const CONFIG = require('./config')
const webpackDev = require('./webpack.dev')
const webpack = require('webpack')
const path = require('path')
const options = require('./server-options')
const WebpackDevServer = require('webpack-dev-server')

const HtmlWebpackPlugin = require('html-webpack-plugin')
const webpackBase = require('./webpack.base')

const isVerbose = process.argv[2] === '-v'
const entries = process.argv[3].split(',')
const htmlTemplate = process.argv[4]
const dist = process.argv[5]
const optionsCustom = process.argv[6]
const parsedOptions = JSON.parse(optionsCustom)


webpackDev.output.publicPath = ''
webpackDev.entry.app = entries

webpackDev.plugins.push(
  new HtmlWebpackPlugin(
    {
      filename: 'index.html',
      template: htmlTemplate,
      inject: true
    }
  )
)

Object.assign(options, parsedOptions)
//options.contentBase = dist
//options.overlay = true
//options.compress = true
//options.writeToDisk= true

if (isVerbose) {
  console.log('_________________ WEBPACK 5 _________________')
  console.log('_________________ TEMPLATE _________________')
  console.log(htmlTemplate)
  console.log('_________________ CUSTOM OPTIONS SERVER _________________')
  console.log(parsedOptions)
  console.log('_________________')
  console.log('_________________ FULL OPTIONS SERVER _________________')
  console.log(options)
  console.log('_________________')
  console.log('_________________ WEBPACK CONF _________________')
  console.log(webpackDev)
  console.log('_________________')
}
//options.open = true

(async () => {
const compiler = webpack(webpackDev)
let server = new WebpackDevServer( options,compiler)

  await server.start();

    if (isVerbose) {
    console.log('_________________ SERVER LISTEN _________________')
    console.log('_________________')
  }

})();


