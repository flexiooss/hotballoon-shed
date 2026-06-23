const staticConfig = require('./static.config.js')

module.exports = {
  ...staticConfig,
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
