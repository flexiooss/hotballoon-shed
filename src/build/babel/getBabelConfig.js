const path = require('path')
const babelOptions = require('./babel-options')
const fs = require('fs')

if (fs.existsSync(path.resolve('./build/babel-options.js'))) {
  const customBabelOptions = require(path.resolve('./build/babel-options.js'))
  Object.assign(babelOptions, customBabelOptions)
}

module.exports = babelOptions
