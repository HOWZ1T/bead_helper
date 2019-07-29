from PIL import Image
import logging
import sys
import os

from data_manager import read_bead_data
from objects import Bead
from bead_utils import approximate_color, approximate_colors


def handle_menu_option_select(valid_range):
    """
    handles user input and validation for menu selection

    Parameters:
    valid_range (list (int)): a list of valid number choices

    Return:
    int: the choice the user selected
    """

    invalid = True
    choice = None
    while invalid:
        choice = input("Enter option: ")
        choice = choice.strip().lower()

        try:
            choice = int(choice)
        except ValueError:
            choice = None

        if choice is None:
            print("invalid option try again...")
            continue

        if choice not in valid_range:
            print("invalid option try again...")
            continue

        invalid = False

    return choice


def brand_color_convert(beads: [Bead]):
    """
    handles the color conversion process between bead brands.

    Parameters:
    beads (list (Bead)): a list of Bead objects
    """

    # getting necessary input from user and validating it
    brand = None
    valid_brand = False
    while not valid_brand:
        brand = input("Enter current brand: ")
        brand = brand.strip().lower()

        # check if brand exists
        for bead in beads:
            if bead.brand == brand:
                valid_brand = True
                break

        if not valid_brand:
            print("invalid brand choice!\n")

    color_id = None
    cur_bead = None
    valid_color_id = False
    while not valid_color_id:
        color_id = input("Enter name or id of the current color: ")
        color_id = color_id.strip().lower()

        # search for color
        for bead in beads:
            if (bead.name == color_id or bead.code == color_id) and bead.brand == brand:
                valid_color_id = True
                cur_bead = bead
                break

        if not valid_color_id:
            print("couldn't find the color by the id: %s for the brand: %s!\n" % (color_id, brand))

    new_brand = None
    valid_new_brand = False
    while not valid_new_brand:
        new_brand = input("Enter new brand: ")
        new_brand = new_brand.strip().lower()

        # check if brand exists
        for bead in beads:
            if bead.brand == new_brand and new_brand != brand:
                valid_new_brand = True
                break

        if not valid_new_brand:
            if brand == new_brand:
                print("invalid brand choice, cannot convert bead between the same brand!\n")
            else:
                print("invalid brand choice!\n")

    # do the actual conversion based on input from user
    matches = approximate_colors(beads, cur_bead.rgb, new_brand)
    if len(matches) == 0:
        print("could not convert the bead: %s [%s] from brand: %s to the brand: %s" % (cur_bead.name, cur_bead.code,
                                                                                       cur_bead.brand, new_brand))
    else:
        for i in range(len(matches)):
            bead, dist = matches[i]
            # 441.67295593 is not magic it is derived from the maximum 3d color space distance,
            # that being the square root of ((255^3) * 3)
            likeness = ((441.67295593 - dist)/441.67295593) * 100.0
            print("%d.: (%-10s) (Likeness: %2.2f%%) %20s [%7s]" % (i+1, bead.brand.capitalize(), likeness,
                                                                 bead.name.capitalize(), bead.code.upper()))
    print("\n")


def cost_of_sprite(beads: [Bead]):
    """
    handles calculating the cost of a sprite based on the given image.

    Parameters:
    beads (list (Bead)): a list of Bead objects
    """

    # getting image file-path from the user and validating it
    fp = None
    valid_fp = False
    while not valid_fp:
        fp = input("Enter path to image file: ")

        # ensuring we have an absolute path
        fp = os.path.abspath(fp)

        if not os.path.isfile(fp):
            print("given file-path is not a file!")
            continue

        if not os.path.exists(fp):
            print("given file-path doesn't exist!")
            continue
        valid_fp = True

    brand = None
    valid_brand = False
    while not valid_brand:
        brand = input("Enter bead brand: ")
        brand = brand.strip().lower()

        # check if brand exists
        for bead in beads:
            if bead.brand == brand:
                valid_brand = True
                break

        if not valid_brand:
            print("invalid brand choice!\n")

    try:
        with Image.open(fp) as img:
            width = img.width
            height = img.height
            total_beads = 0
            count_by_colors = img.getcolors(maxcolors=500)
            beads_by_colors = []

            for pair in count_by_colors:
                count = pair[0]
                rgba = pair[1]

                # ignore transparent pixels
                if rgba[3] != 255:
                    continue

                rgb = (rgba[0], rgba[1], rgba[2])

                # get brand equivalent of color
                bead, dist = approximate_color(beads, rgb, brand)
                if bead is None:
                    print("Error: could not find a matching bead for rgb: %d, %d, %d\n", rgb[0], rgb[1], rgb[2])
                    break

                beads_by_colors.append([bead, count])
                total_beads += count

            print('Details:\nwidth: %d\nheight: %d' % (width, height))
            print('total beads: ' + '{:,}'.format(total_beads))
            print('\n%30s' % 'count by bead color:')
            for bead_pair in beads_by_colors:
                bead = bead_pair[0]
                count = bead_pair[1]
                left = bead.name + " [" + bead.code + "]"
                right = '{:,}'.format(count)
                print('%30s %10s' % (left, right))
            print('\n')
    except IOError:
        print("Error! Something went wrong :(\n")


if __name__ == "__main__":
    # setting up logger
    logging_handlers = [logging.StreamHandler(stream=sys.stderr)]
    if "PYCHARM_HOSTED" in os.environ:
        logging.basicConfig(
            format="%(asctime)s App: | %(name)20s | %(funcName)20s() | %(levelname)8s | %(message)s",
            datefmt="%b %d %H:%M:%S",
            level=logging.DEBUG,
            handlers=logging_handlers
        )
    else:
        logging.basicConfig(
            format="%(asctime)s App: | %(name)20s | %(funcName)20s() | %(levelname)8s | %(message)s",
            datefmt="%b %d %H:%M:%S",
            level=logging.ERROR,
            handlers=logging_handlers
        )
    log = logging.getLogger(__name__)
    logging.getLogger('PIL.PngImagePlugin').setLevel(logging.ERROR)

    log.debug("logger enabled")

    # read in beads from dataset
    log.info("reading bead data...")
    beads = read_bead_data()

    if len(beads) == 0:
        log.error("failed to read in beads!\nexiting...")
        exit(1)

    log.info("read in %d beads", len(beads))

    run = True
    menu = "1. cost of sprite\n2. convert bead color between brands\n3. exit\n"
    while run:
        print(menu)
        choice = handle_menu_option_select([1, 2, 3])

        if choice == 1:
            cost_of_sprite(beads)
        elif choice == 2:
            brand_color_convert(beads)
        elif choice == 3:
            run = False

    exit(0)

