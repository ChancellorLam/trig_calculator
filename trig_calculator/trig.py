import math


def sine(angle):
    """
    Calculate the sine of the given angle using range reduction and Maclaurin series approximation

    :param angle: The input angle in radians.
    :return: The approximate sine value of the input angle.
    """
    if math.isclose(angle % math.pi, 0):
        return 0.0
    angle_info = _domain_reduction(angle)
    series_approximation = _sine_maclaurin_series(angle_info.angle)
    sin_approx = _reconstruct(series_approximation, angle_info.quadrant)
    return sin_approx


def cosine(angle):
    """
    Calculate the cosine of the given angle using range reduction and Maclaurin series approximation.

    :param angle: The input angle in radians.
    :return: The approximate cosine value of the input angle.
    """
    if math.isclose(angle % math.pi / 2, 0) and not math.isclose(angle % math.pi, 0):
        return 0.0
    angle_info = _domain_reduction(angle)
    series_approximation = _cosine_maclaurin_series(angle_info.angle)
    cos_approx = _reconstruct(series_approximation, angle_info.quadrant)
    return cos_approx


def tangent(angle):
    """
    Calculate the tangent of the given angle as sine(angle) / cosine(angle).

    :param angle: The input angle in radians.
    :return: The approximate tangent value of the input angle.
    """
    if math.isclose(angle % math.pi / 2, 0) and not math.isclose(angle % math.pi, 0):
        return "undefined"
    tan_approx = sine(angle) / cosine(angle)
    return tan_approx


def cosecant(angle):
    """
    Calculate the cosecant of the given angle as 1 / sine(angle).

    :param angle: The input angle in radians.
    :return: The approximate cosecant value of the input angle.
    """
    if math.isclose(angle % math.pi, 0):
        return "undefined"

    csc_approx = 1 / sine(angle)
    return csc_approx


def secant(angle):
    """
    Calculate the secant of the given angle as 1 / cosine(angle).

    :param angle: The input angle in radians.
    :return: The approximate secant value of the input angle.
    """
    if math.isclose(angle % math.pi / 2, 0) and not math.isclose(angle % math.pi, 0):
        return "undefined"
    sec_approx = 1 / cosine(angle)
    return sec_approx


def cotangent(angle):
    """
    Calculate the cotangent of the given angle as 1 / tangent(angle).

    :param angle: The input angle in radians.
    :return: The approximate cotangent value of the input angle.
    """
    if math.isclose(angle % math.pi, 0):
        return "undefined"

    cot_approx = 1 / tangent(angle)
    return cot_approx


class AngleInfo:
    def __init__(self, angle, quadrant):
        """
        Initialize the AngleInfo object.

        :param angle: The reduced angle in radians.
        :param quadrant: The quadrant in which the angle lies (1 to 4).
        """
        self.angle = angle
        self.quadrant = quadrant


def _domain_reduction(given_angle):
    """
    First, reduces the given angle to a working angle within the domain [0, 2π] and determine the angle's quadrant
    within the domain. Then shift working angle to [-π/2, π/2] to be closer to 0 for better accuracy

    :param given_angle: The input angle in radians.
    :return: An AngleInfo object containing the reduced angle in the domain [-π/2, π/2] and its quadrant in the domain
             [0, 2π].
    """
    working_angle = given_angle

    # get a working angle that is equivalent to given angle, but in the domain of [0, 2π]
    while working_angle < 0 or working_angle > 2 * math.pi:
        print("Current working angle: " + str(working_angle))
        if working_angle >= 2 * math.pi:
            working_angle = working_angle - 2 * math.pi
            print("Working angle shifted to: " + str(working_angle))
            print()
        elif given_angle < 0:
            working_angle = working_angle + 2 * math.pi
            print("Working angle shifted to: " + str(working_angle))
            print()

    # split 0 to 2π into 4 quadrants and find out which quadrant working angle is in
    quadrant = _get_quadrant_from(working_angle)

    # shift domain from [0, 2π] to [-π/2, π/2] to be closer to 0 for better Maclaurin series accuracy
    working_angle = _shift_to_working_domain(working_angle, quadrant)

    return AngleInfo(working_angle, quadrant)


def _sine_maclaurin_series(working_angle):
    """
    Approximate the sine of the given angle using the Maclaurin series expansion.

    :param working_angle: The angle in the reduced domain [-π/2, π/2].
    :return: The approximate sine value of the reduced angle.
    """
    series_sum = 0

    # 10 terms provides near-perfect double precision for most angles
    for i in range(0, 10):
        power_factor = 2 * i + 1
        if i % 2 == 0:
            series_sum = series_sum + math.pow(working_angle, power_factor) / math.factorial(power_factor)
        else:
            series_sum = series_sum - math.pow(working_angle, power_factor) / math.factorial(power_factor)

    return series_sum


def _cosine_maclaurin_series(working_angle):
    """
    Approximate the cosine of the given angle using the Maclaurin series expansion.

    :param working_angle: The angle in the reduced domain [-π/2, π/2].
    :return: The approximate cosine value of the reduced angle.
    """
    series_sum = 0

    # 10 terms provides near-perfect double precision for most angles
    for i in range(0, 10):
        power_factor = 2 * i
        if i % 2 == 0:
            series_sum = series_sum + math.pow(working_angle, power_factor) / math.factorial(power_factor)
        else:
            series_sum = series_sum - math.pow(working_angle, power_factor) / math.factorial(power_factor)

    return series_sum


def _reconstruct(approximation, quadrant):
    """
    Adjusts the sign of the given approximation based on its quadrant in the domain [0, 2π].

    The approximation is initially computed in the reduced domain [-π/2, π/2]. Depending on
    the quadrant of the original angle, the sign is adjusted to finalize the approximation.

    :param approximation: The approximate value of sine or cosine from the Maclaurin series.
    :param quadrant: The quadrant in which the original angle lies.
    :return: The adjusted approximate value based on the quadrant.
    """
    if quadrant == 2 or quadrant == 3:
        return approximation * -1
    elif quadrant == 1 or quadrant == 4:
        return approximation


def _get_quadrant_from(angle):
    """
   Determine the quadrant of the given angle within the domain [0, 2π].

   :param angle: The angle in radians.
   :return: The quadrant (1 to 4) in which the angle lies.
   """
    if angle - 3 * math.pi / 2 >= 0:
        return 4
    elif angle - math.pi >= 0:
        return 3
    elif angle - math.pi / 2 >= 0:
        return 2
    else:
        return 1


def _shift_to_working_domain(angle, quadrant):
    """
    Shift an angle in the domain [0, 2π] to the working domain [-π/2, π/2] for better Maclaurin series accuracy.

    :param angle: The angle in radians.
    :param quadrant: The quadrant in which the angle lies.
    :return: The angle shifted to the working domain.
    """
    if quadrant == 4:
        return angle - 2 * math.pi
    elif quadrant == 2 or quadrant == 3:
        return angle - math.pi
    elif quadrant == 1:
        return angle
