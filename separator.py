import os
import sys
import argparse
import numpy as np
from . import tifffile

def separate(path, dfs, ffs, prs):
	tiff_stack = tifffile.TiffFile(path)
	for page in tif:
		for tag in page.tags.values():
			t = tag.name, tag.value
			print '{0} = {1}'.format(tag.name, tag.value)

def main():
    # parser = argparse.ArgumentParser()

    #parser.add_argument('--width', type=str, default='1024',
    #                    help="Width or range of width of a generated projection")

    #args = parser.parse_args()

    filename = '~/gr-data2/stack-2.tif'
    dark_fields = [0,5]
    flat_fields = [13,15]
    projections = [6,12]

    separate(filename, dark_fields, flat_fields, projections)


if __name__ == '__main__':
    main()