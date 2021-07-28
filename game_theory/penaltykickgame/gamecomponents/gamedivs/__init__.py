from . import (chances_valid, #A div to track whether aim chances are valid
               counter_made, #A div to track whether a goalie counter is needed
               cpu_selected, #A div to track whether a cpu needs to be selected
               iterations_to_run, #A div to track the number of iterations to run
               kicker_foot, #A div to track the striker's footedness
               kicker_kick, #A div to track the striker's aim direction
               nround, #A div to track the game iteration number
               score, #A div to track the game score
               strategy_to_use, #A div to track the game strategy to use
               select_cpu_tip, #A div containing a tip for selecting the cpu
               chances_lt_0_tip, #A div containing a tip for not having aim chances less than 0
               chances_gt_1_tip, #A div containing a tip for not having aim chances greater than 1
               chances_ne_1_tip, #A div containing a tip for having aim chances add up to 1
               in_an_iter) #A div tracking whether or not the game is currently running an iteratin loop
