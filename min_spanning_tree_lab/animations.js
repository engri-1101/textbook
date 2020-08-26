var is_start = 1;
const TEXT_EVENT_ENUM = {START_NODE : "snode", START_EDGE : "sedge", PICK_ONE : "pkone", PICK_ONE_HIGHLIGHT : "pkoneh", NEGATIVE_PROMPT : "Tryagain", POSITIVE_PROMPT : "goodjob", END : "end", FFFAIL : "fffail"}


let text_event = function(type){
     switch (type){
          case TEXT_EVENT_ENUM.START_EDGE : primary_text.attr("text", "Click the first edge to start"); break;
          case TEXT_EVENT_ENUM.START_NODE : primary_text.attr("text","Click the first node to start"); break;
          case TEXT_EVENT_ENUM.PICK_ONE : primary_text.attr("text","Pick one of these!"); break;
          case TEXT_EVENT_ENUM.NEGATIVE_PROMPT : primary_text.attr("text", "Try again"); break;
          case TEXT_EVENT_ENUM.PICK_ONE_HIGHLIGHT : primary_text.attr("text","Pick one of the highlighted ones!"); break;
          case TEXT_EVENT_ENUM.POSITIVE_PROMPT : primary_text.attr("text","Good job, pick the next one!"); break;
          case TEXT_EVENT_ENUM.END : primary_text.attr("text","Good job you found an MST!"); break;
          case TEXT_EVENT_ENUM.FFFAIL : primary_text.attr("text", "You must select a node before you fan fast foward with Prims algorithm"); break;
     }
}

let cost_text_event = function(val){
    secondary_text.attr("text", "Total Cost "+val);
}
//lens is a different data structure here than normal, it is a bunch of ids
//rather than a 2D array
let hint_visual = function(lens, len_map){
     lens.forEach(element => {
          var nodes = element.split("-");
          var node1 = nodes[0];
          var node2 = nodes[1];
          var len = len_map(parseInt(node1), parseInt(node2));
          hint_length(len);
     })
}
let select_all_nodes_visual = function(nodes){
     general_all_nodes_visual(nodes, select_node_visual)
}
let deselect_all_nodes_visual = function(nodes){
     general_all_nodes_visual(nodes, deselect_node_visual)
}
let select_all_lens_visual = function(lens){
     general_all_lens_visual(lens, select_len_visual)
}
let deselect_all_lens_visual = function(lens){
     general_all_lens_visual(lens, deselect_len_visual)
}
let general_all_lens_visual = function(lens, fn){
     lens.forEach(element => {
          element.forEach(v => {
               if (v != undefined && v != null){
                    fn(v)
               }
          })
     })
}
let general_all_nodes_visual = function(nodes, fn){
     nodes.forEach(function (value, index, array) {
          fn(value)
     });
}
let select_len_visual = function(len){
    len.attr("stroke", "#000000");
}
let deselect_len_visual = function(len){
    len.attr("stroke", "#8e8d8a")
}
let deselect_node_visual = function(node){
    node.attr("fill", "#e98074");
}
let select_node_visual = function(node){
    node.attr("fill", '#0677a1')
}
// let highlight_len_visual = function(len, stroke){
//      var ani = Raphael.animation({stroke: "#0677a1"}, 5000, "linear", function (){
//           len.animate({stroke: stroke_col })
//      });
//      var ani2 = ani//ani.repeat(9);
//      len.animate(ani2);
// }
// let arbitrary_color_node_visual = function(node,val){
//      node.attr("fill", val);
// }