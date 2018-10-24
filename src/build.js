'use strict'
const {spawn, exec} = require('child_process')
const path = require('path');

(function (cmdArguments, exec, spawn, path) {

  const OPTIONS = (function constructOptions(cmdArguments) {
    const ret = {}
    cmdArguments.forEach(function (val, index, array) {
      if (val.startsWith('--')) {
        let option = val.split('=')
        ret[option[0].substr(2)] = (typeof option[1] === 'undefined') ? true : option[1]
      }
    })
    if (isVerbose(ret)) {
      console.log(ret)
    }
    return ret
  }(cmdArguments));

  (function controller(options) {
    if (typeof options.mk === 'undefined') {
      console.error('`--mk` argument should not be empty choose : production | development | test')
      process.exit(1)
    }

    const COMPILER = 'webpack4'

    switch (options.mk) {
      case 'production':
        _processConsoleOut(
          spawn(
            'node',
            [path.resolve(__dirname, './' + COMPILER + '/production.js'),
              isVerbose()]
          )
        )
        break
      case 'development':
        _processConsoleOut(
          spawn(
            'node',
            [path.resolve(__dirname, './' + COMPILER + '/server.js'),
              isVerbose()]
          )
        )
        break

      case 'test':
        exec('jest', _mkClb)
        break
    }
  }(OPTIONS))

  function _mkClb(error, stdout, stderr) {
    if (isVerbose()) {
      console.log(stdout)
      console.error(stderr)
    }
    if (error !== null) {
      console.error('exec error: ' + error)
    }
  }

  function _processConsoleOut(process) {
    if (isVerbose()) {
      process.stdout.on('data', (data) => {
        console.log(`${data}`)
      })
      process.stderr.on('data', (data) => {
        console.error(`${data}`)
      })
      process.on('close', (code) => {
        console.log(`child process exited with code ${code}`)
      })
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
