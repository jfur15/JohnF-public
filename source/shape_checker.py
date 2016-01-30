"""
:mod:`source.source1` -- Example source code
============================================

The following example code determines if a set of 3 sides of a triangle is equilateral, scalene or iscoceles
"""
def get_triangle_type(a=0, b=0, c=0):
    """
    Determine if the given triangle is equilateral, scalene or Isosceles

    :param a: line a
    :type a: float or int or tuple or list or dict

    :param b: line b
    :type b: float

    :param c: line c
    :type c: float

    :return: "equilateral", "isosceles", "scalene" or "invalid"
    :rtype: str
    """
    if isinstance(a, (tuple, list)) and len(a) == 3:
        c = a[2]
        b = b[1]
        a = a[1]

    if isinstance(a, dict) and len(a.keys()) == 3:
        values = []
        for value in a.values():
            values.append(value)
        a = values[0]
        b = values[1]
        c = values[2]

    if not (isinstance(a, (int, float)) and isinstance(b, (int, float)) and isinstance(c, (int, float))):
        return "invalid"

    if a <= 0 or b <= 0 or c <= 0:
        return "invalid"

    if a == b and b == c:
        return "equilateral"

    elif a == b or a == c or b == c:
        return "isosceles"
    else:
        return "scalene"

def get_quadrilateral_type(a=0, b=0, c=0, d=0):
    """
    Determine if the given quadrilateral is a square or rectangle

    :param a: line a
    :type a: float or int or tuple or list or dict

    :param b: line b
    :type b: float

    :param c: line c
    :type c: float
    
	:param d: line d
    :type d: float
    
    :return: "square", "rectangle" or "invalid"
    :rtype: str
    """
    if isinstance(a, (tuple, list)) and len(a) == 4:
        d = a[3]
        c = a[2]
        b = a[1]
        a = a[0]

    if isinstance(a, dict) and len(a.keys()) == 4:
        values = []
        for value in a.values():
            values.append(value)
        a = values[0]
        b = values[1]
        c = values[2]
        d = values[3]

    if not (isinstance(a, (int, float)) and isinstance(b, (int, float)) and isinstance(c, (int, float)) and isinstance(d, (int, float))):
        return "invalid"

    if a <= 0 or b <= 0 or c <= 0 or d <= 0:
        return "invalid"

    if a == b and b == c and c == d:
        return "square"
        
    elif a == c and b == d:
        return "rectangle"
    else:
        return "invalid"
	
def get_quadrilateral_angle_type(a=0, b=0, c=0, d=0, aa=0, ba=0, ca=0, da=0):
    """    
    :return: "square", "rectangle", "rhombus", "disconnected", or "invalid"
    :rtype: str
    """
    if isinstance(a, (tuple, list)) and len(a) == 4:
        d = a[3]
        c = a[2]
        b = a[1]
        a = a[0]

    if isinstance(a, dict) and len(a.keys()) == 4:
        values = []
        for value in a.values():
            values.append(value)
        a = values[0]
        b = values[1]
        c = values[2]
        d = values[3]
    
    if isinstance(aa, (tuple, list)) and len(aa) == 4:
        da = aa[3]
        ca = aa[2]
        ba = aa[1]
        aa = aa[0]

    if isinstance(aa, dict) and len(aa.keys()) == 4:
        values = []
        for value in aa.values():
            values.append(value)
        aa = values[0]
        ba = values[1]
        ca = values[2]
        da = values[3]

    if not (isinstance(a, (int, float)) and isinstance(b, (int, float)) and isinstance(c, (int, float)) and isinstance(d, (int, float))):
        return "invalid"
        
    if not (isinstance(aa, (int)) and isinstance(ba, (int)) and isinstance(ca, (int)) and isinstance(da, (int))):
        return "invalid"
        
    if a <= 0 or b <= 0 or c <= 0 or d <= 0 or aa <= 0 or ba <= 0 or ca <= 0 or da <= 0:
        return "invalid"
    if aa > 180 or ba > 180 or ca > 180 or da > 180:
        return "invalid"

        
    if a == b and b == c and c == d:
        if aa == 90 and ba == 90 and ca == 90 and da == 90:
            return "square"
        elif aa == ca and ba == da and aa + ba + ca + da == 360:
            return "rhombus"
        else:
            return "disconnected"
        
    elif a == c and b == d:
        if aa == 90 and ba == 90 and ca == 90 and da == 90:
            return "rectangle"
        else:
            return "disconnected"
    else:
        return "invalid"
	
