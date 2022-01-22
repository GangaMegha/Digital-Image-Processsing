from PIL import Image
import numpy as np
import sys

im = Image.open(sys.argv[1])
# im.show()
x = np.array(im)

img_out = Image.fromarray(x.astype(np.uint8))
img_out.save(sys.argv[2])