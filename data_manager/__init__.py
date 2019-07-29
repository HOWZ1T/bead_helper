from objects import Bead
from os import path
import logging


__all__ = ['read_bead_data']


log = logging.getLogger(__name__)


def read_bead_data():
    """
    Reads in the bead data from the csv file and returns a list of bead objects.

    Returns:
    list: a list of bead objects
    """

    beads = []
    fp = path.join(path.abspath(path.dirname(__file__)), "../data/beads.csv")
    with open(fp, "r") as file:  # with keyword handles opening and closing the resource(file)
        line = file.readline()  # skips first line (header)
        i = 1  # line counter, starts at 1 for end user ease of use
        while line:
            line = file.readline()
            i += 1

            # parsing csv
            parts = line.split(',')
            if len(parts) != 23:
                log.info("skipping malformed csv line at line: %d", i)
                continue

            name = parts[0]
            code = parts[1]
            r = parts[2]
            g = parts[3]
            b = parts[4]
            brand = parts[20]
            xml = parts[21]
            hex = parts[22]

            # error checking data
            if not name or not code or not r or not g or not b or not brand or not xml or not hex:
                log.warning("skipping data at line: %d due to missing data", i)
                continue

            # cleaning strings
            name = name.strip().lower()
            code = code.strip().lower()
            r = r.strip().lower()
            g = g.strip().lower()
            b = b.strip().lower()
            brand = brand.strip().lower()
            xml = xml.strip().lower()
            hex = hex.strip().lower()

            # converting rgb into tuple of ints
            try:
                rgb = (int(r), int(g), int(b))
            except ValueError:
                log.warning("skipping data at line: %d due to malformed rgb data", i)
                continue

            beads.append(Bead(brand, code, name, xml, hex, rgb))
            log.debug("added bead: %s [%s]", name, code)

    return beads
