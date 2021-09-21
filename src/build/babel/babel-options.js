'use strict'

const path = require('path')

module.exports = {
  root: path.resolve(__dirname, '../../..'),
  presets: [
    [
      path.resolve(__dirname, '../../../node_modules/@babel/preset-env'),
      {
        targets: '> 0.5%, last 3 versions, Firefox ESR, not dead',
        // compact: false
      }
    ]
  ],
  compact: false,
  plugins:
    [
//    path.resolve(__dirname, '../../../node_modules/@babel/plugin-transform-named-capturing-groups-regex'),
//    path.resolve(__dirname, '../../../node_modules/@babel/plugin-syntax-dynamic-import'),
//    path.resolve(__dirname, '../../../node_modules/@babel/plugin-proposal-private-methods'),
//    path.resolve(__dirname, '../../../node_modules/@babel/plugin-proposal-class-properties')
  ]
}
