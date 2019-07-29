from objects import Bead
import logging


__all__ = ['approximate_color']


log = logging.getLogger(__name__)


def approximate_color(beads: [Bead], rgb: (int, int, int), brand: str = "all"):
    """
    Attempts to approximate the nearest matching bead by the given rgb value.

    Parameters:
    beads (list [Bead]): a list containing bead objects to act as the search pool
    rgb (tuple (int, int, int)): a tuple of ints representing the rgb values for a color
    brand (str) (optional): specifies if the bead must be of a certain brand, the default value "all" will ignore the beads' brand

    Returns:
    tuple (Bead, float) or None (if no bead is found)
    """
    brand = brand.lower()

    # check that brand exists
    min_dist = float(999)  # the maximum distance in the rgb space is 441 i.e the distance between black and white
    min_bead = None  # the bead with the lowest difference is the closet match
    for bead in beads:
        if bead.brand != brand and brand != "all":  # handles filtering beads by brand if brand isn't set to "all"
            continue

        # get distance between colors
        dist = bead.color_dist(rgb)
        if dist <= min_dist:
            min_dist = dist
            min_bead = bead

    return min_bead, min_dist
