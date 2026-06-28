const commonConfig = require('./built-commons.config')

module.exports = {
  ...commonConfig,
  outputDir: '/test-results/playwright/results',
  reporter: [
    ['dot'],
    [
      'html',
      {
        open: 'never',
        outputFolder: '/test-results/playwright/html',
      }
    ]
  ],
}
