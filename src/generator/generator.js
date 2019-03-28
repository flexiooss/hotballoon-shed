const utils = require('../childProcessStdLog.js')
const {spawn, exec} = require('child_process')
const path = require('path')
console.log('ici')
console.log(process.argv)
console.log(path.resolve(__dirname, '../..'))
const root = (process.argv.filter((v) => RegExp('^root=.*').test(v)))[0].replace('root=', '')
const rootPackage = require(root + '/package.json')
console.log(rootPackage.name)

utils.childProcessStdLog(
  spawn(
    'npm',
    ['explore', 'value-object-generator', '--', 'npm', 'run-script', 'run', 'yaml_spec_file_path=' + root + '/src/js', 'target_directory=' + root + '/generated', 'root_package=' + 'io.flexio.' + rootPackage.name.replace('-', '')],
    {
      cwd: path.resolve(__dirname, '../..'),
      env: process.env
    }
  ),
  true
)
// npm explore value-object-generator -- npm test --scripts-prepend-node-path
