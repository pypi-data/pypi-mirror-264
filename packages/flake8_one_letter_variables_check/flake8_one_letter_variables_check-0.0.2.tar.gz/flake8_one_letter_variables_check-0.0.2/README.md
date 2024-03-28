# flake8-one-variable-check

PyPI: https://pypi.org/project/flake8_one_letter_variables_check/

## TODO

0. Install flake8 (pip etc...)
1. Clone this repository.
2. Move into src folder.
3. ```python setup.py install```
4. Check whether setup is done ```flake8 --version```. If your result has 'flake8-one-letter-variables: 0.0.1' install is successful. The result example is the following.

    ``` bash
   7.0.0 (flake8-one-letter-variables: 0.0.1, flake8-todo: 0.7, mccabe: 0.7.0,pycodestyle: 2.11.1, pyflakes: 3.2.0) CPython 3.10.2 on Darwin
    ```

5. Test flake8 with the test code in `flake8 ../tests/test_olv001.py` The expected result is in the following picture.

![Expected_result](https://github.com/Daku-on/flake8-one-variable-check/blob/main/pic/test_result.png)

## references

1. [Python: flake8 のプラグインを書いてみる](https://blog.amedama.jp/entry/2016/04/12/063359)