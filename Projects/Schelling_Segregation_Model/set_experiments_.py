
def main():

    N = 200
    num_nnbs = 8
    num_iters = 50
    tolerance_num = 4
    num_simulations = 10

    filename = 'experiments_.sh'
    
    file_sim = open( filename, 'w' )
    for i in range( num_simulations ):
        file_sim.write( 'python3 sweep_schelling_model.py --n {} --num_nnbs {} --num_iters {} --tolerance_num {}\n'\
                        .format( N, num_nnbs, num_iters, tolerance_num ) )
    file_sim.close()


if __name__ == '__main__':
    main()