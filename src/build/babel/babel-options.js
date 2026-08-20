const path = require('path')

module.exports = {
  prod: {
    root: path.resolve(__dirname, '../../..'),
    presets: [
      [
        path.resolve(__dirname, '../../../node_modules/@babel/preset-env'),
        {
          targets: {
            'browsers': 'baseline widely available, last 2 Samsung versions, last 2 Opera versions, last 2 OperaMobile versions',
          },
          "bugfixes": true,
          useBuiltIns: 'entry',
          corejs: 3
        }
      ]
    ],
    sourceType: "unambiguous",
    compact: "auto",
    plugins:
      [
       path.resolve(__dirname, '../../../node_modules/@babel/plugin-transform-runtime')
    ]
  },
  test: {
    root: path.resolve(__dirname, '../../..'),
    presets: [
      [
        path.resolve(__dirname, '../../../node_modules/@babel/preset-env'),
        {
          targets: 'maintained node versions',
        }
      ]
    ],
    compact: false,
    plugins:
      []
  }
}
