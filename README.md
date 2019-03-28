# hotballoon-shed
Test, Develop, Manage, Generate sources, Build Hotballoon applications

### Installation
https://github.com/flexiooss/hotballoon-shed-playbook

### Configuration
package.json
```json
{
"hotballoon-shed": {
    "build": {
      "builder": "webpack4",
      "entries": [
        "src/main/js/bootstrap.js"
      ],
      "html_template": "src/main/js/index.html",
      "ouput": "dist"
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
              self-install      Install dependencies & generator
              self-update       Not implemented yet !!!

              clean             Remove dependencies & generate sources 
              install           Install dependencies
              generate-sources  Generate value objects...

              dev               Build a dev server       
              build             Build code

              test              Test
```