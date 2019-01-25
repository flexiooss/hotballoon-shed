const {defaults} = require('jest-config')
const path = require('path')

module.exports = {
  // modulePaths: [path.resolve(__dirname, '../../../node_modules')],
  rootDir:path.resolve(),
  roots: [path.resolve()],
  verbose: true,
  globals: {
    __ASSERT__: true,
    window: {}
  },
  transformIgnorePatterns: [],
  testEnvironment: 'jsdom',
  transform: {
    '^.+\\.jsx?$': 'babel-jest'
  }
}
