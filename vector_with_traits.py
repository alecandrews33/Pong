# run pip install traitsui
# pip install PyQt5
from traits.api import HasTraits, Float


class vector(HasTraits):

    x = Float()
    y = Float()


if __name__ == '__main__':
    vector().configure_traits()