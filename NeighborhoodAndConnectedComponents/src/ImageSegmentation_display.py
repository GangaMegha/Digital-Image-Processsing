import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib as mpl
im = Image.open("/home/ganga/Documents/GitHub/DIP/NeighborhoodAndConnectedComponents/output/img22gd2_out.tif")
x = np.array(im)
N=np.max(x)
cmap = mpl.colors.ListedColormap(np.random.rand(N+1,3))
plt.imshow(x,cmap=cmap,interpolation='none')
plt.colorbar( )
plt.title('Image')
plt.show()