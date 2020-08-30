/// <reference path="./interactive-algorithms.js" />
/// <reference path="./animations.js"/>
var ffactive = false;
var start_node = -1;
var index = 0;
var index = 0;
const num_nodes = 16;
var algo_type;
var algo_state;
var len_in_map;
var value_map;
var len_map;
var node_in_map;
var cost = 0;
var clust_num = 0;
var color_array = ['#e98074', '#9A6324', '#ffe119', '#f58231', '#fabebe', '#ffd8b1', '#fffac8', '#bfef45', '#3cb44b', '#aaffc3', '#42d4f4', '#469990', '#000075', '#4363d8', '#911eb4', '#e6beff', '#f032e6', '#0677a1'];
var clickables;
var max_clust_num = 0;

//TODO: init/modify/len_in_map, and its usage
//TODO: Fix all of the things below noted part
//Put things in right order on index.html
//TODO: fix reset to use proper intits, ... possibly refactor into utility
//NUM NODES SHOULD NOT BE CONSTANT


//TODO: fix interactive algorithms len_in_map, value map, etc
//TODO: fix usage below of len_in ...


//reverse KRUSKAL kint>???
//FAST FOWARD DISABLED???

let UTILITY = {

    len_map : function(i , j){
        if (lens[i - 1][j - 1] == 0){
            return lens[j - 1][i - 1]
        } else {
            return lens[i - 1][j - 1]
        }
    },

    len_map2 : function(len_str){
        var nodes = len_str.split("-")
        return UTILITY.len_map(parseInt(nodes[0]), parseInt(nodes[1]))
    },

    init_node_in_map : function(num_of_nodes){
        node_in_map = new Array(num_of_nodes).fill(0)
    },

    init_node_in_map_2 : function (num_of_nodes){
        node_in_map = new Array(num_of_nodes).fill(1)
    },

    init_len_in_map_base : function(num_of_nodes, val_fill){
        len_in_map = new Array(num_of_nodes).fill(0).map(x => new Array(num_of_nodes).fill(-1))
        len_in_map.forEach(function(row, y_index, array) {
            row.forEach(function(element, x_index, array) {
                if (lens[x_index][y_index] != undefined) {
                    len_in_map[x_index][y_index] = val_fill;
                    len_in_map[y_index][x_index] = val_fill;
                } else if (lens[y_index][x_index] != undefined){
                    len_in_map[x_index][y_index] = val_fill;
                    len_in_map[y_index][x_index] = val_fill;
                }
            })
        })
    },

    init_len_in_map : function(num_of_nodes) {
        UTILITY.init_len_in_map_base(num_of_nodes, 0)
    },

    init_len_in_map_2 : function(num_of_nodes) {
        UTILITY.init_len_in_map_base(num_of_nodes, 1)
    },

    value_map : function(i, j){
        if (len_value[i - 1][j - 1] == undefined){
            return len_value[j  - 1][i - 1]
        } else {
            return len_value[i - 1][j - 1]
        }
    },
    total_value_in_graph : function(num_of_nodes){
        var i;
        var j;
        var total = 0;
        for (i = 0; i < num_of_nodes; i++){
            for (j = i + 1; j < num_of_nodes; j++){
                var val = UTILITY.value_map(i + 1,j + 1)
                if (val != undefined){
                    total = total + val;
                }
            }
        }
        return total
    }
}

let node_hover = function(node, hitbox){
    hitbox.hover(function() {
         if (is_start == 1){
              select_node_visual(node)
         }
    },
    function(){
         if (is_start == 1){
              deselect_node_visual(node)
         }
    });
}

let len_hover = function(x_val, y_val, len, hitbox){
    hitbox.hover(function(){
        if (algo_type != AlgoTypeEnum["Rev-Kruskal"]){
            if (is_start != 1 && (len_in_map[x_val][y_val] == 0 || len_in_map[x_val][y_val] == 0)){
                select_len_visual(len)
            }
        } else {
            if (len_in_map[x_val][y_val] == 1 || len_in_map[y_val][x_val] == 1){
                deselect_len_visual(len)
            }
        }
    },
    function(){
        if (algo_type != AlgoTypeEnum["Rev-Kruskal"]){
            if (is_start != 1 && (len_in_map[x_val][y_val] == 0 || len_in_map[x_val][y_val] == 0)){
                deselect_len_visual(len)
            }
        } else {
            if (len_in_map[x_val][y_val] == 1 || len_in_map[y_val][x_val] == 1){
                select_len_visual(len)
            }
        }
    })
}

let node_click_handle = function(node, hitbox){
    hitbox.click(function (){
         if (is_start == 1 && algo_type == AlgoTypeEnum.Prim){
              start_node = parseInt(node.data("id").replace("n",""));
              is_start = 0;
              node.attr('fill', '#0677a1' );
              text_event(TEXT_EVENT_ENUM.START_EDGE)
              clickables = get_clickables(algo_state, algo_type, node_in_map, len_in_map, lens, UTILITY.len_map, UTILITY.value_map);
         }
    })
}

let is_len_in_arr = function(len, arr){
    var gaurd = false
    if (arr == len.data("id")){
        return true;
    }
    arr.forEach(x => {
        if (len.data("id") == x){
            gaurd = true;
        }
    })
    return gaurd
}

let len_click_handle = function(len, hitbox){
    hitbox.click(function (){
        if (ffactive) return;
        if (is_len_in_arr(len, clickables)){
            algo_state = AlgoStateEnum.Mid
            step_algorithm(len)
        } else {
            var id = len.data("id");
            var nodes = id.split("-");
            var node1 = parseInt(nodes[0]);
            var node2 = parseInt(nodes[1]);
            var is_selected = len_in_map[node1 - 1][node2 - 1] == 1 || len_in_map[node2 - 1][node1 - 1] == 1;
            reject_length(len, is_selected)
            text_event(TEXT_EVENT_ENUM.NEGATIVE_PROMPT)
        }
    })
}

let prims_clicked = function (){

    algo_type = AlgoTypeEnum["Prim"]
    text_event(TEXT_EVENT_ENUM.START_NODE)

    is_start = 1
    max_clust_num = 1;

    UTILITY.init_node_in_map(num_nodes)
    UTILITY.init_len_in_map(num_nodes);

    deselect_all_lens_visual(lens);
    deselect_all_nodes_visual(nodes);

    cost = 0
    cost_text_event("X");
    algo_state = AlgoStateEnum["Start"]
    start_node = -1;

    kruskals_button.attr({fill: "#8E8D8B"})
    prims_button.attr({fill: "#DC8578"})
    rkruskals_button.attr({fill: "#8E8D8B"})

}
let kruskals_clicked = function (){
    algo_type = AlgoTypeEnum["Kruskal"];
    algo_state = AlgoStateEnum.Start

    is_start = 1
    max_clust_num = 1;

    UTILITY.init_node_in_map(num_nodes)
    UTILITY.init_len_in_map(num_nodes);

    deselect_all_lens_visual(lens);
    deselect_all_nodes_visual(nodes);

    cost = 0
    cost_text_event("X");

    start_node = -1;

    text_event(TEXT_EVENT_ENUM.START_EDGE)

    clickables = get_clickables(algo_state, algo_type, node_in_map, len_in_map, lens, UTILITY.len_map, UTILITY.value_map);
    is_start = 0
    //alert(clickables)
    clust_num = 0

    kruskals_button.attr({fill: "#DC8578"})
    prims_button.attr({fill: "#8E8D8B"})
    rkruskals_button.attr({fill: "#8E8D8B"})
}
let r_kruskals_clicked = function (){
    algo_state = AlgoStateEnum.Start
    algo_type = AlgoTypeEnum["Rev-Kruskal"];
    text_event(TEXT_EVENT_ENUM.START_EDGE)

    UTILITY.init_node_in_map_2(num_nodes)
    UTILITY.init_len_in_map_2(num_nodes)

    is_start = 1;
    clickables = get_clickables(algo_state, algo_type, node_in_map, len_in_map, lens, UTILITY.len_map, UTILITY.value_map);
    is_start = 0;

    select_all_nodes_visual(nodes);
    select_all_lens_visual(lens);

    cost = UTILITY.total_value_in_graph(num_nodes);
    cost_text_event(cost)

    kruskals_button.attr({fill: "#8E8D8B"})
    prims_button.attr({fill: "#8E8D8B"})
    rkruskals_button.attr({fill: "#DC8578"})
}
//Start here
let hint_clicked = function (){
    if (!ffactive) {
        if (is_start == 1){
            return;
        } else {
            var data = get_hint(algo_type, node_in_map, len_in_map, lens, UTILITY.value_map);
            hint_visual(data, UTILITY.len_map);
        }
    }
}
let sensitivity_clicked = function(){
    var node1;
    var node2;
    var new_value;
    while(true){
        var val = prompt("What is the first node of the length you want to change?", "");
        if (!isNaN(val) && parseInt(val) > 0 && parseInt(val) < 17){
            node1 = parseInt(val);
            break;
        } else {
            alert("This is not an acceptable node")
            return;
        }
    }
    while(true){
        var val = prompt("What is the second node of the length you want to change?", "");
        if (!isNaN(val) && parseInt(val) > 0 && parseInt(val) < 17){
            node2 = parseInt(val);
            break;
        } else {
            alert("This is not an acceptable node")
            return;
        }
    }
    while (true){
        var val = prompt("To what integer value would you like to change?");
        if (!isNaN(val) && parseInt(val) > 0 && parseInt(val) < 10000){
            new_value = parseInt(val);
            break;
        } else {
            alert("This is not an acceptable value")
            return;
        }
    }
    if (line_texts[node1 - 1][node2 - 1] == undefined && line_texts[node2 - 1][node1 - 1] == undefined){
        alert("No such edge")
    } else {
        var text = line_texts[node1 - 1][node2 - 1] == undefined ? line_texts[node2 - 1][node1 - 1] : line_texts[node1 - 1][node2 - 1]
        var type = len_value[node1 - 1][node2 - 1] == undefined
        text.attr("text", new_value);
        text.attr("fill", "#FF0000");
        if (type){
            len_value[node2 - 1][node1 - 1] = new_value
        } else {
            len_value[node1 - 1][node2 - 1] = new_value
        }
    }
}

let fast_foward_clicked = function (){
    if (!ffactive) {
        if (algo_type == AlgoTypeEnum.Prim && is_start == 1){
            text_event(TEXT_EVENT_ENUM.FFFAIL);
            return;
        }
        ffactive = true;
        recursive_animate( UTILITY.len_map2(clickables[0]))
    }
}

let restore_clicked = function (){
    location.reload();
    return false;
}



//TODO: fix the below
let reset = function (){
    ffactive = false
    if (algo_type == AlgoTypeEnum.Prim){
        prims_clicked();
    } else if (algo_type == AlgoTypeEnum.Kruskal){
        kruskals_clicked();
    } else {
        r_kruskals_clicked();
    }
}
// //Not actually an visual animation, but rather a cycle fix when doing ff
function recursive_animate(it){
    if (ffactive == false) {return}
    primary_text.animate({fill: primary_text.attr("fill") }, 1500, function () {
        if (ffactive == false) {return}
         step_algorithm(it)
         if (clickables.length != 0){
              it = UTILITY.len_map2( clickables[0])
              recursive_animate(it);
         } else {
             ffactive = false;
         }
    });
}
// //because I don't like the order of colors on my color array
// function re_index(index){
//     if (index % 2 == 0){
//          return index;
//     } else{
//          return color_array.length - index
//     }
// }
// function colorize_nodes(algo_type, nodes, node_in_map, node1, node2){
//     if (algo_type == AlgoTypeEnum["Kruskal"]){
//          node_in_map.forEach( function (value, index, array) {
//               val = value ==  0 ? 0 : Math.log2(value) + 1
//               val = re_index(val);
//               arbitrary_color_node_visual(nodes[index], color_array[val])
//          });
//     } else{
//         arbitrary_color_node_visual(nodes[node1 - 1], "#0677a1")
//         arbitrary_color_node_visual(nodes[node2 - 1], "#0677a1")
//     }
// }

function update_node_in_maps(node1, node2){
    var clust1 = node_in_map[node1 - 1]
    var clust2 = node_in_map[node2 - 1]
    if (clust1 == 0 && clust2 == 0){
        node_in_map[node1 - 1] = 1 << max_clust_num;
        node_in_map[node2 - 1] = 1 << max_clust_num++;
    } else if (clust1 != 0 && clust2 == 0){
        node_in_map[node1 - 1] = clust1;
        node_in_map[node2 - 1] = clust1;
    } else if (clust1 == 0 && clust2 != 0){
        node_in_map[node1 - 1] = clust2;
        node_in_map[node2 - 1] = clust2;
    } else {
        var min_clust = clust1 < clust2 ? clust1 : clust2
        var other_clust = clust1 < clust2 ? clust2: clust1
        var i;
        for (i = 0; i < node_in_map.length; i++){
            if (node_in_map[i] == other_clust){
                node_in_map[i] = min_clust
            }
        }
    }
}


function step_algorithm(len) {
    text_event(TEXT_EVENT_ENUM.POSITIVE_PROMPT);
    var id = len.data("id");
    var nodesl = id.split("-");
    var node1 = parseInt(nodesl[0]);
    var node2 = parseInt(nodesl[1]);
    if (algo_type != AlgoTypeEnum["Rev-Kruskal"]) {
        cost = cost + UTILITY.value_map(node1, node2)
        select_len_visual(len);
        select_node_visual(nodes[node1 - 1])
        select_node_visual(nodes[node2 - 1])
    } else {
        cost = cost - UTILITY.value_map(node1, node2);
        deselect_len_visual(len);
    }
    cost_text_event(cost.toString());

    if (algo_type != AlgoTypeEnum["Rev-Kruskal"]){
        len_in_map[node1 - 1][node2 - 1] = 1;
        len_in_map[node2 - 1][node1 - 1] = 1;
    } else {
        len_in_map[node1 - 1][node2 - 1] = 0;
        len_in_map[node2 - 1][node1 - 1] = 0;
    }
    // node_in_map[node1 - 1] = 1;
    // node_in_map[node2 - 1] = 1;

    update_node_in_maps(node1, node2)
    // node_in_map = arr[0];
    // clust_num = arr[1];

    // var update_len_val = algo_type == AlgoTypeEnum["Rev-Kruskal"] ? 0 : 1;
    // len_in_map[node1][node2] = update_len_val;
    // len_in_map[node2][node1] = update_len_val;
    // colorize_nodes(algo_type, nodes, node_in_map, node1, node2)

    clickables = get_clickables(algo_state, algo_type, node_in_map, len_in_map, lens, UTILITY.len_map, UTILITY.value_map);
    if (clickables == undefined || clickables.length == 0) {
         text_event(TEXT_EVENT_ENUM.END);
         algo_state =  AlgoStateEnum["End"];
    }
}