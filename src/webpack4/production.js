const webpackProd = require('./webpack.prod')
const webpack = require('webpack')


const compiler = webpack(webpackProd)
compiler.run((err, stats) => {
  console.log(err)
  // console.log(stats)
})
