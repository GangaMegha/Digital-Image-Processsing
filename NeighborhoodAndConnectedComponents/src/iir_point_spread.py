from PIL import Image
import numpy as np
import sys
import matplotlib.pyplot as plt


def fix_boundary_clip_val(pixel_val):

	if pixel_val>255:
		return 255
	elif pixel_val<0:
		return 0
	else:
		return int(pixel_val)


# y(m, n) = 0.01x(m, n) + 0.9(y(m − 1, n) + y(m, n − 1)) − 0.81y(m − 1, n − 1)
def IIR_Filter(x):

	# Initialize output array
	y = np.zeros_like(x)

	for i in range(x.shape[0]):
		for j in range(x.shape[1]):
			for c in range(x.shape[2]):
				if(i>=1 and j>=1):
					pixel_val =  0.01 * x[i][j][c] + 0.9 * ( y[i-1][j][c] + y[i][j-1][c] ) - 0.81 * y[i-1][j-1][c] 
				elif i>=1:
					pixel_val =  0.01 * x[i][j][c] + 0.9 * ( y[i-1][j][c] )
				elif j>=1:
					pixel_val =  0.01 * x[i][j][c] + 0.9 * ( y[i][j-1][c] )
				else:
					pixel_val =  0.01 * x[i][j][c]

				y[i][j][c] = pixel_val

	return y

def main(h, w, c, outfile):
	# Creating delta input : x(m, n) = δ(m−127, n−127)
	x = np.zeros((h, w, c))
	x[127, 127, :] = [1, 1, 1]

	# Get point spread
	# y(m, n) = 0.01x(m, n) + 0.9(y(m − 1, n) + y(m, n − 1)) − 0.81y(m − 1, n − 1) ; for x(m, n) = δ(m−127, n−127)
	y = IIR_Filter(x)

	# Save output image
	img_out = Image.fromarray( (255*100*y).astype(np.uint8) )
	img_out.save(outfile)

if __name__=="__main__":
	main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])