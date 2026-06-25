const commonConfig = require('./built-commons.config')

module.exports = {
  ...commonConfig,
  outputDir: '/test-results/playwright/results',
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
