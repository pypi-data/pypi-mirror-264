# observableprops

A simple utility to add observers to instance properties

## Example Usage

``` python
from observableprops import ObservablesMeta


class ColorBox(metaclass=ObservablesMeta):
    observable_properties = {
        "color": "add_color_observer",
    }

def gui_update_color(new):
    """
    Updates the color of the label in the GUI.
    """
    print("Color updated", new)

colorbox = ColorBox()
colorbox.add_color_observer(gui_update_color)

colorbox.color = "Blue" # All of the observers will be called
```

