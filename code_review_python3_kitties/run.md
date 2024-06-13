## RUN OUTPUT

```shell
> make run

pipenv run python -m kitties.viewer 
[[{'height': 10, 'src': 'kitty1.jpg', 'width': 12.5},
  {'height': 10, 'src': 'kitty2.jpg', 'width': 5.0},
  {'height': 10, 'src': 'kitty3.jpg', 'width': 25.0},
  {'height': 10, 'src': 'kitty4.jpg', 'width': 20.0}],
 [{'height': 10, 'src': 'kitty5.jpg', 'width': 20.0},
  {'height': 10, 'src': 'kitty6.jpg', 'width': 15.0}]]
```
```shell 
> make run flags="--page_width=80 --row_height=200"

pipenv run python -m kitties.viewer --page_width=80 --row_height=200
[[], [{'height': 200, 'src': 'kitty1.jpg', 'width': 250.0}],
 [{'height': 200, 'src': 'kitty2.jpg', 'width': 100.0}],
 [{'height': 200, 'src': 'kitty3.jpg', 'width': 500.0}],
 [{'height': 200, 'src': 'kitty4.jpg', 'width': 400.0}],
 [{'height': 200, 'src': 'kitty5.jpg', 'width': 400.0}],
 [{'height': 200, 'src': 'kitty6.jpg', 'width': 300.0}]]
```
```shell
>  make run flags="--page_width=0 --row_height=0"  

pipenv run python -m kitties.viewer --page_width=0 --row_height=0
[[{'height': 0, 'src': 'kitty1.jpg', 'width': 0.0},
  {'height': 0, 'src': 'kitty2.jpg', 'width': 0.0},
  {'height': 0, 'src': 'kitty3.jpg', 'width': 0.0},
  {'height': 0, 'src': 'kitty4.jpg', 'width': 0.0},
  {'height': 0, 'src': 'kitty5.jpg', 'width': 0.0},
  {'height': 0, 'src': 'kitty6.jpg', 'width': 0.0}]]
```
```shell
> make run flags="--page_width=20 --row_height=122" 

pipenv run python -m kitties.viewer --page_width=20 --row_height=122
[[], [{'height': 122, 'src': 'kitty1.jpg', 'width': 152.5}],
 [{'height': 122, 'src': 'kitty2.jpg', 'width': 61.0}],
 [{'height': 122, 'src': 'kitty3.jpg', 'width': 305.0}],
 [{'height': 122, 'src': 'kitty4.jpg', 'width': 244.0}],
 [{'height': 122, 'src': 'kitty5.jpg', 'width': 244.0}],
 [{'height': 122, 'src': 'kitty6.jpg', 'width': 183.0}]]
```

## Tests

```shell
> make test

pipenv run python -m unittest
.ERROR:root:Empty image list
....
----------------------------------------------------------------------
Ran 5 tests in 0.001s

OK
```