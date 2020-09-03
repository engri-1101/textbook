window.onload = function () {
    var w = 400
    var h = 400
    var canvas = document.getElementById('canvas_container');
    var rsr = new Raphael(document.getElementById('canvas_container'), 1500, 1500);
    rsr.setViewBox(0, 0, w, h, true);


    canvas.addEventListener(PART_1_EVENT_NAME, function(event) {
        part1(rsr, canvas)
    });

    canvas.addEventListener(PART_2A_EVENT_NAME, function(event) {
        part2a(rsr, canvas, metric_type_enum.MANHATTAN)
    });
    canvas.addEventListener(PART_2B_EVENT_NAME, function(event){
        part2b(rsr, canvas, metric_type_enum.EUCLIDIAN)
    })
    canvas.addEventListener(PART_3_EVENT_NAME, function(event) {
        part3(rsr, canvas)
    });

    document.addEventListener("keyup", function(event) {
        if (event.code == "KeyA"){
            back_clicked()
        } else if (event.code == "KeyD"){
            foward_clicked()
        } else if (event.code == "KeyR"){
            restart_clicked()
        }
    });

    usImg.onload = function () {
        height = usImg.height
        width = usImg.width
        canvas.dispatchEvent(new CustomEvent(PART_1_EVENT_NAME, {
            detail: null
        }));
    }
    usImg.src = IMG_URL;
}