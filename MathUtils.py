from cmath import pi
from math import atan2, degrees

def get_angle(tail_x, tail_y, head_x, head_y):
	delta_x = tail_x - head_x
	delta_y = tail_y - head_y
	angle = atan2(delta_y, delta_x)
	if angle < 0:
		angle = abs(angle)
	else:
		angle = 2 * pi - angle
	if delta_x > 0:
		return -angle
	return degrees(angle)
