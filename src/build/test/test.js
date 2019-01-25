'use strict'

const path = require('path')
const {spawn, exec} = require('child_process')
const utils = require('../../childProcessStdLog.js')
const callerPackage = require(path.resolve('package.json'))
const isVerbose = process.argv[2];

(function (callerPackage, path, spawn, exec, childProcessStdLog, isVerbose) {

  // if (!_hasPackageTestScriptEntry(callerPackage)) {
  //
  //   const myP = exec(
  //     'yarn why jest',
  //     [isVerbose], (error, stdout, stderr) => {
  //       if (error) {
  //         console.error(`yarn why jest : exec error: ${error}`)
  //         return
  //       }
  //       console.log(`yarn why jest : stdout: ${stdout}`)
  //     }
  //   ).on('close', (code, signal) => {
  //     if (code === 0 && signal === null) {
  //       console.log('Jest dependency is found: tests are run by default')
  //       childProcessStdLog(
  //         exec(
  //           'jest'
  //         ), isVerbose)
  //     }
  //   }).stderr.on('data', (data) => {
  //     console.error(`yarn why jest : stderr: ${data}`)
  //     myP.kill()
  //   })
  //
  // } else {
  //   console.log('Package scripts.test command run')
  //   childProcessStdLog(
  //     exec(
  //       'yarn test'
  //     ), isVerbose)
  // }

  /**
   *
   * @param packageCaller
   * @return {boolean}
   * @private
   */
  function _hasPackageTestScriptEntry(packageCaller) {
    return typeof callerPackage.scripts.test !== 'undefined'
  }

  // const myP = exec(
  //   'jest --config={"rootDir":"'+ path.resolve() +'"}',
  //   [isVerbose], (error, stdout, stderr) => {
  //     if (error) {
  //       console.error(`1 : exec error: ${error}`)
  //       return
  //     }
  //     console.log(`2 : stdout: ${stdout}`)
  //   }
  // ).on('close', (code, signal) => {
  //   if (code === 0 && signal === null) {
  //     console.log('3')
  //     // childProcessStdLog(
  //     //   exec(
  //     //     'jest'
  //     //   ), isVerbose)
  //   }
  // }).stderr.on('data', (data) => {
  //   console.error(`la : stderr: ${data}`)
  //   myP.kill()
  // })
  // exec(
  //   'yarn jest --clearCache')

  const myP = exec(
    'yarn jest-webpack --no-cache --config=' + path.resolve(__dirname, './jest-config.js'),
    [isVerbose], (error, stdout, stderr) => {
      if (error) {
        console.error(`1 : exec error: ${error}`)
        return
      }
      console.log(`2 : stdout: ${stdout}`)
    }
  ).on('close', (code, signal) => {
    if (code === 0 && signal === null) {
      console.log('3')
      // childProcessStdLog(
      //   exec(
      //     'jest'
      //   ), isVerbose)
    }
  }).stderr.on('data', (data) => {
    // console.error(`la : stderr: ${data}`)
    // myP.kill()
  })

  console.log(path.resolve())


}(callerPackage, path, spawn, exec, utils.childProcessStdLog, isVerbose))

