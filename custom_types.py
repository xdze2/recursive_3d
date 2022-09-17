from itertools import combinations
from math import sqrt
from typing import List, NamedTuple
from typing_extensions import Self

import numpy as np


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


class Triangle:
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
            Triangle([a, ab, ca], self.fill),
            Triangle([ab, b, bc], self.fill),
            Triangle([ca, bc, c], self.fill),
            Triangle([ab, ca, bc], not self.fill),
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
            Triangle([Point(*a), Point(*b), Point(*d)], fill=self.fill),
            Triangle([Point(*b), Point(*c), Point(*d)], fill=self.fill),
            Triangle([Point(*c), Point(*a), Point(*d)], fill=self.fill),
        ]





class Tetra:
    def __init__(self, vertices, fill: bool = True) -> None:
        self.vertices = vertices
        self.fill = fill

    @classmethod
    def default(cls):
        return cls([Point(1, 1, 1), Point(-1, -1, 1), Point(-1, 1, -1), Point(1, -1, -1)], fill=True)

    def get_summit_tetra(self, summit_idx: int) -> 'Tetra': 
 
        return Tetra(
            [get_middle_point(self.vertices[summit_idx], self.vertices[k]) for k in range(4)]
        )

    def bi_split(self):
        return [
            self.get_summit_tetra(k)
            for k in range(4)
        ]

    def get_faces(self) -> List[List[Point]]:
        return list(combinations(self.vertices, 3))