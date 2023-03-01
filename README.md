# LearnQA_Python_API

### Run tests at different env

Fist of all you need to set up ENV var.

`export ENV=dev # MAC`

It will use different URL or API according to the settings. Possible values
are:

* prod
* dev

To make sure, that var were sated correctly run command `printenv`.

### Allure Test run command

tests/test_user_auth.py - test suite for run test_results - dir with Allure
results

```rb
python3 -m pytest --alluredir=test_results/ tests/test_user_auth.py
```

How to collect Allure report

```rb
allure serve test_results
```