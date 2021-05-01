import matplotlib.style as mpst
mpst.use('classic')
from matplotlib import pyplot as plt
import numpy as np
from time import time, sleep
from IPython import display
import click

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
    
    


def run_schelling_simulation( N, num_iters, all_people, num_nnbs, tolerance_num, colors_dict, to_plot ):
    t1 = time()
    avg_happy = []
    t = 0
    moved = 1
    while (t < num_iters) and ( moved == 1 ):
        ids_2_move = [ ]

        for i in range( N ):
            is_happy = all_people[ i ].find_comfiness(all_people, i, num_nnbs, tolerance_num)

            if not is_happy:
                ids_2_move.append( i )

        for k in ids_2_move:
            all_people[ k ].move_out( )

        if len( ids_2_move ) > 0:
            moved = 1
        else:
            moved = 0

        avg_happy.append( (N - len(ids_2_move))/N )

        if to_plot:
            plot_city( all_people, colors_dict )
            display.clear_output(wait=True)
            display.display(plt.gcf())
            sleep(1)
        t = t + 1
    t2 = time()

    print('Simulation took: ', t2-t1, ' seconds.')
    
    if to_plot:
        plt.close()
        plot_city( all_people, colors_dict )
    
    
    return all_people, avg_happy
    



def plot_city( all_people, colors_dict ):
    """Plots the whole population
    all_people: <List> All agents in array 
    """
    all_xs = [ each_person.x for each_person in all_people]
    all_ys = [ each_person.y for each_person in all_people]
    all_groups = [ each_person.social_group for each_person in all_people]
    all_colors = [ colors_dict[ dis_group ] for dis_group in all_groups ]
    
    plt.figure(figsize = (4,4) )
    plt.scatter( all_xs, all_ys, c = all_colors, s = 100 )
    plt.xlim([ 0, 1])
    plt.ylim([ 0, 1])
    plt.xlabel('x')
    plt.xlabel('y')
    plt.grid()
    
def plot_historic_happiness(avg_happy):
    """Plots the comfiness level of the population each time step of the simulation.
    avg_happy: List of happiness values
    """
    plt.figure( figsize = (6,4) )
    plt.plot( avg_happy, ms = 10, marker = '.',
             linewidth = 2, color = 'purple', label = 'Overall Comfiness' )
    plt.legend( loc=4 )
    plt.grid()
    plt.savefig( 'sim_result_.png' )
    
def plot_errorbars( all_results ):
    max_result_size = np.max([len(a_list) for a_list in all_results])

    clean_results = np.array([np.pad( np.array(res_vec), (0, max_result_size - len( res_vec ) ),
           mode = 'constant', constant_values = 1 ) for res_vec in all_results])

    plt.figure( figsize = (6,4) )
    plt.errorbar( np.arange(0, max_result_size), np.mean( clean_results, axis = 0 ),
                 yerr = np.std( clean_results, axis = 0 ),
                linewidth = 1.5, ms = 3, marker = 'd',
                 color = 'darkgreen', label = 'Overall Comfiness')
    plt.ylim(top=1)
    plt.legend(loc=4)
    plt.grid()
    
def plot_errorbars_multiparam( ax, all_results, param_val, param_name ):
    max_result_size = np.max([len(a_list) for a_list in all_results])

    clean_results = np.array([np.pad( np.array(res_vec), (0, max_result_size - len( res_vec ) ),
           mode = 'constant', constant_values = 1 ) for res_vec in all_results])


    ax.errorbar( np.arange(0, max_result_size), np.mean( clean_results, axis = 0 ),
                 yerr = np.std( clean_results, axis = 0 ),
                linewidth = 1.5, ms = 3, marker = 'd',
                label = 'Overall Comfiness - {} = {}'.format( param_name, param_val ) )


@click.command()
@click.option( '--n', default = 200, help = 'Population size.' )
@click.option( '--num_nnbs', default = 200, help = 'Number of closest neighbours to consider.' )
@click.option( '--num_iters', default = 200, help = 'Maximum iterations.' )
@click.option( '--tolerance_num', default = 200, help = 'Number of similar neighbours required.' )
def main( n, num_nnbs, num_iters, tolerance_num ):
    print('Start simulation')
    social_groups = ['democratic', 'republican']
    colors_dict = {'democratic' : 'navy', 'republican' : 'crimson'}

    all_people = []
    for i in range( n ):
        dis_group = np.random.choice( social_groups ) 
        all_people.append( SomePerson( dis_group, np.random.rand(), np.random.rand() ) )
        
    all_people_end, avg_happy = run_schelling_simulation( n, num_iters, all_people, num_nnbs,
                                                            tolerance_num, colors_dict, False )

    #plot_historic_happiness( avg_happy )
    print('End simulation')
if __name__ == '__main__':
    main()