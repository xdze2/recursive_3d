
from typing import List
import numpy as np
from math import sqrt

from custom_types import Tetra




def create_mesh(tetrades: List[Tetra]):
    """Create mesh to use with `mesh.from_pydata(vertices, edges, faces)` """
    points_int = sorted({v.to_int() for tetra in tetrades for v in tetra.vertices})
    points_to_idx = {pts: idx for idx, pts in enumerate(points_int)}

    faces = [[points_to_idx[v.to_int()] for v in face] for tetra in tetrades for face in tetra.get_faces()]
    vertices = np.array(points_int, dtype=np.float) * 1e-7
    return vertices, [], faces





# Blender
try:
    import bpy
except ImportError:
  
    exit()
    

def split(tetraedes):
    return [
        tetra
        for tetra1 in tetraedes
        for tetra in tetra1.bi_split()
    ]


def main():
    tetraedes = [Tetra.default()]
    for _ in range(6):
        tetraedes = split(tetraedes)

    print(len(tetraedes))
    vertices, edges, faces = create_mesh(tetraedes)

    new_mesh = bpy.data.meshes.new("Tetra")
    new_mesh.from_pydata(vertices, edges, faces)
    new_mesh.update()
    my_object = bpy.data.objects.new("Tetra", new_mesh)

    collection = bpy.data.collections["Collection"]
    collection.objects.link(my_object)
