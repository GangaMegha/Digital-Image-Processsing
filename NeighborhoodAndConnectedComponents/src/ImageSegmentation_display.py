import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib as mpl

import sys

im = Image.open(sys.argv[1])
x = np.array(im)
N=np.max(x)
cmap = mpl.colors.ListedColormap(np.random.rand(N+1,3))
plt.imshow(x,cmap=cmap,interpolation='none')
plt.colorbar( )
plt.title('Image')
plt.savefig(sys.argv[2])
# plt.show()