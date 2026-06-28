// Resolve @playwright/test from the project under test (cwd), NOT this toolchain's own
// node_modules. The runner (`npx playwright`, launched from the project) and the spec files
// (realpath'd back into the project tree) both load the project's copy first; loading a second
// physical copy here makes playwright/lib/index.js throw "Requiring @playwright/test second time".
const {defineConfig} = require(require.resolve('@playwright/test', {paths: [process.cwd()]}))

const VERBOSE = process.env.E2E_VERBOSE === '1'

const TRANSPORT = process.env.E2E_TRANSPORT
if (!TRANSPORT) throw new Error('E2E_TRANSPORT is not set')
const config = require(`./${TRANSPORT}.config.js`)

if (VERBOSE) {
  console.log('**** CWD: ' + process.cwd())
  console.log('**** ENV ****')
  console.log(process.env)
  console.log('**** BASE CONFIG ****')
  console.log(config)
}

let definedConfig = defineConfig(config)
module.exports = definedConfig

