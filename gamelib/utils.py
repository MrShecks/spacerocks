
def clamp_point_to_rect (pt, rect):

    x = pt[0]
    y = pt[1]

    if x < rect.left:
        x = rect.right + (rect.left - x)
    elif x > rect.right:
        x = rect.left + (x - rect.right)

    if y < rect.top:
        y = rect.bottom + (y - rect.top)
    elif y > rect.bottom:
        y = rect.top  + (y - rect.bottom)

    return (x, y)

def clamp (n, min_value, max_value):
    return min (max (n, min_value), max_value)