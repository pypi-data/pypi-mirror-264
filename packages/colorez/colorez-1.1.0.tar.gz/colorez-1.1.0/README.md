# colorez

Simple addition of color to the builtin print and input functions

## Installation

Simply run `pip install colorez`. The PyPI package is at https://pypi.org/project/colorez/

## Example Usage

```python
from colorez import color_print, Color, color_input, line_print, object_print, style, print_gradient

# color and styles added to builtin print
color_print("This is red", color="red")
color_print("This is gold and bold", color=178, bold=True)
color_print("This is pink with white background", color="#ed0ecc", bg_color="white")

# stylized text as objects for terminal output
print(Color("hi", 23, ["1", "2"], color="blue"), Color(0, 0, 255, color="plum"))
print("No color", Color(1, 2, 3, color="green"), "\t", Color("orange and italic", color="orange", italic=True))

# Choose style of the prompt for inputs
color_input("yellow and underlined>", color="yellow", underline=True)

# Rewrite lines with the same identifier
line_print("Starting")
line_print("Status: working", identifier="status", color="green")
line_print("Status: broken", identifier="status", color="red")

# Highlight types of objects
object_print({"foo": "bar"}, str_color="green", num_color="red")
object_print([1, 2, 3], str_color="green", num_color="red")

# Use style decorators to change all prints in a function
@style(color="green")
def my_function():
    print("this will be green")
    print("these green too", 2, [], {"foo": "bar"})
    color_print("this will be red", color="red")
my_function()

# Print with a gradient
print_gradient("This will print from red to blue", start_color="red", end_color="blue")
```

![](https://github.com/CodingYuno/colorez/blob/main/example.png)

```python
view_color_names()
```

![](https://github.com/CodingYuno/colorez/blob/main/color_names.png)

```python
test_terminal_color_set()
```

![](https://github.com/CodingYuno/colorez/blob/main/terminal_colors.png)