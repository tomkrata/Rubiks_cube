import copy
import numpy, math, utils
from cube import Cube


def sort_crit(e):
    return e.get_center()[1]


def apply_rotation(cube, matrix):
    cube.points = cube.points.dot(matrix)
    cube.center = cube.get_center()


class Rubiks:
    def __init__(self, cubes, max_side):
        self.cubes = cubes
        self.test_cube = copy.deepcopy(self.cubes[0])
        self.selected_vector = None
        self.selected_side = None
        self.selected_cubes = []
        self.selected_side_vector = None
        self.side_vectors = numpy.array([
            [max_side, 0, 0],  # right
            [-max_side, 0, 0],  # left
            [0, max_side, 0],  # back
            [0, -max_side, 0],  # front
            [0, 0, max_side],  # down
            [0, 0, -max_side]])  # up
        self.d = max_side**2
        self.side_centers_mapping = {'r': 0, 'l': 1, 'b': 2, 'f': 3, 'd': 4, 'u': 5}
        pass

    def get_cubes_on_side(self, side):
        """
        :param side: letter which defines side of rubiks
        :return: array of cubes which are on the given side
        """
        self.selected_cubes.clear()
        if side not in self.side_centers_mapping:
            for cube in self.cubes:
                cube.selected = False
            self.selected_vector = None
            self.selected_side = None
            self.selected_side_vector = None
            return
        self.selected_side = side
        self.selected_side_vector = self.side_centers_mapping[side]
        self.selected_vector = self.side_vectors[self.side_centers_mapping[side]]
        a, b, c = self.selected_vector
        for cube in self.cubes:
            if utils.is_point_in_surface(cube.center, (a, b, c, self.d)):
                self.selected_cubes.append(cube)
                cube.selected = True
            else:
                cube.selected = False

    def rotate_around_vector(self, angle):
        if self.selected_vector is None:
            return
        self.selected_vector = self.side_vectors[self.selected_side_vector]
        x, y, z = utils.normalize_vector(self.selected_vector)
        matrix = numpy.array([[math.cos(angle) + x**2 * (1 - math.cos(angle)),
                               x*y*(1 - math.cos(angle)) - z * math.sin(angle),
                               x*z*(1-math.cos(angle)) + y*math.sin(angle)],
                              [y*x*(1 - math.cos(angle)) + z*math.sin(angle),
                               math.cos(angle) + y**2 * (1 - math.cos(angle)),
                               y*z*(1 - math.cos(angle)) - x*math.sin(angle)],
                              [z*x*(1-math.cos(angle)) - y*math.sin(angle),
                               z*y*(1-math.cos(angle)) + x*math.sin(angle),
                               math.cos(angle) + z**2 * (1 - math.cos(angle))]])
        for cube in self.selected_cubes:
            cube.points = cube.points.dot(matrix)
            cube.center = cube.get_center()
        return self.selected_side

    def rotate_z(self, angle):
        matrix = numpy.array([[math.cos(angle), -math.sin(angle), 0],
                              [math.sin(angle), math.cos(angle), 0],
                              [0, 0, 1]])
        for cube in self.cubes:
            apply_rotation(cube, matrix)
        apply_rotation(self.test_cube, matrix)
        self.side_vectors = self.side_vectors.dot(matrix)

    def rotate_x(self, angle):
        matrix = numpy.array([[1, 0, 0],
                              [0, math.cos(angle), -math.sin(angle)],
                              [0, math.sin(angle), math.cos(angle)]])
        for cube in self.cubes:
            apply_rotation(cube, matrix)
        apply_rotation(self.test_cube, matrix)
        self.side_vectors = self.side_vectors.dot(matrix)

    def draw(self, center, canvas, fov):
        selected_visible = False
        for side in self.test_cube.get_visible_sides():
            if side == self.selected_side:
                selected_visible = True
                break
        self.cubes.sort(reverse=True, key=sort_crit)
        self.selected_cubes.sort(reverse=True, key=sort_crit)
        if selected_visible:
            for cube in self.cubes:
                if cube not in self.selected_cubes:
                    cube.draw(center, canvas, fov)
            for cube in self.selected_cubes:
                cube.draw(center, canvas, fov)
        else:
            for cube in self.selected_cubes:
                cube.draw(center, canvas, fov)
            for cube in self.cubes:
                if cube not in self.selected_cubes:
                    cube.draw(center, canvas, fov)


