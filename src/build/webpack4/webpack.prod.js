'use strict'

const path = require('path')
const webpack = require('webpack')
const UglifyJsPlugin = require('uglifyjs-webpack-plugin')
const CleanWebpackPlugin = require('clean-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const LinkStylesheetHtmlWebpackPlugin = require('link-stylesheet-html-webpack-plugin')
const WebpackPwaManifest = require('webpack-pwa-manifest')

const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin')
const Terser = require('terser')
const SriPlugin = require('webpack-subresource-integrity')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const WorkboxPlugin = require('workbox-webpack-plugin');

const babelOptions = require('../babel/getBabelConfig')
const webpackBase = require('./webpack.base')
const CONFIG = require('./config')

const isVerbose = process.argv[2] === '-v'
const entries = process.argv[3].split(',')
const html_template = process.argv[4]
const dist_path = process.argv[5]

const manifestConfig = process.argv[6]
const parsedManifestConfig = JSON.parse(manifestConfig)

webpackBase.entry.app = entries

webpackBase.mode = 'production'
webpackBase.devtool = false
webpackBase.output.crossOriginLoading = 'anonymous'
webpackBase.output.path = dist_path
//webpackBase.output.publicPath = '/'

if (isVerbose) {
  console.log('_________________ MANIFEST _________________')
  console.log(parsedManifestConfig)
}

webpackBase.optimization = {
  splitChunks: {
    chunks: 'all',
    cacheGroups: {
      flexioClient: {
        test: /[\\/]node_modules[\\/]@flexio-corp[\\/].*-client[\\/]/,
        name: 'api-client',
        chunks: 'all',
        reuseExistingChunk: true,
      },
      flexio: {
        test: /[\\/]node_modules[\\/](@flexio-corp|@flexio-oss)[\\/]/,
        name: 'corp',
        chunks: 'all',
        reuseExistingChunk: true,
      },
      styles: {
        name: 'styles',
//          type: 'css/mini-extract',
        // For webpack@4
        test: /\.css$/,
        chunks: 'all',
        enforce: true
      }
    }
  },
  minimizer: [
    new UglifyJsPlugin({
      uglifyOptions: {
        output: {
          comments: false,
//      TODO: check this for tinymce
          "ascii_only": true
        }
      },
      sourceMap: true,
      minify(file, sourceMap) {
        const uglifyJsOptions = {
          output: {
            comments: false,
            //      TODO: check this for tinymce
            "ascii_only": true
          }
        }

        if (sourceMap) {
          uglifyJsOptions.sourceMap = {
            content: sourceMap
          }
        }

        return Terser.minify(file, uglifyJsOptions)
      }
    }),
    new OptimizeCSSAssetsPlugin({
      cssProcessorPluginOptions: {
        preset: ['default', {discardComments: {removeAll: true}}]
      }
    })
  ]
}

webpackBase.plugins.push(
  new CleanWebpackPlugin([dist_path + '/*'], {
    root: path.resolve(),
    verbose: true,
    watch: true
  }),
  new webpack.DefinePlugin({
    'window.__DEVELOPMENT__': JSON.stringify(false)
  }),
  new WebpackPwaManifest({
    filename: "manifest.json",
    inject: true,
    fingerprints: true,
    ios: false,
    publicPath: null,
    includeDirectory: true,
    name: parsedManifestConfig.name,
    short_name: parsedManifestConfig.short_name,
    description: parsedManifestConfig.description,
    crossorigin: parsedManifestConfig.crossorigin,
    display: parsedManifestConfig.display,
    theme_color: parsedManifestConfig.theme_color,
    background_color: parsedManifestConfig.background_color,
    orientation: parsedManifestConfig.orientation,
    start_url: parsedManifestConfig.start_url,
    icons: [
      {
        src: path.resolve(__dirname, './assets/icon.png'),
        sizes: [96, 128, 192, 256, 384, 512, 1024]
      }
    ]
  }),
  new HtmlWebpackPlugin(
    {
      filename: 'index.html',
      template: html_template,
      inject: true,
      scriptLoading: 'defer',
      meta: {
        viewport: 'width=device-width, initial-scale=1, shrink-to-fit=no',
        charset: "utf-8"
      },
      favicon: path.resolve(__dirname, './assets/favicon.ico')
    }
  ),
  new MiniCssExtractPlugin({
    filename: '[name].[hash].css',
    chunkFilename: '[id].[hash].css',
  }),
  new SriPlugin({
    hashFuncNames: ['sha256', 'sha384']
  }),
  new WorkboxPlugin.GenerateSW()
// new LinkStylesheetHtmlWebpackPlugin()
)

webpackBase.module.rules.push(
{
        test: /\.js$/,
        loader: 'babel-loader',
        options: babelOptions
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
          localIdentName: '[sha1:hash:hex:4]',
          sourceMap: false,
          camelCase: true
        }
      },
//      {
//        loader: 'css-media-queries-loader',
//        options: CONFIG.mediaqueries
//      }
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
//      {
//        loader: 'css-media-queries-loader',
//        options: CONFIG.mediaqueries
//      }
    ]
  }
)

module.exports = webpackBase
