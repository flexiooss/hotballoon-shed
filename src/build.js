'use strict'
const {spawn, exec} = require('child_process')
const path = require('path');

(function(cmdArguments, exec, spawn, path) {
  const OPTIONS = (function constructOptions(cmdArguments) {
    const ret = {}
    cmdArguments.forEach(function(val, index, array) {
      if (val.startsWith('--')) {
        let option = val.split('=')
        ret[option[0].substr(2)] = option[1]
      }
    })
    if (isVerbose(ret)) {
      console.log(ret)
    }
    return ret
  }(cmdArguments))

  if (typeof OPTIONS.mk === 'undefined') {
    console.error('--mk option should not be empty : production | development | test')
    process.exit(1)
  }

  switch (OPTIONS.mk) {
    case 'production':
      exec('webpack --config ' + path.resolve(__dirname, './webpack.prod.js'), _mkClb)
      break
    case 'development':
      const pr = spawn('node', [path.resolve(__dirname, './server.js')])

      if (isVerbose()) {
        pr.stdout.on('data', (data) => {
          console.log(`stdout: ${data}`)
        })

        pr.stderr.on('data', (data) => {
          console.log(`stderr: ${data}`)
        })

        pr.on('close', (code) => {
          console.log(`child process exited with code ${code}`)
        })
      }
      break

    case 'test':
      console.log(path.resolve())
      exec('jest', _mkClb)
      break
  }

  function _mkClb(error, stdout, stderr) {
    if (isVerbose()) {
      console.log('stdout: ' + stdout)
      console.log('stderr: ' + stderr)
    }
    if (error !== null) {
      console.log('exec error: ' + error)
    }
  }

  /**
   *
   * @return {boolean}
   */
  function isVerbose(options = OPTIONS) {
    return typeof options.verbose !== 'undefined' && !!options.verbose
  }
}(process.argv, exec, spawn, path))
