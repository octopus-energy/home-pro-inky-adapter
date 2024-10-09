import argparse
import pathlib
import sys
from inky_drivers.inky_uc8159_mod import Inky as InkyUC8159
from inky_drivers.inky_ac0735c1a_mod import Inky as Inky_AC0735c1a

from PIL import Image

parser = argparse.ArgumentParser()

parser.add_argument(
    "--saturation", "-s", type=float, default=0.5, help="Colour palette saturation"
)
parser.add_argument("--file", "-f", type=pathlib.Path, help="Image file")
parser.add_argument(
    "--device",
    "-d",
    type=str,
    default="Impression5-7",
    help="Inky device to use, "
    "e.g. Impression4, Impression7-3 or Impression5-7 (default)",
)


args, _ = parser.parse_known_args()


if args.device == "Impression4":
    inky = InkyUC8159(device_type="Impression4")
elif args.device == "Impression7-3":
    inky = Inky_AC0735c1a()
else:
    inky = InkyUC8159(device_type="Impression5-7")


saturation = args.saturation

if not args.file:
    print(
        f"""Usage:
    {sys.argv[0]} --file image.png (--saturation 0.5)"""
    )
    sys.exit(1)

image = Image.open(args.file)
resizedimage = image.resize(inky.resolution)

try:
    inky.set_image(resizedimage, saturation=saturation)
except TypeError:
    inky.set_image(resizedimage)

inky.show()
