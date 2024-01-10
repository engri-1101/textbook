LABS = baseball_elimination \
	   branch_and_bound \
	   bipartite_matching \
	   diet \
	   fws \
	   game_theory \
	   lp_formulation \
	   maximum_flow \
	   min-cost_flow \
	   minimum_spanning_tree \
	   redistricting \
	   seat_packing \
	   shortest_path \
	   simplex \
	   transportation \
	   traveling_salesman_problem \
	   tsp_integer_programming \
	   minimum_cut \
	   project_selection

all:
	for lab in $(LABS); do \
		make -C $$lab all; \
	done

jhub-labs:
	for lab in $(LABS); do \
		make -C $$lab jhub-labs; \
	done

clean:
	for lab in $(LABS); do \
		make -C $$lab clean; \
	done
