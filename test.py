
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-f', "--flux", nargs='?', help="Perform Additional Flux Analysis // True or False", const='True', type=str, default='False')
args = parser.parse_args()

x = (args)
print(x[0])
