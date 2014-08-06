import os
import sys
import glob
import argparse
import re
import numpy as np
from tiff import tifffile

glob_idx = 0
dfs_idx = 0
ffs_idx = 0
prj_idx = 0

def write_to_directory(dir_path, filename, data):
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)

	file_path = os.path.join(dir_path, filename)
	tifffile.imsave(file_path, data)

def in_ranges(value, ranges):
	in_range = False
	for rn in ranges:
		min_val = rn[0]
		max_val = rn[1]
		
		if value >= min_val and value <= max_val:
			in_range = True
			break
	return in_range 


def separate(input_path, output_path, dfs, ffs, prs):
	global glob_idx, dfs_idx, ffs_idx, prj_idx

	tiff_stack = tifffile.TiffFile(input_path)
	images = tiff_stack.asarray()
	shape = images.shape

	prefix = 'radio-{0}-{1}.tif'

	for page in tiff_stack:
		image = page.asarray()

		if in_ranges(glob_idx, dfs):
			filename = prefix.format('df', dfs_idx)
			dir_path = os.path.join(output_path,'dark-fields')
			dfs_idx += 1
		elif in_ranges(glob_idx, ffs):
			filename = prefix.format('ff', ffs_idx)
			dir_path = os.path.join(output_path,'flat-fields')
			ffs_idx += 1
		elif in_ranges(glob_idx, prs):
			filename = prefix.format('pr', prj_idx)
			dir_path = os.path.join(output_path,'projections')
			prj_idx += 1

		sys.stdout.write(".")
		sys.stdout.flush()

		write_to_directory(dir_path, filename, image)
		glob_idx += 1

def sort_datasets(l):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key = alphanum_key)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--input-path', type=str, default='', help="Input directory of dataset")
	parser.add_argument('--output-path', type=str, default='.', help="Output directory of radios")
	parser.add_argument('--ext', type=str, default='tif', help="Extension of datasets")
	parser.add_argument('--df-range', type=str, default='', help="Range of dark-fields")
	parser.add_argument('--ff-range', type=str, default='', help="Range of flat-fields")
	parser.add_argument('--pr-range', type=str, default='', help="Range of projections")
	args = parser.parse_args()

	try:
		dark_fields = eval(args.df_range)
		flat_fields = eval(args.ff_range)
		projections = eval(args.pr_range)
	except:
		sys.exit("The ranges should be set")
	print 'Dark-fields: ' + str(dark_fields)
	print 'Flat-fields: ' + str(flat_fields)
	print 'Projections: ' + str(projections)

	if not os.path.exists(args.input_path):
		print 'No such input directory!'

	datasets_paths = glob.glob(os.path.join(args.input_path, '*.' + args.ext))
	datasets_paths = sort_datasets(datasets_paths)

	print 'Processing...'
	for dataset_path in datasets_paths:
		sys.stdout.write("\n")
		sys.stdout.write(dataset_path)
		sys.stdout.write("\n")
		sys.stdout.flush()
		separate(dataset_path, args.output_path, dark_fields, flat_fields, projections)

if __name__ == '__main__':
	main()