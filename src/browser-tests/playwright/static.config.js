// Pin @playwright/test to the project's copy (cwd), see note in playwright.config.js — avoids
// the "Requiring @playwright/test second time" guard when this config lives outside the project.
const {devices} = require(require.resolve('@playwright/test', {paths: [process.cwd()]}))
const fs = require('fs')
const path = require('path')
const baseConfig = require('./base.config.js')

const PORT = 8100

const browsers = [
  {name: 'chromium', use: {...devices['Desktop Chrome']}},
  {name: 'firefox', use: {...devices['Desktop Firefox']}},
]

module.exports = {
  const runDir = process.env.E2E_RUN_DIR
  if(
!runDir
)
throw new Error('E2E_RUN_DIR is not set')

const testsRoot = path.join(runDir, 'tests')
const distRoot = path.join(runDir, 'dist')

// Each entry is a symlink (package name -> <module>/src/test-playwright).
// Do NOT filter by Dirent.isDirectory(): readdir reports symlinks as symlinks, not dirs.
// Playwright follows the symlink via statSync when it is a project's testDir.
const modules = fs.readdirSync(testsRoot)

const projects = modules.flatMap(name => {
  const distPath = path.join(distRoot, name)
  if (!fs.existsSync(distPath) || !fs.statSync(distPath).isDirectory()) {
    throw new Error(`No matching dist directory for test module "${name}": ${distPath}`)
  }
  return browsers.map(browser => ({
    ...browser,
    name: `${browser.name}:${name}`,
    testDir: path.join(testsRoot, name),            // the symlink; statSync follows it
    use: {
      ...browser.use,
      baseURL: `http://localhost:${PORT}/${name}/`, // this module's built fixture
    },
  }))
})

return {
  ...baseConfig,
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: !!process.env.CI ? 2 : 0,
  projects,
  use: {
    ignoreHTTPSErrors: false,
    trace: 'on-first-retry',
  },
  webServer: {
    command: `npx http-server ${distRoot} -p ${PORT} -s`,
    url: `http://localhost:${PORT}`,
    reuseExistingServer: !process.env.CI,
    timeout: 30_000,
  },
}
