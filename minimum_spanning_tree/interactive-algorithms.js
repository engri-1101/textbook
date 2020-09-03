const AlgoTypeEnum = {"Prim":1, "Kruskal":2, "Rev-Kruskal":3 };
const AlgoStateEnum = {"Start": 1, "Mid": 2, "End": 3};
const ExtremeValEnum = {"Min": 1, "Max" :2}
var store_index = 0;
var lengthsl;

// function sort_lens(value_map, len_map){
//     var lens2 = Object.keys(value_map).map(function(key) {
//         return [key, value_map[key]];
//     });
      
//     lens2.sort(function(first, second) {
//     return second[1] - first[1];
//     }); 
//     var lens = lens2.map( arr => len_map[arr[0]]);
//     return lens
// }

function is_end(algo_state){
    return AlgoStateEnum["End"] == algo_state;
}

function check_cond_prim(nodes, node_in_map){
    if ((node_in_map[parseInt(nodes[0]) - 1] ^ node_in_map[parseInt(nodes[1]) - 1]) == 1){
        return true;
    } else {
        return false;
    }
}
function id_from_value(value){
    return value.data("id");
}
function get_avaible_lengths(lens, len_in_map, node_in_map, id_function, cond_function){
    var avaible_lengths = [];
    lens.forEach(function(value, index, array){
        value.forEach(function(item, index2, array2){
            if (item != undefined){
                var id = id_function(item);
                var len_str = id
                var nodes = id.split("-");
                var cond = cond_function(nodes, node_in_map)
                if (len_in_map[parseInt(nodes[0]) - 1][parseInt(nodes[1]) - 1] == 0 && cond){
                    avaible_lengths.push(len_str);
                } 
            } 
        })
    })
    return avaible_lengths;
}
function get_extreme_value_length(value_map, avaible_lengths, type){
    if (avaible_lengths.length == 0) {
        return -1
    }
    var nodes = avaible_lengths[0].split("-");
    var node1 = parseInt(nodes[0]);
    var node2 = parseInt(nodes[1]);
    var extreme_value = value_map(node1, node2)
    avaible_lengths.forEach(function (value, index, array){
        nodes = value.split("-");
        node1 = parseInt(nodes[0]);
        node2 = parseInt(nodes[1]);
        if (type == ExtremeValEnum["Min"] && value_map(node1, node2) < extreme_value 
            || type == ExtremeValEnum["Max"] && value_map(node1,node2) > extreme_value ){
            extreme_value = value_map(node1, node2);
        } 
    });
    return extreme_value;
}
function calculate_prim(len_in_map, node_in_map, value_map, lens, len_map, id_function){
    var avaible_lengths = get_avaible_lengths(lens, len_in_map, node_in_map, id_function, check_cond_prim);
    var min_value = get_extreme_value_length(value_map, avaible_lengths, ExtremeValEnum["Min"]);
    var clickable_lengths = [];
    avaible_lengths.forEach( function(value, index, array){
        var nodes = value.split("-");
        var node1 = parseInt(nodes[0]);
        var node2 = parseInt(nodes[1]);
        if (value_map(node1,node2) == min_value)
            clickable_lengths.push(value);
    });
    return clickable_lengths;
}
function check_cond_kruskal(nodes, node_in_map){
    return (node_in_map[parseInt(nodes[0]) -1] & node_in_map[parseInt(nodes[1]) - 1]) == 0
}
function calculate_kruskal(len_in_map, node_in_map, value_map, lens, len_map, id_function){
    var avaible_lengths = get_avaible_lengths(lens, len_in_map, node_in_map, id_function, check_cond_kruskal);
    var min_value = get_extreme_value_length(value_map, avaible_lengths, ExtremeValEnum["Min"]);
    var clickable_lengths = [];
    avaible_lengths.forEach( function(value, index, array){
        var nodes = value.split("-");
        var node1 = parseInt(nodes[0]);
        var node2 = parseInt(nodes[1]);
        if (value_map(node1,node2) == min_value)
            clickable_lengths.push(value);
    });
    return clickable_lengths;
}
function is_all_1s(arr){
    var i;
    for (i = 0; i< arr.length; i++){
        if (arr[i] == 0){
            return false;
        }
    }
    return true;
}
function len_map_to_darr(len_in_map, lens, num_nodes, id_function){
    darr = new Array(num_nodes).fill([]);
    lens.forEach(function (value, index, array) {
        var nodes = id_function(value).replace("v", "").split("-");
        if (len_in_map[parseInt(nodes[0]) - 1][parseInt(nodes[1]) - 1] == 1){
            node1 = parseInt(nodes[0]);
            node2 = parseInt(nodes[1]);
            if (darr[node1 -1].length == 0){
                darr[node1 -1] = [node2]
            } else{
                var sub_arr = darr[node1 -1];
                sub_arr.push(node2)
                darr[node1 -1] = sub_arr;
            }
            if (darr[node2 -1].length == 0){
                darr[node2 -1] = [node1]
            } else{
                var sub_arr = darr[node2 -1];
                sub_arr.push(node1)
                darr[node2 -1] = sub_arr;
            }
        }
    });
    return darr;
}
//DFS on nodes
function check_cond_r_kruskal_help(curr_node, nodes_in_mapl, len_darr){
    nodes_in_mapl[curr_node - 1] = 1;
    var poss_edges = len_darr[curr_node - 1];
    poss_edges.forEach( function (value, index, array){
            if (nodes_in_mapl[value -1] == 0){
                check_cond_r_kruskal_help(value, nodes_in_mapl, len_darr);
            }
        }
    );
    return nodes_in_mapl;
}


function check_cond_r_kruskal(len_darr){
    var nodes_in_mapl = new Array(num_nodes).fill(0);
    var arr = check_cond_r_kruskal_help(1, nodes_in_mapl, len_darr);
    return is_all_1s(arr);
}
function r_kruskal_hint(lengths, value_map, length_index, num_nodes, len_in_map, id_function){
    var i;
    var max = 0;
    var arr = [];
    var max_in;
    for (i = length_index; i <lengths.length; i++){
        var nodes = id_function(lengths[i]).replace("v","").split("-");
        var nodes1 = parseInt(nodes[0]);
        var nodes2 = parseInt(nodes[1]);
        if (len_in_map[nodes1][nodes2] == 0) { continue;}
        len_in_map[nodes1][node2] = 0;
        len_in_map[nodes2][nodes1] = 0;
        var darr = len_map_to_darr(len_in_map, lengths, num_nodes, id_function);
        len_in_map[nodes1][node2] = 1;
        len_in_map[nodes2][nodes1] = 1;
        if (check_cond_r_kruskal(darr)){
            arr.push(lengths[i])
        }
    }
    return arr;
}
//Assumes ordered data structure for lengths based on weight, goes through and
//tries to delete the largest one
//takes in length index, returns a struct with the legal clickables and the
//new length index.
function calculate_r_kruskal(lengths, value_map, length_index, num_nodes, len_in_map, id_function){
    var i;
    var max = 0;
    var arr = [];
    var max_in;
    for (i = length_index; i < lengths.length; i++){
        var nodes = id_function(lengths[i]).replace("v","").split("-");
        var node1 = parseInt(nodes[0]);
        var node2 = parseInt(nodes[1]);
        if (len_in_map[node1 - 1][node2 - 1] == 0) { continue;}
        len_in_map[node1 - 1][node2 - 1] = 0;
        len_in_map[node1 - 1][node2 - 1] = 0;
        var darr = len_map_to_darr(len_in_map, lengths, num_nodes, id_function);
        len_in_map[node1 - 1][node2 - 1] = 1;
        len_in_map[node1 - 1][node2 - 1] = 1;
        if (arr.length == 0) {
            if (check_cond_r_kruskal(darr)){
                max = value_map(node1,node2);
                max_in = i
                arr.push(lengths[i].data("id"));
            }
        } else{
            if (value_map(node1, node2) < max){
                return {legal: arr, index: max_in}
            } else if (check_cond_r_kruskal(darr)){
                arr.push(lengths[i].data("id"))
            }
        }
    } 
    return {legal: [], index: i}
}
function calculate_r_kruskal_hint(lengths, value_map, length_index, num_nodes, len_in_map, id_function){
    var i;
    var max = 0;
    var arr = [];
    var max_in;
    for (i = length_index; i < lengths.length; i++){
        var nodes = id_function(lengths[i]).replace("v","").split("-");
        var node1 = parseInt(nodes[0]);
        var node2 = parseInt(nodes[1]);
        if (len_in_map[node1 - 1][node2 - 1] == 0) { continue;}
        len_in_map[node1 - 1][node2 - 1] = 0;
        len_in_map[node1 - 1][node2 - 1] = 0;
        var darr = len_map_to_darr(len_in_map, lengths, num_nodes, id_function);
        len_in_map[node1 - 1][node2 - 1] = 1;
        len_in_map[node1 - 1][node2 - 1] = 1;
        if (check_cond_r_kruskal(darr)){
            max = value_map(node1,node2);
            max_in = i
            arr.push(lengths[i].data("id").replace("v", ""));
        }
    } 
    return arr;
}


function is_length_in(length, lengths){
    var i;
    for (i =0; i < lengths.length; i++){
        if (lengths[i].data("id") === length.data("id")) {
            return true;
        }
    }
    return false;
}
function change_all_x_to_y(arr, x, y){
    var i;
    for (i = 0; i< arr.length; i++){
        if (arr[i] == x) {
            arr[i] = y
        }
    }
    return arr
}
// function set_color_node(node, color){
//     node.attr("fill", color);
// }
// function colorize_nodes(algo_type, nodes, node_in_map, set_color_fn, node1, node2){
//     if (algo_type == AlgoTypeEnum["Kruskal"]){
//         node_in_map.forEach( function (value, index, array) {
//             set_color_fn(nodes[index] , color_array[Math.log2(value)]);
//         });
//     } else if (algo_type == AlgoTypeEnum["Prim"]) {
//         nodes[node1 - 1].attr('fill', '#0677a1' )
//         nodes[node2 - 1].attr('fill', '#0677a1' )
//     }
// }

//sorts increasing
function merge_sort_lengths(lens, compare_fn){
    if (lens.length == 2){
        if (compare_fn(lens[1], lens[0])){
            var temp = lens[0];
            lens[0] = lens[1];
            lens[1] = temp;
        }
        return lens;
    } else if (lens.length == 1 ){
        return lens;
    } else {
        var mid = Math.ceil(lens.length / 2)
        var arr1 = merge_sort_lengths(lens.slice(0, mid), compare_fn);
        var arr2 = merge_sort_lengths(lens.slice(mid, lens.length), compare_fn)
        var i = 0;
        var j = 0;
        var ret = []
        while (i < arr1.length || j < arr2.length){
            if (j == arr2.length || (i < arr1.length && compare_fn(arr1[i], arr2[j]))){
                ret.push(arr1[i]);
                i++;
            } else {
                ret.push(arr2[j]);
                j++;
            }
        }
        return ret;
    }
}
function gr_f(value_map){
    return function(len1, len2){
        var nodes = len1.data("id").split("-")
        var node1 = parseInt(nodes[0]);
        var node2 = parseInt(nodes[1]);
        var value1 = value_map(node1, node2);
        nodes = len2.data("id").split("-")
        node1 = parseInt(nodes[0]);
        node2 = parseInt(nodes[1]);
        var value2 = value_map(node1, node2);
        return value1 > value2;
    }
}

// var test = [2, 1, 0, -1 , 16, 30, -400];
// alert(test)
// alert(less_f)
// alert(less_f(0 , 1))
// alert(merge_sort_lengths(test, less_f))


function lens_to_lengths_stack(lens, value_map){
    var ret = []
    lens.forEach(x => x.forEach(y => {
        if (y != undefined){
            ret.push(y);
        }
    }))
    var fn = gr_f(value_map)
    ret = merge_sort_lengths(ret, fn);
    return ret;
}

function get_hint(algo_type, node_in_map, len_in_map, lens, value_map){
    if (algo_type == AlgoTypeEnum["Prim"]){
        return get_avaible_lengths(lens, len_in_map, node_in_map, id_from_value, check_cond_prim);
    } else if (algo_type == AlgoTypeEnum["Kruskal"]){
        return get_avaible_lengths(lens, len_in_map, node_in_map, id_from_value, check_cond_kruskal);
    } else { //PRECONDITION: Must have called get_clickables at least once
        var num_nodes = node_in_map.length;
        return calculate_r_kruskal_hint(lengthsl, value_map, store_index, num_nodes, len_in_map, id_from_value);
    }
}

function get_clickables(algo_state, algo_type, node_in_map, len_in_map, lens, len_map, value_map){
    if (AlgoStateEnum["End"] == algo_state){
        return [];
    }
    if (AlgoStateEnum["Start"] == algo_state && algo_type == AlgoTypeEnum["Prim"]){
        node_in_map[start_node - 1] = 1;
    } else if (AlgoStateEnum["Start"] == algo_state){
        store_index = 0;
        lengthsl = lens_to_lengths_stack(lens, value_map)
    }
    algo_state++;
    if (algo_type == AlgoTypeEnum["Prim"]) {
        return calculate_prim(len_in_map, node_in_map, value_map, lens, len_map, id_from_value);
    } else if (algo_type == AlgoTypeEnum["Kruskal"]) {
        return calculate_kruskal(len_in_map, node_in_map, value_map, lens, len_map, id_from_value);
    } else if (algo_type == AlgoTypeEnum["Rev-Kruskal"]){
        
        var num_nodes = node_in_map.length;
        var info = calculate_r_kruskal(lengthsl, value_map, store_index, num_nodes, len_in_map, id_from_value);
        store_index = info["index"];
        return info["legal"];
    } else{
        throw TypeError;
    }   
}

//module.exports = {calculate_r_kruskal, check_cond_r_kruskal, is_all_1s, len_map_to_darr, change_all_x_to_y, update_node_in_maps, sort_lens, calculate_prim, calculate_kruskal , get_avaible_lengths, get_extreme_value_length, check_cond_prim, check_cond_kruskal, AlgoStateEnum, AlgoTypeEnum, ExtremeValEnum, get_clickables}