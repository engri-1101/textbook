//BFS through the whole graph, creating a "previous", data scructure.
var graphtype = 0;
var ff_enabled = false;
var algo_state = AlgoStateEnum.Start
var test_iter = 0;
var verify_eligible = false;
var verify_ready = false;
var verify_arr = [];

function recursive_animate(){
    ffh.animate({opacity: 0} , 1500, function () {
        algorithm_step(clickables.node[0],true);
        algorithm_step_pt2(true);
        if (clickables.node.length > 0){
            if (ff_enabled == true) {recursive_animate()}
        }
    })
}
function verify_work(){
    var i;
    var str_arr = new Array(visited.length).fill("-");
    var work_arr = new Array(visited.length).fill({"str": "", "prev": -1});
    for (i =0; i< visited.length; i++){
        var first = str_arr[visited[i]["prev"] - 1] == "-" ? "" : str_arr[visited[i]["prev"] - 1] + " + ";
        var second =  len_value_map(visited[i]["node"], visited[i]["prev"]) == -1 ? "0" : len_value_map(visited[i]["node"], visited[i]["prev"]).toString();
        str_arr[visited[i].node - 1] = first + second;
        work_arr[visited[i].node - 1] = {"str": first + second, "prev": visited[i].prev};
    }
    verify_ready = true;
    return work_arr;
}
function len_hovered(len_hitbox){
    if (verify_ready){
        var nodes = len_hitbox.data("id").replace("h", "").replace("v", "").split("-")
        // instructtxt.attr("text", nodes);
        var poss1 = verify_arr[parseInt(nodes[0]) - 1].prev == parseInt(nodes[1]) ? parseInt(nodes[0]) : -1
        var poss2 = verify_arr[parseInt(nodes[1]) - 1].prev == parseInt(nodes[0]) ? parseInt(nodes[1]) : -1
        var node = poss1 == -1 ? poss2 : poss1
        // instructtxt.attr("text", nodes);
        if (node != -1){
            var text_graphic = len_text_map(node, verify_arr[node  - 1].prev);
            text_graphic.attr("text", verify_arr[node - 1].str);
            text_graphic.attr("stroke", "#FF0000")
            text_graphic.attr("fill", "#FF0000")

        }
    }
}
function is_node_in(node, set){
    var i;
    for (i =0; i < set.length; i++){
        if (set[i] == node){
            return true;
        }
    }
    return false;
}
function restart(){
    //Set tables and colors to be as in the beggining, algorithm state to start, clickables to nothing; start node = something else if neccessary
    restart_graph(value_map, previous_map);
    restart_algorithm();
    set_graph(0);
    algo_state = AlgoStateEnum.Start
    ff_enabled = false;
    verify_eligible = false;
    verify_ready = false;
    verify_arr = [];
}
function algorithm_step(node_id, is_ff) {
    //Update tables and
    if (is_ff == false || ff_enabled) {
        node_in[node_id - 1] = 1;
        clickables = get_clickables(algo_state, node_id);
        increment_iteration()
        setTable(value_map, previous_map, false);
        setLensAndNodes(visited);
        //instructtxt.attr("text", is_node_in(2, clickables.node));
        // ffh.animate({opacity: 0} , 600, function () {
        //     highlight_nodes(clickables["highlight"]);
        // })

        positiveText();

        if (clickables.node.length == 0){
            verify_eligible = true;
            complete_text();
        }
    }
}
function algorithm_step_pt2(is_ff){
    if (is_ff){
        ffh.animate({opacity: 0} , 600, function () {
            if (ff_enabled) {
                highlight_nodes(clickables["highlight"]);
            }
        })
    } else{
        highlight_nodes(clickables["highlight"]);
    }
}
function node_clicked(node) {
    var id = parseInt(node.data("id").replace("n", ""));
    if (algo_state == AlgoStateEnum.Start && id == start_node ){
        algorithm_step(id,false);
        algorithm_step_pt2(false);
    } else {
        if (is_node_in(id, clickables.node)){
            algorithm_step(id,false);
            algorithm_step_pt2(false);
        } else{
            reject(id)
        }
    }
}


//TODO: set start node
function edit_clicked() {

    edge_indices = new Array(15).fill([]).map(x => new Array(15).fill(undefined));
    edge_indices[9][10] = 0
    edge_indices[3][4] = 1
    edge_indices[4][5] = 2
    edge_indices[5][6] = 3
    edge_indices[6][7] = 4
    edge_indices[7][8] = 5
    edge_indices[14][4] = 6
    edge_indices[9][13] = 7
    edge_indices[13][14] = 8
    edge_indices[7][9] = 9
    edge_indices[8][9] = 10
    edge_indices[14][7] = 11
    edge_indices[14][5] = 12
    edge_indices[13][7] = 13
    edge_indices[14][3] = 14
    edge_indices[2][14] = 15
    edge_indices[12][13] = 16
    edge_indices[1][14] = 17
    edge_indices[1][11] = 18
    edge_indices[11][12] = 19
    edge_indices[1][12] = 20
    edge_indices[1][2] = 21
    edge_indices[2][12] = 22
    edge_indices[2][3] = 23
    edge_indices[12][3] = 24
    edge_indices[10][12] = 25
    edge_indices[10][11] = 26


    var node1;
    var node2;
    var new_value;
    while(true){
        var val = prompt("What is the first node of the length you want to change?", "");
        if (!isNaN(val) && parseInt(val) > 0 && parseInt(val) < 15){
            node1 = parseInt(val);
            break;
        } else {
            alert("This is not an acceptable node")
            return;
        }
    }
    while(true){
        var val = prompt("What is the second node of the length you want to change?", "");
        if (!isNaN(val) && parseInt(val) > 0 && parseInt(val) < 15){
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
    if (edge_indices[node1][node2] == undefined && edge_indices[node2][node1] == undefined){
        alert("No such edge")
    } else {

        if (visited_index != 0) {
            restart();
        }
        var i = edge_indices[node1][node2] == undefined ? edge_indices[node2][node1] : edge_indices[node1][node2]
        len_values[i] = new_value
        set_len_values(false);
        len_texts[i].attr("stroke", "red")
        len_texts[i].attr("fill", "red")
    }

    // graphtype = graphtype + 1 == TOTAL_GRAPHS ? 0 : graphtype + 1;
    // set_graph(graphtype);
}
function reset_clicked() {
    restart();
}
function hi(){
    instructtxt.attr("text", "???!")
}
function inspect_clicked() {
    if (verify_eligible){
        verify_arr = verify_work();
        verify_message();
    }
}

function ff_clicked() {
    // instructtxt.attr("text", "HERE!")
    ff_enabled = true;
    recursive_animate()
}


