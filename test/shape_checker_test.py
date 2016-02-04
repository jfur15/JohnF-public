"""
Test for source.shape_checker
"""
from source.shape_checker import get_triangle_type, get_quadrilateral_type, get_quadrilateral_angle_type
from unittest import TestCase
from tests.plugins.ReqTracer import requirements

class TestGetTriangleType(TestCase):

    @requirements(['#0001'])
    def test_get_triangle_equilateral_all_int(self):
        result = get_triangle_type(1, 1, 1)
        self.assertEqual(result, 'equilateral')
        
    @requirements(['#0002'])
    def test_get_triangle_equilateral_all_float(self):
        result = get_triangle_type(float(1.5), float(1.5), float(1.5))
        self.assertEqual(result, 'equilateral')
        
    @requirements(['#0001'])    
    def test_get_triangle_scalene_all_int(self):
        result = get_triangle_type(1, 2, 3)
        self.assertEqual(result, 'scalene')
    
    @requirements(['#0001'])
    def test_get_triangle_isosceles_all_int(self):
        result = get_triangle_type(1, 2, 2)
        self.assertEqual(result, 'isosceles')
        
    def test_get_triangle_invalid_range_all_int(self):
        result = get_triangle_type(0, 2, 2)
        self.assertEqual(result, 'invalid')
        
    def test_get_triangle_equ_tuple_range_all_int(self):
        result = get_triangle_type([2, 2, 2])
        self.assertEqual(result, 'equilateral')
        
    def test_get_triangle_total_range_all_int(self):
        result = get_triangle_type(-1, 2, 2)
        self.assertEqual(result, 'invalid')
        
    def test_get_triangle_invalid_type_all_int(self):
        result = get_triangle_type('a', 2, 2)
        self.assertEqual(result, 'invalid')

        
    def test_get_triangle_dict_all_int(self):
        result = get_triangle_type(dict(one = 1, two = 1, three = 1))
        self.assertEqual(result, 'equilateral')
    
class TestGetQuadrilateralType(TestCase):

    def test_get_quadrilateral_square_all_int(self):
        result = get_quadrilateral_type(1, 1, 1, 1)
        self.assertEqual(result, 'square')
        
    def test_get_quadrilateral_square_all_float(self):
        result = get_quadrilateral_type(float(1.5), float(1.5), float(1.5), float(1.5))
        self.assertEqual(result, 'square')
        
    def test_get_quadrilateral_rectangle_all_int(self):
        result = get_quadrilateral_type(1, 2, 1, 2)
        self.assertEqual(result, 'rectangle')
        
    def test_get_quadrilateral_invalid_range_all_int(self):
        result = get_quadrilateral_type(0, 1, 1, 1)
        self.assertEqual(result, 'invalid')
        
    def test_get_quadrilateral_invalid_type_all_int(self):
        result = get_quadrilateral_type('a', 1, 1, 1)
        self.assertEqual(result, 'invalid')   
        
    def test_get_quadrilateral_irregular_range_all_int(self):
        result = get_quadrilateral_type(1, 1, 1, 2)
        self.assertEqual(result, 'invalid')
        
    def test_get_quadrilateral_dict_all_int(self):
        result = get_quadrilateral_type(dict(one = 1, two = 1, three = 1, four = 1))
        self.assertEqual(result, 'square')
    def test_get_quadrilateral_tuple_all_int(self):
        result = get_quadrilateral_type([1,1,1,1])
        self.assertEqual(result, 'square')
        
class TestGetQuadrilateralAngleType(TestCase):
    @requirements(['#0003'])
    def test_get_quadrilateral_angle_square_all_int(self):
        result = get_quadrilateral_angle_type(1, 1, 1, 1, 90, 90, 90, 90)
        self.assertEqual(result, 'square')
    
    def test_get_quadrilateral_angle_rectangle_disconnected_angles_all_int(self):
        result = get_quadrilateral_angle_type(1, 2, 1, 2, 90, 100, 90, 90)
        self.assertEqual(result, 'disconnected')
        
    @requirements(['#0004'])
    def test_get_quadrilateral_angle_square_all_float(self):
        result =  get_quadrilateral_angle_type(float(1.5), float(1.5), float(1.5), float(1.5), 90, 90, 90, 90)
        self.assertEqual(result, 'square')
        
    @requirements(['#0003'])
    def test_get_quadrilateral_angle_rectangle_all_int(self):
        result =  get_quadrilateral_angle_type(1, 2, 1, 2, 90, 90, 90, 90)
        self.assertEqual(result, 'rectangle')
    
    @requirements(['#0003'])    
    def test_get_quadrilateral_angle_invalid_range_all_int(self):
        result =  get_quadrilateral_angle_type(0, 1, 1, 1, 90, 90, 90, 90)
        self.assertEqual(result, 'invalid')
        
    def test_get_quadrilateral_angle_invalid_type_all_int(self):
        result =  get_quadrilateral_angle_type('a', 1, 1, 1, 90, 90, 90, 90)
        self.assertEqual(result, 'invalid')   
        
    def test_get_quadrilateral_angle_irregular_range_all_int(self):
        result =  get_quadrilateral_angle_type(1, 1, 1, 2, 90, 90, 90, 90)
        self.assertEqual(result, 'invalid')
        
    def test_get_quadrilateral_angle_dict_all_int(self):
        result =  get_quadrilateral_angle_type(dict(one = 1, two = 1, three = 1, four = 1), 0, 0, 0, 90, 90, 90, 90)
        self.assertEqual(result, 'square')
        
    @requirements(['#0003'])    
    def test_get_quadrilateral_angle_rhombus_all_int(self):
        result = get_quadrilateral_angle_type(3, 3, 3, 3, 45, 135, 45, 135)
        self.assertEqual(result, 'rhombus')
        
    def test_get_quadrilateral_angle_disconnected_all_int(self):
        result = get_quadrilateral_angle_type(3, 3, 3, 3, 90, 179, 90, 1)
        self.assertEqual(result, 'disconnected')
        
    def test_get_quadrilateral_angle_invalid_anglerange_all_int(self):
        result =  get_quadrilateral_angle_type(1, 1, 1, 1, 90, 90, 90, 200)
        self.assertEqual(result, 'invalid')
    
    @requirements(['#0005'])
    def test_get_quadrilateral_angle_invalid_angletype_all_int(self):
        result =  get_quadrilateral_angle_type(1, 1, 1, 1, 90, 90, 90, float(90.0))
        self.assertEqual(result, 'invalid')
        
        
    def test_get_quadrilateral_angle_invalid_type_all_int(self):
        result =  get_quadrilateral_angle_type('a', 1, 1, 1, 90, 90, 90, 90)
        self.assertEqual(result, 'invalid')   
        
    def test_get_quadrilateral_angle_angledict_all_int(self):
        result =  get_quadrilateral_angle_type(1, 1, 1, 1, dict(one = 90, two = 90, three = 90, four = 90))
        self.assertEqual(result, 'square')


    def test_get_quadrilateral_angle_tuple_range_all_int(self):
        result =  get_quadrilateral_angle_type([1, 1, 1, 1], 0, 0, 0, [90, 90, 90, 90])
        self.assertEqual(result, 'square')
