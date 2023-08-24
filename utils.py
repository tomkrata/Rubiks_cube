import numpy


def normalize_vector(vector):
    return vector / numpy.linalg.norm(vector)


def is_point_in_surface(point, surface):
    """
    :param point: tuple (x, y)
    :param surface: tuple (a, b, c, d)
    :return: true if point lies on the surface, false otherwise
    """
    summ = 0
    for i in range(len(point)):
        summ += point[i] * surface[i]
    return round(summ, 2) == round(surface[3], 2)


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)
