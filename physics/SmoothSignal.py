INDEX = 0
VALUE = 0
SUM = 0
AVERAGED = 0


def smooth_angle(angle_arr, newval, WINDOW_SIZE=5):
    if len(angle_arr) > WINDOW_SIZE:
        global SUM, INDEX
        SUM = SUM - angle_arr[INDEX]
        VALUE = newval
        angle_arr[INDEX] = VALUE
        SUM = SUM + VALUE
        INDEX = (INDEX+1) % WINDOW_SIZE
        AVERAGED = SUM / WINDOW_SIZE
        return AVERAGED
    return newval
