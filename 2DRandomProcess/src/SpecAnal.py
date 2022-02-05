#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 18:54:16 2021

@author: Wenrui Li

@modified by: Ganga
"""

import numpy as np                 # Numpy is a library support computation of large, multi-dimensional arrays and matrices.
from PIL import Image              # Python Imaging Library (abbreviated as PIL) is a free and open-source additional library for the Python programming language that adds support for opening, manipulating, and saving many different image file formats.
import matplotlib.pyplot as plt    # Matplotlib is a plotting library for the Python programming language.

from mpl_toolkits import mplot3d

import sys

def MeshPlot_3D(Zabs=None, N=64, outfile="", flag=False):
	# Plot the result using a 3-D mesh plot and label the x and y axises properly. 
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	a = b = np.linspace(-np.pi, np.pi, num = N)
	X, Y = np.meshgrid(a, b)

	if flag:
		Zabs = Theoretical_PSD(X, Y)	

	surf = ax.plot_surface(X, Y, Zabs, cmap='coolwarm', edgecolor='none')
			

	ax.set_xlabel('$\mu$ axis')
	ax.set_ylabel('$\\nu$ axis')
	ax.set_zlabel('Z Label')

	fig.colorbar(surf, shrink=0.5, aspect=5)

	plt.savefig(outfile)
	plt.show()

def get_log_power_sprectrum(z, N):
	# Compute the power spectrum for the NxN region.
	Z = (1/N**2)*np.abs(np.fft.fft2(z))**2

	# Use fftshift to move the zero frequencies to the center of the plot.
	Z = np.fft.fftshift(Z)

	# Compute the logarithm of the Power Spectrum.
	Zabs = np.log(Z)

	return Zabs

def BetterSpecAnal(img, N, k):
	W = np.outer(np.hamming(N), np.hamming(N))

	# To position final computation at centre
	x_offset = int(img.shape[0]/2 - k*N/2)
	y_offset = int(img.shape[1]/2 - k*N/2)

	Z = np.zeros_like(W)

	for i in range(k):
		for j in range(k):
			z = img[ x_offset+i*N : x_offset+(i+1)*N, y_offset+j*N : y_offset+(j+1)*N ] * W
			Z += get_log_power_sprectrum(z, N)

	Z /= 25

	return Z

def BasicSpecAnal(img, N):
	i = 99
	j = 99

	z = img[i:N+i, j:N+j]

	# Compute the logarithm of the Power Spectrum.
	Z = get_log_power_sprectrum(z, N)

	return Z


def display_image_array(img_arr, outfile=""):
	# Display numpy array by matplotlib.
	plt.imshow(img_arr, cmap=plt.cm.gray)
	plt.title('Image')

	# Set colorbar location. [left, bottom, width, height].
	cax =plt.axes([0.9, 0.15, 0.04, 0.7]) 
	plt.colorbar(cax=cax)
	if outfile!="":
		plt.savefig(outfile)
	plt.show()


def read_image(img_file):
	# Read in a gray scale TIFF image.
	im = Image.open(img_file)
	print('Read img04.tif.')
	print('Image size: ', im.size)

	# Display image object by PIL.
	im.show(title='image')

	# Import Image Data into Numpy array.
	# The matrix x contains a 2-D array of 8-bit gray scale values. 
	img_arr = np.array(im)
	print('Data type: ', img_arr.dtype)

	return img_arr


def Theoretical_PSD(mu, nu):
	i = 1j

	H = 3 / ( 1 - 0.99*np.exp(-i*mu) - 0.99*np.exp(-i*nu) + 0.9801*np.exp(-i*(mu+nu)) + 1e-15) 

	S = (1/12) * ( np.abs(H)**2 )

	return np.log(S)


def IIR_Filter(img):
	# y(m, n) = 3x(m, n) + 0.99y(m − 1, n) + 0.99y(m, n − 1) − 0.9801y(m − 1, n − 1)
	out_img = np.zeros_like(img)

	# Apply the filter on the input image to get the output image
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			# y(m, n) = 3x(m, n) + 0.99y(m − 1, n) + 0.99y(m, n − 1) − 0.9801y(m − 1, n − 1)
			if(i>=1 and j>=1):
				out_img[i,j] =  3 * img[i,j] + 0.99 * ( out_img[i-1,j] + out_img[i,j-1] ) - 0.9801 * out_img[i-1][j-1]
			elif(i>=1):
				out_img[i,j] =  3 * img[i,j] + 0.99 * ( out_img[i-1,j] ) 
			elif(j>=1):
				out_img[i,j] =  3 * img[i,j] + 0.99 * ( out_img[i,j-1] ) 
			else:
				out_img[i,j] =  3 * img[i,j]

	return out_img


def generate_image(H, W, low, high):
	print('Image size: ', (H, W))

	return np.random.uniform(low=low, high=high, size=(H, W))


def Power_Spectral_Density_of_a_2D_AR_Process():
	img_arr = generate_image(512, 512, -0.5, 0.5)

	# Display numpy array by matplotlib.
	display_image_array(255*(img_arr+0.5), "./random_img.png")

	img_filtered = IIR_Filter(img_arr)

	# Display numpy array by matplotlib.
	display_image_array(img_filtered + 127, "./random_img_iir.png")

	# Theoretical PSD
	N = int(sys.argv[3])
	MeshPlot_3D(None, N, "./random_img_iir_TheoreticalPSD_3-D_mesh_{}.png".format(N), True)

	Zabs = BetterSpecAnal(img_filtered, N, 5)

	MeshPlot_3D(Zabs, N, "./random_img_iir_BetterSpecAnal_3-D_mesh_{}.png".format(N))



def Power_Spectral_Density_of_an_Image():
	img_arr = read_image(sys.argv[2])

	N = int(sys.argv[3])

	# Display numpy array by matplotlib.
	display_image_array(img_arr, "./img04g.png")

	img_arr_norm = np.double(img_arr)/255.0

	# Compute and display logarithm of the Power Spectrum
	Zabs = BasicSpecAnal(img_arr_norm, N)

	MeshPlot_3D(Zabs, N, "./img04g_3-D_mesh_{}.png".format(N))

	if N==64:
		Zabs = BetterSpecAnal(img_arr_norm, N, 5)

		MeshPlot_3D(Zabs, N, "./img04g_BetterSpecAnal_3-D_mesh_{}.png".format(N))

def main():

	if int(sys.argv[1]) == 1:
		print("\n\n\n\nRunning Power_Spectral_Density_of_an_Image on {} using N={}....\n\n".format(sys.argv[2], sys.argv[3]))
		Power_Spectral_Density_of_an_Image()

	elif int(sys.argv[1]) == 2:
		print("\n\n\n\nRunning Power_Spectral_Density_of_a_2D_AR_Process on {}....\n\n".format("randomly generated image"))
		Power_Spectral_Density_of_a_2D_AR_Process()
	else:
		print("\n\n\n\t\tWRONG CHOICE SPECIFIED!!\n\n\n")
		print("Please choose the second argument as \n\t1: Power_Spectral_Density_of_an_Image \n\t2: Power_Spectral_Density_of_a_2D_AR_Process")		

if __name__=="__main__":
	main()
