# GGP-2048
## A general game playing agent for 2048-inspired games. Final project for CS182: Artificial Intelligence.
### By Paul Lisker and Ahmed Ahmed

All code is contained within the `src/game/` subfolder. A number of settings and parameters can be tuned in the `constants.py` file. This includes practical settings such as display options and implementation settings such as the computational budget you'd like to set for each move. To run an experiment with the chosen settings, navigate to to the the `src/game/` folder in the terminal and run the command:

`python main.py -n {number of trials} -f {outfile}`

The outfile will be left in the same folder in a csv file `outfile.csv` that contains score and highest tile data from the trials in the experiment.