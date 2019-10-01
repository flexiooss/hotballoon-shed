# hotballoon-shed
Test, Develop, Manage, Generate sources, Build Hotballoon applications

### Installation
https://github.com/flexiooss/hotballoon-shed-playbook

| before usage : ensure you have your settings with de right access for `codingmatters-realeases` repository


### Configuration
package.json
```json
{
"hotballoon-shed": {
    "build": {
      "builder": "webpack4",
      "entries": [
        "polyfill/for/crazy-browser.js",
        "src/main/js/bootstrap.js"
      ],
      "html_template": "src/main/js/index.html",
      "ouput": "dist"
    },
    "dev": {
        "entries": [
            "src/main/js/devBootstrap.js"
          ],
        "server": {
            "host": "172.17.0.1",
            "disableHostCheck": true,
            "publicPath": "/",
            "public": "https://dev.flexio.io/devui",
            "sockPath": "/socketjs"
        }
    },
    "test": {
      "tester": "code-altimeter-js",
      "path": "src/test"
    },
    "modules": {
      "component-name": "src/main/js/modules/component-name",
      "component-other": "src/main/js/modules/component-other"
    },
    "generate-sources": {
      "value-objects": {
        "extension": ".spec"
      }
    }
  }
}
```

### Usage
```bash
hbshed
              <...task> <...option>
              
              <options>
              --help, -H
              --verbose, -V


              <tasks>
              self-install          Install dependencies & generator
              self-update           Not implemented yet !!!
              
              set-flexio-registry   Set all flexio private registry

              clean                 Remove dependencies & generate sources 
              install               Install dependencies
              generate-sources      Generate value objects...
              cig                   alias for clean install generate-sources

              dev                   Build a dev server       
              build                 Build code

              test                  Test
```