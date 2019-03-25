'use strict'

const CONFIG = require('./config')
const webpackDev = require('./webpack.dev')
const webpack = require('webpack')
const path = require('path')
const options = require('./server-options')
const WebpackDevServer = require('webpack-dev-server')
const fs = require('fs')

const isVerbose = process.argv[2] == '-v'

if (fs.existsSync(path.resolve('./build/server-options.js'))) {
  const serverOptions = require(path.resolve('./build/server-options.js'))
  Object.assign(options, serverOptions)
  if (isVerbose) {
    console.log('_________________ CUSTOM OPTIONS SERVER _________________')
    console.log(serverOptions)
    console.log('_________________')
  }
}
WebpackDevServer.addDevServerEntrypoints(webpackDev, options)

const compiler = webpack(webpackDev)

let server = new WebpackDevServer(compiler, options)
server.listen(CONFIG.port, CONFIG.host, (err) => {
  if (isVerbose) {
    console.log('_________________ SERVER LISTEN _________________')
    console.log(webpackDev.output.publicPath)
    console.log('_________________')
    if (err) {
      console.log('_________________ SERVER ERROR _________________')
      console.error(err)
      console.log('_________________')
    }
  }
})
