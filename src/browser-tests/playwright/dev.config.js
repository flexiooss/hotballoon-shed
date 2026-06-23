const baseConfig = require('./base.config.js')

const testDir = process.env.E2E_TEST_DIR
if (!testDir) throw new Error('E2E_TEST_DIR is not set')

module.exports = function (config) {
  return {
    ...baseConfig,
    testDir,
    use: {
      baseURL: 'https://localhost:8080',
      ignoreHTTPSErrors: config.DEV,
      trace: 'on-first-retry',
    },
    webServer: {
      command: `hbshed dev --entry ${testDir}/browser-fixture.js --server-config local --port 8080`,
      cwd: process.cwd(),
      url: 'https://localhost:8080',
      ignoreHTTPSErrors: true,
      reuseExistingServer: true,
      timeout: 120_000,
      wait: /successfully/,
      stdout: 'pipe',
      stderr: 'pipe',
    }
  }
}