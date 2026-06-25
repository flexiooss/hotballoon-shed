const commonConfig = require('./built-commons.config')

module.exports = {
  ...commonConfig,
  grepInvert: /@visual/,
  reporter: [
    ['list'],
    [
      'html',
      {
        open: 'never',
        outputFolder: process.cwd() + '/playwright-report',
      }
    ]
  ],
}
