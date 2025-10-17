# cfn-ci-helper

Cloudformation CI Helper, a series of helpers to help you deploy a cloudformation
template(s) as a part of a CI pipeline in a reasonably safe manner.

## Commands

* Running Tests
  
  ```
  uv run ./run_tests.py
  ```

* Running Tests with Coverage

  ```
  uv run coverage run ./run_tests.py
  ```

* Build Docs

  ```
  uv run --directory docs --group docs make html
  ```

    