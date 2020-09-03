//Heuristics
const extreme_type_enum = {"MIN": "min", "MAX" : "max"};
var last_index = 0;

function opt2(distance_map, visited){
    var i;
    var j;
    for (i = 0; i < visited.length - 1 ; i++){
        var pair1a = visited[i]
        var pair1b = visited[i + 1]
        var distance1 = distance_map(pair1a, pair1b)
        for (j = i + 2; j < visited.length - 1; j++){
                var pair2a = visited[j]
                var pair2b = visited[j + 1]
                var distance2 = distance_map(pair2a, pair2b)
                var distance3 = distance_map(pair1a, pair2a)
                var distance4 = distance_map(pair1b, pair2b)
                if (distance1 + distance2 > distance3 + distance4){
                    var section1 = visited.slice(0, i + 1)
                    var section2 = visited.slice(i + 1, j + 1);
                    var section3 = visited.slice(j + 1, visited.length);
                    visited =  section1.concat(section2.reverse(), section3);
                    return {"visited" : visited, "old_index" : i, "new_index" : j}
                }
        }
        if (i > 0 && i != visited.length - 2){
            var pair2a = visited[visited.length - 1]
            var pair2b = visited[0]
            var distance2 = distance_map(pair2a, pair2b)
            var distance3 = distance_map(pair1a, pair2a)
            var distance4 = distance_map(pair1b, pair2b)
            if (distance1 + distance2 > distance3 + distance4){
                var section1 = visited.slice(0, i + 1)
                var section2 = visited.slice(i + 1, j + 1);
                var section3 = visited.slice(j + 1, visited.length);
                visited = section1.concat(section2.reverse())
                return {"visited" : visited, "old_index" : i, "new_index" : -1}
            }
        }
    }
    return {"visited" : visited, "old_index" : -2, "new_index" : -2}
}
function undo_alg(){
    last_added = node_history.pop()
    visited.splice(visited.indexOf(last_added),1)
    unvisited.push(last_added)
}
function get_one(){
    return 1;
}

function get_random_int(max) {
    return Math.floor(Math.random() * Math.floor(max));
}
function random_tour(visited, unvisited){
    brenda_mode = false
    var index  = get_random_int(unvisited.length);
    var value = unvisited[index]
    last_index = index
    unvisited.splice(index, 1);
    visited.push(value);
    return value;
}

function nearest_neihbor(distance_map, visited, unvisited){
    brenda_mode = false
    var recent_node = visited[visited.length -1];
    var min_value = distance_map(recent_node, unvisited[0])
    var min = unvisited[0]
    var min_index = 0;
    unvisited.forEach(function (element, index, array) {
        var distance = distance_map(recent_node, element);
        if (distance < min_value){
            min_value = distance;
            min = element
            min_index = index
        }
    });
    // Added: check for other nodes with min value
    var mins = [min]
    var min_indices = [min_index]
    unvisited.forEach(function (element, index, array) {
        var distance = distance_map(recent_node, element);
        if (distance == min_value && element != min){
            mins.push(element)
            min_indices.push(index)
        }
    });
    rand = Math.floor(Math.random() * mins.length);
    min = mins[rand]
    min_index = min_indices[rand]
    last_index = min_index
    unvisited.splice(min_index, 1)
    visited.push(min);
    return min;
}

function extreme_insertion(distance_map, visited, unvisited, type){
    brenda_mode = true;
    var extreme_value = distance_map(visited[0], unvisited[0])
    var extremes = [unvisited[0]]
    var extreme_indices = [0]
    // For every visited node
    for (var j =0; j < unvisited.length; j ++) {
        // Find the distance to the closest node
        var smallest_distance = distance_map(unvisited[j], visited[0])
        var closest_node = visited[0]
        var closest_index = 0
        for (var i =0 ;  i < visited.length; i ++) {
            dist = distance_map(unvisited[j], visited[i])
            if (dist < smallest_distance) {
                smallest_distance = dist
                closest_node = visited[i]
                closest_index = i
            }
        }
        var cond = type == extreme_type_enum.MIN ? smallest_distance < extreme_value : smallest_distance > extreme_value
        if (cond){
            extreme_value = smallest_distance;
            extremes = [unvisited[j]]
            extreme_indices = [j]
        }
        if (smallest_distance == extreme_value) {
            extremes.push(unvisited[j])
            extreme_indices.push(j)
        }
    }
    rand = Math.floor(Math.random() * extremes.length);
    extreme = extremes[rand]
    extreme_index = extreme_indices[rand]
    last_index = extreme_index
    unvisited.splice(extreme_index, 1)
    visited.push(extreme);
    return extreme;
}

function nearest_insertion(distance_map, visited, unvisited){
    return extreme_insertion(distance_map, visited, unvisited, extreme_type_enum.MIN)
}

function furthest_insertion(distance_map, visited, unvisited){
    return extreme_insertion(distance_map, visited, unvisited, extreme_type_enum.MAX)
}

function nearest_insertion_place(distance_map, visited, unvisited){
    var node_last = visited[visited.length - 1];
    visited.pop();
    // Henry
    var n = visited.length
    var min_insertion_cost = (distance_map(visited[n-1], node_last)
                              + distance_map(node_last, visited[0])
                              - distance_map(visited[0], visited[n-1]))
    var insertion_index = -1;
    for (var i = 0; i < visited.length - 1; i++){
        var new_cost = distance_map(visited[i], node_last) + distance_map(node_last, visited[i + 1])
        var old_cost = distance_map(visited[i], visited[i + 1]);
        var insertion_cost = new_cost - old_cost
        if (insertion_cost < min_insertion_cost) {
            min_insertion_cost = insertion_cost
            insertion_index = i
        }
    }
    if (insertion_index == -1){
        visited.push(node_last);
    } else {
        visited.splice(insertion_index+1, 0, node_last);
    }
    return min_insertion_cost;
}
module.exports = {opt2}