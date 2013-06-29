"""this will be my first attempt at a test file for a game using TDD principals.  The idea behind this file is that it is built concurrently and before functions
enter in to the code base.  There is an overall object which holds the tests.  This object then defines methods which describe the details of the testing
situation (variables, objects on which the test depends, etc.) An assertion is declared at the end of a method with the expected results.  Then, a function 
and whatever else is added to the code of the program itself to make ALL these tests pass when this file is run. This should force me to focus on modeling the
action that must be taken to get from the current state of the program to one that implements the new feature (ie, passes all the tests) in as simple and clean
a manner as possible.  Done right, I should end up with a particularly resilient codebase as a result."""

import unittest
import newPythonProject as game

class TestFeatures(unittest.TestCase):
    '''This class is a holder for methods designed to test features as they
    are implemented.  Each method should take only 'self' as a parameter and
    should end with an assertion containing the expected result'''
    
    #----------------------------------------------------------------------
    # def test_all_ones(self):
        # """description of the feature being tested"""
        # game = Game()   #call an object in the program code that will contain the new method
        # game.roll(11, 1) #explicitly state the test here, should call a method and feed it parameters, and set up variables required
        # self.assertEqual(game.score, 11)    #an assertion that can be answered boolean with the expected results of the new feature
    #----------------------------------------------------------------------
    
    def test_Tile_init_params(self):
        tile = game.Tile(True) #feed it a blocked tile
        self.assertEqual(tile.block_sight, True)    #does the tile block sight?

    def test_Map_init_params(self):
        map = game.Map(5, 5, "testmap", False)
        self.assertEqual(map.x,5)
        self.assertEqual(map.y,5)
        self.assertEqual(map.blocked, False)
        self.assertEqual(map.name, "testmap")

    def test_Rect_center(self):
        rect = game.Rect(0, 0, 2, 2)
        center_x = (rect.x1 + rect.x2) / 2  #checks for center of rectangle
        center_y = (rect.y1 + rect.y2) / 2
        center = rect.center()
        #print center
        x_center = center[0]
        y_center = center[1]
        self.assertEqual(x_center, center_x)
        self.assertEqual(y_center, center_y)

    def test_Rect_intersect(self): #checks intersection of two rectangles
        rect1 = game.Rect(0, 0, 2, 2)
        rect2 = game.Rect(1, 1, 2, 2)
        intersect = (rect1.x1 <= rect2.x2 and rect1.x2 >= rect2.x1 and rect1.y1 <= rect2.y2 and rect1.y2 >= rect2.y1)
        self.assertEqual(rect1.intersect(rect2), True)

    def test_indoors_map_gen(self): #creates a new indoor (blocked) map
        map = game.Map(100, 100, "testmap", True)   #map array is a map object
        map.indoors_map(80, 80, map.blocked, 10, 4, 5, 20)      #use map object to create a new map
        
        obscure_list = []           #check if all tiles are blocked
        for x in range(map.x):      #if so, obscured = True
            for y in range(map.y):
                tile = map.list_tile(x, y)
                entry = tile.block_sight
                obscure_list.append(entry)
        obscured = True
        for i in obscure_list:
            if i != True:
                obscured = False
                
                
        
        self.assertEqual(map.x, 80)
        self.assertEqual(map.y, 80)
        self.assertFalse(obscured)
        self.assertEqual(map.name, "testmap")

    def test_render_all(self):  #checks the rendering system
        render = game.render_all()
        """some assertion"""
        
        
        
        
if __name__ == '__main__':
    unittest.main()
