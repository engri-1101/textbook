var rsr
var canvas

window.onload = function (){
    var w = 400
    var h = 400
    rsr = new Raphael(document.getElementById('canvas_container'), 1500, 1500);
    rsr.setViewBox(0, 0, w, h, true);
    canvas = document.getElementById('canvas_container');

    canvas.addEventListener(PART_1_EVENT_NAME, function(event) {
        part1(rsr, canvas)
    });

    canvas.addEventListener(PART_2_EVENT_NAME, function(event) {
        part2(rsr, canvas)

    });


    canvas.dispatchEvent(new CustomEvent(PART_1_EVENT_NAME, {
        detail: null
    }));
}