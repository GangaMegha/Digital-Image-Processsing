from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import cm

import sys

i = 1j

def FIR_low_pass_filter(mu, nu):
	return (1/81) * np.sin(mu*9/2) * np.sin(nu * 9/2) / ( np.sin(mu * 1/2) * np.sin(nu * 1/2) + 1e-15 )
	# H = 1/81 * ( ( np.exp(i*nu*4) * np.exp(-i*nu*5) ) / ( 1 - np.exp(-i*nu) ) ) * ( ( np.exp(i*mu*4) * np.exp(-i*mu*5) ) / ( 1 - np.exp(-i*mu) ) )
	# return np.abs(H)

def FIR_sharpening_filter_H(mu, nu):
	return (1/25) * np.sin(5/2 * mu) * np.sin(5/2 * nu) / ( np.sin(1/2 * mu) * np.sin(1/2 * nu) + 1e-15 )

def FIR_sharpening_filter_G(mu, nu, lbda):
	return 1 + lbda * ( 1 - (1/25) * np.sin(5/2 * mu) * np.sin(5/2 * nu) / ( np.sin(1/2 * mu) * np.sin(1/2 * nu) + 1e-15 ) )

def IIR_filter(mu, nu):
	H = 0.01 / ( 1 - 0.9*np.exp(-i*mu) - 0.9*np.exp(-i*nu) + 0.81*np.exp(-i*(mu+nu)) + 1e-15)
	return np.abs(H)

def plot(filter_type, title, outfile, lbda):
	mu = np.linspace(-np.pi, np.pi, 50)
	nu = np.linspace(-np.pi, np.pi, 50)

	X, Y = np.meshgrid(mu, nu)

	if filter_type == "lpf":
		Z = FIR_low_pass_filter(X, Y)
	elif filter_type == "sharp_h":
		Z = FIR_sharpening_filter_H(X, Y)	
	elif filter_type == "sharp_g":
		Z = FIR_sharpening_filter_G(X, Y, lbda)	
	elif filter_type == "iir":
		Z = IIR_filter(X, Y)
	else:
		print("Wrong filter type specified!!\n\n\n Please choose from : lpf, sharp_h, sharp_g, iir")
		return

	fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

	surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='inferno', edgecolor='none')
	fig.colorbar(surf, shrink=0.5, aspect=5)

	ax.set_xlabel(r'$\mu$')
	ax.set_ylabel(r'$\nu$')
	ax.set_zlabel(r'$H(e^{j\mu}, e^{j\nu})$')

	if filter_type == "sharp_g":
		ax.set_xlim(-3.5, 3.5)
		ax.set_ylim(-3.5, 3.5)
		ax.set_zlim(1, 2.8)

	ax.set_title(title)

	plt.savefig(outfile)

if __name__=="__main__":
	plot(sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]))
