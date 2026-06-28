module.exports = {
  outputDir: process.cwd() + '/test-results',
  expect: {
    toHaveScreenshot: {animations: 'disabled', caret: 'hide', maxDiffPixelRatio: 0.01}
  },
}