import os
import scipy as sp

inp = sp.array(input('>>>Path/s to search for images?:'))

images = []

for path in inp:
    for name in os.listdir(path):
        if name[-4:]=='fits':
            images.append(name)

sp.savetxt()
