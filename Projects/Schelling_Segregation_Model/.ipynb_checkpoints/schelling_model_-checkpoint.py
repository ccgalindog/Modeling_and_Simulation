import matplotlib.style as mpst
mpst.use('classic')
from matplotlib import pyplot as plt
import numpy as np
from time import time, sleep
from IPython import display


class SomePerson():
    """
    Class that describes the properties and methods that describe an agent.
    Each agent will have a position (x, y) in the plane, as well as a social group.
    """
    def __init__( self, social_group, x, y ):
        self.social_group = social_group
        self.x = x
        self.y = y
        
    def move_out( self ):
        self.x = np.random.rand( )
        self.y = np.random.rand( )
        
    def find_comfiness( self, all_people, my_index, num_nnbs, tolerance_num ):
        neighbors = all_people.copy()
        neighbors.pop( my_index )
        distances = np.linalg.norm( 
                        np.array( [ self.x, self.y ] ) \
                        - np.array( [ [each_nb.x, each_nb.y] for each_nb in neighbors ] ),
                        axis = 1 )

        neighbors = np.array(neighbors)
        closest_nbs = neighbors[ np.argsort(distances) ][ : num_nnbs ]
        
        closest_parties = np.array([ some_nb.social_group for some_nb in closest_nbs ])
        
        happy_level = np.sum( closest_parties == self.social_group )

        return happy_level >= tolerance_num
    
    
    
    
