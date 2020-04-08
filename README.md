# hotballoon-shed
Test, Develop, Manage, Generate sources, Build Hotballoon applications

### Installation
https://github.com/flexiooss/hotballoon-shed-playbook

> before usage : ensure you have your settings with de right access for `codingmatters-realeases` repository


### Configuration
package.json
> For an application
```json
{
  "hotballoon-shed": {
    "build": {
      "builder": "webpack4",
      "entries": [
        "src/js/bootstrap.js"
      ],
      "html_template": "src/js/index.html",
      "output": "./dist"
    },
    "generate-sources": {
      "value-objects": {
        "extension": ".spec"
      }
    },
    "dev": {
      "entries": [
        "src/js/bootstrap.js"
      ]
    },
    "test": {
      "tester": "code-altimeter-js",
      "path": "src/test"
    }
  }
}
```
> For a package
```json
{
  "hotballoon-shed": {
    "build": {
      "builder": "webpack4"
    },
    "test": {
      "tester": "code-altimeter-js",
      "path": "src/test"
    },
    "generate-sources": {
      "value-objects": {
        "extension": ".spec"
      }
    }
  }
}
```
### Modules
Configuration example for this following folder structure
```
pakage-a
|- package-b
|- package-c
   |-package-d
``` 
> package-a
```json
{
    "name": "package-a",
    "devDependencies": {
      "dependency-a": "latest"
    },
    "dependencies": {
      "dependency-b": "latest"
    },
    "hotballoon-shed": {
        "modules": [
        "package-b",
        "package-c"
        ]
      }
}
```
> package-c
```json
{
    "name": "package-c",
    "hotballoon-shed": {
        "module" : {
            "parent": {
              "name" : "package-a"        
            },
            "devDependencies": ["dependency-a"],
            "dependencies": ["dependency-b"]
        },
        "modules": ["package-d"]
      }
}
```

### dev server config
Choose your server config option with
```bash
hbshed dev server-config stack
hbshed dev server-config local
```
or set a configuration used with 
```bash
hbshed dev 
```

```json
{
  "hotballoon-shed": {
    "dev": {
      "server": {
        "host": "172.17.0.1",
        "disableHostCheck": true,
        "publicPath": "/",
        "public": "https://dev.flexio.io/devui",
        "sockPath": "/socketjs",
        "proxy": [
          {
            "context": [
              "//[a-z]+/*"
            ],
            "logLevel": "debug",
            "target": "https://dev.flexio.io/devui",
            "secure": false,
            "pathRewrite": {
              "^//[a-z]+/*": "/"
            }
          }
        ]
      }
    }
  }
}
```
### Usage
```bash
hbshed --help
```
