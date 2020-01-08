# License Scanning Action

A Github action to scan code for license violations based on a configuration file per repository.

This actions uses a dedicated docker image available from:

https://github.com/zephyrproject-rtos/docker_scancode

## Example workflow

```

name: Scancode

on: [pull_request]

jobs:
  scancode_job:
    runs-on: ubuntu-latest
    name: Scan code for licenses
    steps:
    - uses: actions/checkout@v1
    - name: Scan the code
      id: scancode
      uses: zephyrproject-rtos/action_scancode@v1
      with:
        directory-to-scan: 'scan/'
    - name: Artifact Upload
      uses: actions/upload-artifact@v1
      with:
        name: scancode
        path: ./artifacts

    - name: Verify
      run: |
        test ! -s ./artifacts/report.txt || (cat ./artifacts/report.txt && exit 1 )

```

The above example checks out the code and runs scancode on all new files being
added by the pull request. New files are copied into the `scan/` directory to
avoid scanning of existing files in the repository.

Once scanning is complete, resulting files are uploaded as artifacts and
available for further inspection.

The scanner generates a report that can be displayed to show the violations.
Depending on your setup, you can either display it as part of the overall
action log or you can upload it or put it in a comment in the pull-request.



## Configuration

The action expects a configuration file under `.github/` named `license_config.yml`. This file is used to filter the scanning results and identify violations based on whitelisted licenses and license categories.

```
license:
  main: apache-2.0
  category: Permissive
exclude:
  extensions:
    - yml
    - yaml
    - html
    - rst
    - conf
    - cfg
  langs:
    - HTML
 ```
 
 
The `license` section sets the main license for the repository and its category. Files licensed under the same category would be allowed in this case.

The `exclude` section is used to tell the scanner which extensions and content types to ignore when looking for license/copyright boilerplate.
