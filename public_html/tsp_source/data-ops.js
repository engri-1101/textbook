var visited;
var opt_mode = 0;
var unvisited;
var is_start = true;
var is_end = false;
var next_node;
var nodes_in = [];
var total_cost = 0;
var old_index;
var new_index;
var node_history = [];
var prev_toss;
var was_part_2 = false;

var cache;

function nn_clicked(){
    change_heur(mode_heur_type_enum.NEAREST_NEIGHBOR)
    restart_ops()
    start_automatic()
}
function ri_clicked(){
    change_heur(mode_heur_type_enum.RANDOM)
    restart_ops()
    start_automatic()
}
function ni_clicked(){
    change_heur(mode_heur_type_enum.NEAREST_INSERTION)
    restart_ops()
    start_automatic()
}
function fi_clicked(){
    change_heur(mode_heur_type_enum.FURTHEST_INSERTION)
    restart_ops()
    start_automatic()
}

function node_clicked(node){
    manual(get_node_hitbox_id(node));
}
function foward_clicked(){
    if (mode == mode_type_enum.BEYONCE){
        // Nothing
    } else if(toss == mode_heur_type_enum.TWOOPT){
        if (is_start) {
            // Randomly generate tour
            toss = mode_heur_type_enum.RANDOM
            start_automatic()
            while (is_end == false) {
                foward_clicked()
            }
            toss = mode_heur_type_enum.TWOOPT
            is_start = false;
            is_end = false;
        } else {
            opt();
            if (is_end == false) {
                text_event(text_event_type_enum.TWOOPTITER)
            }
        }
    } else if (toss == mode_heur_type_enum.RANDOM & !is_end){
        // Randomly generate tour
        while (is_end == false) {
            automatic()
        }
    } else {
        automatic()
    }
}


function restart_clicked(){
    restart_ops();
}

function two_opt_clicked(){
    if (toss == mode_heur_type_enum.TWOOPT) {
        alert('You are already running 2-Opt.')
    } else if (is_end){
        text_event(text_event_type_enum.TWOOPTITER)
        prev_toss = toss
        toss = mode_heur_type_enum.TWOOPT
    } else {
        alert('Can only run 2-Opt once a tour has been found.')
    }
}

// This function does the setup for starting a TSP heuristic
function start_automatic(){
    is_start = false;
    is_end = false;
    if (toss == mode_heur_type_enum.NEAREST_INSERTION) {
        visited = [1,2];
    } else if (toss == mode_heur_type_enum.FURTHEST_INSERTION){
        visited = [1,num_nodes];
    } else {
        visited = [1]
    }
    for (i in visited) {
        accept(visited[i])
    }
    unvisited = []
    for (var i = 1; i <= num_nodes; i++) {
        if (!visited.includes(i)) {
            unvisited.push(i)
        }
    }
    lens_and_nodes_graphics(nodes_in, len_function_type_enum.SELECT);
}

function back_clicked(){
    if (is_end || toss == mode_heur_type_enum.TWOOPT){
        return
    }
    if (toss == mode_heur_type_enum.NEAREST_INSERTION ||
        toss == mode_heur_type_enum.FURTHEST_INSERTION) {
            if (nodes_in.length > 2) {
                last_added = node_history[node_history.length-1]
                index = nodes_in.indexOf(last_added)
                if (index == 0) {
                    total_cost -= distance_map(nodes_in[nodes_in.length-1],last_added);
                    total_cost -= distance_map(last_added, nodes_in[index+1]);
                    total_cost += distance_map(nodes_in[nodes_in.length-1],nodes_in[index+1]);
                } else if (index == nodes_in.length - 1) {
                    total_cost -= distance_map(nodes_in[index-1],last_added);
                    total_cost -= distance_map(last_added, nodes_in[0]);
                    total_cost += distance_map(nodes_in[index-1],nodes_in[0]);
                } else {
                    total_cost -= distance_map(nodes_in[index-1],last_added);
                    total_cost -= distance_map(last_added, nodes_in[index+1]);
                    total_cost += distance_map(nodes_in[index-1],nodes_in[index+1]);
                }
                lens_and_nodes_graphics(nodes_in, len_function_type_enum.UNSELECT);
                undo_alg()
                nodes_in = visited.slice()
                lens_and_nodes_graphics(nodes_in, len_function_type_enum.SELECT);
                text_event(text_event_type_enum.BACK)
                change_cost_graphic(total_cost);
            }
    } else {
        if (nodes_in.length > 1) {
            total_cost -= distance_map(nodes_in[nodes_in.length - 2], nodes_in[nodes_in.length - 1]);
            change_cost_graphic(total_cost);
            lens_and_nodes_graphics(nodes_in, len_function_type_enum.UNSELECT);
            nodes_in.pop();
            lens_and_nodes_graphics(nodes_in, len_function_type_enum.SELECT);
            text_event(text_event_type_enum.BACK)
            undo_alg()
        }
    }
}

function automatic(){
    if (!is_end){
        if (is_start){
            start_automatic();
        }
        var mode_heur = toss;
        if (mode_heur == mode_heur_type_enum.RANDOM){
            next_node = random_tour(visited, unvisited);
        } else if (mode_heur == mode_heur_type_enum.NEAREST_INSERTION){
            next_node = nearest_insertion(distance_map, visited, unvisited)
        } else if (mode_heur == mode_heur_type_enum.FURTHEST_INSERTION){
            next_node = furthest_insertion(distance_map, visited, unvisited)
        } else if (mode_heur == mode_heur_type_enum.NEAREST_NEIGHBOR){
            next_node = nearest_neihbor(distance_map, visited, unvisited)
        }
        accept(next_node);
    }
}
function manual(node){
    if (!is_element_in_set(node, nodes_in)){
        accept(node);
    } else{
        reject(node);
    }
}
function opt(){
    if (opt_mode == 0){
        cache = visited.slice();
        var ret = opt2(distance_map, visited);
        //visited = ret.visited;
        old_index = ret.old_index;
        new_index = ret.new_index;
        highlight_opt(old_index, new_index, visited);
        visited = ret.visited
        opt_mode = 1;
    } else {
        unhighlight_opt(old_index, new_index, cache)
        var flag = true;
        visited.forEach(function(value, index, array){
            if (value != cache[index]){
                flag = false;
            }
        })
        if (flag){
            text_event(text_event_type_enum.TWOOPT)
            is_end = true
            if (toss == mode_heur_type_enum.TWOOPT && was_part_2) {
                change_heur(prev_toss)
            }
        }
        opt_set_ops();
        opt_mode = 0;
    }
}

//set things to be the new graphic, but you still can't interact
function opt_set_ops(){
    lens_and_nodes_graphics(nodes_in, len_function_type_enum.UNSELECT);
    nodes_in = []
    total_cost = 0
    visited.forEach(element => {
        nodes_in.push(element)
    })
    for (var i = 0; i < nodes_in.length - 1; i++){
        total_cost += distance_map(nodes_in[i], nodes_in[i + 1]);
    }
    total_cost +=  distance_map(nodes_in[0], nodes_in[nodes_in.length-1])
    change_cost_graphic(total_cost)
    lens_and_nodes_graphics(nodes_in, len_function_type_enum.SELECT)

}
function restart_ops(){
    if (toss == mode_heur_type_enum.TWOOPT && opt_mode == 1) {
        opt()
    }
    if (toss == mode_heur_type_enum.TWOOPT && was_part_2) {
        change_heur(prev_toss)
        restart_ops()
        start_automatic()
    } else {
        opt_mode = 0;
        brenda_mode = false;
        lens_and_nodes_graphics(nodes_in, len_function_type_enum.UNSELECT);
        if (nodes_in.length > 2) {
            start = nodes_in[0]
            end = nodes_in[nodes_in.length - 1]
            lens_and_nodes_graphics([start, end], len_function_type_enum.UNSELECT);
        }
        is_start = true;
        is_end = false;
        asked_2_opt = false;
        nodes_in = [];
        total_cost = 0;
        change_cost_graphic(total_cost)
        // Travis:
        // text_event(text_event_type_enum.NEW);
        if (toss == mode_heur_type_enum.TWOOPT){
            text_event(text_event_type_enum.TWOOPTSTART);
        } else if (toss == mode_heur_type_enum.MANUAL){
            text_event(text_event_type_enum.NEW);
        } else {
            text_event(text_event_type_enum.SELECT);
        }
        new_index = -2
        old_index = -2
    }
}
function accept(node){
    nodes_in.push(node)
    node_history.push(node)
    if (nodes_in.length > 1){
        if (brenda_mode){
            total_cost += nearest_insertion_place(distance_map, visited, unvisited);
            lens_and_nodes_graphics(nodes_in, len_function_type_enum.UNSELECT);
            nodes_in = visited.slice();
        } else{
            total_cost += distance_map(nodes_in[nodes_in.length - 2], nodes_in[nodes_in.length - 1]);
        }
    }
    if (nodes_in.length == 2) {
        if (toss == mode_heur_type_enum.NEAREST_INSERTION ||
            toss == mode_heur_type_enum.FURTHEST_INSERTION) {
                total_cost *= 2
        }
    }
    if (nodes_in.length == num_nodes){
        if (!brenda_mode) {
            total_cost += distance_map(nodes_in[0], nodes_in[nodes_in.length - 1]);
        }
        text_event(text_event_type_enum.FINISH)
        is_end = true;
    } else {
        text_event(text_event_type_enum.ACCEPT)
    }
    change_cost_graphic(total_cost);
    lens_and_nodes_graphics(nodes_in, len_function_type_enum.SELECT);
}
function reject(node){
    reject_animation(node, nodes_in)
    text_event(text_event_type_enum.REJECT)
}