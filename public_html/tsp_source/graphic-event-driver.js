const PART_1_EVENT_NAME = "part 1"
const PART_2A_EVENT_NAME = "part 2a"
const PART_2B_EVENT_NAME = "part 2b"
const PART_3_EVENT_NAME = "part 3"

function basic(){
    restart.click(function (){
        restart_clicked();
    })
    back.click(function (){
        back_clicked();
    })
}

function part2(rsr, canvas, x, y, norm, next_part_name){
    was_part_2 = true;
    Graph_Grid(rsr, x, y, norm, mode_heur_type_enum.RANDOM, next_part_name);
    basic();

    two_opt_mode.click(function (){
        two_opt_clicked();
    })

    ri_clicked()
    nearest_neighbor_g.attr({fill: normal_stroke_color})
    random_insertion_g.attr({fill: "#DC8578"})
    nearest_insertion_g.attr({fill: normal_stroke_color})
    furthest_insertion_g.attr({fill: normal_stroke_color})
    text_event(text_event_type_enum.SELECT)

    random_insertion_g.click(function (){
        ri_clicked()
        nearest_neighbor_g.attr({fill: normal_stroke_color})
        random_insertion_g.attr({fill: "#DC8578"})
        nearest_insertion_g.attr({fill: normal_stroke_color})
        furthest_insertion_g.attr({fill: normal_stroke_color})
        text_event(text_event_type_enum.SELECT)
    })
    nearest_neighbor_g.click(function (){
        nn_clicked()
        nearest_neighbor_g.attr({fill: "#DC8578"})
        random_insertion_g.attr({fill: normal_stroke_color})
        nearest_insertion_g.attr({fill: normal_stroke_color})
        furthest_insertion_g.attr({fill: normal_stroke_color})
        text_event(text_event_type_enum.SELECT)
    })
    nearest_insertion_g.click(function (){
        ni_clicked()
        nearest_neighbor_g.attr({fill: normal_stroke_color})
        random_insertion_g.attr({fill: normal_stroke_color})
        nearest_insertion_g.attr({fill: "#DC8578"})
        furthest_insertion_g.attr({fill: normal_stroke_color})
        text_event(text_event_type_enum.SELECT)
    })
    furthest_insertion_g.click(function (){
        fi_clicked()
        nearest_neighbor_g.attr({fill: normal_stroke_color})
        random_insertion_g.attr({fill: normal_stroke_color})
        nearest_insertion_g.attr({fill: normal_stroke_color})
        furthest_insertion_g.attr({fill: "#DC8578"})
        text_event(text_event_type_enum.SELECT)
    })
}
function part2a(rsr, canvas, metric){

    part2(rsr, canvas, 6, 8, metric, "Part 2b: 9 x 9 Grid");
    next_part.click(function (){
        restart_clicked()
        canvas.dispatchEvent(new CustomEvent(PART_2B_EVENT_NAME, {
            detail : null
        }));
    })

    next_part.hover(function () {
        this.attr({fill : "#DC8578"})
    }, function () {
        this.attr({fill : "#8E8D8B"})
    })

    if (metric == metric_type_enum.MANHATTAN) {
        manhattan_mode.attr({fill: "#DC8578"})
    } else {
        euclidian_mode.attr({fill: "#DC8578"})
    }

    manhattan_mode.click(function(){
        part2a(rsr, canvas, metric_type_enum.MANHATTAN)
        manhattan_mode.attr({fill: "#DC8578"})


    })
    euclidian_mode.click(function(){
        part2a(rsr, canvas, metric_type_enum.EUCLIDIAN)
        euclidian_mode.attr({fill: "#DC8578"})
    })

}
function part2b(rsr, canvas, metric){
    part2(rsr, canvas, 9, 9, metric, "Part 3: 2-Opt")
    next_part.click(function (){
        restart_clicked()
        canvas.dispatchEvent(new CustomEvent(PART_3_EVENT_NAME, {
            detail : null
        }));
    })

    next_part.hover(function () {
        this.attr({fill : "#DC8578"})
    }, function () {
        this.attr({fill : "#8E8D8B"})
    })

    if (metric == metric_type_enum.MANHATTAN) {
        manhattan_mode.attr({fill: "#DC8578"})
    } else {
        euclidian_mode.attr({fill: "#DC8578"})
    }

    manhattan_mode.click(function(){
        part2b(rsr, canvas, metric_type_enum.MANHATTAN)
        manhattan_mode.attr({fill: "#DC8578"})
        restart_clicked();
    })
    euclidian_mode.click(function(){
        part2b(rsr, canvas, metric_type_enum.EUCLIDIAN)
        euclidian_mode.attr({fill: "#DC8578"})
        restart_clicked();
    })
}
function part3(rsr, canvas){
    Graph_two_opt(rsr);
    was_part_2 = false

    basic();
    /*
    optimize.click(function (){
        if (is_end){
            toss = mode_heur_type_enum.TWOOPT;
            text_event(text_event_type_enum.TWOOPTSTART);
            is_end = false;
        }
    })
    */

    next_part.click(function (){
        restart_clicked()
        canvas.dispatchEvent(new CustomEvent(PART_1_EVENT_NAME, {
            detail : null
        }));
    })

    next_part.hover(function () {
        this.attr({fill : "#DC8578"})
    }, function () {
        this.attr({fill : "#8E8D8B"})
    })
}

function part1(rsr, canvas){
    was_part_2 = false
    //instructxt.attr("text", "part 3");
    Graph_Beyonce(rsr)

    nodes_hitbox_arr.forEach(element => {
        element.click(function (){
            node_clicked(element);
        })
    });

    basic();
    next_part.click(function (){
        restart_clicked()
        canvas.dispatchEvent(new CustomEvent(PART_2A_EVENT_NAME, {
            detail : {norm : metric_type_enum.EUCLIDIAN, x : 9, y : 9 }
        }));
    })

    next_part.hover(function () {
        this.attr({fill : "#DC8578"})
    }, function () {
        this.attr({fill : "#8E8D8B"})
    })
}