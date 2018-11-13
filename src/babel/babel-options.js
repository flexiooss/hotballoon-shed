'use strict'

const path = require('path')

module.exports = {
  presets: [
    [
      // path.resolve(__dirname, '../../node_modules/@babel/preset-env'),
      'preset-env',
      {
        targets: {
          'browsers': [
            'edge >= 13'
          ]
        }
      }
    ]
  ]
}
