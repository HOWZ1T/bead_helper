from dataclasses import dataclass
from math import sqrt, pow
__all__ = ['Bead']


@dataclass
class Bead:
    """
    The Bead class represents a bead with its' relevant data

    Attributes:
        brand (str): the brand of the bead
        code (str): the code of the bead
        name (str): the name of the bead
        xml (str): the xml code for this bead object
        hex (str): the hex value for this bead's color
        rgb (tuple(int, int, int)): an tuple containing the rgb values for this bead's color
    """
    __slots__ = ['brand', 'code', 'name', 'rgb', 'xml', 'hex']

    brand: str
    code: str
    name: str
    xml: str
    hex: str
    rgb: (int, int, int)

    def color_dist(self, rgb: (int, int, int)):
        """
        Calculates the distance between the bead's color and the given color.

        Parameters:
        rgb (tuple(int, int, int)): an tuple representation of the given color's rgb values

        Returns:
        float: distance between the bead's color and the given color
        """

        r1 = float(self.rgb[0])
        g1 = float(self.rgb[1])
        b1 = float(self.rgb[2])

        r2 = float(rgb[0])
        g2 = float(rgb[1])
        b2 = float(rgb[2])

        return sqrt(pow((r2 - r1), 2) + pow((g2 - g1), 2) + pow((b2 - b1), 2))
