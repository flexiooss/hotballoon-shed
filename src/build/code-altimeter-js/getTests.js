const babel = require('@babel/core')
const fs = require('fs')
const path = require('path')

module.exports = babel.transform(
  fs.readFileSync(path.resolve('TestSuite.js'), 'utf8'), require(path.resolve(__dirname, '../babel/getBabelConfig'))
).code
