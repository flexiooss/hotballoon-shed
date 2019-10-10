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
     "browserTest": {
      "path": "src/browserTest"
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
              --source, -S  path of sources


              <tasks>
              self-install          Install dependencies & generator
              self-update           Not implemented yet !!!

              set-flexio-registry   Set all flexio private registry

              clean                 Remove dependencies & generate sources
              install               Install dependencies
              generate-sources  Generate value objects...

              dev               Build a dev server
              build             Build code

              test              Test
                  <options>
                  --restrict, -R    fileName (regexp validation /.*\/fileName.*/)

              browser-test              Test
                  <options>
                  --restrict, -R    fileName (file path relative to the browser test directory) [required]

              extract-package
                  <options>
                  --target, -T    target directory to extract [required]

              publish
                  <options>
                  --registry    js registry url [required]
                  --email       [required]
                  --password    [required]
                  --username    [required]
```
