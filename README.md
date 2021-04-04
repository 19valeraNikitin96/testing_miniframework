# About mini test framework

Mini framework was created as test task for GlobalLogic company.

## Prerequisites

* python3
* unittest lib 

## About structure
Project contains two main directories: app_remote, testcases

### app_remote
This directory contains class which describes AUT (Application Under Testing)

### testcases
Contains testcases which inherited from unittest.TestCase class
In 'init.py' you can find two classes:
* Testcase - same unittest.TestCase, but can consume object of AppRemote class and test data
* MonolithicTestcase - object of this class can execute tests in defined order. You should user next pattern for your tests: 'stepN_*' (N is number of test)

You can use these classes for creation own testcases

## Configuration
You can pass own configuration. You should create 'config.json' file.
In future can be added support of environment variables.

```json
{
  "testing": {
    "logging-level": "DEBUG",
    "resources": [
      {
        "name": "users",
        "suites": ["UsersCreatePassed", "UsersCreateFailed"],
        "test-data": {
          "name": "John",
            "gender": "Male",
            "email": "e@a.a",
            "status": "Active"
        }
      },
      {
        "name": "users",
        "suites": ["UserTests"],
        "test-data": {
          "name": "John",
            "gender": "Male",
            "email": "e@a.a",
            "status": "Active"
        }
      }
    ],
    "concurrent-testing": true
  },
  "app-settings": {
    "protocol": "https",
    "domain": "gorest.co.in",
    "port": 443,
    "access_token": "<YOUR ACCESS TOKEN>"
  }
}
```

### About json config structure
You json config must contain next key values: testing and app-settings

* testing - it contains all needed data for running tests
'name' field is name of module which contains tests
'suites' field is list class names which contain tests
You can execute tests concurrently using 'concurrent-testing' field with 'true' value
You can provide test data using field 'test-data'

* app-settings - it contains all needed information about application location

### How to run?

python3 main.py