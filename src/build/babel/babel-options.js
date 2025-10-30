const path = require('path')

module.exports = {
  prod: {
    root: path.resolve(__dirname, '../../..'),
    presets: [
      [
        path.resolve(__dirname, '../../../node_modules/@babel/preset-env'),
        {
          targets: {
            'browsers': [
              'last 2 versions',
              'edge >= 18',
              'Safari >= 14',
              'not dead'
            ]
          },
          "bugfixes": true,
          useBuiltIns: 'usage',
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
