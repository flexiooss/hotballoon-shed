const webpackProd = require('./webpack.prod')
const webpack = require('webpack')
const ProgressPlugin = require('webpack/lib/ProgressPlugin')

const compiler = webpack(webpackProd)


compiler.apply(new ProgressPlugin(function (percentage, msg) {
  console.log((percentage * 100) + '%', msg)
}))

compiler.run((err, stats) => {
  console.log('[webpack:build]', stats.toString())
})
