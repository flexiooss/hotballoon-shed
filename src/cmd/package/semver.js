const semver = require('semver')
const v1 = process.argv[2]
const v2 = process.argv[3]

console.log(semver.satisfies(v1,v2))