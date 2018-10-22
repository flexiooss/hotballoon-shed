'use strict'

const CONFIG = require('./config')
const HtmlWebpackPlugin = require('html-webpack-plugin')

module.exports = {
  entry: CONFIG.entry,
  output: {
    path: CONFIG.dist_path,
    filename: '[name].js'
  },
  plugins: [
    new HtmlWebpackPlugin(
      {
        filename: 'index.html',
        template: CONFIG.template_html,
        inject: true
      }
    )
  ],
  module: {
    rules: [
      {
        test: /\.js$/,
        // exclude: [/node_modules/, /libs/],
        loader: 'babel-loader'
      },
      {
        test: /\.worker\.js$/,
        loader: 'worker-loader',
        options: {
          name: '[name].[hash].js'
        }
      },
      {
        test: /\.(png|jpe?g|gif|svg|woff2?|eot|ttf|otf|wav)(\?.*)?$/,
        use: [{
          loader: 'url-loader',
          query: {
            limit: 10
          }
        }]

      }
    ]
  }
}
