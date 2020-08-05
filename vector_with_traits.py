# run pip install traitsui
# pip install PyQt5
from traits.api import HasTraits, Float

from traitsui.api import View


class vector(HasTraits):

    x = Float()
    y = Float()


if __name__ == '__main__':
    vector(3,4).configure_traits()