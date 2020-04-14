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

> The main purpose of this module manager is only to ensure the consistency of the versions of the project packages without breaking the npm philosophy. 

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
    "version": "1.0.0",
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

It is possible to declare an external parent with an optional version
```json
{
    "name": "package-a",
    "version": "1.0.0",
    "devDependencies": {
      "dependency-a": "latest"
    },
    "dependencies": {
      "dependency-b": "latest"
    },
    "hotballoon-shed": {
        "module": {
            "name": "my-external-parent",
            "version": "0.0.0",
            "external": true
        },
        "modules": [
        "package-b",
        "package-c"
        ]
      }
}
```
It is possible to declare an external parent with dependencies
```json
{
    "name": "package-a",
    "version": "1.0.0",
    "devDependencies": {
      "dependency-a": "latest"
    },
    "dependencies": {
      "dependency-b": "latest"
    },
    "hotballoon-shed": {
        "module": {
            "name": "my-external-parent",
            "version": "0.0.0",
            "external": true,
            "dependencies": ["my-external-dep"]
        },
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

It is possible to declare parent version with :
```json
{
    "name": "package-c",
    "hotballoon-shed": {
        "module" : {
            "parent": {
              "name" : "package-a",
              "version": "1.0.0"        
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
