// Resolve @playwright/test from the project under test (cwd), NOT this toolchain's own
// node_modules. The runner (`npx playwright`, launched from the project) and the spec files
// (realpath'd back into the project tree) both load the project's copy first; loading a second
// physical copy here makes playwright/lib/index.js throw "Requiring @playwright/test second time".
const {defineConfig} = require(require.resolve('@playwright/test', {paths: [process.cwd()]}))

// console.log(process.env)
// console.log(process.argv)
// console.log(process.cwd())

const VERBOSE = process.env.E2E_VERBOSE === '1'

const TRANSPORT = process.env.E2E_TRANSPORT
if (!TRANSPORT) throw new Error('E2E_TRANSPORT is not set')
const DEV = TRANSPORT === 'dev'

// const TARGETS = JSON.parse(getArgv(2))
// const target = TARGETS.find(t => t.name === process.env.E2E_TARGET)
// if (DEV && !target) throw new Error('E2E_TRANSPORT=dev requires E2E_TARGET=<name>')

const configBuilder = DEV ? require('./dev.config') : require('./static.config')
const config = configBuilder({
  DEV,
})

if (VERBOSE) {
  console.log('**** BASE CONFIG ****')
  console.log(config)
}

let definedConfig = defineConfig(config)
module.exports = definedConfig

