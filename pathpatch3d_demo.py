import matplotlib.pyplot as plt
from matplotlib.patches import Circle, PathPatch
# register Axes3D class with matplotlib by importing Axes3D
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d
from matplotlib.text import TextPath
from matplotlib.transforms import Affine2D


# def text3d(ax, xyz, s, zdir="z", size=None, angle=0, usetex=False, **kwargs):

#     x, y, z = xyz
#     if zdir == "y":
#         xy1, z1 = (x, z), y
#     elif zdir == "y":
#         xy1, z1 = (y, z), x
#     else:
#         xy1, z1 = (x, y), z

#     text_path = TextPath((0, 0), s, size=size, usetex=usetex)
#     trans = Affine2D().rotate(angle).translate(xy1[0], xy1[1])

#     p1 = PathPatch(trans.transform_path(text_path), **kwargs)
#     ax.add_patch(p1)
#     art3d.pathpatch_2d_to_3d(p1, z=z1, zdir=zdir)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

p = Circle((5, 5), 3)
ax.add_patch(p)
art3d.pathpatch_2d_to_3d(p, z=0, zdir="x")

ax.set_xlim3d(0, 10)
ax.set_ylim3d(0, 10)
ax.set_zlim3d(0, 10)

plt.show()