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

## Status Reporter

### Usage:

Add:
- repository secret
  - `GITEA_TOKEN` with your custom access token
- repository variable
  - `GITEA_API`with your API endpoint
- the following section to your workflow steps list
  - ```
    - name: Report CI status
      uses: d3datadevelopment/ci-actions/status-reporter@dev
      with:
        api_status_endpoint: >
          ${{ vars.GITEA_API }}statuses/${{ github.sha }}
        auth_token: ${{ secrets.GITEA_TOKEN }}
        state: ${{ needs.plugin-tests.result }}
        description: >
          CI result: ${{ needs.plugin-tests.result }}
        target_url: >
          ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
    ```

### Arguments

## Examples

See examples for integration.