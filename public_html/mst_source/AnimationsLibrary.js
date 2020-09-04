let standard_hover = function(element){
    element.hover( function () {
        this.attr("font-weight", 800);

   },
   function () {
        this.attr("font-weight", 400);
   });
}
let reject_length = function(element, is_selected){
    var stroke_val = is_selected ? "#000000" : "#8e8d8a";
    var ani = Raphael.animation({stroke: "#FF0000"}, 200, "linear", function (){
        element.animate({stroke : stroke_val})
    });
    var ani2 = ani.repeat(3);
    element.animate(ani2);
}
let hint_length = function(element){
    var pre_val = element.attr("stroke")
    var stroke_val = "1A99EE"

    callback(0);
    function callback(n){
        if (n<6){
            element.animate({stroke: stroke_val}, 190, "linear", function () {
                var id = element.data("id");
                var nodes = id.split("-");
                var node1 = parseInt(nodes[0]);
                var node2 = parseInt(nodes[1]);
                if (algo_type == AlgoTypeEnum["Rev-Kruskal"]) {
                    if (len_in_map[node1 - 1][node2 - 1] == 0 || len_in_map[node2 - 1][node1 - 1] == 0) {
                        element.attr({"stroke" : "#8e8d8a"})
                    } else {
                        element.animate({stroke: pre_val}, 10, "linear", callback.bind(null,n+1));
                    }
                } else {
                    if (len_in_map[node1 - 1][node2 - 1] == 1 || len_in_map[node2 - 1][node1 - 1] == 1) {
                        element.attr({"stroke" : "#000000"})
                    } else {
                        element.animate({stroke: pre_val}, 10, "linear", callback.bind(null,n+1));
                    }
                }
            });
        }
    }

    // var ani = Raphael.animation({stroke: stroke_val}, 200, "linear", function (){
    //     element.attr("stroke", pre_val);
    //     alert('done')
    // });
    // var ani2 = ani.repeat(6);
    // element.animate(ani2);

}
let reject_node = function(element){
    var fill_val = element.attr("fill")
    var ani = Raphael.animation({stroke: "#FF0000"}, 200, "linear", function (){
        len.animate({fill : fill_val})
    });
    var ani2 = ani.repeat(3);
    len.animate(ani2);
}