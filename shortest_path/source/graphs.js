var len_map_ds;
var nodes;
var ffh;
var instructtxt
var edith
var refreshh
var refresh;
var verifyh
var verify;
var ff
var edit
var lens
var values;
var len_value_ds;
var num_nodes;
var start_node = 1;
var node_in;
var highlight_cache = [];
const infinity = 10000
var table_int = 0;
var toptable;
var bottomtable;
var len_values
var len_texts;
var clickables;
var len_hitboxes;
var len_text_ds;
var node_texts;
var TOTAL_GRAPHS = 2;

const direction_array = ['f', 'b', 'f', 'f', 'f', 'f', 'f', 'b', 'b', 'b', 'b']

function verify_message(){
    instructtxt.attr("text", "You may mouse over lengths to verify the work!")
}
function complete_text(){
    instructtxt.attr("text", "Good job you found the shortest path!")
}
function len_map(i, j){
    var vee = "v"
    var str1 = vee.concat(i.toString(), "-", j.toString());
    var str2 = vee.concat(j.toString(), "-", i.toString());
    return len_map_ds.get(str1) != undefined ? len_map_ds.get(str1) : len_map_ds.get(str2);
}
function len_text_map(i, j){
    return len_text_ds.get(len_map(i, j).data("id"));
}
function color_node(node){
    if (node_in[parseInt(node.data("id").replace("n","")) - 1] == 0){
        node.attr("fill", '#0677a1')
    }
}
function color_non_node(element){
    element.attr("stroke", "#000000")
}
function de_color_node(node){
    if (node_in[parseInt(node.data("id").replace("n","")) - 1] == 0){
        node.attr("fill", "#e98074")
    }
}
function de_color_non_node(element){
    element.attr("stroke", "#8e8d8a")
}
function len_in_map(i, j){
    if (len_map(i,j) != undefined){
        return 1;
    } else{
        return 0;
    }
}
function len_value_map(i, j){
    if (len_in_map(i, j)){
        return len_value_ds.get(len_map(i,j));
    } else{
        return -1;
    }
}
function node_map(i){
    return nodes[i - 1]
}
//TODO: finish these functions, make it compile with factored out items, finish verify
function setTable(value_map, prev_map, restart) {
    var i;
    for (i = 0; i < num_nodes ; i++){
        if (restart) {
            // set bottom table to given maps
            labels_t2[i].attr("text", (value_map[i] == infinity ? "inf" : value_map[i].toString() + (node_in[i] == 1 ? "*" : "")));
            prev_t2[i].attr("text", (prev_map[i] == -1 ? "-" : prev_map[i].toString()));
        } else {
            // set bottom table to previous top table
            labels_t2[i].attr("text", labels_t1[i].attr("text"));
            prev_t2[i].attr("text", prev_t1[i].attr("text"));
        }
        labels_t1[i].attr("text", (value_map[i] == infinity ? "inf" : value_map[i].toString() + (node_in[i] == 1 ? "*" : "")));
        prev_t1[i].attr("text", (prev_map[i] == -1 ? "-" : prev_map[i].toString()));
        toptable.attr("text", "Table for iteration "+table_int)
        bottomtable.attr("text", "Table for iteration "+(table_int -1));
    }
}
function setLensAndNodes(visited){
    visited.forEach(element => {
        var i = element["node"]
        var j = element["prev"]
        var len = len_map(i, j);

        if (len_in_map(i, j) == 1) {
            len.attr("stroke", "#000000");
            node_map(i).attr("fill", '#0677a1');
            node_map(j).attr("fill", '#0677a1')
        }
    })
}
function highlight_nodes(highlight){
    var new_arr = highlight.map(x => x.value);

    highlight_cache.forEach(element => {
        var node = node_map(element);
        node.attr("stroke", "none");
    })


    highlight_cache = highlight_cache.concat(new_arr);
    highlight_cache = highlight_cache.filter(x => node_in[x - 1] == 0);

    highlight_cache.forEach(element => {
        var node = node_map(element);
        node.attr("stroke", "#0677a1");
    })
}

function positiveText(){
    instructtxt.attr("text", "Good job, now select the next node!");
}

function restart_graph(value_map, prev_map){
    table_int = 0;
    lens.forEach(element => {
        element.attr('stroke', "#8e8d8a")
    })
    nodes.forEach(element => {
        element.attr('fill', '#e98074')
        element.attr('stroke', 'none')
    })
    highlight_cache = []
    instructtxt.attr("text", "Select the first node to begin!");
    node_in = new Array(num_nodes).fill(0);
    var value_map = new Array(num_nodes).fill(infinity);
    var prev_map = new Array(num_nodes).fill(-1);
    setTable(value_map, prev_map, true);
}

function increment_iteration(){
    table_int++;
}

// function setGraphType1(){}
// function setGraphType2(){}
function setVerify(str_array, visited){
    // visited.forEach(element => {
    //     var i = element["node"]

    // })

}

function flow_direction(){

}

function set_graph(i) {
    len_values = [[14, 3, 3, 4, 2, 3, 8, 5, 2, 6, 6, 5, 7, 5, 8, 14, 12, 17, 2, 5, 3, 2, 3, 18, 19, 3, 1],
                  [14, 3, 3, 4, 2, 3, 8, 5, 2, 6, 6, 5, 7, 5, 8, 14, 12, 17, 2, 5, 3, 2, 3, 18, 19, 3, 30]][i]
    set_len_values(true);
}

function set_len_values(change){
    len_value_ds = new Map();
    var i;
    for (i = 0; i < lens.length; i++){
        len_value_ds.set(lens[i], len_values[i])
        len_texts[i].attr("text", len_values[i].toString());
        if (change) {
            len_texts[i].attr("stroke", "#8e8d8a")
            len_texts[i].attr("fill", "#8e8d8a")
        }
    }
}

function reject(node_id){
    var l_node = node_map(node_id)
    callback(0);
    function callback(n){
        if (n<3){
            l_node.animate({fill: "#FF0000"}, 190, "linear", function () {
                if (node_in[node_id-1] == 0) {
                    l_node.animate({fill: "#DC8578"}, 10, "linear", callback.bind(null,n+1));
                } else {
                    l_node.animate({fill:'#0677a1'}, 10, "linear", callback.bind(null,n+1));
                }
            });
        } else {
            if (node_in[node_id-1] == 0) {
                l_node.attr({fill: "#DC8578"})
            } else{
                l_node.attr({fill:"#0677a1"});
            }
        }
    }

//    var ani2 = ani.repeat(3);
//    l_node.animate(ani2);
//    instructtxt.attr("text", "Try again! (ties broken arbitrarily)")
}

function Graph1(rsr){
    var layer4 = rsr.set();
    layer4.attr({'id': 'layer4','name': 'layer4'});
    var layer2 = rsr.set();
    //instructtxt = rsr.text(109.49885, 21.746574, 'Click node one to start!').attr({id: 'instruct-txt',parent: 'layer2',"font-style": 'normal',"font-variant": 'normal',"font-weight": 'normal',"font-stretch": 'normal',"font-size": '10.58333302px',"line-height": '1.25',"font-family": 'sans-serif',"-inkscape-font-specification": 'sans-serif, Normal',"font-variant-ligatures": 'normal',"font-variant-caps": 'normal',"font-variant-numeric": 'normal',"font-feature-settings": 'normal',"text-align": 'center',"letter-spacing": '0px',"word-spacing": '0px',"writing-mode": 'lr-tb',"text-anchor": 'middle',fill: '#8e8d8a',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'instructtxt');
    var v910 = rsr.path("M 132.82083,134.41354 148.23281,49.879173").attr({id: 'v9-10',parent: 'layer2',display: 'inline',opacity: '1',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v9-10');
    var v34 = rsr.path("m 50.932291,122.70573 9.32656,14.02292").attr({id: 'v3-4',parent: 'layer2',display: 'inline',opacity: '1',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v3-4');
    var v45 = rsr.path("m 60.258851,136.72865 8.598958,12.03854").attr({id: 'v4-5',parent: 'layer2',display: 'inline',opacity: '1',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v4-5');
    var v56 = rsr.path("m 68.857809,148.76719 14.948958,0.19844").attr({id: 'v5-6',parent: 'layer2',display: 'inline',opacity: '1',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v5-6');
    var v67 = rsr.path("m 83.806767,148.96563 11.773958,-4.23334").attr({id: 'v6-7',parent: 'layer2',display: 'inline',opacity: '1',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v6-7');
    var v78 = rsr.path("m 94.985413,157.82917 0.59531,-13.09688").attr({id: 'v7-8',parent: 'layer2',display: 'inline',opacity: '1',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v7-8');
    var v144 = rsr.path("M 60.258851,136.72865 106.49479,118.27396").attr({id: 'v14-4',parent: 'layer2',display: 'inline',opacity: '1',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v14-4');
    var v913 = rsr.path("m 120.5177,117.74479 12.30313,16.66875").attr({id: 'v9-13',parent: 'layer2',display: 'inline',opacity: '1',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v9-13');
    var v1314 = rsr.path("m 106.49479,118.27396 14.02291,-0.52917").attr({id: 'v13-14',parent: 'layer2',display: 'inline',opacity: '1',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v13-14');
    var v79 = rsr.path("M 95.580723,144.73229 132.82083,134.41354").attr({id: 'v7-9',parent: 'layer2',display: 'inline',opacity: '1',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v7-9');
    var v89 = rsr.path("M 94.985413,157.82917 132.82083,134.41354").attr({id: 'v8-9',parent: 'layer2',display: 'inline',opacity: '1',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v8-9');
    var v147 = rsr.path("M 106.49479,118.27396 95.580723,144.73229").attr({id: 'v14-7',parent: 'layer2',display: 'inline',opacity: '1',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v14-7');
    var v145 = rsr.path("M 68.857809,148.76719 106.49479,118.27396").attr({id: 'v14-5',parent: 'layer2',display: 'inline',opacity: '1',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v14-5');
    var v137 = rsr.path("M 95.580723,144.73229 120.5177,117.74479").attr({id: 'v13-7',parent: 'layer2',display: 'inline',opacity: '1',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v13-7');
    var v143 = rsr.path("m 106.49479,118.27396 -55.562499,4.43177").attr({id: 'v14-3',parent: 'layer2',display: 'inline',opacity: '1',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v14-3');
    var v214 = rsr.path("m 111.59839,44.710937 -5.1036,73.563023").attr({id: 'v2-14',parent: 'layer2',display: 'inline',opacity: '1',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v2-14');
    var v1213 = rsr.path("m 120.5177,117.74479 6.70259,-54.324989").attr({id: 'v12-13',parent: 'layer2',display: 'inline',opacity: '1',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v12-13');
    var v114 = rsr.path("M 106.49479,118.27396 127.0332,40.220807").attr({id: 'v1-14',parent: 'layer2',display: 'inline',opacity: '1',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v1-14');
    var v111 = rsr.path("M 141.15839,40.875619 127.0332,40.220807").attr({id: 'v11-1',parent: 'layer2',display: 'inline',opacity: '1',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v11-1');
    var v1112 = rsr.path("m 127.22029,63.419801 13.9381,-22.544182").attr({id: 'v11-12',parent: 'layer2',display: 'inline',opacity: '1',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v11-12');
    var v112 = rsr.path("m 127.0332,40.220807 0.18709,23.198994").attr({id: 'v1-12',parent: 'layer2',display: 'inline',opacity: '1',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v1-12');
    var v12 = rsr.path("m 111.59839,44.710937 15.43481,-4.49013").attr({id: 'v1-2',parent: 'layer2',display: 'inline',opacity: '1',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v1-2');
    var v212 = rsr.path("m 111.59839,44.710937 15.6219,18.708864").attr({id: 'v2-12',parent: 'layer2',display: 'inline',opacity: '1',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v2-12');
    var v23 = rsr.path("M 50.932291,122.70573 111.59839,44.710937").attr({id: 'v2-3',parent: 'layer2',display: 'inline',opacity: '1',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v2-3');
    var v123 = rsr.path("M 127.22029,63.419801 50.932291,122.70573").attr({id: 'v12-3',parent: 'layer2',display: 'inline',opacity: '1',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v12-3');
    var v1012 = rsr.path("M 127.22029,63.419801 148.23281,49.879173").attr({id: 'v10-12',parent: 'layer2',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v10-12');
    var v1011 = rsr.path("m 141.15839,40.875619 7.07442,9.003554").attr({id: 'v10-11',parent: 'layer2',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v10-11');
    layer2.attr({'id': 'layer2','style': 'display:inline','name': 'layer2'});

    refresh = rsr.set();
    var path907 = rsr.path("m 65.362914,255.16111 c 1.582786,-1.58279 3.769384,-2.56176 6.184633,-2.56176 4.830499,0 8.746392,3.91589 8.746395,8.74639 3e-6,4.8305 -3.915892,8.7464 -8.746395,8.7464 -4.830503,0 -8.746398,-3.9159 -8.746395,-8.7464").attr({id: 'path907',parent: 'layer2',opacity: '1',fill: 'none',"fill-opacity": '1',stroke: '#8e8d8a',"stroke-width": '1.3',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).transform("m0.68898241,-0.68898241,0.68898241,0.68898241,-123.01125,69.765656").data('id', 'path907');
    var path927 = rsr.path("m 62.508873,260.2886 c 2.245059,2.24505 2.250905,2.2509 2.250905,2.2509").attr({id: 'path927',parent: 'layer2',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).transform("m0.68898241,-0.68898241,0.68898241,0.68898241,-123.01125,69.765656").data('id', 'path927');
    var path9273 = rsr.path("m 63.199798,260.29879 c -2.24506,2.24506 -2.2509,2.2509 -2.2509,2.2509").attr({id: 'path927-3',parent: 'layer2',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).transform("m0.68898241,-0.68898241,0.68898241,0.68898241,-123.01125,69.765656").data('id', 'path9273');
    refresh.attr({'id': 'refresh','style': 'display:inline','parent': 'layer2','name': 'refresh'});
    refresh.transform("m0.68898241,-0.68898241,0.68898241,0.68898241,-123.01125,69.765656");
    ff = rsr.set();
    var hff = rsr.rect(155.54523, 190.49792, 28.511898, 16.814631).attr({y: '190.49792',x: '155.54523',id: 'h-ff',parent: 'layer2',display: 'inline',opacity: '0',fill: '#8e8d8a',"fill-opacity": '1',stroke: '#8e8d8a',"stroke-width": '5.8',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).transform("m0.87756773,0,0,0.87756773,18.164657,25.980457").data('id', 'hff');
    var p1ff = rsr.path("m 160.80887,193.05662 v 11.69725 l 10.52745,-5.84862 z").attr({id: 'p1-ff',parent: 'layer2',display: 'inline',fill: 'none',"fill-opacity": '1',stroke: '#8e8d8a',"stroke-width": '1.35',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).transform("m0.87756773,0,0,0.87756773,18.164657,25.980457").data('id', 'p1ff');
    var p2ff = rsr.path("m 173.96818,193.05661 v 11.69725 l 10.52745,-5.84863 z").attr({id: 'p2-ff',parent: 'layer2',display: 'inline',fill: 'none',"fill-opacity": '1',stroke: '#8e8d8a',"stroke-width": '1.35',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).transform("m0.87756773,0,0,0.87756773,18.164657,25.980457").data('id', 'p2ff');
    ff.attr({'id': 'ff','style': 'display:inline','parent': 'layer2','name': 'ff'});
    ff.transform("m0.87756773,0,0,0.87756773,18.164657,25.980457");
    verify = rsr.set();
    var path987 = rsr.circle(123, 200, 8).attr({id: 'path987',parent: 'layer2',opacity: '1',fill: 'none',"fill-opacity": '1',stroke: '#8e8d8a',"stroke-width": '1.6',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).transform("m0.87756773,0,0,0.87756773,13.819233,23.691555").data('id', 'path987');
    var path989 = rsr.path("m 130.17552,205.99144 11.97538,8.15823").attr({id: 'path989',parent: 'layer2',fill: '#8e8d8a',"fill-opacity": '1',stroke: '#8e8d8a',"stroke-width": '1.6',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).transform("m0.87756773,0,0,0.87756773,13.819233,23.691555").data('id', 'path989');
    var path949 = rsr.path("m 123.44779,202.87737 4.83058,-4.8306").attr({id: 'path949',parent: 'layer2',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.28',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).transform("m0.87756773,0,0,0.87756773,13.819233,23.691555").data('id', 'path949');
    var path9497 = rsr.path("m 128.17545,198.14502 4.83058,-4.83058").attr({id: 'path949-7',parent: 'layer2',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.28',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).transform("m0.87756773,0,0,0.87756773,13.819233,23.691555").data('id', 'path9497');
    var path94978 = rsr.path("m 132.81658,193.49923 4.8306,-4.83059").attr({id: 'path949-7-8',parent: 'layer2',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.28',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).transform("m0.87756773,0,0,0.87756773,13.819233,23.691555").data('id', 'path94978');
    var path94977 = rsr.path("m 124.31701,202.83179 -4.83059,-4.83059").attr({id: 'path949-7-7',parent: 'layer2',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.28',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).transform("m0.87756773,0,0,0.87756773,13.819233,23.691555").data('id', 'path94977');
    verify.attr({'id': 'verify','style': 'display:inline','parent': 'layer2','name': 'verify'});
    verify.transform("m0.87756773,0,0,0.87756773,13.819233,23.691555");

    var g4691 = rsr.set();
    var path537732 = rsr.path("m 45.817428,84.706654 c 52.117551,0 52.117551,0 52.117551,0").attr({id: 'path5377-3-2',parent: 'layer2',display: 'inline',opacity: '0.75',fill: 'none',stroke: '#000000',"stroke-width": '0.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).transform("m1.0797791,0,0,1,173.43833,-25.161636").data('id', 'path537732');
    var path5377859 = rsr.path("m 97.934979,84.706654 c 96.529761,0 96.529761,0 96.529761,0").attr({id: 'path5377-8-5-9',parent: 'layer2',display: 'inline',opacity: '0.75',fill: 'none',stroke: '#000000',"stroke-width": '0.53',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).transform("m1.0797791,0,0,1,173.43833,-25.161636").data('id', 'path5377859');
    var path537787938 = rsr.path("m 45.817428,84.706654 c -19.54407,0 -19.54407,0 -19.54407,0").attr({id: 'path5377-87-9-3-8',parent: 'layer2',display: 'inline',opacity: '0.75',fill: 'none',stroke: '#000000',"stroke-width": '0.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).transform("m1.0797791,0,0,1,173.43833,-25.161636").data('id', 'path537787938');
    g4691.attr({'id': 'g4691','style': 'display:inline','parent': 'layer2','name': 'g4691'});
    g4691.transform("m1.0797791,0,0,1,173.43833,-25.161636");
    var g46913 = rsr.set();
    var path5377329 = rsr.path("m 45.817428,84.706654 c 52.117551,0 52.117551,0 52.117551,0").attr({id: 'path5377-3-2-9',parent: 'layer2',display: 'inline',opacity: '0.75',fill: 'none',stroke: '#000000',"stroke-width": '0.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).transform("m1.0797791,0,0,1,173.1045,38.71634").data('id', 'path5377329');
    var path53778595 = rsr.path("m 97.934979,84.706654 c 96.529761,0 96.529761,0 96.529761,0").attr({id: 'path5377-8-5-9-5',parent: 'layer2',display: 'inline',opacity: '0.75',fill: 'none',stroke: '#000000',"stroke-width": '0.53',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).transform("m1.0797791,0,0,1,173.1045,38.71634").data('id', 'path53778595');
    var path5377879389 = rsr.path("m 45.817428,84.706654 c -19.54407,0 -19.54407,0 -19.54407,0").attr({id: 'path5377-87-9-3-8-9',parent: 'layer2',display: 'inline',opacity: '0.75',fill: 'none',stroke: '#000000',"stroke-width": '0.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).transform("m1.0797791,0,0,1,173.1045,38.71634").data('id', 'path5377879389');
    g46913.attr({'id': 'g4691-3','style': 'opacity:0.5','parent': 'layer2','name': 'g46913'});
    g46913.transform("m1.0797791,0,0,1,173.1045,38.71634");
    var tablegroup = rsr.set();

    toptable = rsr.text(288.83893, 41.430828, 'Table for Iteration n').attr({id: 'top-table',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '10.58333302px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'toptable');
    var path53778768 = rsr.path("m 232.31313,55.875864 c 0,26.058777 0,26.058777 0,26.058777").attr({id: 'path5377-87-6-8',parent: 'layer2',display: 'inline',fill: 'none',stroke: '#000000',"stroke-width": '0.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'path53778768');
    var text5426603 = rsr.text(216.26816, 66.330467, 'Label').attr({id: 'text5426-60-3',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '10.58333302px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'text5426603');
    var t1a = rsr.text(239.99255, 65.576271, '22').attr({id: 't1-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't1a');
    var t2a = rsr.text(249.74902, 65.576271, '22').attr({id: 't2-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't2a');
    var t3a = rsr.text(259.50549, 65.576279, '22').attr({id: 't3-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't3a');
    var t4a = rsr.text(269.26218, 65.576271, '22').attr({id: 't4-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't4a');
    var t5a = rsr.text(279.01868, 65.576271, '22').attr({id: 't5-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't5a');
    var t6a = rsr.text(288.77521, 65.576279, '22').attr({id: 't6-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't6a');
    var t7a = rsr.text(298.53162, 65.576279, '22').attr({id: 't7-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't7a');
    var t8a = rsr.text(308.28833, 65.576279, '22').attr({id: 't8-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't8a');
    var t9a = rsr.text(318.04453, 65.576279, '22').attr({id: 't9-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't9a');
    var t10a = rsr.text(327.80118, 65.576271, '22').attr({id: 't10-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't10a');
    var t11a = rsr.text(337.55789, 65.576271, '22').attr({id: 't11-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't11a');
    var t12a = rsr.text(347.31406, 65.576279, '22').attr({id: 't12-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't12a');
    var t13a = rsr.text(357.0708, 65.576271, '22').attr({id: 't13-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't13a');
    var t14a = rsr.text(366.82758, 65.576279, '22').attr({id: 't14-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't14a');
    //var t15a = rsr.text(376.58374, 65.576279, '22').attr({id: 't15-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't15a');
    var text5426936 = rsr.text(214.80054, 76.443512, 'Prev').attr({id: 'text5426-9-3-6',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '10.58333302px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'text5426936');
    var t1b = rsr.text(239.76286, 75.785431, '22').attr({id: 't1-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't1b');
    var t2b = rsr.text(249.51935, 75.785431, '22').attr({id: 't2-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't2b');
    var t3b = rsr.text(259.27582, 75.785431, '22').attr({id: 't3-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't3b');
    var t4b = rsr.text(269.0325, 75.785431, '22').attr({id: 't4-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't4b');
    var t5b = rsr.text(278.78897, 75.785431, '22').attr({id: 't5-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't5b');
    var t6b = rsr.text(288.54553, 75.785431, '22').attr({id: 't6-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't6b');
    var t7b = rsr.text(298.30194, 75.785431, '22').attr({id: 't7-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't7b');
    var t8b = rsr.text(308.05862, 75.785431, '22').attr({id: 't8-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't8b');
    var t9b = rsr.text(317.81491, 75.785431, '22').attr({id: 't9-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't9b');
    var t10b = rsr.text(327.57156, 75.785431, '22').attr({id: 't10-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't10b');
    var t11b = rsr.text(337.32825, 75.785431, '22').attr({id: 't11-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't11b');
    var t12b = rsr.text(347.08444, 75.785431, '22').attr({id: 't12-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't12b');
    var t13b = rsr.text(356.84119, 75.785431, '22').attr({id: 't13-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't13b');
    var t14b = rsr.text(366.59796, 75.785431, '22').attr({id: 't14-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't14b');
    //var t15b = rsr.text(376.3541, 75.785431, '22').attr({id: 't15-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 't15b');
    var text542649040 = rsr.text(237.34673, 52.472904, '1').attr({id: 'text5426-4-9-0-4-0',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text542649040');
    var text5426436403 = rsr.text(247.1032, 52.500446, '2').attr({id: 'text5426-4-3-6-4-0-3',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text5426436403');
    var text54264374950 = rsr.text(256.85965, 52.467609, '3').attr({id: 'text5426-4-37-4-9-5-0',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text54264374950');
    var text54264063720 = rsr.text(266.61633, 52.467609, '4').attr({id: 'text5426-4-0-63-7-2-0',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text54264063720');
    var text5426457193 = rsr.text(276.3728, 52.434772, '5').attr({id: 'text5426-4-5-7-1-9-3',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text5426457193');
    var text54264583197 = rsr.text(286.12936, 52.464428, '6').attr({id: 'text5426-4-58-3-1-9-7',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text54264583197');
    var text54264359776 = rsr.text(295.88577, 52.467609, '7').attr({id: 'text5426-4-3-5-9-7-7-6',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text54264359776');
    var text542643771591 = rsr.text(305.64252, 52.467609, '8').attr({id: 'text5426-4-37-7-1-5-9-1',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text542643771591');
    var text54264065641 = rsr.text(315.3988, 52.46867, '9').attr({id: 'text5426-4-0-6-5-6-4-1',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text54264065641');
    var text54264599317 = rsr.text(325.15546, 52.466549, '10').attr({id: 'text5426-4-5-9-9-3-1-7',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text54264599317');
    var text5426420355 = rsr.text(334.91217, 52.472904, '11').attr({id: 'text5426-4-2-0-3-5-5',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text5426420355');
    var text54264398551 = rsr.text(344.66833, 52.500446, '12').attr({id: 'text5426-4-3-9-8-5-5-1',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text54264398551');
    var text542643705562 = rsr.text(354.42508, 52.467609, '13').attr({id: 'text5426-4-37-0-5-5-6-2',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text542643705562');
    var text54264030889 = rsr.text(364.18185, 52.472904, '14').attr({id: 'text5426-4-0-3-0-8-8-9',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text54264030889');
    //var text54264561476 = rsr.text(373.93802, 52.440067, '15').attr({id: 'text5426-4-5-6-1-4-7-6',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text54264561476');
    var text5426628 = rsr.text(216.37822, 53.254631, 'Node').attr({id: 'text5426-6-2-8',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '10.58333302px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'text5426628');
    var path537787576 = rsr.path("m 232.31313,46.448037 c 0,9.427827 0,9.427827 0,9.427827").attr({id: 'path5377-87-5-7-6',parent: 'layer2',display: 'inline',fill: 'none',stroke: '#000000',"stroke-width": '0.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'path537787576');
    bottomtable = rsr.text(288.5051, 105.30882, 'Table for Iteration n').attr({id: 'bottom-table',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '10.58333302px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'bottomtable');
    var path537787682 = rsr.path("m 231.97931,119.75384 c 0,26.05878 0,26.05878 0,26.05878").attr({id: 'path5377-87-6-8-2',parent: 'layer2',display: 'inline',opacity: '0.5',fill: 'none',stroke: '#000000',"stroke-width": '0.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'path537787682');
    var text54266032 = rsr.text(215.93434, 130.20844, 'Label').attr({id: 'text5426-60-3-2',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '10.58333302px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'text54266032');
    var z1a = rsr.text(239.65874, 129.45424, '22').attr({id: 'z1-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z1a');
    var z2a = rsr.text(249.41521, 129.45424, '22').attr({id: 'z2-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z2a');
    var z3a = rsr.text(259.17166, 129.45425, '22').attr({id: 'z3-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z3a');
    var z4a = rsr.text(268.92834, 129.45424, '22').attr({id: 'z4-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z4a');
    var z5a = rsr.text(278.68484, 129.45424, '22').attr({id: 'z5-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z5a');
    var z6a = rsr.text(288.44138, 129.45425, '22').attr({id: 'z6-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z6a');
    var z7a = rsr.text(298.19778, 129.45425, '22').attr({id: 'z7-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z7a');
    var z8a = rsr.text(307.95453, 129.45425, '22').attr({id: 'z8-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z8a');
    var z9a = rsr.text(317.71069, 129.45425, '22').attr({id: 'z9-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z9a');
    var z10a = rsr.text(327.46722, 129.45424, '22').attr({id: 'z10-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z10a');
    var z11a = rsr.text(337.22397, 129.45424, '22').attr({id: 'z11-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z11a');
    var z12a = rsr.text(346.98013, 129.45425, '22').attr({id: 'z12-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z12a');
    var z13a = rsr.text(356.73688, 129.45424, '22').attr({id: 'z13-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z13a');
    var z14a = rsr.text(366.49365, 129.45425, '22').attr({id: 'z14-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z14a');
    //var z15a = rsr.text(376.24982, 129.45425, '22').attr({id: 'z15-a',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z15a');
    var text54269368 = rsr.text(214.46671, 140.32149, 'Prev').attr({id: 'text5426-9-3-6-8',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '10.58333302px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'text54269368');
    var z1b = rsr.text(239.42905, 139.66342, '22').attr({id: 'z1-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z1b');
    var z2b = rsr.text(249.18552, 139.66342, '22').attr({id: 'z2-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z2b');
    var z3b = rsr.text(258.94199, 139.66342, '22').attr({id: 'z3-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z3b');
    var z4b = rsr.text(268.69867, 139.66342, '22').attr({id: 'z4-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z4b');
    var z5b = rsr.text(278.45514, 139.66342, '22').attr({id: 'z5-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z5b');
    var z6b = rsr.text(288.2117, 139.66342, '22').attr({id: 'z6-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z6b');
    var z7b = rsr.text(297.96808, 139.66342, '22').attr({id: 'z7-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z7b');
    var z8b = rsr.text(307.72482, 139.66342, '22').attr({id: 'z8-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z8b');
    var z9b = rsr.text(317.48105, 139.66342, '22').attr({id: 'z9-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z9b');
    var z10b = rsr.text(327.23761, 139.66342, '22').attr({id: 'z10-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z10b');
    var z11b = rsr.text(336.99435, 139.66342, '22').attr({id: 'z11-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z11b');
    var z12b = rsr.text(346.75052, 139.66342, '22').attr({id: 'z12-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z12b');
    var z13b = rsr.text(356.50726, 139.66342, '22').attr({id: 'z13-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z13b');
    var z14b = rsr.text(366.26404, 139.66342, '22').attr({id: 'z14-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z14b');
    //var z15b = rsr.text(376.0202, 139.66342, '22').attr({id: 'z15-b',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'z15b');
    var text5426490405 = rsr.text(237.01289, 116.35089, '1').attr({id: 'text5426-4-9-0-4-0-5',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text5426490405');
    var text54264364039 = rsr.text(246.76936, 116.37843, '2').attr({id: 'text5426-4-3-6-4-0-3-9',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text54264364039');
    var text542643749505 = rsr.text(256.52582, 116.34559, '3').attr({id: 'text5426-4-37-4-9-5-0-5',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text542643749505');
    var text542640637204 = rsr.text(266.2825, 116.34559, '4').attr({id: 'text5426-4-0-63-7-2-0-4',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text542640637204');
    var text54264571938 = rsr.text(276.03897, 116.31275, '5').attr({id: 'text5426-4-5-7-1-9-3-8',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text54264571938');
    var text542645831974 = rsr.text(285.79556, 116.34241, '6').attr({id: 'text5426-4-58-3-1-9-7-4',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text542645831974');
    var text542643597764 = rsr.text(295.55197, 116.34559, '7').attr({id: 'text5426-4-3-5-9-7-7-6-4',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text542643597764');
    var text5426437715910 = rsr.text(305.30865, 116.34559, '8').attr({id: 'text5426-4-37-7-1-5-9-1-0',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text5426437715910');
    var text542640656410 = rsr.text(315.06497, 116.34666, '9').attr({id: 'text5426-4-0-6-5-6-4-1-0',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text542640656410');
    var text542645993173 = rsr.text(324.8215, 116.34454, '10').attr({id: 'text5426-4-5-9-9-3-1-7-3',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text542645993173');
    var text54264203557 = rsr.text(334.57825, 116.35089, '11').attr({id: 'text5426-4-2-0-3-5-5-7',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text54264203557');
    var text542643985517 = rsr.text(344.33441, 116.37843, '12').attr({id: 'text5426-4-3-9-8-5-5-1-7',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text542643985517');
    var text5426437055621 = rsr.text(354.09116, 116.34559, '13').attr({id: 'text5426-4-37-0-5-5-6-2-1',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text5426437055621');
    var text542640308898 = rsr.text(363.84793, 116.35089, '14').attr({id: 'text5426-4-0-3-0-8-8-9-8',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text542640308898');
    //var text542645614769 = rsr.text(373.6041, 116.31805, '15').attr({id: 'text5426-4-5-6-1-4-7-6-9',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '9.29684258px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.23'}).data('id', 'text542645614769');
    var text54266283 = rsr.text(216.0444, 117.13261, 'Node').attr({id: 'text5426-6-2-8-3',parent: 'layer2',"font-style": 'normal',"font-weight": 'normal',"font-size": '10.58333302px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',display: 'inline',opacity: '0.5',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'text54266283');
    var path5377875762 = rsr.path("m 231.97931,110.32601 c 0,9.42783 0,9.42783 0,9.42783").attr({id: 'path5377-87-5-7-6-2',parent: 'layer2',display: 'inline',opacity: '0.5',fill: 'none',stroke: '#000000',"stroke-width": '0.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'path5377875762');
    tablegroup.attr({'id': 'table-group','style': 'display:inline','parent': 'layer2','name': 'tablegroup'});

    var g1603 = rsr.set();
    var path3119 = rsr.path("M 38.250789,197.48591 H 57.224688").attr({id: 'path3119',parent: 'layer2',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.58',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'path3119');
    var path3196 = rsr.path("m 51.803852,192.03117 6.030689,6.0307").attr({id: 'path3196',parent: 'layer2',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.58',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'path3196');
    var path31967 = rsr.path("m 57.834541,196.97769 -6.030689,6.03069").attr({id: 'path3196-7',parent: 'layer2',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.58',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'path31967');
    g1603.attr({'id': 'g1603','style': 'display:inline','parent': 'layer2','name': 'g1603'});
    var g1414 = rsr.set();
    var path31192 = rsr.path("M 116.86008,123.60724 H 103.63024").attr({id: 'path3119-2',parent: 'layer2',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.1',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).transform("m1.4341744,0,0,1.4341744,-109.08361,27.681494").data('id', 'path31192');
    var path31961 = rsr.path("m 107.41,127.41063 -4.20499,-4.20499").attr({id: 'path3196-1',parent: 'layer2',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.1',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).transform("m1.4341744,0,0,1.4341744,-109.08361,27.681494").data('id', 'path31961');
    var path319676 = rsr.path("M 103.20501,123.9616 107.41,119.75661").attr({id: 'path3196-7-6',parent: 'layer2',fill: 'none',stroke: '#8e8d8a',"stroke-width": '1.1',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).transform("m1.4341744,0,0,1.4341744,-109.08361,27.681494").data('id', 'path319676');
    g1414.attr({'id': 'g1414','style': 'display:inline','parent': 'layer2','name': 'g1414'});
    g1414.transform("m1.4341744,0,0,1.4341744,-109.08361,27.681494");
    var layer5 = rsr.set();
    var v910h = rsr.path("M 132.82083,134.41354 148.23281,49.879173").attr({id: 'v9-10-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v9-10h');
    var v34h = rsr.path("m 50.93229,122.70573 9.32656,14.02292").attr({id: 'v3-4-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v3-4h');
    var v45h = rsr.path("m 60.25885,136.72865 8.59896,12.03855").attr({id: 'v4-5-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v4-5h');
    var v56h = rsr.path("m 68.85781,148.7672 14.94896,0.19844").attr({id: 'v5-6-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v5-6h');
    var v67h = rsr.path("M 83.80677,148.96564 95.58073,144.7323").attr({id: 'v6-7-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v6-7h');
    var v78h = rsr.path("M 94.98542,157.82918 95.58073,144.7323").attr({id: 'v7-8-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v7-8h');
    var v144h = rsr.path("m 60.25885,136.72865 46.23594,-18.45469").attr({id: 'v14-4-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v14-4h');
    var v913h = rsr.path("m 120.5177,117.74479 12.30313,16.66875").attr({id: 'v9-13-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v9-13h');
    var v1314h = rsr.path("m 106.49479,118.27396 14.02291,-0.52917").attr({id: 'v13-14-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v13-14h');
    var v79h = rsr.path("m 95.58073,144.7323 37.2401,-10.31876").attr({id: 'v7-9-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v7-9h');
    var v89h = rsr.path("m 94.98542,157.82918 37.83541,-23.41564").attr({id: 'v8-9-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v8-9h');
    var v147h = rsr.path("M 106.49479,118.27396 95.58073,144.7323").attr({id: 'v14-7-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v14-7h');
    var v145h = rsr.path("m 68.85781,148.7672 37.63698,-30.49324").attr({id: 'v14-5-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v14-5h');
    var v137h = rsr.path("M 95.58073,144.7323 120.5177,117.74479").attr({id: 'v13-7-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v13-7h');
    var v143h = rsr.path("m 106.49479,118.27396 -55.5625,4.43177").attr({id: 'v14-3-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v14-3h');
    var v214h = rsr.path("m 111.59839,44.710937 -5.1036,73.563023").attr({id: 'v2-14-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v2-14h');
    var v1213h = rsr.path("m 120.5177,117.74479 6.70259,-54.324989").attr({id: 'v12-13-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v12-13h');
    var v114h = rsr.path("M 106.49479,118.27396 127.0332,40.220807").attr({id: 'v1-14-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v1-14h');
    var v111h = rsr.path("M 141.15839,40.875619 127.0332,40.220807").attr({id: 'v11-1-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v1-11h');
    var v1112h = rsr.path("m 127.22029,63.419801 13.9381,-22.544182").attr({id: 'v11-12-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v11-12h');
    var v112h = rsr.path("m 127.0332,40.220807 0.18709,23.198994").attr({id: 'v1-12-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v1-12h');
    var v12h = rsr.path("m 111.59839,44.710937 15.43481,-4.49013").attr({id: 'v1-2-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v1-2h');
    var v212h = rsr.path("m 111.59839,44.710937 15.6219,18.708864").attr({id: 'v2-12-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v2-12h');
    var v23h = rsr.path("m 50.93229,122.70573 60.6661,-77.994793").attr({id: 'v2-3-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v2-3h');
    var v123h = rsr.path("m 127.22029,63.419801 -76.288,59.285929").attr({id: 'v12-3-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v12-3h');
    var v1012h = rsr.path("M 127.22029,63.419801 148.23281,49.879173").attr({id: 'v10-12-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v10-12h');
    var v1011h = rsr.path("m 141.15839,40.875619 7.07442,9.003554").attr({id: 'v10-11-h',parent: 'layer5',display: 'inline',opacity: '0',fill: 'none',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-linecap": 'butt',"stroke-linejoin": 'miter',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'v10-11h');
    edith = rsr.rect(38.233482, 187.74106, 25,25).attr({id: 'edit-h',x: '38.233482',y: '187.74106',ry: '0.48161307',parent: 'layer5',opacity: '0',fill: '#8e8d8a',"fill-opacity": '1',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'edith');
    refreshh = rsr.rect(96.467216, 187.53175, 25,25).attr({id: 'refresh-h',x: '96.467216',y: '187.53175',ry: '0.48161307',parent: 'layer5',opacity: '0',fill: '#8e8d8a',"fill-opacity": '1',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'refreshh');
    verifyh = rsr.rect(300,300, 31.814865, 28.047314).attr({id: 'verify-h',x: '118.09617',y: '186.69452',ry: '0.48161307',parent: 'layer5',opacity: '0',fill: '#8e8d8a',"fill-opacity": '1',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'verifyh');
    ffh = rsr.rect(158.09746, 187.74106, 25,25).attr({id: 'ff-h',x: '158.09746',y: '187.74106',ry: '0.48161307',parent: 'layer5',opacity: '0',fill: '#8e8d8a',"fill-opacity": '1',stroke: '#8e8d8a',"stroke-width": '3.5',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'ffh');
    layer5.attr({'id': 'layer5','style': 'opacity:1','name': 'layer5'});
    var layer1 = rsr.set();
    var n1 = rsr.circle(127, 40, 2).attr({id: 'n1',parent: 'layer1',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.79',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n1');
    var n2 = rsr.circle(111, 44, 2).attr({id: 'n2',parent: 'layer1',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.79',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n2');
    var n11 = rsr.circle(141, 40, 2).attr({id: 'n11',parent: 'layer1',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.79',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n11');
    var n10 = rsr.circle(148, 49, 2).attr({id: 'n10',parent: 'layer1',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.79',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n10');
    var n12 = rsr.circle(127, 63, 2).attr({id: 'n12',parent: 'layer1',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.79',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n12');
    var n13 = rsr.circle(120, 117, 2).attr({id: 'n13',parent: 'layer1',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.79',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n13');
    var n14 = rsr.circle(106, 118, 2).attr({id: 'n14',parent: 'layer1',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.79',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n14');
    var n9 = rsr.circle(132, 134, 2).attr({id: 'n9',parent: 'layer1',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.79',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n9');
    var n7 = rsr.circle(95, 144, 2).attr({id: 'n7',parent: 'layer1',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.79',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n7');
    var n8 = rsr.circle(94, 157, 2).attr({id: 'n8',parent: 'layer1',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.79',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n8');
    var n6 = rsr.circle(83, 148, 2).attr({id: 'n6',parent: 'layer1',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.79',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n6');
    var n5 = rsr.circle(68, 148, 2).attr({id: 'n5',parent: 'layer1',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.79',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n5');
    var n4 = rsr.circle(60, 136, 2).attr({id: 'n4',parent: 'layer1',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.79',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n4');
    var n3 = rsr.circle(51, 122, 2).attr({id: 'n3',parent: 'layer1',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.79',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n3');
    var v12txt = rsr.text(116.62663, 39.474209, '5').attr({id: '1-2-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v1-2-txt');
    var v1011txt = rsr.text(147.20628, 44.533169, '5').attr({id: 'v10-11-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v10-11-txt');
    var v111txt = rsr.text(131.81393, 36.836998, '5').attr({id: 'v11-1-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v11-1-txt');
    var v910txt = rsr.text(143.95021, 90.118195, '5').attr({id: 'v9-10-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v9-10-txt');
    var v1213txt = rsr.text(127.66985, 86.270111, '5').attr({id: 'v12-13-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v12-13-txt');
    var v1012txt = rsr.text(137.73405, 60.517532, '5').attr({id: 'v10-12-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v10-12-txt');
    var v1112txt = rsr.text(137.73407, 50.74931, '5').attr({id: 'v11-12-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v11-12-txt');
    var v112txt = rsr.text(128.17278, 51.68005, '5').attr({id: 'v1-12-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v1-12-txt');
    var v212txt = rsr.text(116.08524, 57.854649, '5').attr({id: 'v2-12-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v2-12-txt');
    var v214txt = rsr.text(106.03843, 65.4944, '5').attr({id: 'v2-14-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v2-14-txt');
    var v123txt = rsr.text(89.484985, 97.518364, '5').attr({id: 'v12-3-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v12-3-txt');
    var v23txt = rsr.text(78.384735, 79.609962, '5').attr({id: '2-3-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v2-3-txt');
    var v34txt = rsr.text(50.85611, 132.59515, '5').attr({id: 'v3-4-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v3-4-txt');
    var v143txt = rsr.text(83.712852, 117.49882, '5').attr({id: 'v14-3-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v14-3-txt');
    var v144txt = rsr.text(76.460693, 128.59906, '5').attr({id: 'v14-4-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v14-4-txt');
    var v145txt = rsr.text(80.308777, 136.29523, '5').attr({id: 'v14-5-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v14-5-txt');
    var v147txt = rsr.text(94.221092, 137.92328, '5').attr({id: 'v14-7-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v14-7-txt');
    var v67txt = rsr.text(88.448959, 151.24356, '5').attr({id: 'v6-7-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v6-7-txt');
    var v56txt = rsr.text(74.240639, 154.79565, '5').attr({id: 'v5-6-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v5-6-txt');
    var v78txt = rsr.text(97.033157, 151.9836, '5').attr({id: 'v7-8-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v7-8-txt');
    var v89txt = rsr.text(109.90944, 153.75963, '5').attr({id: 'v8-9-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v8-9-txt');
    var v79txt = rsr.text(111.68548, 137.62726, '5').attr({id: 'v7-9-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v7-9-txt');
    var v913txt = rsr.text(121.74971, 128.89507, '5').attr({id: 'v9-13-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v9-13-txt');
    var v137txt = rsr.text(109.02142, 125.6613, '5').attr({id: 'v13-7-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v13-7-txt');
    var v1314txt = rsr.text(113.01751, 114.98277, '5').attr({id: 'v13-14-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v13-14-txt');
    var v114txt = rsr.text(115.68157, 91.894234, '5').attr({id: 'v1-14-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v1-14-txt');
    var v45txt = rsr.text(58.848293, 145.17543, '5').attr({id: 'v4-5-txt',parent: 'layer4',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'v4-5-txt');
    layer1.attr({'id': 'layer1','name': 'layer1'});
    var q10 = rsr.text(146.25871, 51.331402, '10').attr({id: 'q10',parent: 'layer6',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'q10');
    var q1 = rsr.text(125.70117, 41.848846, '1').attr({id: 'q1',parent: 'layer6',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'q1');
    var q2 = rsr.text(110.34036, 46.042969, '2').attr({id: 'q2',parent: 'layer6',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'q2');
    var q3 = rsr.text(49.538551, 123.92703, '3').attr({id: 'q3',parent: 'layer6',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'q3');
    var q4 = rsr.text(58.862762, 137.98735, '4').attr({id: 'q4',parent: 'layer6',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'q4');
    var q5 = rsr.text(67.07695, 149.90163, '5').attr({id: 'q5',parent: 'layer6',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'q5');
    var q6 = rsr.text(82.321289, 150.27162, '6').attr({id: 'q6',parent: 'layer6',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'q6');
    var q7 = rsr.text(94.309563, 146.57155, '7').attr({id: 'q7',parent: 'layer6',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'q7');
    var q8 = rsr.text(93.643547, 159.07782, '8').attr({id: 'q8',parent: 'layer6',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'q8');
    var q9 = rsr.text(131.6064, 135.9153, '9').attr({id: 'q9',parent: 'layer6',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'q9');
    var q13 = rsr.text(119.24812, 119.19093, '13').attr({id: 'q13',parent: 'layer6',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'q13');
    var q14 = rsr.text(104.9658, 119.56094, '14').attr({id: 'q14',parent: 'layer6',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'q14');
    var q12 = rsr.text(125.98227, 65.021713, '12').attr({id: 'q12',parent: 'layer6',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'q12');
    var q11 = rsr.text(139.82059, 42.451202, '11').attr({id: 'q11',parent: 'layer6',"font-style": 'normal',"font-weight": 'normal',"font-size": '4.23333311px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: '#000000',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'q11');
    var rsrGroups = [layer5,layer4,layer2, refresh, ff,verify,layer1];

    layer5.push( v910h , v34h , v45h , v56h , v67h , v78h , v144h , v913h , v1314h , v79h , v89h , v147h , v145h , v137h , v143h , v214h , v1213h , v114h , v111h , v1112h , v112h , v12h , v212h , v23h , v123h , v1012h , v1011h , edith , refreshh , verifyh , ffh );
    layer4.push( v12txt , v1011txt , v111txt , v910txt , v1213txt , v1012txt , v1112txt , v12txt , v212txt , v214txt , v123txt , v23txt , v34txt , v143txt , v144txt , v145txt , v147txt , v67txt , v56txt , v78txt , v89txt , v79txt , v913txt , v137txt , v1314txt , v114txt , v45txt,  v112txt );
    layer2.push( instructtxt , v910 , v34 , v45 , v56 , v67 , v78 , v144 , v913 , v1314 , v79 , v89 , v147 , v145 , v137 , v143 , v214 , v1213 , v114 , v111 , v1112 , v112 , v12 , v212 , v23 , v123 , v1012 , v1011 );
    refresh.push( path907 , path927 , path9273 );
    ff.push( hff , p1ff , p2ff );
    verify.push( path987 , path989 , path949 , path9497 , path94978 , path94977 );
    layer1.push( n1 , n2 , n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14);

    g1603.push( path3119 , path3196 , path31967 );
    g1414.push( path31192 , path31961 , path319676 );
    //layer5.attr("opacity", "1");
    edit = [g1603, g1414]


    // ///TEST!!:
    // var nerd0 = rsr.circle(20, 30, 3)
    // var nerd1 = rsr.circle(190, 30, 3)
    // var nerd1 = rsr.circle(210, 30, 3)
    // var nerd3 = rsr.circle(380, 30, 3)

    // var ned0 = rsr.circle(20, 185, 3)
    // var ned1 = rsr.circle(190, 185, 3)
    // var ned1 = rsr.circle(210, 185, 3)
    // var ned3 = rsr.circle(380, 185, 3)

    // var need0 = rsr.circle(20, 220, 3)
    // var need1 = rsr.circle(190, 220, 3)
    // var need1 = rsr.circle(210, 220, 3)
    // var need3 = rsr.circle(380, 220, 3)


    instructtxt = rsr.text(195.49885, 7.746574, 'Click node one to start!').attr({id: 'instruct-txt',parent: 'layer2',"font-style": 'normal',"font-variant": 'normal',"font-weight": 'normal',"font-stretch": 'normal',"font-size": '10.58333302px',"line-height": '1.25',"font-family": 'sans-serif',"-inkscape-font-specification": 'sans-serif, Normal',"font-variant-ligatures": 'normal',"font-variant-caps": 'normal',"font-variant-numeric": 'normal',"font-feature-settings": 'normal',"text-align": 'center',"letter-spacing": '0px',"word-spacing": '0px',"writing-mode": 'lr-tb',"text-anchor": 'middle',fill: '#8e8d8a',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'instructtxt');
    // var text_durr = rsr.text(295.49885, 23.746574, 'Click node one to start!').attr({id: 'instruct-txt',parent: 'layer2',"font-style": 'normal',"font-variant": 'normal',"font-weight": 'normal',"font-stretch": 'normal',"font-size": '8.58333302px',"line-height": '1.25',"font-family": 'sans-serif',"-inkscape-font-specification": 'sans-serif, Normal',"font-variant-ligatures": 'normal',"font-variant-caps": 'normal',"font-variant-numeric": 'normal',"font-feature-settings": 'normal',"text-align": 'center',"letter-spacing": '0px',"word-spacing": '0px',"writing-mode": 'lr-tb',"text-anchor": 'middle',fill: '#8e8d8a',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'instructtxt');
    // ///END TEST

    lens = [v910 , v34 , v45 , v56 , v67 , v78 , v144 , v913 , v1314 , v79 , v89 , v147 , v145 , v137 , v143 , v214 , v1213 , v114 , v111 , v1112 , v112 , v12 , v212 , v23 , v123 , v1012 , v1011]

    len_texts = [v910txt,  v34txt, v45txt, v56txt, v67txt, v78txt, v144txt, v913txt, v1314txt, v79txt, v89txt, v147txt, v145txt, v137txt, v143txt, v214txt, v1213txt, v114txt, v111txt, v1112txt, v112txt, v12txt, v212txt, v23txt, v123txt, v1012txt, v1011txt]
    //FIX ME
    len_values = new Array(lens.length).fill(4);

    len_hitboxes = [v910h , v34h , v45h , v56h , v67h , v78h , v144h , v913h , v1314h , v79h , v89h , v147h , v145h , v137h , v143h , v214h , v1213h , v114h , v111h , v1112h , v112h , v12h , v212h , v23h , v123h , v1012h , v1011h]


    len_values.forEach(function (value, index, array) {
        len_values[index] = Math.floor(Math.random() * 10) + 1;
    })

    len_values = [14, 3, 3, 4, 2, 3, 8, 5, 2, 6, 6, 5, 7, 5, 8, 14, 12, 17, 2, 5, 3, 2, 3, 18, 19, 3, 1]

    len_value_ds = new Map();

    node_texts = [q10 , q1 , q2 , q3 , q4 , q5 , q6 , q7 , q8 , q9 , q13 , q14 , q12 , q11];

    node_texts.forEach(element => {
        element.translate(1, -1.5);
    })

    q10.translate(0.5, -1.5 / 2);
    q8.translate(-0.5, -0.25);
    q7.translate(-0.5, -0.5);
    q9.translate(-0.4, 0);
    q13.translate(-0.25, -0.4);
    q6.translate(-0.25, -0.4);
    q2.translate(-0.25, -0.2);
    q11.translate(0, -0.4);


    set_len_values(true);
    // var i;


    // for (i = 0; i < lens.length; i++){
    //     len_value_ds.set(lens[i], len_values[i])
    //     len_texts[i].attr("text", len_values[i].toString());
    // }

    len_map_ds = new Map();

    lens.forEach(element => {
        len_map_ds.set(element.data("id"), element);
    })

    len_text_ds = new Map();

    len_texts.forEach(element => {
        len_text_ds.set(element.data("id").replace("-txt", ""), element);
    })

    swap = [path3119 , path3196 , path31967, path31192 , path31961 , path319676 ]

    //ad hoc fixes for things
    layer5.translate(-1,-1)
    layer2.translate(-1, -1);
    n14.translate(-0.5, -1);
    n3.translate(-0.5, -0.5);
    n9.translate(0, -1);
    n13.translate(-0.5, 0);
    n12.translate(-0.5, -1);
    n1.translate(-1, -0.6);
    n11.translate(-0.75, -0.25);
    n10.translate(-0.5, 0);
    v56txt.translate(0, -3);
    v144txt.translate(0, -1);
    v112.translate(-1, 0);

    layer5.forEach(element => {
        element.translate(-1, 1);
    });
    layer4.forEach(element => {
        element.translate(-1, -1);
    });
    tablegroup.push( toptable , path53778768 , text5426603 , t1a , t2a , t3a , t4a , t5a , t6a , t7a , t8a , t9a , t10a , t11a , t12a , t13a , t14a , text5426936 , t1b , t2b , t3b , t4b , t5b , t6b , t7b , t8b , t9b , t10b , t11b , t12b , t13b , t14b , text542649040 , text5426436403 , text54264374950 , text54264063720 , text5426457193 , text54264583197 , text54264359776 , text542643771591 , text54264065641 , text54264599317 , text5426420355 , text54264398551 , text542643705562 , text54264030889  , text5426628 , path537787576 , bottomtable , path537787682 , text54266032 , z1a , z2a , z3a , z4a , z5a , z6a , z7a , z8a , z9a , z10a , z11a , z12a , z13a , z14a, text54269368 , z1b , z2b , z3b , z4b , z5b , z6b , z7b , z8b , z9b , z10b , z11b , z12b , z13b , z14b , text5426490405 , text54264364039 , text542643749505 , text542640637204 , text54264571938 , text542645831974 , text542643597764 , text5426437715910 , text542640656410 , text542645993173 , text54264203557 , text542643985517 , text5426437055621 , text542640308898 , text54266283 , path5377875762 );

    numbers = [t1a , t2a , t3a , t4a , t5a , t6a , t7a , t8a , t9a , t10a , t11a , t12a , t13a , t14a , t1b , t2b , t3b , t4b , t5b , t6b , t7b , t8b , t9b , t10b , t11b , t12b , t13b , t14b , z1a , z2a , z3a , z4a , z5a , z6a , z7a , z8a , z9a , z10a , z11a , z12a , z13a , z14a, z1b , z2b , z3b , z4b , z5b , z6b , z7b , z8b , z9b , z10b , z11b , z12b , z13b , z14b ];
    other_numbers = [text542649040 , text5426436403 , text54264374950 , text54264063720 , text5426457193 , text54264583197 , text54264359776 , text542643771591 , text54264065641 , text54264599317 , text5426420355 , text54264398551 , text542643705562 , text54264030889 , text5426490405 , text54264364039 , text542643749505 , text542640637204 , text54264571938 , text542645831974 , text542643597764 , text5426437715910 , text542640656410 , text542645993173 , text54264203557 , text542643985517 , text5426437055621 , text542640308898]

    labels_t1 = [t1a , t2a , t3a , t4a , t5a , t6a , t7a , t8a , t9a , t10a , t11a , t12a , t13a , t14a]
    prev_t1 = [t1b , t2b , t3b , t4b , t5b , t6b , t7b , t8b , t9b , t10b , t11b , t12b , t13b , t14b]

    labels_t2 = [z1a , z2a , z3a , z4a , z5a , z6a , z7a , z8a , z9a , z10a , z11a , z12a , z13a , z14a]
    prev_t2 = [z1b , z2b , z3b , z4b , z5b , z6b , z7b , z8b , z9b , z10b , z11b , z12b , z13b , z14b ];

    nodes = [ n1 , n2 , n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14];

    numbers.forEach(element => {
        element.attr("font-size", "4");
    })
    other_numbers.forEach(element => {
        element.attr("font-size", "4");
    })

    num_nodes = nodes.length
    node_in = new Array(num_nodes).fill(0);

    nodes.forEach(element => {
        element.transform("s1.764");
    })

    lens.forEach(element => {
        var stroke_l = element.attr("stroke-width")
        element.attr("stroke-width", stroke_l * 1.75 + "")
    })

    var val_map_dummy = new Array(num_nodes).fill(infinity);
    var prev_map_dummy = new Array(num_nodes).fill(-1);
    setTable(val_map_dummy, prev_map_dummy, false);
    setTable(val_map_dummy, prev_map_dummy, false);
    bottomtable.attr("text", "Table for iteration -1");

    verify.attr("opacity", "0");
    //TEST
    var string = "";
    nodes.forEach(element =>{
        string = string + element.attr("cx") + " " + element.attr("cy") + "= true; \n "
    })
    string = "";
    len_texts.forEach(function(element, index, array) {
        var val;
        val = element.data("id").replace("-txt","").replace("v", "");
        var nodes = val.split("-");
        var node1 = nodes[0]
        var node2 = nodes[1]
        if (node1 < node2){
            var temp = node1;
            node1 = node2;
            node2 = temp;
        }
        var value = len_values[index]
        string = string + "len_value[" + node2 + "]" + "[" + node1 + "] = " + value + "\n"
    })
    //prompt("hi", string)


    //TESTS!::

    // len_map(1, 2).attr("stroke", "#FFFFFF")
    // len_map(2, 1).attr("stroke", "#000000")
    // len_map_ds.get("v1-2").attr("stroke", "#000000")
    // node_map(0).attr("fill", "#000000")
    // var value_map = new Array(num_nodes).fill(3);
    // var prev_map = new Array(num_nodes).fill(0);
    // setTable(value_map, prev_map);
    // var visited = [{"node": 1, "prev": 1 }, {"node": 1, "prev": 2 }]
    // var highlight = [v23, v1012];

    // setLensAndNodes(visited, highlight);
    // // positiveText()


    // value_map = new Array(num_nodes).fill(0);
    // prev_map = new Array(num_nodes).fill(0);
    // restart_graph(value_map, prev_map);

    // len_text_map(14, 3).attr("text", "???")
}
