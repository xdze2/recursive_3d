from typing import NamedTuple, List
import numpy as np
from math import sqrt


class Point(NamedTuple):
    x: float
    y: float
    z: float

    def to_int(self):
        alpha = 1e8
        return (
            int(round(alpha * self.x)),
            int(round(alpha * self.y)),
            int(round(alpha * self.z)),
        )

    def as_array(self):
        return np.array(self)


def get_middle_point(a: Point, b: Point) -> Point:
    return Point(
        (a.x + b.x) / 2,
        (a.y + b.y) / 2,
        (a.z + b.z) / 2,
    )


b = sqrt(3) / 2
h = sqrt(2 / 3) /3


class Triange:
    def __init__(self, vertices, fill: bool = True) -> None:
        self.vertices = vertices
        self.fill = fill

    @classmethod
    def default(cls):
        return cls([Point(0, 0, 0), Point(1, 0, 0), Point(0.5, b, 0)], fill=True)

    def bi_split(self):
        self.fill = True
        a, b, c = self.vertices
        ab = get_middle_point(a, b)
        bc = get_middle_point(b, c)
        ca = get_middle_point(c, a)
        return [
            Triange([a, ab, ca], self.fill),
            Triange([ab, b, bc], self.fill),
            Triange([ca, bc, c], self.fill),
            Triange([ab, ca, bc], not self.fill),
        ]

    def get_face_center(self) -> Point:
        return np.array(
            (
                sum(v.x for v in self.vertices) / 3,
                sum(v.y for v in self.vertices) / 3,
                sum(v.z for v in self.vertices) / 3,
            )
        )

    def get_face_normal(self):
        a, b, c = (v.as_array() for v in self.vertices)
        ab = b - a
        bc = c - b
        normal = np.cross(ab, bc)
        return normal / np.linalg.norm(normal)

    def embose(self):
        a, b, c = (v.as_array() for v in self.vertices)
        ab = b - a
        side_lenght = np.linalg.norm(ab)
        d = side_lenght * h * self.get_face_normal() + self.get_face_center()

        return [
            Triange([Point(*a), Point(*b), Point(*d)], fill=self.fill),
            Triange([Point(*b), Point(*c), Point(*d)], fill=self.fill),
            Triange([Point(*c), Point(*a), Point(*d)], fill=self.fill),
        ]


def create_mesh(triangles: List[Triange]):
    points_int = sorted({v.to_int() for tri in triangles for v in tri.vertices})
    points_to_idx = {pts: idx for idx, pts in enumerate(points_int)}

    faces = [[points_to_idx[v.to_int()] for v in tri.vertices] for tri in triangles]
    vertices = np.array(points_int, dtype=np.float) * 1e-7
    return vertices, [], faces


# Script
# default
# bi_split
# embose + filled
# embose - non filled
# bi_split
# embose + filled
# embose - non filled



triangles = [Triange.default()]

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


# Blender
try:
    import bpy
except ImportError:
    exit()

vertices, edges, faces = create_mesh(triangles)

new_mesh = bpy.data.meshes.new("Tetra")
new_mesh.from_pydata(vertices, edges, faces)
new_mesh.update()
my_object = bpy.data.objects.new("Tetra", new_mesh)

collection = bpy.data.collections["Collection"]
collection.objects.link(my_object)

# # To exec. in Blender: 
# filename = "/home/etienne/projets/vrac/tri_mesh.py"
# exec(compile(open(filename).read(), filename, 'exec'))
