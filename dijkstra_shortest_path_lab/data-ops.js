//BFS through the whole graph, creating a "previous", data scructure.
var graphtype = 1;
var ff_enabled = true;
var algo_state = AlgoStateEnum.Middle
var test_iter = 0;
var verify_eligible = false;
var verify_ready = false;
var verify_arr = [];

function recursive_animate(){
    ffh.animate({opacity: 0} , 1200, function () {
        algorithm_step(clickables.node[0]);
        algorithm_step_pt2(true);
        if (clickables.node.length > 0){
            recursive_animate()
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
    ff_enabled = true;
    verify_eligible = false;
    verify_ready = false;
    verify_arr = [];
    //alert(clickables)
    //highlight_nodes(clickables["highlight"]) // Henry: added to un-highlight nodes
}
function algorithm_step(node_id) {
    //Update tables and
    node_in[node_id - 1] = 1;
    clickables = get_clickables(algo_state, node_id);
    increment_iteration()
    setTable(value_map, previous_map);
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
function algorithm_step_pt2(is_ff){
    if (is_ff){
        ffh.animate({opacity: 0} , 600, function () {
            highlight_nodes(clickables["highlight"]);
        })
    } else{
        highlight_nodes(clickables["highlight"]);
    }
}
function node_clicked(node) {
    var id = parseInt(node.data("id").replace("n", ""));
    if (algo_state = AlgoStateEnum.Start && id == start_node ){
        algorithm_step(id);
        algorithm_step_pt2(false);
    } else {
        if (is_node_in(id, clickables.node)){
            algorithm_step(id);
            algorithm_step_pt2(false);
        } else{
            reject(id);
        }
    }
}


//TODO: set start node
function edit_clicked() {
    if (graphtype == 1){
        graphtype = 2;
        set_graph2();
        restart();
    } else{
        graphtype = 1;
        set_graph1();
        restart();
    }
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
    if (ff_enabled){
        ff_enabled = false;
        recursive_animate()
    }
}


