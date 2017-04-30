from: http://stackoverflow.com/questions/37885056/python-config-file-as-json-with-inheritance

```bash
dictknife concat config.json -f yaml | sed 's@_extends: production@$inherit: "#/production"@g;s@_extends: staging@$inherit: "#/staging"@g' > config.yaml
zenmai config.yaml --select '#/development' > dev.yaml
```

dev.yaml

```yaml
phpSettings:
  display_startup_errors: false
  display_errors: false
includePaths:
  library: APPLICATION_PATH/../library
bootstrap:
  path: APPLICATION_PATH/Bootstrap.php
  class: Bootstrap
appnamespace: Application
resources:
  frontController:
    controllerDirectory: APPLICATION_PATH/controllers
    moduleDirectory: APPLICATION_PATH/modules
    params:
      displayExceptions: true
  modules: []
  db:
    adapter: pdo_sqlite
    params:
      dbname: APPLICATION_PATH/../data/db/application.db
  layout:
    layoutPath: APPLICATION_PATH/layouts/scripts/
```
