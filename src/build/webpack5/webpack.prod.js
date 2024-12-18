'use strict'

const path = require('path')
const webpack = require('webpack')

const {WebpackManifestPlugin} = require('webpack-manifest-plugin')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const HtmlMinimizerPlugin = require("html-minimizer-webpack-plugin");
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
const TerserPlugin = require("terser-webpack-plugin");

const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin')

const babelOptions = require('../babel/getBabelConfig')
const webpackBase = require('./webpack.base')
const CONFIG = require('./config')

const isVerbose = process.argv[2] === '-v'
const entries = JSON.parse(process.argv[3])
const html_template = process.argv[4]
const dist_path = process.argv[5]
/**
 * @type {boolean}
 */
const inspect = process.argv[6] === '1'
webpackBase.entry = entries
webpackBase.mode = 'production'
webpackBase.devtool = false
webpackBase.output.crossOriginLoading = 'anonymous'
webpackBase.output.path = dist_path
webpackBase.output.clean = true
webpackBase.stats = {errorDetails: true}
// webpackBase.target = 'browserslist: > 0.5%, last 3 versions, Firefox ESR, not dead'
webpackBase.target = 'web'

webpackBase.optimization = {
  minimize: true,
    runtimeChunk: {
      name: (entrypoint) => {
        if (entrypoint.name.startsWith("boot")) {
          return null;
        }
        if (entrypoint.name === "service-worker") {
          return null;
        }

        return `runtime-${entrypoint.name}`
      }
    },
  splitChunks: {
    chunks(chunk) {
        return chunk.name !== "boot" && chunk.name !== "service-worker";
    },
    maxSize: 5000000,
    cacheGroups: {
      apiClient: {
        test: /\/node_modules\/@flexio-corp\/.*-client/,
        name: 'api-client',
        reuseExistingChunk: true,
        priority: 1
      },
      oss: {
        test: /[\\/]node_modules[\\/]@flexio-oss/,
        name: 'oss',
        reuseExistingChunk: true,
      },
      corp: {
        test: /[\\/]node_modules[\\/]@flexio-corp/,
        name: 'corp',
        reuseExistingChunk: true,
      },
      eui: {
        test: /[\\/]node_modules[\\/]@flexio-corp[\\/]component-standard-entity-bundle/,
        name: 'eui',
        reuseExistingChunk: true,
        priority: 1
      },
      tinymce: {
        test: /[\\/]node_modules[\\/]tinymce/,
        name: 'tinymce',
      },
      styles: {
        name: 'styles',
        type: 'css/mini-extract',
        test: /\.css$/,
        enforce: true
      }
    }
  },
  minimizer: [
    `...`,
    new CssMinimizerPlugin(),
    new HtmlMinimizerPlugin()
  ]
}

webpackBase.plugins.push(
  new webpack.DefinePlugin({
    '__DEVELOPMENT__': JSON.stringify(false),
     '__ASSERT__': JSON.stringify(false),
    '__DEBUG__': JSON.stringify(false)
  }),
  new MiniCssExtractPlugin({
    filename: "[name].[contenthash].css",
    chunkFilename: "[id].[contenthash].css",
    linkType: false,
    attributes: {
      rel: "preload",
      as: "style",
      onLoad: "this.onload=null;this.rel='stylesheet'"
    }
  }),
  new HtmlWebpackPlugin(
    {
      filename: 'index.html',
      template: html_template,
      inject: 'body',
      scriptLoading: 'defer',
      meta: {
        viewport: 'width=device-width, initial-scale=1, shrink-to-fit=no',
        charset: 'utf-8'
      },
      favicon: path.resolve(__dirname, '../html/assets/favicon-32.png'),
      excludeChunks:['service-worker']
    }
  ),
  new WebpackManifestPlugin({fileName: 'files-manifest.json'}),
)

if (inspect) {
  webpackBase.plugins.push(
    new BundleAnalyzerPlugin()
  )
}

webpackBase.module.rules.push(
  {
    test: /\.(png|jpe?g|gif|svg|woff2?|eot|ttf|otf|wav)(\?.*)?$/,
    type: 'asset/resource'
  },
  {
    test: /\.js$/,
    loader: 'babel-loader',
    options: babelOptions.prod
  },
    {
    test: /\/[\d\w_-]+\.txt\.css$/,
    loader: 'css-loader',
        options: {
          modules: false,
          exportType: 'string',
          importLoaders: 1,
          sourceMap:false
        }
  },
  {
    test: /\.module\.css$/,
    use: [
      MiniCssExtractPlugin.loader,
      {
        loader: 'css-loader',
        options: {
          modules: true,
          importLoaders: 1,
          sourceMap: false,
        }
      }
    ]
  },
  {
    test: /\/[\d\w_-]+\.css$/,
    use: [
      MiniCssExtractPlugin.loader,
      {
        loader: 'css-loader',
        options: {
          modules: false
        }
      },
    ]
  }
)

module.exports = webpackBase
