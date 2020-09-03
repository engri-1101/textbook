var visited;
var unvisited;
var value_map;
var index_map;
var adjacency_map;
var previous_map;
const neg_infinity = -10e5
var max_in;
var visited_index = 0;
var spy;
var spy_block = true;

var AlgoStateEnum = {"Start": 1, "Middle": 2, "End": 3}
//Ordered triple of visited, unvisited, previous. visited is a map, unvisisted is an priority queue.
//Basically requires you click on the lowest cost path unvisited
//Implementation supports only up to 32 nodes instead of 2^52 nodes which it might of if implemented with a tuple
//Instead of binary numbers. But this is faster.

//TODO: off by one on all maps
function left_index(array, i){
    index = 2 * i + 1;
    if (index < array.length && array[index] != -1){
        return index;
    } else {
        return -1;
    }
}
function right_index(array, i){
    index = 2 * i + 2;
    if (index < array.length && array[index] != -1){
        return index;
    } else{
        return -1;
    }
}
function parent_index(i){
    var parent = i % 2 == 0 ? (i - 2) / 2 : (i - 1) / 2;
    return parent >= 0 ? parent : -1;
}
var count;
function heapify_down(array, i){
    var parent = array[i];
    var left_value = array[left_index(array, i)];
    var right_value = array[right_index(array,i)];
    var left = value_map[left_value - 1];
    var right = value_map[right_value - 1];
    var child = left > right ? right_value : left_value;
    var child_index = left > right ? right_index(array, i) : left_index(array, i);
    if ((left_value != -1 || right_value != -1) && (value_map[parent - 1] > value_map[child - 1])){
        var temp1 = index_map[child - 1];
        index_map[child - 1] = index_map[parent - 1];
        index_map[parent -1] = temp1;
        var temp = child;
        array[child_index] = array[i]
        array[i] = temp;
        count++;
        heapify_down(array, child_index)
    }
}
var parent;
var bool;
var temp;
function heapify_up(array, j){
    parent = parent_index(j)
    if (parent != -1 && (value_map[array[parent] - 1] > value_map[array[j] - 1])){
        index_map[array[parent] - 1] = j;
        index_map[array[j] - 1] = parent;
        temp = array[parent];
        array[parent] = array[j]
        array[j] = temp;
        heapify_up(array, parent)
    }
}
function get_min(array){
    return array[0];
}
function extract_min(array){
    count = 0;
    var min = array[0];
    index_map[min - 1] = -1;
    array[0] = array[--max_in];
    index_map[array[0] - 1] = 0;
    array.pop();
    heapify_down(array, 0)
    return min
}
function decrease_key(array, key, value){
    var i = index_map[key - 1];
    value_map[key - 1] = value;
    heapify_up(array, i)
}
function insert(array, key){
    index_map[key - 1] = max_in;
    array[max_in] = key;
    heapify_up(array, max_in )
    max_in++;
}
//TODO, extract min test, index side effects, heapify down?
//TODO: find out why it does undfined, fix.
function del(array, key){
    var value = value_map[key - 1];
    decrease_key(array, key, neg_infinity)
    extract_min(array)
    value_map[key - 1] = value
}

var min_heap = {
    heap : [],
    getMin : get_min,
    extractMin : extract_min,
    decreaseKey : decrease_key,
    insert : insert,
    delete : del,
}

//Returns apropriate node for next step, side effects are updating as needed.

function d_help(value){
    var nodes_arr = [];
    while(value_map[unvisited.getMin(unvisited.heap) - 1] == value){
        nodes_arr.push(unvisited.extractMin(unvisited.heap));
    }
    nodes_arr.forEach(element =>{
        unvisited.insert(unvisited.heap, element);
    })
    return nodes_arr;
}
function dijkstra(curr_node){
    unvisited.delete(unvisited.heap, curr_node);

    var nodes = adjacency_map[curr_node - 1];
    // instructtxt.attr("font-size", "1");
    // instructtxt.attr("text", JSON.stringify(nodes))
    var cost = value_map[curr_node - 1]
    nodes.forEach(function (element, index, array) {
        var node = element["value"];
        var cost2 = element["cost"];
        if (cost + cost2 < value_map[node - 1]){
            unvisited.decreaseKey(unvisited.heap, node, cost + cost2);
            previous_map[node -1] = curr_node;
        }
    });

    var fin_node = unvisited.extractMin(unvisited.heap);
    var return_nodes = [];
    if (fin_node != undefined){
        return_nodes = d_help(value_map[fin_node - 1]);
        return_nodes.push(fin_node)
    }
    unvisited.insert(unvisited.heap, fin_node);
    // instructtxt.attr("font-size", "1");
    // instructtxt.attr("text", JSON.stringify(value_map))
    visited[visited_index++] = {"node": curr_node, "prev": previous_map[curr_node -1]}
    return {"node" : return_nodes, "highlight" : nodes};
}

//Make sure start node does right thing
function is_node_in(node, array){
    array.forEach(element => {
        if (node == element){
            return true;
        }
    })
    return false;
}


function restart_algorithm(){
    algo_state = AlgoStateEnum.Middle
    unvisited = min_heap;
    visited_index = 0;
    max_in = 0;
    value_map = new Array(num_nodes).fill(infinity);
    value_map[start_node -1] = 0;
    visited = new Array(num_nodes).fill({"node": -1, "prev": -1});
    index_map = new Array(num_nodes).fill(-1);
    previous_map = new Array(num_nodes).fill(-1);
    previous_map[0] = start_node;
    adjacency_map = new Array(num_nodes).fill(0).map(x => new Array(0))
    var i;
    var j;
    var q = 0;
    for (i =0 ; i < num_nodes; i++){
        unvisited.insert(unvisited.heap, i + 1);
        for (j = 0; j < num_nodes; j++){
            if (len_in_map(i + 1, j + 1) == 1){
                q++;
                var value = {"value": j + 1, "cost" : len_value_map(i + 1, j + 1)}
                adjacency_map[i].push(value);
            }
        }
    }
}


//TODO: factor out this start for reset.
function get_clickables(algo_state, node_selected){
    if (algo_state == AlgoStateEnum["Start"]){
        restart_algorithm()
        algo_state = AlgoStateEnum["Middle"]
    }
    return dijkstra(node_selected);
}
function set_up_test(){
    var num_nodes_test = 4;
    max_in = 0;
    algo_state = AlgoStateEnum["Middle"];
    visited_index = 1;
    value_map = new Array(num_nodes_test).fill(infinity);
    value_map[start_node -1] = 0;
    visited = new Array(num_nodes_test).fill({"node": -1, "prev": -1});
    visited[0] = {"node": 1, "prev": 1};
    index_map = new Array(num_nodes_test).fill(-1);
    previous_map = new Array(num_nodes_test).fill(-1);
    adjacency_map = new Array(num_nodes_test).fill([]);
    min_heap["heap"] = []
    unvisited = min_heap

}
function get_item(){
    return value_map;
}
function set_up_value_map(){
    value_map[1-1] = 10;
    value_map[2-1] = 5;
    value_map[3-1] = 3;
    value_map[4-1] = 100;
}
function change_value_map(){
    value_map[2] = 15;
}
function init_special(){
    index_map = [3, 1, 2, 0]
    min_heap.heap = [4, 2, 3, 1];
    value_map = [10,1,3,0]
}
function init_dijkstra(){
    value_map[0] = 0;
    value_map[1] = infinity;
    value_map[2] = infinity;
    value_map[3] = infinity;
    var num_nodes_test = 4;
    adjacency_map = [
    [{"value" : 2 , "cost": 1 }, {"value" : 3 , "cost": 2 }, {"value" : 4 , "cost": 40 }],
    [{"value" : 1 , "cost": 1 }, {"value" : 3 , "cost": 50 }, {"value" : 4 , "cost": 4 }],
    [{"value" : 1 , "cost": 2 }, {"value" : 2 , "cost": 50 }, {"value" : 4 , "cost": 6 }],
    [{"value" : 1 , "cost": 40 }, {"value" : 2 , "cost": 4 }, {"value" : 3 , "cost": 6 }]]
    var i;
    for (i =0 ; i < num_nodes_test; i++){
        unvisited.insert(unvisited["heap"], i + 1);
    }
}

module.exports = {min_heap, parent_index, left_index, right_index, heapify_down, visited,
     unvisited, value_map, index_map, adjacency_map, previous_map, infinity, neg_infinity, max_in,
      AlgoStateEnum, set_up_test, set_up_value_map, change_value_map,
      init_dijkstra, dijkstra, get_item, init_special}