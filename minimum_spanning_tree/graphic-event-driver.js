const PART_1_EVENT_NAME = "part 1"
const PART_2_EVENT_NAME = "part 2"

let nodes_function = function(hitbox,index, array){
    var node = nodes[index];
    node_hover(node, hitbox);
    node_click_handle(node, hitbox);
}

let lens_hitbox_function = function(x_index, y_index, len_h){
    var len = lens[y_index][x_index]
    len_hover(x_index, y_index, len, len_h);
    len_click_handle(len, len_h);
}

let basic = function(){

    standard_hover(kruskals_button);
    standard_hover(prims_button);
    standard_hover(rkruskals_button);
    standard_hover(hint_button);
    standard_hover(fast_foward_button);
    standard_hover(restart_button);
    //standard_hover(swap_graph_button);
    standard_hover(sensitivity_button);
    standard_hover(restore_button);
    reset();
    nodes_hitboxes.forEach(nodes_function)
    lens_hitboxes.forEach(function(x, y_index, array){
        x.forEach(function(len_h, x_index, array2){
            if (len_h != undefined){
                lens_hitbox_function(x_index, y_index, len_h)
            }
        })
    })

    restart_button.click( function () {reset()})
    kruskals_button.click(kruskals_clicked)
    rkruskals_button.click(r_kruskals_clicked)
    prims_button.click(prims_clicked)
    hint_button.click(hint_clicked)
    fast_foward_button.click(fast_foward_clicked)
    sensitivity_button.click(sensitivity_clicked);
    restore_button.click(restore_clicked);
    prims_clicked()

}

let part1 = function(rsr, canvas){
    Graph1(rsr);
    basic()
}
let part2 = function(rsr, canvas){
    Graph2(rsr)
    basic()
}