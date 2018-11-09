'use strict'
const utils = require('./childProcessStdLog.js')
const {spawn, exec} = require('child_process')
const path = require('path');

(function (cmdArguments, exec, spawn, path, _childProcessStdLog) {

  const OPTIONS = {
    operation: {
      alias: 'op',
      values: ['production', 'development']
    },
    help: {
      alias: 'h'
    },
    verbose: {
      alias: 'v'
    },
    compiler: {
      alias: 'comp',
      values: ['webpack4']
    },
    test: {
      alias: 't'
    }
  }

  const CMD_CONTEXT = _buildContextCmd(cmdArguments);

  (function controller(cmdContext) {
    _showHelp(cmdContext)
    if (hasTestOption(cmdContext)) {
      _execTest(cmdContext, _execOperation, cmdContext).on('close', (code) => {
        if (code === 0) {
          _execOperation(cmdContext).on('close', (code) => {
            if (code === 0) {
              process.exit(0)
            }
          })
        }
      })
    } else {
      _execOperation(cmdContext)
    }
  }(CMD_CONTEXT))


  /**
   *
   * @param cmdContext
   * @return {boolean}
   */
  function isVerbose(cmdContext = CMD_CONTEXT) {
    return typeof cmdContext.verbose !== 'undefined' && !!cmdContext.verbose
  }

  /**
   *
   * @param cmdContext
   * @return {boolean}
   */
  function hasTestOption(cmdContext = CMD_CONTEXT) {
    return typeof cmdContext.test !== 'undefined' && !!cmdContext.test
  }

  /**
   *
   * @param {Array} cmdArguments : process.argv
   * @return {Object}
   */
  function _buildContextCmd(cmdArguments) {
    const ret = {}
    cmdArguments.forEach(function (val, index, array) {
      if (val.startsWith('--')) {
        let option = val.split('=')
        const OPTION_KEY = option[0].substr(2)
        _addOption(ret, OPTION_KEY, option[1])
      } else if (val.startsWith('-')) {
        let option = val.split('=')
        const OPTION_KEY = _getOptionKeyByAlias(option[0].substr(1))
        _addOption(ret, OPTION_KEY, option[1])
      }
    })
    if (isVerbose(ret)) {
      console.log(ret)
    }
    return ret
  }

  /**
   *
   * @param {Object} options
   * @param {string} key
   * @param {string|boolean} value
   * @private
   */
  function _addOption(options, key, value = true) {
    if (typeof  OPTIONS[key] !== 'undefined') {
      const VAL = _setOptionValue(key, value)
      if (VAL !== null) {
        options[key] = VAL
      }
    }
  }

  /**
   *
   * @param {string} key
   * @param {string|boolean} val
   * @return {string|null}
   * @private
   */
  function _setOptionValue(key, val) {
    if (typeof OPTIONS[key].values === 'undefined' || OPTIONS[key].values.includes(val)) {
      return val
    }
    return null
  }

  /**
   *
   * @param {string} alias
   * @return {*}
   * @private
   */
  function _getOptionKeyByAlias(alias) {
    for (const key in OPTIONS) {
      if (typeof OPTIONS[key].alias !== 'undefined' && OPTIONS[key].alias === alias) {
        return key
      }
    }
    return null
  }

  /**
   *
   * @param {Object} cmdContext
   * @private
   */
  function _showHelp(cmdContext = CMD_CONTEXT) {
    if (cmdContext.help !== 'undefined' && !!cmdContext.help) {
      console.info('########################################')
      console.info('HOTBALLOON SHELD  -  HELP')
      console.info('########################################')
      for (const key in OPTIONS) {
        const OPTION = OPTIONS[key]
        console.info('')
        console.info(`--${key} ${(typeof OPTION.alias !== 'undefined') ? ' | -' + OPTION.alias : ''}`)
        if (typeof OPTION.values !== 'undefined') {
          console.info(`## Available values : ${OPTION.values.join(' | ')}`)
        }
      }
      console.info('########################################')
      process.exit(0)
    }
  }

  /**
   *
   * @param {Object} cmdContext
   * @private
   */
  function _execOperation(cmdContext = CMD_CONTEXT) {
    if (typeof cmdContext.operation === 'undefined') {
      console.error('`--operation` argument should not be empty choose : ' + OPTIONS.operation.values.join(' | '))
      process.exit(1)
    }

    const COMPILER = cmdContext.compiler || 'webpack4'


    switch (cmdContext.operation) {
      case 'production':
        return _childProcessStdLog(
          spawn(
            'node',
            [path.resolve(__dirname, './' + COMPILER + '/production.js'),
              isVerbose()]
          ),
          isVerbose()
        )
      case 'development':
        return _childProcessStdLog(
          spawn(
            'node',
            [path.resolve(__dirname, './' + COMPILER + '/server.js'),
              isVerbose()]
          ),
          isVerbose()
        )
    }
  }

  function _execTest() {

    return _childProcessStdLog(
      spawn(
        'node',
        [path.resolve(__dirname, './test/test.js'),
          isVerbose()]
      ),
      isVerbose()
    )

  }
}(process.argv, exec, spawn, path, utils.childProcessStdLog))
