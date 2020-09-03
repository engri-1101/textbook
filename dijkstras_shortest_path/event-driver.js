window.onload = function () {
     var w = 400
     var h = 400
     var rsr = new Raphael(document.getElementById('canvas_container'), 1500, 1500);
     rsr.setViewBox(0, 0, w, h, true);

    Graph1(rsr);
    //extract lens here

    nodes.forEach(element => {
        element.click(function () {
            node_clicked(element);
        })
        element.hover(function () {
            color_node(element)
        }, function () {
            de_color_node(element)
        })
    })

    node_texts.forEach(element_in => {
        var node_in = node_map(parseInt(element_in.data("id").replace("q","")));
        element_in.click(function () {
            node_clicked(node_in);
        })
        element_in.hover(function () {
            color_node(node_in)
        }, function () {
            de_color_node(node_in)
        })
    })


    len_hitboxes.forEach(element => {
        element.hover(function () {
            len_hovered(element);
        }, function () {
            if (verify_ready){
                set_len_values();
            }
        })
    })

    edith.click(function (){
        edit_clicked();
    });
    edith.hover(function () {
        edit.forEach(element => {
            color_non_node(element);
        })
    }, function () {
        edit.forEach(element => {
            de_color_non_node(element);
        })
    })

    refreshh.click(function (){
        reset_clicked();
    })
    refreshh.hover(function () {
        color_non_node(refresh);

    }, function () {
        de_color_non_node(refresh);

    })

    // verifyh.click(function (){
    //     inspect_clicked()
    // });
    // verifyh.hover(function () {
    //     color_non_node(verify);

    // }, function () {
    //     de_color_non_node(verify);

    // })

    ffh.click(function (){
        ff_clicked();
    })
    ffh.hover(function () {
        color_non_node(ff);

    }, function () {
        de_color_non_node(ff);

    })
}
