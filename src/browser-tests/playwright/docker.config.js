const staticConfig = require('./static.config.js')

module.exports = {
  ...staticConfig,
  outputDir: '/test-results/playwright',
  reporter: [
    ['list'],
    [
      'html',
      {
        open: 'never',
        outputFolder: '/test-results/playwright/html',
      }
    ]
  ],
}
