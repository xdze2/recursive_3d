
from typing import List
import numpy as np
from math import sqrt

from custom_types import Triangle



def create_mesh(triangles: List[Triangle]):
    """Create mesh to use with `mesh.from_pydata(vertices, edges, faces)` """
    points_int = sorted({v.to_int() for tri in triangles for v in tri.vertices})
    points_to_idx = {pts: idx for idx, pts in enumerate(points_int)}

    faces = [[points_to_idx[v.to_int()] for v in tri.vertices] for tri in triangles]
    vertices = np.array(points_int, dtype=np.float) * 1e-7
    return vertices, [], faces



# Blender
try:
    import bpy
except ImportError:
    exit()
    

def main():
    triangles = [Triangle.default()]

    triangles = [
        tt
        for tri1 in triangles
        for tri in tri1.bi_split()
        for tt in ([tri] if tri.fill else tri.embose())
    ]

    triangles = [
        tt
        for tri1 in triangles
        for tri in tri1.bi_split()
        for tt in ([tri] if tri.fill else tri.embose())
    ]

    # triangles = [
    #     tt
    #     for tri in triangles
    #     for tt in ([tri] if tri.fill else tri.embose())
    # ]

    print(len(triangles))
    # sub2_triangles = [
    #     sub_tri
    #     for tri in sub_triangles
    #     if tri.fill
    #     for sub_tri in tri.bi_split()
    #     if sub_tri.fill
    # ]




    vertices, edges, faces = create_mesh(triangles)

    new_mesh = bpy.data.meshes.new("Tetra")
    new_mesh.from_pydata(vertices, edges, faces)
    new_mesh.update()
    my_object = bpy.data.objects.new("Tetra", new_mesh)

    collection = bpy.data.collections["Collection"]
    collection.objects.link(my_object)

