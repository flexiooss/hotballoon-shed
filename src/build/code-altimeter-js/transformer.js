const webpackTest = require('./webpack.test')
const webpack = require('webpack')

/**
 *
 * @param {string} testId
 * @param {array<string>} testsPath
 * @param {Object} env
 * @param {Transformer~transformedCallback} clb
 * @param {bool} sourceMap
 */
module.exports = function (testId, testsPath, env, clb, sourceMap=false) {
console.log('writing test file... ... ...')
  const filePath = '/tmp/hotballoon-shed/tests'
  const fileName = 'test_' + testId + '.js'
  const sourceMapFileNameOut = 'test_' + testId + '.js.map'

  webpackTest.entry.app = testsPath
  webpackTest.output = {
    filename: fileName,
    path: filePath,
    sourceMapFilename: sourceMapFileNameOut,
    pathinfo: false
  }
  webpackTest.plugins.push(
    new webpack.DefinePlugin(Object.assign(env, {
      'process.env.NODE_ENV': JSON.stringify('test')
    }))
  )

  webpackTest.devtool = false
  if(sourceMap){
    webpackTest.devtool = 'cheap-module-eval-source-map'
  }

//webpackTest.optimization = {
//  splitChunks: {
//    chunks: 'all'
//  }
//  }

  // webpackTest.target = 'node'
  const compiler = webpack(webpackTest)

  compiler.run((err, stats) => {
  console.log('test file write at : '+filePath + '/' + fileName)
    clb(filePath + '/' + fileName,sourceMap)
  })
}
/**
 *
 * @callback Transformer~transformedCallback
 * @param {string} filePath
 */
