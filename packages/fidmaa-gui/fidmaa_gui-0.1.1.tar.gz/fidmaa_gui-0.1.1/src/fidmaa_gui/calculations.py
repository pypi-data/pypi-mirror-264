import math

from PySide6.QtCore import QPoint


def findPoint(
    startX,
    startY,
    direction=1,
    maxWidth=480,
    maxHeight=640,
    angle=None,
    linear_coefficient=None,
):
    """
    Starting on (startX, startY), find a point going to the rigth (direction=1) or left (direction=-1)
    which lies on the bounds of the image (minimum point (0, 0), maximum point (maxWidth, maxHeight)),
    so that the angle of the line to the x axis is equal to angle (in deg).

    You can pass either angle or linear_coefficient
    """

    if direction not in [1, -1]:
        raise ValueError

    if linear_coefficient is None and angle is None:
        raise ValueError("Pass either angle or linear_coefficient")

    nx = 0

    if linear_coefficient is None:
        linear_coefficient = math.tan(math.radians(angle))

    while True:
        ny = linear_coefficient * float(nx) + startY

        if ny <= 0:
            ny = 0
            break

        if ny >= maxHeight:
            ny = maxHeight
            break

        if nx + direction + startX > maxWidth or nx + direction + startX < 0:
            break

        nx += direction

    return QPoint(nx + startX, ny)


def findParalellPoint(midpointX, midpointY, angle, distance, direction=1):
    # Get the midpoint of a paralell line to the left -- this point
    # can also be used to calculate a perpendicular line

    lpx1 = midpointX + direction * math.sin(math.radians(-angle)) * distance
    lpy1 = midpointY + direction * math.cos(math.radians(-angle)) * distance

    return (lpx1, lpy1)
