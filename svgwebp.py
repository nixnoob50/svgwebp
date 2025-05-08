#!/usr/bin/env python3

import argparse
import os
import re
import base64
import sys
import html

svg_filename = "";

def main():
    # Instantiate the parser
    parser = argparse.ArgumentParser(
                        prog='SVG WebP Compressor',
                        description='Compress embedded images in svg as wepb. Requires cwebp to be installed.',
                        epilog='Thank you for helping save bandwidth')

    # Required positional argument
    parser.add_argument('filename',
                        help='SVG filename to compress')
    parser.add_argument('-q', '--quality',
                        help='WebP quality 0 = Low, 100 = High, Defaults to 75',
                        type=int,
                        default=75)

    args = parser.parse_args()
    compress_svg(args.filename,args.quality)


def compress_svg(filename,quality):
    global svg_filename
    global webp_quality
    svg_filename = filename
    webp_quality = quality
    svg = open(filename, "r")
    svg_content = svg.read()
    svg.close()
    # print(svg_content)
    new_svg_content = re.sub(r"xlink:href=\"data:image/(png|jpg|jpeg|bmp|tiff);base64\,([^\"]+)\"", compress_image_callback, svg_content)
    del svg_content # clear up memory
    
    #write out new svg
    new_svg_filename = svg_filename.replace(".svg","_compressed.svg")
    if svg_filename == new_svg_filename:
        error_exit("Error generating new filename")

    f = open(new_svg_filename, "w")
    f.write(new_svg_content)
    f.close()

def compress_image_callback(match):
    global svg_filename
    global webp_quality
    # print("|"+match.group(2)+"|")
    tmp_image_filename = svg_filename+".tmp."+match.group(1)
    f = open(tmp_image_filename, "wb")
    decoded_bytes = html.unescape(match.group(2))
    decoded_bytes = base64.b64decode(decoded_bytes)
    f.write(decoded_bytes)
    f.close()
    tmp_webp_filename = tmp_image_filename+".webp"
    os.system("cwebp -q "+str(webp_quality)+" "+tmp_image_filename+" -o "+tmp_webp_filename+" >/dev/null 2>&1")

    webp = open(tmp_webp_filename, "rb")
    webp_content = webp.read()
    webp.close()
    encoded_bytes = base64.b64encode(webp_content)
    # delete temp files
    if os.path.exists(tmp_image_filename):
        os.remove(tmp_image_filename)
    if os.path.exists(tmp_webp_filename):
        os.remove(tmp_webp_filename)

    return "xlink:href=\"data:image/webp;base64,"+encoded_bytes.decode("utf-8")+"\""

def error_exit(message, exit_code=1):
    print(message, file=sys.stderr)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
