const webpackProd = require('./webpack.prod_debug')
const webpack = require('webpack')
const verbose = process.argv[2] === '-v'

const compiler = webpack(webpackProd)

compiler.run((err, stats) => {

  if (err) {
    console.error(err.stack || err)
    if (err.details) {
      console.error('*** Webpack ERRORS : ')
      console.error(err.details)
    }
  }

  if (verbose) {
    const info = stats.toJson()

    if (stats.hasErrors()) {
      console.error('*** Webpack build ERRORS : ')
      console.error(info.errors)
    }

    if (stats.hasWarnings()) {
      console.warn('*** Webpack build WARNING : ')
      console.warn(info.warnings)
    }
  }

  console.log(
    '***** [webpack:app:build]',
    stats.toString({
      chunks: false,
      colors: true
    }))

  if (err || stats.hasErrors()) {
    process.exit(1)
  }
})
