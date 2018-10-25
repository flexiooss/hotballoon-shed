const webpackProd = require('./webpack.prod')
const webpack = require('webpack')


const compiler = webpack(webpackProd)
compiler.run((err, stats) => {
  console.error(err)
  // console.log(stats)
})
