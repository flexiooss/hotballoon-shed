const staticConfig = require('./static.config.js')

module.exports = {
  ...staticConfig,
  outputDir: '/test-results/playwright',
}
