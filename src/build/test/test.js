'use strict'

const path = require('path')
const {exec} = require('child_process')
const verbose = process.argv[2] === 'true'
const testTransformer = require('./transformer')
const TEST_ID = Date.now()
const CodeAltimeter = require('code-altimeter-js')

CodeAltimeter.testsPath(path.resolve(), (testsPath) => {
  if (verbose) {
    console.log('Find tests entries :')
    console.log(testsPath)
  }
  testsPath.unshift(CodeAltimeter.pathForExecutionContext)
  testTransformer(
    TEST_ID,
    testsPath,
    {
      'process.env.TEST_VERBOSE': JSON.stringify((verbose) ? 1 : 0)
    },
    (filePath) => {
      exec(
        'node ' + filePath,
        {
          cwd: path.resolve(),
          env: process.env
        },
        (error, stdout, stderr) => {
          console.log(stdout)
          console.log(stderr)
          if (error) {
            process.exit(error.code)
          }
        }
      )
    })
})
