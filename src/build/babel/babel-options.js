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
              'Safari >= 12',
              'not dead'
            ]
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
//      path.resolve(__dirname, '../../../node_modules/@babel/plugin-transform-unicode-regex')
//    path.resolve(__dirname, '../../../node_modules/@babel/plugin-transform-named-capturing-groups-regex'),
//    path.resolve(__dirname, '../../../node_modules/@babel/plugin-syntax-dynamic-import'),
//    path.resolve(__dirname, '../../../node_modules/@babel/plugin-proposal-private-methods'),
//    path.resolve(__dirname, '../../../node_modules/@babel/plugin-proposal-class-properties')
       [path.resolve(__dirname, '../../../node_modules/@babel/plugin-transform-runtime')
//       ,
//         {
//           corejs: 3,
//         }
       ]
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
