'use strict'
/* global require */

const path = require('path')
const {spawn} = require('child_process')
const argTestPath = process.argv[2]
const verbose = process.argv[3] === '-v'
const restrict = process.argv[4]
const source_map = process.argv[5] === '1'
const builder = process.argv[6]
const testTransformer = require('./transformer')
const TEST_ID = Date.now() + ''
const CodeAltimeter = require('@flexio-oss/code-altimeter-js')

CodeAltimeter.testsPath(argTestPath, (testsPath) => {
  if (restrict) {
    console.log('\x1b[46m%s\x1b[0m', ' Restrict :' + restrict)
    testsPath = testsPath.filter((name) => {
      const re = new RegExp('.*\/' + restrict + '.*')
      return re.test(name)
    })
  }

  if (verbose) {
    console.log('\x1b[46m%s\x1b[0m', ' Find tests entries :')
    console.log(testsPath)
  }

  testsPath.unshift(CodeAltimeter.entries.before)
  testsPath.push(CodeAltimeter.entries.after)

  testTransformer(
    TEST_ID,
    testsPath,
    {
      'process.env.TEST_VERBOSE': JSON.stringify((verbose) ? 1 : 0)
    },
    (filePath, sourceMap) => {
      const args = ['--stack-trace-limit=100000','--unhandled-rejections=strict']
      if (sourceMap) {
        args.push('--enable-source-maps')
      }
      args.push(filePath)
      const p = spawn('node',
        args,
        {
          cwd: path.resolve(),
          env: process.env,
          stdio: [process.stdin, process.stdout, process.stderr]
        }
      )


      p.on('close', (code) => {
        console.log(`Test child process exited with code ${code}`)
        process.exit(code)
      })
    },
    source_map,
    builder
  )
})
