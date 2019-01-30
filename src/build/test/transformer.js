const webpackTest = require('./webpack.test')
const webpack = require('webpack')

/**
 *
 * @param {string} testId
 * @param {array<string>} testsPath
 * @param {Object} env
 * @param {Transformer~transformedCallback} clb
 */
module.exports = function(testId, testsPath, env, clb) {
  const filePath = '/tmp/hotballon-shed/tests'
  const fileName = 'test_' + testId + '.js'

  webpackTest.entry.app = testsPath
  webpackTest.output = {
    filename: fileName,
    path: filePath
  }
  webpackTest.plugins.push(
    new webpack.DefinePlugin(Object.assign(env, {
      'process.env.NODE_ENV': JSON.stringify('test')
    }))
  )
  webpackTest.target = 'node'
  const compiler = webpack(webpackTest)

  compiler.run((err, stats) => {
    clb(filePath + '/' + fileName)
  })
}
/**
 *
 * @callback Transformer~transformedCallback
 * @param {string} filePath
 */
