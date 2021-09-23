const path = require('path')

module.exports = {
  prod: {
    root: path.resolve(__dirname, '../../..'),
    presets: [
      [
        path.resolve(__dirname, '../../../node_modules/@babel/preset-env'),
        {
          targets: 'defaults',
          useBuiltIns: 'entry',
          corejs: 3
        }
      ]
    ],
    compact: "auto",
    plugins:
      [
//    path.resolve(__dirname, '../../../node_modules/@babel/plugin-transform-named-capturing-groups-regex'),
//    path.resolve(__dirname, '../../../node_modules/@babel/plugin-syntax-dynamic-import'),
//    path.resolve(__dirname, '../../../node_modules/@babel/plugin-proposal-private-methods'),
//    path.resolve(__dirname, '../../../node_modules/@babel/plugin-proposal-class-properties')
//       [path.resolve(__dirname, '../../../node_modules/@babel/plugin-transform-runtime'),
//         {
//           corejs: 3,
//           regenerator:false
//         }
//       ]
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
