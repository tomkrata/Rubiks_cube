import numpy
import utils


class Cube:
    def __init__(self, size, position, rubiks_size):
        self.size = size
        self.rubiks_size = rubiks_size
        self.points = numpy.array([[size, size, size],
                                   [size, size, -size],
                                   [size, -size, -size],
                                   [size, -size, size],
                                   [-size, size, size],
                                   [-size, size, -size],
                                   [-size, -size, size],
                                   [-size, -size, -size]])
        self.current_sides = []
        for i, coord in enumerate(position):
            if coord != 0:
                self.points[:, i] += coord
        self.center = self.get_center()
        self.z_rotation = 0
        self.x_rotation = 0
        self.side_size = 4
        self.sides = []
        self.sides.append((0, 1, 2, 3, '#ff0000', 'r'))  # right
        self.sides.append((4, 5, 7, 6, '#ff9900', 'l'))  # left
        self.sides.append((2, 3, 6, 7, '#00ff00', 'f'))  # front
        self.sides.append((0, 1, 5, 4, '#0000ff', 'b'))  # back
        self.sides.append((0, 3, 6, 4, '#ffff00', 'd'))  # down
        self.sides.append((1, 2, 7, 5, '#ffffff', 'u'))  # up
        self.selected = False

    def sort_crit(self, side):
        summ = 0.0
        count = 0
        for i in range(self.side_size):
            summ += self.points[side[i]][1]
            count += 1
        return summ / count

    def get_center(self):
        return [numpy.average(self.points[:, 0]),
                numpy.average(self.points[:, 1]),
                numpy.average(self.points[:, 2])]

    def get_visible_sides(self):
        front_point = numpy.where(numpy.min(self.points[:, 1], axis=0) == self.points[:, 1])
        for side in self.sides:
            if front_point[0][0] in side:
                yield side[self.side_size + 1]

    def draw(self, center, canvas, fov):
        outline = '#00ffff' if self.selected else '#000000'
        if fov == 0:
            temp_points = numpy.array([[x[0] + center[0],
                                        x[2] + center[1]] for x in
                                       self.points])
        else:
            temp_points = numpy.array([[x[0] / (x[1] + self.rubiks_size * fov + center[2]) * self.rubiks_size * fov + center[0],
                                        x[2] / (x[1] + self.rubiks_size * fov + center[2]) * self.rubiks_size * fov + center[1]] for x in
                                       self.points])
        front_point = numpy.where(numpy.min(self.points[:, 1], axis=0) == self.points[:, 1])
        self.sides.sort(reverse=True, key=self.sort_crit)
        for side in self.sides:
            if front_point[0][0] in side:
                canvas.create_polygon(temp_points[[side[:self.side_size]]].flatten().tolist(),
                                      fill=side[self.side_size],
                                      outline=outline)
