import argparse
import os

from fontTools.ttLib import TTFont

def genCSS(font, base):
    """Generates a CSS snippet for webfont usage based on:
    http://www.fontspring.com/blog/the-new-bulletproof-font-face-syntax"""

    style = "normal"
    if font["post"].italicAngle != 0:
        style = "oblique"
    weight = font["OS/2"].usWeightClass
    family = font["name"].getName(nameID=1, platformID=3, platEncID=1)
    family = str(family).replace(" ", "").replace("\0", "")

    css = """
@font-face {
    font-family: %(family)sWeb;
    font-style: %(style)s;
    font-weight: %(weight)s;
    src: url('%(base)s.woff2') format('woff2'),
         url('%(base)s.woff') format('woff');
}
""" %{"style":style, "weight":weight, "family":family, "base":base}

    return css

def makeCss(infiles, outfile):
    """Builds a CSS file for the entire font family."""

    css = "/* Example CSS snippet for using Amiri as web font */\n"

    for f in infiles.split():
        base = os.path.splitext(os.path.basename(f))[0]
        font = TTFont(f)
        css += genCSS(font, base)

    with open(outfile, "w") as out:
        out.write(css)

def main():
    parser = argparse.ArgumentParser(description="Create a CSS snippet from Amiri fonts.")
    parser.add_argument("--fonts", metavar="FILES", help="input fonts to process", required=True)
    parser.add_argument("--css", metavar="FILE", help="output font to write", required=True)

    args = parser.parse_args()

    makeCss(args.fonts, args.css)

if __name__ == "__main__":
    main()
