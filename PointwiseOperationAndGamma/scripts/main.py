from histogram import *

import sys

def main(img_file, out_dir, choice):
	if choice=="histogram":
		x = read_img(img_file)
		display_gray_img(img_file, out_dir)
		plot_histogram(x, img_file, out_dir)
	elif choice=="equilize":
		equalize(img_file, out_dir)
	elif choice=="stretch":
		stretch(img_file, out_dir, T1=70, T2=175)
	elif choice=="gamma":
		create_checkerboard_pattern(out_dir, 256, 256, gray=160, stripe=16, block=4)
		display_gray_img(img_file, out_dir)
		gamma_correct_img(img_file, out_dir, gamma=1.487)


if __name__=="__main__":
	img_file = "..\\images\\" + sys.argv[1]
	out_dir = "..\\output\\"
	choice = sys.argv[2]


	main(img_file, out_dir, choice)