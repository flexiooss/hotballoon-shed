'use strict'

const path = require('path')

module.exports = {
  root: path.resolve(),
  presets: [
    [
      // path.resolve(__dirname, '../../node_modules/@babel/preset-env'),
      '@babel/preset-env',
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
    ['transform-modern-regexp']
}
