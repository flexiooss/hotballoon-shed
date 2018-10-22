'use strict'

const CONFIG = require('./config')
const webpackDev = require('./webpack.dev')
const webpack = require('webpack')
const path = require('path')
const options = require('./server-options')
const WebpackDevServer = require('webpack-dev-server')
const fs = require('fs')

if (fs.existsSync(path.resolve('server-options.js'))) {
  const serverOptions = require(path.resolve('server-options.js'))
  console.log(serverOptions)
  Object.assign(options, serverOptions)
}
WebpackDevServer.addDevServerEntrypoints(webpackDev, options)

const compiler = webpack(webpackDev)

let server = new WebpackDevServer(compiler, options)
server.listen(CONFIG.port, CONFIG.host, (err) => {
  console.log(webpackDev.output.publicPath)
  if (err) {
    console.log(err)
  }
})
