/**
 *
 * @param {child_process} currentProcess
 * @param {boolean} verbose
 * @return {child_process} currentProcess
 */
exports.childProcessStdLog = function (currentProcess, verbose = false) {
  if (verbose) {
    currentProcess.stdout.on('data', (data) => {
      console.log(`${data}`)
    })
    currentProcess.stderr.on('data', (data) => {
      console.error(`${currentProcess.pid} : ${data}`)
    })
    currentProcess.on('close', (code) => {
      if (code > 0) {
        console.error(`child process ${currentProcess.pid} exited with code ${code}`)
        process.exit(code)
      } else {
        console.log(`child process ${currentProcess.pid} exited with code ${code}`)
      }

    })
  } else {
    currentProcess.on('close', (code) => {
      if (code > 0) {
        process.exit(code)
      }
    })
  }
  return currentProcess
}
