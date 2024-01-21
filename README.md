# CUB3D PARSING MAP TESTER

## Setup

Clone the repository inside your Cub3D folder. Check in the config.json if the executable path is correct.

## Run

#### > make
#
if the tester doesn't works with make, do :
#### > pythonX.YY parsing_tester.py 
(X.YY is the version, ex. : 3.11) 

## How works config.json

#### > filepath : The path of the executable. If the executabls is inside the cub3d_map_tester folder, don't forget to make "./" before the name. (ex. : ./cub3d)
#### > clear : If true, when you press enter that will clear the terminal between each test and at the end.
#### > invalid_map_folder : The folder of maps that will be tested. You can adding your own map in the "maps/invalid/custom/" folder.
