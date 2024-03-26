import unittest
from observableprops import ObservablesMeta


class ColorBox(metaclass=ObservablesMeta):
    observable_properties = [
        "color",
    ]


class TestObservableProps(unittest.TestCase):
    def test_color_change(self):
        self.color_updated = False

        def gui_update_color(new):
            self.color_updated = True


        colorbox = ColorBox()
        colorbox.add_observer("color", gui_update_color)
        colorbox.color = "Blue"  # All of the observers will be called

        self.assertTrue(self.color_updated, "Color was not updated")

if __name__ == '__main__':
    unittest.main()