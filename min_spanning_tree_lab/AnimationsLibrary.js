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
    var ani = Raphael.animation({stroke: stroke_val}, 200, "linear", function (){
        element.attr("stroke", pre_val);
    });
    var ani2 = ani.repeat(6);
    element.animate(ani2);
}
let reject_node = function(element){
    var fill_val = element.attr("fill")
    var ani = Raphael.animation({stroke: "#FF0000"}, 200, "linear", function (){
        len.animate({fill : fill_val})
    });
    var ani2 = ani.repeat(3);
    len.animate(ani2);
}