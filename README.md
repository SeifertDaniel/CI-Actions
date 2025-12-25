# Github Actions

## OXID plugin test

### Usage:

Add this chapter to `steps` list:

```
- name: Run OXID tests
  uses: d3datadevelopment/ci-actions/oxid-plugin-test@dev
  with:
    php_version: ${{ matrix.php }}
    oxid_ref: ${{ matrix.oxid_ref }}
    phpunit_version: "^9 || ^10"
    sourceguardian: "true"
    composer_package_name: "d3/mypackage"
    oxid_module_id: "d3myplugin"
    test_suites: "unit,integration"
```

### Arguments
