'use strict'

const CONFIG = require('./config')
const webpackDev = require('./webpack.dev')
const webpack = require('webpack')
const path = require('path')
const options = require('./server-options')
const WebpackDevServer = require('webpack-dev-server')
const fs = require('fs')

const isVerbose = process.argv[2]

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
  console.log('server listen : '+ webpackDev.output.publicPath)
  if (err) {
    console.error(err)
  }
})
