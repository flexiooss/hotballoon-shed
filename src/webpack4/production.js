const webpackProd = require('./webpack.prod')
const webpack = require('webpack')


const compiler = webpack(webpackProd)
compiler.run((err, stats) => {
  console.log('[webpack:build]', stats.toString())
})
