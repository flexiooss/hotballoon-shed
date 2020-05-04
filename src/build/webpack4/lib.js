const webpackLib = require('./webpack.lib')
const webpack = require('webpack')
const verbose = process.argv[2] === '-v'
const compiler = webpack(webpackLib)

compiler.run((err, stats) => {

  if (err) {
    console.error(err.stack || err);
    if (err.details) {
      console.error("*** Webpack ERRORS : ")
      console.error(err.details);
    }
  }

  const info = stats.toJson();

  if (stats.hasErrors()) {
    console.error("*** Webpack build ERRORS : ")
    console.error(info.errors.toString());
  }

  if (err || stats.hasErrors()) {
    process.exit(1)
  }


if(verbose){
  if (stats.hasWarnings()) {
    console.error("*** Webpack build WARNING : ")
    console.warn(info.warnings.toString());
  }

  console.log(
  '***** [webpack:lib-bundle:build]',
  stats.toString({
    chunks: false,
    colors: true
  }))
}
})
