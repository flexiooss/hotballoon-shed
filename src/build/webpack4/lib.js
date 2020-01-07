const webpackLib = require('./webpack.lib')
const webpack = require('webpack')
const ProgressPlugin = require('webpack/lib/ProgressPlugin')

const compiler = webpack(webpackLib)


compiler.apply(
  // new ProgressPlugin(function (percentage, msg) {
  //   console.log((percentage * 100) + '%', msg)
  // })
)

compiler.run((err, stats) => {
  console.log('***** [webpack:lib:build]', stats.toString())
})
