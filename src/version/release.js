
/**
 * @description script for upgrade package version
 * option
 * < patch|minor|major >
 */

// const path = require('path')
// const currentPackage = require(path.resolve(__dirname, '../package.json'))
const exec = require('child_process').exec
// const assert = require('assert')

const CONSOLE_COLORS = {
  red: '\x1b[31m',
  green: '\x1b[32m'
}

const VERSIONS = {
  patch: 'patch',
  minor: 'minor',
  major: 'major'
}

const VERSION = process.argv[2]

if (VERSION in VERSIONS) {
  exec(`yarn version --new-version ${VERSION}`)
  console.info(CONSOLE_COLORS.green, `package '${VERSION}ed' !!!`)
  // console.info(CONSOLE_COLORS.green, `package '${VERSION}ed' to ${currentPackage.version} !!!`)
} else {
  console.error(CONSOLE_COLORS.red, `'${VERSION}' first argument should be : version < patch|minor|major >`)
}
