import argparse

#Initialization - Arguments
parser = argparse.ArgumentParser(description="Multi Modal Affect Detection")
parser.add_argument("-debug", action="store_true", help="Enables debug mode")
args = parser.parse_args()

#Initialization - Sawyer


##### MAIN #####
if args.debug == True:
    print("RUNNING IN DEBUG MODE")


