// var nodes;
// var kruskals_button;
// var prims_button;
// var rkruskals_button;
// var hint_button;
// var fast_foward_button;
// var restart_button;
// var swap_graph_button;

// var nodes;
// var nodes_hitboxes;
// var lens;
// var lens_hitboxes;

// var primary_text;
// var secondary_text;

// var len_data;
// var len_values;
// var nodes_centers


//TODO: refactor node_click
//TOOD: len_hover stuff

const TEXT_EVENT_ENUM = {START_NODE : "snode", START_EDGE : "sedge", SPECIAL_EDGE : "specedge"}
let node_hover_on_g = function(){
     // if (is_start == 1){
     //      this.attr('fill', '#0677a1');
     // }
}
let node_hover_off_g = function(){
     // if (is_start == 1){
     //      this.attr('fill', '#e98074');
     // }
}
//TODO: refactor the below completly
let node_click_event_g = function () {
     if (is_start == 1){
          start_node = parseInt(element.data("id").replace("n",""));
          is_start = 0;
          this.attr('fill', '#0677a1' );
          node_in_map[start_node - 1] = 1;
          text_event(TEXT_EVENT_ENUM.SPECIAL_EDGE)
          //TODO: refactor this most likley
          clickables = get_clickables(algo_state, algo_type, node_in_map, len_in_map, lens, len_map, value_map);
     }
}
let len_hover_on_g = function (){

}
let len_hover_off_g = function(){

}
let len_click_event_g = function (){

}
let text_event = function(type){
     switch (type){
          case TEXT_EVENT_ENUM.START_EDGE : primary_text.attr("Click the first edge to start"); break;
          case TEXT_EVENT_ENUM.START_NODE : primary_text.attr("Click the first node to start"); break;
          case TEXT_EVENT_ENUM.SPECIAL_EDGE : primary_text.attr("Now click the first edge!"); break;
     }
}
let get_len_from_hitbox = function(len_hitbox){
    var data = len_hitbox.data("id").split("-")
    var x = data[0]
    var y = data[1]
    return lens[x][y]
}