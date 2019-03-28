'use strict'

const path = require('path')

module.exports = {
  root: path.resolve(__dirname, '../../..'),
  presets: [
    [
      path.resolve(__dirname, '../../../node_modules/@babel/preset-env'),
      {
        targets: {
          'browsers': [
            'edge >= 13'
          ]
        }
      }
    ]
  ],
  plugins:
    [path.resolve(__dirname, '../../../node_modules/babel-plugin-transform-modern-regexp')]
}
