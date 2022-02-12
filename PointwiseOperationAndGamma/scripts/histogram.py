import numpy as np
import matplotlib.pyplot as plt 

from PIL import Image


def read_img(img_file):
	im = Image.open(img_file)
	x = np.array(im)
	return x

def display_gray_img(img_file, out_dir):
	x = read_img(img_file)
	plt.clf()
	plt.imshow(x, cmap="gray")
	plt.savefig(out_dir + img_file.split("\\")[-1].strip(".tif")+".png")

def get_histogram(x):
	bins = np.zeros(256)
	for pixel in x.flatten():
		bins[pixel] += 1
	return bins

def plot_histogram(x, img_file, out_dir):
	plt.clf()
	plt.hist(x.flatten(), bins=np.linspace(0,255,256))
	plt.title("Histogram of {}".format(img_file.split("\\")[-1]))
	plt.xlabel("pixel intensity")
	plt.ylabel("number of pixels")
	plt.savefig(out_dir + img_file.split("\\")[-1].strip(".tif")+"_histogram.png")

def plot_cdf(F, img_file, out_dir):
	plt.clf()
	plt.plot(np.arange(256), F)
	plt.title("CDF of {}".format(img_file.split("\\")[-1]))
	plt.xlabel("pixel intensity i")
	plt.ylabel(r"$\^{F}_x(i)$")
	plt.savefig(out_dir + img_file.split("\\")[-1].strip(".tif")+"_CDF.png")

def equalize(img_file, out_dir):
	x = read_img(img_file)
	h = get_histogram(x)

	Fx = np.cumsum(h)/sum(h)

	Y = Fx[x]

	Y_max = Fx[np.max(x)]
	Y_min = Fx[np.min(x)]

	Z = 255 * (Y - Y_min)/(Y_max - Y_min)

	plot_cdf(Fx, img_file, out_dir)

	# Save equilized Image Z
	plt.clf()
	plt.imshow(Z, cmap="gray")
	plt.savefig(out_dir + img_file.split("\\")[-1].strip(".tif")+"_equilized.png")

	# Plot histogram of equilized image
	plot_histogram(Z.astype(int), img_file.split("\\")[-1].strip(".tif")+"_equilized", out_dir)

def stretch(img_file, out_dir, T1, T2):
	x = read_img(img_file)

	for i in range(x.shape[0]):
		for j in range(x.shape[1]):
			if x[i, j]<=T1:
				x[i, j]=0
			elif x[i, j]>=T2:
				x[i, j]=255
			else:
				x[i, j] = 255 * (x[i, j]-T1)/(T2-T1)

	# Save stretched Image x
	plt.clf()
	plt.imshow(x, cmap="gray")
	plt.savefig(out_dir + img_file.split("\\")[-1].strip(".tif")+"_stretched.png")

	# Plot histogram of stretched image
	plot_histogram(x.astype(int), img_file.split("\\")[-1].strip(".tif")+"_stretched", out_dir)

def create_checkerboard_pattern(out_dir, h, w, gray=160, stripe=16, block=4):
	img = np.ones((h, w))*gray # 160
	for s in range(0, h, stripe):
		if (s//stripe)%2==0:
			for j in range(s, s+stripe, block):
					# initialize block rows as black
					img[j:j+block] = 0
					for k in range(0, block):
						skip = k//(block//2)*(block//2)
						# Modify every 4th (size of block) element from skip and skip+1 as white for row j+k
						img[j+k, skip::block] = 255
						img[j+k, skip+1::block] = 255
	# print(img)
	plt.clf()
	plt.imshow(img, cmap="gray")
	plt.savefig(out_dir +"checkerboard.png")

def gamma_correct_img(img_file, out_dir, gamma=1.487):
	y = read_img(img_file)

	# Gamma correction
	x = 255 * ((y/255)**(1/gamma))

	# Save Gamma corrected Image x
	plt.clf()
	plt.imshow(x, cmap="gray")
	plt.savefig(out_dir + img_file.split("\\")[-1].strip(".tif")+"_gamma_corrected.png")
