# lazy-main
Generalized framework for main loop function.

## Installation
```sh
pip install lazy-main
```

## How to Use
```python
from lazy_main import LazyMain

def main(*args, **kwargs):
    print("Hello World!")

def error_handler(exception):
    print("An error occurred!", exception)

if __name__ == "__main__":
    LazyMain(
        main=main,
        error_handler=error_handler, # This is optional.
        sleep_min=3,
        sleep_max=5,
        loop_count=-1 # -1 Means it will loop infinitely.
    ).run()
```

You can also pass arguments to the `main` function.

```python
from lazy_main import LazyMain

def main(*args, **kwargs):
    print(kwargs["hello"]) # World!

if __name__ == "__main__":
    LazyMain(
        main=main,
    ).run(
        hello="World!",
    )
```