const webpack4Config = require('../webpack4/webpack.test')
const webpack5Config = require('../webpack5/webpack.test')
const webpack = require('webpack')

/**
 *
 * @param {string} testId
 * @param {array<string>} testsPath
 * @param {Object} env
 * @param {Transformer~transformedCallback} clb
 * @param {boolean} sourceMap
 * @param {string} builder
 */
module.exports = function (testId, testsPath, env, clb, sourceMap = false, builder) {
  console.log('writing test file... ... ...')
  const filePath = '/tmp/hotballoon-shed/tests'
  const fileName = 'test_' + testId + '.js'
  const sourceMapFileNameOut = 'test_' + testId + '.js.map'
  let webpackConfig = null

  if (builder === 'webpack4') {
    webpack4Config.entry.app = testsPath
    webpack4Config.output = {
      filename: fileName,
      path: filePath,
      sourceMapFilename: sourceMapFileNameOut,
      pathinfo: false
    }
    webpack4Config.plugins.push(
      new webpack.DefinePlugin(Object.assign(env, {
        'process.env.NODE_ENV': JSON.stringify('test')
      }))
    )
    webpack4Config.devtool = false
    if (sourceMap) {
      webpack4Config.devtool = 'cheap-module-eval-source-map'
    }

    webpackConfig = webpack4Config

  } else if (builder === 'webpack5') {
    webpack5Config.entry.app = testsPath
    webpack5Config.output = {
      filename: fileName,
      path: filePath,
      sourceMapFilename: sourceMapFileNameOut,
      pathinfo: false
    }
    webpack5Config.plugins.push(
      new webpack.DefinePlugin(Object.assign(env, {
        'process.env.NODE_ENV': JSON.stringify('test')
      }))
    )

    webpack5Config.devtool = false
    if (sourceMap) {
      webpack5Config.devtool = 'eval-cheap-module-source-map'
    }

    webpackConfig = webpack5Config
  }

  const compiler = webpack(webpackConfig)

  compiler.run((err, stats) => {
    console.log('test file write at : ' + filePath + '/' + fileName)
    clb(filePath + '/' + fileName, sourceMap)
  })
}
/**
 *
 * @callback Transformer~transformedCallback
 * @param {string} filePath
 */
