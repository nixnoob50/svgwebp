# svgwebp
Converts/compresses embedded images in a svg as webp significantly reducing the filesize of the svg.

The resulting compressed svg will render properly in most browsers such as firefox and chrome, but will display a missing image placeholder if you try to edit it in inkscape or illustrator.
You can still edit the compressed svg in Inkscape and the embeded webp images will still render in the browser.

## usage
```bash
python svgwebp.py test1.svg
```
