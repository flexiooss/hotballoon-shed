module.exports = {
  reporter: [
    ['list'],
    ['html', {open: 'never'}]
  ],
  expect: {
    toHaveScreenshot: {animations: 'disabled', caret: 'hide', maxDiffPixelRatio: 0.01}
  },
}