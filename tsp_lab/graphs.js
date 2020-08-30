var lens_arr;
var num_nodes;
const IMG_URL = "./img-us.png"
var nodes_arr;
var restart;
var nodes_to_distances;
const beyonce_matrix = [[0.0, 305.5372745549659, 358.09098967775765, 397.18166344827546, 549.3792474323199, 629.2624189704453, 307.4184145812818, 90.17283965174569, 172.73742574245378, 519.8009004663546, 126.61122475448958, 459.5385752385598, 555.8988186561961, 896.1763447402936, 1090.292663694195, 1040.7537935486384, 925.3807692561847, 1114.6754957380458, 1745.9450024457487, 2045.1502048397183, 2030.7047088154873, 2148.391533357352, 2020.6233928505726],
[305.5372745549659, 0.0, 123.08485893725425, 204.28247068802963, 393.6916111074088, 932.5764622429068, 594.816718654357, 395.43393873298925, 292.65394843237317, 404.90031527664314, 327.37427919437977, 566.8409318955886, 542.551287867109, 757.747602464916, 924.9304587150147, 1200.0857168978735, 965.2071702292657, 1219.0110617015202, 1978.5337673789472, 2295.2382882004076, 2271.0550589397276, 2420.0017922534066, 2323.0573559323348],
[358.09098967775765, 123.08485893725425, 0.0, 82.2434470549576, 270.75247815804266, 983.1436773672485, 663.6742927681818, 441.7280516669174, 279.58997818660885, 523.1899757525094, 414.62074518656226, 683.3790738637018, 665.5972294734266, 864.1708873529803, 1021.6023301707627, 1314.6292659355868, 1088.267421898054, 1339.860566583855, 2077.9440195556435, 2388.342152184137, 2368.0409006332375, 2502.2205002866285, 2373.3516022357294],
[397.18166344827546, 204.28247068802963, 82.2434470549576, 0.0, 189.78478134361197, 1008.4477007243398, 704.4346795247849, 473.469692307717, 283.85780684680094, 605.3777663464398, 471.38783447210193, 756.4436123516175, 746.6115469442656, 943.399186280137, 1097.0749808217313, 1384.8128862456902, 1168.5797123227474, 1416.3095923481105, 2134.7845416035766, 2439.9528239943206, 2422.701457951755, 2545.448074280391, 2393.7374030151245],
[549.3792474323199, 393.6916111074088, 270.75247815804266, 189.78478134361197, 0.0, 1120.88452461862, 848.6393356605977, 611.7761316866786, 399.1621592473572, 790.8183157400827, 642.0887990130961, 941.8319722979081, 936.2248848298927, 1115.7944158839298, 1257.712526960845, 1565.9296766136963, 1358.364343687991, 1604.0430792265952, 2295.253461133938, 2591.0496009430562, 2579.0417851701427, 2681.350525452859, 2485.725248671926],
[629.2624189704453, 932.5764622429068, 983.1436773672485, 1008.4477007243398, 1120.88452461862, 0.0, 354.5564662958726, 541.9918457859083, 729.1957996085206, 997.9785128153767, 626.9050371343395, 697.1208050875257, 907.9301141487878, 1309.4528515482175, 1512.9698868088299, 870.5104795503655, 1052.719800859064, 1057.6970985625346, 1278.52338369207, 1521.5307918231008, 1530.9645798507229, 1572.7571359253122, 1391.373100431457],
[307.4184145812818, 594.816718654357, 663.6742927681818, 704.4346795247849, 848.6393356605977, 354.5564662958726, 0.0, 236.9540794381571, 451.8165452476062, 651.7712546174947, 275.7000777893746, 397.5336953882658, 588.7631446896957, 986.2619941089747, 1190.5024152651406, 817.6678764618114, 835.2766465331052, 941.9349306804759, 1451.7614235561807, 1742.4127719430985, 1731.7964568993652, 1841.0216418151292, 1733.0206543919453],
[90.17283965174569, 395.43393873298925, 441.7280516669174, 473.469692307717, 611.7761316866786, 541.9918457859083, 236.9540794381571, 0.0, 215.39737928987364, 585.9791749107669, 163.7955233408728, 470.71414862629797, 597.6267087770801, 957.7376385601807, 1155.5163901619903, 1014.0334954324181, 940.1902684097687, 1105.9019993719035, 1687.3998053656937, 1979.32198753126, 1968.5348571223403, 2074.1612592536644, 1933.1671247143793],
[172.73742574245378, 292.65394843237317, 279.58997818660885, 283.85780684680094, 399.1621592473572, 729.1957996085206, 451.8165452476062, 215.39737928987364, 0.0, 624.9863583526709, 293.7725519460517, 626.5649076606876, 698.218445761019, 1001.2419426859631, 1184.7769635321026, 1213.1526702148813, 1086.9810956849099, 1285.9981103276932, 1902.7971147530163, 2193.4086078879864, 2183.6127698792434, 2282.5472680930466, 2110.6060011833742],
[519.8009004663546, 404.90031527664314, 523.1899757525094, 605.3777663464398, 790.8183157400827, 997.9785128153767, 651.7712546174947, 585.9791749107669, 624.9863583526709, 0.0, 425.9186557856572, 357.55999395256504, 193.3473174177471, 377.98302425354774, 570.5875282478494, 930.6322345567684, 598.6959896223364, 889.6933727450003, 1777.2696576881713, 2118.7774775137996, 2076.210600983362, 2290.5800748648985, 2321.6524287538205],
[126.61122475448958, 327.37427919437977, 414.62074518656226, 471.38783447210193, 642.0887990130961, 626.9050371343395, 275.7000777893746, 163.7955233408728, 293.7725519460517, 425.9186557856572, 0.0, 333.6241922228155, 436.2428204925024, 794.7446871258604, 993.5720547983274, 928.8884192182697, 798.7695880200441, 992.6209121387749, 1664.1669234046599, 1973.8853111851329, 1953.5515809683973, 2093.1321467704565, 2008.5682066871382],
[459.5385752385598, 566.8409318955886, 683.3790738637018, 756.4436123516175, 941.8319722979081, 697.1208050875257, 397.5336953882658, 470.71414862629797, 626.5649076606876, 357.55999395256504, 333.6241922228155, 0.0, 214.80027653891295, 613.7243646483266, 816.4323813136886, 633.7798967085553, 469.5057784434603, 665.4969939731283, 1442.9699789791396, 1776.668052292116, 1740.51261423253, 1937.6158707312743, 1970.5880032377047],
[555.8988186561961, 542.551287867109, 665.5972294734266, 746.6115469442656, 936.2248848298927, 907.9301141487878, 588.7631446896957, 597.6267087770801, 698.218445761019, 193.3473174177471, 436.2428204925024, 214.80027653891295, 0.0, 401.6267550811731, 605.5621350975009, 737.6939313674324, 424.12639533915063, 700.9135798906922, 1588.4679911998885, 1932.5968366641216, 1887.5108342023423, 2112.4515158134386, 2178.322455214381],
[896.1763447402936, 757.747602464916, 864.1708873529803, 943.399186280137, 1115.7944158839298, 1309.4528515482175, 986.2619941089747, 957.7376385601807, 1001.2419426859631, 377.98302425354774, 794.7446871258604, 613.7243646483266, 401.6267550811731, 0.0, 204.33864845638163, 977.8824812856451, 532.9542457604689, 847.9882007248256, 1842.5128168966294, 2197.7000119698846, 2137.098013038317, 2410.6958419301413, 2546.5428270015577],
[1090.292663694195, 924.9304587150147, 1021.6023301707627, 1097.0749808217313, 1257.712526960845, 1512.9698868088299, 1190.5024152651406, 1155.5163901619903, 1184.7769635321026, 570.5875282478494, 993.5720547983274, 816.4323813136886, 605.5621350975009, 204.33864845638163, 0.0, 1125.3894857992107, 668.4255451798858, 966.9214695133428, 1978.3557337450075, 2335.2018372696702, 2267.9613402488567, 2562.1950304887723, 2730.9953830782865],
[1040.7537935486384, 1200.0857168978735, 1314.6292659355868, 1384.8128862456902, 1565.9296766136963, 870.5104795503655, 817.6678764618114, 1014.0334954324181, 1213.1526702148813, 930.6322345567684, 928.8884192182697, 633.7798967085553, 737.6939313674324, 977.8824812856451, 1125.3894857992107, 0.0, 457.4682435769493, 229.75915159635736, 866.9953357004923, 1220.5889001965736, 1164.1356353400656, 1436.9278665375953, 1669.202169354589],
[925.3807692561847, 965.2071702292657, 1088.267421898054, 1168.5797123227474, 1358.364343687991, 1052.719800859064, 835.2766465331052, 940.1902684097687, 1086.9810956849099, 598.6959896223364, 798.7695880200441, 469.5057784434603, 424.12639533915063, 532.9542457604689, 668.4255451798858, 457.4682435769493, 0.0, 317.7546046550654, 1313.1994711751659, 1669.5111528879438, 1605.9703510401546, 1893.8497029930602, 2098.960043130651],
[1114.6754957380458, 1219.0110617015202, 1339.860566583855, 1416.3095923481105, 1604.0430792265952, 1057.6970985625346, 941.9349306804759, 1105.9019993719035, 1285.9981103276932, 889.6933727450003, 992.6209121387749, 665.4969939731283, 700.9135798906922, 847.9882007248256, 966.9214695133428, 229.75915159635736, 317.7546046550654, 0.0, 1014.1600580580098, 1370.9919294110678, 1301.297910154124, 1611.7477876982277, 1889.393332213408],
[1745.9450024457487, 1978.5337673789472, 2077.9440195556435, 2134.7845416035766, 2295.253461133938, 1278.52338369207, 1451.7614235561807, 1687.3998053656937, 1902.7971147530163, 1777.2696576881713, 1664.1669234046599, 1442.9699789791396, 1588.4679911998885, 1842.5128168966294, 1978.3557337450075, 866.9953357004923, 1313.1994711751659, 1014.1600580580098, 0.0, 356.9366114972953, 299.04370717880107, 618.1408368473279, 1114.5955716798157],
[2045.1502048397183, 2295.2382882004076, 2388.342152184137, 2439.9528239943206, 2591.0496009430562, 1521.5307918231008, 1742.4127719430985, 1979.32198753126, 2193.4086078879864, 2118.7774775137996, 1973.8853111851329, 1776.668052292116, 1932.5968366641216, 2197.7000119698846, 2335.2018372696702, 1220.5889001965736, 1669.5111528879438, 1370.9919294110678, 356.9366114972953, 0.0, 111.39762879447268, 308.8486120263217, 960.2657058582668],
[2030.7047088154873, 2271.0550589397276, 2368.0409006332375, 2422.701457951755, 2579.0417851701427, 1530.9645798507229, 1731.7964568993652, 1968.5348571223403, 2183.6127698792434, 2076.210600983362, 1953.5515809683973, 1740.51261423253, 1887.5108342023423, 2137.098013038317, 2267.9613402488567, 1164.1356353400656, 1605.9703510401546, 1301.297910154124, 299.04370717880107, 111.39762879447268, 0.0, 419.6325596319644, 1063.8450857240807],
[2148.391533357352, 2420.0017922534066, 2502.2205002866285, 2545.448074280391, 2681.350525452859, 1572.7571359253122, 1841.0216418151292, 2074.1612592536644, 2282.5472680930466, 2290.5800748648985, 2093.1321467704565, 1937.6158707312743, 2112.4515158134386, 2410.6958419301413, 2562.1950304887723, 1436.9278665375953, 1893.8497029930602, 1611.7477876982277, 618.1408368473279, 308.8486120263217, 419.6325596319644, 0.0, 708.6529554167225],
[2020.6233928505726, 2323.0573559323348, 2373.3516022357294, 2393.7374030151245, 2485.725248671926, 1391.373100431457, 1733.0206543919453, 1933.1671247143793, 2110.6060011833742, 2321.6524287538205, 2008.5682066871382, 1970.5880032377047, 2178.322455214381, 2546.5428270015577, 2730.9953830782865, 1669.202169354589, 2098.960043130651, 1889.393332213408, 1114.5955716798157, 960.2657058582668, 1063.8450857240807, 708.6529554167225, 0.0]]
var distance_arr;
var node_color = '#e98074'
var node_select_color = '#0677a1'
var normal_stroke_color = '#8e8d8a'
var stroke_select_color = "#000000";
var len_function_type_enum = {"SELECT": "select",
                              "UNSELECT" : "unselect"}
var text_event_type_enum = {"FINISH" : "finish",
                            "NEW" : "new",
                            "PRESS" : "press",
                            "SELECT" : "select",
                            "REJECT": "reject",
                            "ACCEPT": "accept",
                            "BACK": "back",
                            "TWOOPT": "twoopt",
                            "TWOOPTSTART" : "opstart",
                            "TWOOPTITER" : "twooptiter"}
var metric_type_enum = {"MANHATTAN" : "man",
                        "EUCLIDIAN" : "eu"}
var mode_type_enum = {"TWOOPT" : "two",
                      "BEYONCE" : "bey",
                      "GRID" : "grid"}
var mode_heur_type_enum = {"RANDOM" : "rand",
                           "NEAREST_NEIGHBOR" : "nn",
                           "NEAREST_INSERTION" : "ni",
                           "FURTHEST_INSERTION" : "fi",
                           "MANUAL" : "man",
                           "TWOOPT" : "twoopter"}
var costsofar;
var costsofar_text = 'Cost So Far: '
var back;
var two_opt_mode;
var nodes_hitbox_arr;
var instructxt;
var mode;
var next_part;
var toss;
var random_g;
var nearest_neighbor_g;
var random_insertion_g;
var nearest_insertion_g;
var furthest_insertion_g;
var optimize;
var width;
var height;

var insert;
var agument;
var brenda_mode = false;

var usImg = new Image();

function change_heur(heur){
    toss = heur;
}

function text_event(type){
    switch (type) {
        case text_event_type_enum.FINISH: instructxt.attr("text", "You found a tour!"); break;
        case text_event_type_enum.NEW: instructxt.attr("text", "Click the first node to start!");break;
        case text_event_type_enum.PRESS: instructxt.attr("text", "Press D to add next node!");break;
        case text_event_type_enum.SELECT: instructxt.attr("text", "Press D to add next node!");break;
        case text_event_type_enum.REJECT: instructxt.attr("text", "City already on tour!");break;
        case text_event_type_enum.ACCEPT: instructxt.attr("text", "City added!");break;
        case text_event_type_enum.BACK: instructxt.attr("text", "City removed!");break;
        case text_event_type_enum.TWOOPT: instructxt.attr("text", "Can not be further improved by 2-Opt!");break;
        case text_event_type_enum.TWOOPTSTART: instructxt.attr("text", "Press D to create a random tour!"); break;
        case text_event_type_enum.TWOOPTITER: instructxt.attr("text", "Press D to do iterations of 2-Opt!"); break;
    }
}

function get_node_hitbox_id(node){
    return parseInt(node.data("id").replace("h", ""))
}

function is_element_in_set(element, set){
    return set.filter(x => x == element).length != 0;
}

function reject_animation(node_number, nodes_in){
    var l_node = nodes_arr[node_number - 1]
    var color = l_node.attr("fill");
    var ani = Raphael.animation({fill: "#FF0000"}, 200, "linear", function (){
        if (!is_element_in_set(node_number, nodes_in)) {
            l_node.animate({fill: "#e98074"})
        } else{
            l_node.animate({fill: color});
        }
    });
   var ani2 = ani.repeat(3);
   l_node.animate(ani2);
}
function round_to_2_places(number){
    return Math.round(number * 100) / 100
}

function change_cost_graphic(total_cost){
    costsofar.attr("text",  costsofar_text +  Math.round(total_cost) + " mi")
}

function lens_map(i , j){
    if (lens_arr[i - 1][j - 1] == 0){
        return lens_arr[j - 1][i - 1];
    } else {
        return lens_arr[i - 1][j - 1];
    }
}

function lens_and_nodes_graphics(nodes_in, type){
    if (nodes_in.length == 0) return;
    var opacity_param;
    var fill_param;
    if (type == len_function_type_enum.SELECT){
        opacity_param = "1";
        fill_param = node_select_color;
    } else{
        opacity_param = "0";
        fill_param = node_color;
    }
    var i;

    for (i = 0; i < nodes_in.length - 1; i++){
        var first = nodes_in[i]
        var second = nodes_in[i + 1]
        nodes_arr[first - 1].attr("fill", fill_param)
        lens_map(first, second).attr("opacity", opacity_param);
    }
    nodes_arr[nodes_in[nodes_in.length - 1] - 1].attr("fill", fill_param);
    var first = nodes_in[nodes_in.length -1]
    var second = nodes_in[0]
    if (brenda_mode) {
        lens_map(first, second).attr("opacity", opacity_param);
        if (nodes_in.length > 3){
            lens_map(nodes_in[nodes_in.length - 2], nodes_in[0]).attr("opacity", "0")
        }
    } else {
        if (nodes_in.length == num_nodes){
            lens_map(first, second).attr("opacity", opacity_param);
            lens_map(nodes_in[nodes_in.length - 2], nodes_in[0]).attr("opacity", "0")
        }
    }

}

function distance_map(i, j){
    return mode == mode_type_enum.BEYONCE  ? beyonce_matrix[nodes_to_distances[i - 1] - 1][nodes_to_distances[j - 1] - 1] :
    distance_arr[i - 1][j - 1] == 0 ? distance_arr[j - 1][i - 1] : distance_arr[i - 1][j - 1];
}

function switch_graph_clean(){

}

function euclidian(x1, y1, x2, y2){
    return Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2- y1, 2))
}

function manhattan(x1, y1, x2, y2){
    return Math.abs(x2 - x1) + Math.abs(y2- y1)
}

function get_y(x){
    return q => Math.floor(q / x);
}

function get_x(x){
    return q => q % x;
}

function get_reverse_exception_array(){
    return [[0,0],[0,7],[2,0],[2,9],[8,1],[8,6],[9,0],[9,6],[9,9]];
}

function get_y_s(q){
    var arr = get_reverse_exception_array()
    return arr[q][1]
}

function get_x_s(q){
    var arr = get_reverse_exception_array()
    return arr[q][0]
}

function get_exception_array_two_opt(x, y){
    var exception_array = new Array(y).fill(0).map(v => new Array(x).fill(0));
    exception_array[0][0] = 1;
    exception_array[2][0] = 1;
    exception_array[9][0] = 1;
    exception_array[8][1] = 1;
    exception_array[9][6] = 1;
    exception_array[8][6] = 1;
    exception_array[0][7] = 1;
    exception_array[2][9] = 1;
    exception_array[9][9] = 1;
    return exception_array;
}

function highlight_opt(old_index, new_index, visited){
    var len1_old;
    var len2_old;
    var len1_new;
    var len2_new;
    if (old_index == -2){
        return;
    } else if (new_index == -1){
        len1_old = lens_map(visited[visited.length - 1], visited[0])
        len2_old = lens_map(visited[old_index], visited[old_index + 1])
        len1_new = lens_map(visited[old_index], visited[visited.length - 1])
        len2_new = lens_map(visited[old_index + 1], visited[0])
    } else {
        len1_old = lens_map(visited[new_index], visited[new_index + 1])
        len2_old = lens_map(visited[old_index], visited[old_index + 1])
        len1_new = lens_map(visited[old_index], visited[new_index])
        len2_new = lens_map(visited[old_index + 1], visited[new_index + 1])
    }
    len1_old.attr("stroke", "#FF0000")
    len2_old.attr("stroke", "#FF0000")
    len1_new.attr("stroke", "#86c5da").attr("opacity", "1")
    len2_new.attr("stroke", "#86c5da").attr("opacity", "1")
}
function unhighlight_opt(old_index, new_index, visited){
    var len1_old;
    var len2_old;
    var len1_new;
    var len2_new;
    if (old_index == -2){
        return;
    } else if (new_index == -1){
        len1_old = lens_map(visited[visited.length - 1], visited[0])
        len2_old = lens_map(visited[old_index], visited[old_index + 1])
        len1_new = lens_map(visited[old_index], visited[visited.length - 1])
        len2_new = lens_map(visited[old_index + 1], visited[0])
    } else {
        len1_old = lens_map(visited[new_index], visited[new_index + 1])
        len2_old = lens_map(visited[old_index], visited[old_index + 1])
        len1_new = lens_map(visited[old_index], visited[new_index])
        len2_new = lens_map(visited[old_index + 1], visited[new_index + 1])
    }
    len1_old.attr("stroke", "#000000")
    len2_old.attr("stroke", "#000000")
    len1_new.attr("stroke", "#000000").attr("opacity", "0")
    len2_new.attr("stroke", "#000000").attr("opacity", "0")
}



function Graph_Beyonce(rsr){
    rsr.clear();
    var layer1 = rsr.set();
    instructxt = rsr.text(97.322628, 63.713089, 'Click the first node to start!').attr({id: 'instructxt',parent: 'layer1',"font-style": 'normal',"font-weight": 'normal',"font-size": '10.58333302px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: normal_stroke_color,"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'instructxt');
    restart = rsr.text(57.160713, 186.40414, 'Restart').attr({id: 'restart',parent: 'layer1',"font-style": 'normal',"font-weight": 'normal',"font-size": '8.46666667px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: normal_stroke_color,"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'restart');
    back = rsr.text(127.90714, 186.52858, 'Back').attr({id: 'back',parent: 'layer1',"font-style": 'normal',"font-weight": 'normal',"font-size": '8.46666622px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: normal_stroke_color,"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'back');
    next_part = rsr.text(93.273811, 248.75891, '(Next) Part 2a: 6 x 8 Grid').attr({id: 'part2',parent: 'layer1',"font-style": 'normal',"font-weight": 'normal',"font-size": '10.58333302px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: normal_stroke_color,"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'part2');
    costsofar = rsr.text(100.595238, 76.639877, 'Cost So Far: 0 mi').attr({id: 'cost-so-far',parent: 'layer1',"font-style": 'normal',"font-weight": 'normal',"font-size": '8.58333302px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: normal_stroke_color,"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'costsofar')


    num_nodes = 23;

    mode = mode_type_enum.BEYONCE;
    toss = mode_heur_type_enum.MANUAL

    var image_1 = rsr.image(IMG_URL, 35, 87, width / 3.795, height / 3.795);

    var nodes_points = [[45, 93], [38, 124], [42, 133], [47, 138], [59, 141], [105, 107], [115, 154], [140, 156], [144, 163], [131, 142], [139, 139], [148, 120], [150, 116], [156, 110], [119, 118], [124, 134], [145, 123], [139, 110], [131, 122], [134, 117], [129, 114], [97, 145], [100, 156]]

    var nodes_to_distances_pre = [18,13,14,15,16,23,22,21,17,12,19,20,11,9,10,6,8,7,5,3,4,2,1];

    var nodes_index_remap_pre = [1 , 2 , 3 , 4 , 5 , 23 , 8 , 9 , 10 , 11 , 12 , 14 , 15 , 16 , 22 , 20 , 13 , 17 , 19 , 18 , 21 , 6 , 7];



    nodes_to_distances = new Array(num_nodes).fill(0);

    var nodes_index_remap = new Array(num_nodes).fill(0);

    nodes_to_distances_pre.forEach(function (element, index, array) {
        nodes_to_distances[element - 1] = index + 1;
    });

    nodes_index_remap_pre.forEach(function (element, index, array){
        nodes_index_remap[element - 1] = index + 1;
    })

    lens_arr = new Array(num_nodes).fill(0).map(x => new Array(num_nodes).fill(0));
    //instructxt.attr("font-size", "1")
    //instructxt.attr("text", JSON.stringify(nodes_index_remap));
    //instructxt.attr("text", nodes_points[nodes_index_remap[5] - 1][0]);

    var i;
    var j;
    for (i = 0; i < num_nodes; i++){
        for (j = i + 1 ; j < num_nodes; j++){
            var id_str = "v" + (i + 1) + "-" + (j + 1);
            var location1x = nodes_points[nodes_index_remap[i] - 1][0]
            var location1y = nodes_points[nodes_index_remap[i] - 1][1]
            var location2x = nodes_points[nodes_index_remap[j] - 1][0]
            var location2y = nodes_points[nodes_index_remap[j] - 1][1]


            var path_str = "M " + location1x + "," + location1y + " " + location2x+ "," + location2y;

            lens_arr[i][j] = rsr.path(path_str).attr({
                id: id_str,
                parent: 'layer1',
                "font-family": 'Times New Roman',
                fill: 'none',
                stroke: "#000000",
                "stroke-width": '1.1',
                "stroke-linecap": 'butt',
                "stroke-linejoin": 'miter',
                "stroke-miterlimit": '10',
                "stroke-dasharray": 'none',
                "stroke-opacity": '1'
              }).data('id', id_str);
            lens_arr[i][j].attr("opacity", "0")
        }

    }


    var n1 = rsr.circle(45, 93, 1).attr({id: 'n1',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n1');
    var n2 = rsr.circle(38, 124, 1).attr({id: 'n2',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n2');
    var n3 = rsr.circle(42, 133, 1).attr({id: 'n3',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n3');
    var n4 = rsr.circle(47, 138, 1).attr({id: 'n4',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n4');
    var n5 = rsr.circle(59, 141, 1).attr({id: 'n5',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n5');
    var n23 = rsr.circle(105, 107, 1).attr({id: 'n23',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n23');
    var n8 = rsr.circle(115, 154, 1).attr({id: 'n8',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n8');
    var n9 = rsr.circle(140, 156, 1).attr({id: 'n9',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n9');
    var n10 = rsr.circle(144, 163, 1).attr({id: 'n10',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n10');
    var n11 = rsr.circle(131, 142, 1).attr({id: 'n11',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n11');
    var n12 = rsr.circle(139, 139, 1).attr({id: 'n12',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n12');
    var n14 = rsr.circle(148, 120, 1).attr({id: 'n14',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n14');
    var n15 = rsr.circle(150, 116, 1).attr({id: 'n15',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n15');
    var n16 = rsr.circle(156, 110, 1).attr({id: 'n16',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n16');
    var n22 = rsr.circle(119, 118, 1).attr({id: 'n22',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n22');
    var n20 = rsr.circle(124, 134, 1).attr({id: 'n20',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n20');
    var n13 = rsr.circle(145, 123, 1).attr({id: 'n13',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n13');
    var n17 = rsr.circle(139, 110, 1).attr({id: 'n17',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n17');
    var n19 = rsr.circle(131, 122, 1).attr({id: 'n19',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n19');
    var n18 = rsr.circle(134, 117, 1).attr({id: 'n18',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n18');
    var n21 = rsr.circle(129, 114, 1).attr({id: 'n21',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n21');
    var n6 = rsr.circle(97, 145, 1).attr({id: 'n6',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n6');
    var n7 = rsr.circle(100, 156, 1).attr({id: 'n7',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n7');

    var h1 = rsr.circle(45, 93, 2.5).attr({id: 'h1',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'h1');
    var h2 = rsr.circle(37, 124, 2.5).attr({id: 'h2',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'h2');
    var h3 = rsr.circle(42, 133, 2.5).attr({id: 'h3',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'h3');
    var h4 = rsr.circle(45, 138, 2.5).attr({id: 'h4',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'h4');
    var h5 = rsr.circle(59, 141, 2.5).attr({id: 'h5',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'h5');
    var h23 = rsr.circle(105, 107, 2.5).attr({id: 'h23',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'h23');
    var h8 = rsr.circle(115, 154, 2.5).attr({id: 'h8',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'h8');
    var h9 = rsr.circle(140, 156, 2.5).attr({id: 'h9',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'h9');
    var h10 = rsr.circle(144, 163, 2.5).attr({id: 'h10',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'h10');
    var h11 = rsr.circle(131, 142, 2.5).attr({id: 'h11',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'h11');
    var h12 = rsr.circle(139, 139, 2.5).attr({id: 'h12',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'h12');
    var h14 = rsr.circle(148, 120, 2.5).attr({id: 'h14',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'h14');
    var h15 = rsr.circle(150, 116, 2.5).attr({id: 'h15',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'h15');
    var h16 = rsr.circle(156, 110, 2.5).attr({id: 'h16',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'h16');
    var h22 = rsr.circle(119, 118, 2.5).attr({id: 'h22',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'h22');
    var h20 = rsr.circle(124, 134, 2.5).attr({id: 'h20',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'h20');
    var h13 = rsr.circle(145, 123, 2.5).attr({id: 'h13',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'h13');
    var h17 = rsr.circle(139, 110, 2.5).attr({id: 'h17',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'h17');
    var h19 = rsr.circle(131, 122, 2.5).attr({id: 'h19',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'h19');
    var h18 = rsr.circle(134, 117, 2.5).attr({id: 'h18',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'h18');
    var h21 = rsr.circle(129, 114, 2.5).attr({id: 'h21',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'h21');
    var h6 = rsr.circle(97, 145, 2.5).attr({id: 'h6',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'h6');
    var h7 = rsr.circle(100, 156, 2.5).attr({id: 'h7',parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'h7');

    nodes_arr = [n1 ,n2 ,n3 ,n4 ,n5 ,n6 ,n7 ,n8 ,n9 ,n10 ,n11 ,n12 ,n13 ,n14 ,n15 ,n16 ,n17 ,n18 ,n19 ,n20 ,n21 ,n22 ,n23]


    layer1.attr({'id': 'layer1','name': 'layer1'});
    var rsrGroups = [layer1];
    layer1.push(n1 ,n2 ,n3 ,n4 ,n5 ,n23 ,n22 ,n6 ,n7 ,n8 ,n9 ,n10 ,n11 ,n20 ,n12 ,n13 ,n14 ,n15 ,n16 ,n17 ,n19 ,n18 ,n21 ,instructxt ,restart ,back , part2 );

    nodes_hitbox_arr = [h1 ,h2 ,h3 ,h4 ,h5 ,h6 ,h7 ,h8 ,h9 ,h10 ,h11 ,h12 ,h13 ,h14 ,h15 ,h16 ,h17 ,h18 ,h19 ,h20 ,h21 ,h22 ,h23]

    nodes_hitbox_arr.forEach(element => {
        element.attr("opacity", "0")
    })
    // instructxt.attr("text", "hi1");
    rsr.forEach(element => {
        element.translate(100, -50)
    })

}
function Graph_Grid(rsr, x, y, type, heuristic, part_name_next, special){
    rsr.clear();
    var layer1 = rsr.set();
    if (special == undefined){
        instructxt = rsr.text(100, 60, 'Press D to add next node!').attr({id: 'instructxt',parent: 'layer1',"font-style": 'normal',"font-weight": 'normal',"font-size": '10.58333302px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: normal_stroke_color,"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'instructxt');
    } else {
        instructxt = rsr.text(100, 60, 'Press D to create a random tour!').attr({id: 'instructxt',parent: 'layer1',"font-style": 'normal',"font-weight": 'normal',"font-size": '10.58333302px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: normal_stroke_color,"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'instructxt');
    }
    restart = rsr.text(75, 190, 'Restart').attr({id: 'restart',parent: 'layer1',"font-style": 'normal',"font-weight": 'normal',"font-size": '8.46666667px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: normal_stroke_color,"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'restart');
    back = rsr.text(125, 190, 'Back').attr({id: 'back',parent: 'layer1',"font-style": 'normal',"font-weight": 'normal',"font-size": '8.46666622px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: normal_stroke_color,"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'back');
    costsofar = rsr.text(100, 75, 'Cost So Far: 0 mi').attr({id: 'cost-so-far',parent: 'layer1',"font-style": 'normal',"font-weight": 'normal',"font-size": '8.58333302px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: normal_stroke_color,"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'costsofar')

    next_part = rsr.text(100, 260, '(Next) ' + part_name_next).attr({id: 'part2',parent: 'layer1',"font-style": 'normal',"font-weight": 'normal',"font-size": '10.58333302px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: normal_stroke_color,"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'}).data('id', 'part2');

    if (special == undefined){
        heur = rsr.text(65, 205, "Heuristics").attr({id: 'part2',parent: 'layer1',"font-style": 'normal',"font-weight": 'normal',"font-size": '8px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill:'#696969',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'})
        random_insertion_g = rsr.text(65, 215, "Random Neighbor").attr({id: 'part2',parent: 'layer1',"font-style": 'normal',"font-weight": 'normal',"font-size": '8px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: normal_stroke_color,"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'})
        nearest_neighbor_g = rsr.text(65, 225, "Nearest Neighbor").attr({id: 'part2',parent: 'layer1',"font-style": 'normal',"font-weight": 'normal',"font-size": '8px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: normal_stroke_color,"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'})
        nearest_insertion_g = rsr.text(65, 235, "Nearest Insertion").attr({id: 'part2',parent: 'layer1',"font-style": 'normal',"font-weight": 'normal',"font-size": '8px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: normal_stroke_color,"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'})
        furthest_insertion_g = rsr.text(65, 245, "Furthest Insertion").attr({id: 'part2',parent: 'layer1',"font-style": 'normal',"font-weight": 'normal',"font-size": '8px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: normal_stroke_color,"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'})
        mode = rsr.text(135, 207, "Mode").attr({id: 'part2',parent: 'layer1',"font-style": 'normal',"font-weight": 'normal',"font-size": '8px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill:'#696969',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'})
        manhattan_mode = rsr.text(135, 217, "Manhattan").attr({id: 'part2',parent: 'layer1',"font-style": 'normal',"font-weight": 'normal',"font-size": '8px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: normal_stroke_color,"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'})
        euclidian_mode = rsr.text(135, 227, "Euclidian").attr({id: 'part2',parent: 'layer1',"font-style": 'normal',"font-weight": 'normal',"font-size": '8px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: normal_stroke_color,"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'})
        two_opt_mode = rsr.text(135, 242, "Do 2-Opt").attr({id: 'part2',parent: 'layer1',"font-style": 'normal',"font-weight": 'normal',"font-size": '8px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: normal_stroke_color,"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'})
    } else{
        inst1 = rsr.text(100, 220, "Press D to create a random tour.").attr({id: 'part2',parent: 'layer1',"font-style": 'normal',"font-weight": 'normal',"font-size": '8.58333302px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: normal_stroke_color,"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'})
        inst2 = rsr.text(100, 230, "Then, press D to run iterations of 2-Opt.").attr({id: 'part2',parent: 'layer1',"font-style": 'normal',"font-weight": 'normal',"font-size": '8.58333302px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: normal_stroke_color,"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'})
        //optimize = rsr.text(92.273811, 218.75891, "Run Two-Opt").attr({id: 'part2',parent: 'layer1',"font-style": 'normal',"font-weight": 'normal',"font-size": '8.58333302px',"line-height": '1.25',"font-family": 'sans-serif',"letter-spacing": '0px',"word-spacing": '0px',fill: normal_stroke_color,"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.26'})
    }

    mode = special == undefined ? mode_type_enum.GRID : mode_type_enum.TWOOPT
    mode_heur = "eu"
    toss = heuristic
    if (special != undefined){
        toss = mode_heur_type_enum.TWOOPT
    }

    var horizontal_delta = 10
    var vertical_delta = 10
    var left_point = 100 - (x*horizontal_delta)/2 + 3
    var lower_point = 135 - (y*vertical_delta)/2 + 3
    // Travis
    // var left_point = 45;
    // var right_point = 145;
    // var upper_point = 163
    // var lower_point = 93;
    // var horizontal_delta = (right_point - left_point) / (x - 1)
    // var vertical_delta = (upper_point - lower_point) / (y - 1)
    var nodes_points = [];
    var radius_circle = 1;
    var radius_shadow = 2.5;
    var i;
    var j;
    var exception_array = special == undefined ? new Array(y).fill(0).map(v => new Array(x).fill(1)) : get_exception_array_two_opt(x, y)
    for (i = 0; i < y; i ++ ){
        for (j = 0; j < x; j++){
            if (exception_array[i][j] == 1){
                nodes_points.push([left_point + (j * horizontal_delta), lower_point + (i * vertical_delta)]);
            }
        }
    }
    nodes_arr = []
    nodes_points.forEach(function (value, q, array){
        nodes_arr.push(rsr.circle(value[0], value[1], radius_circle).attr({id: 'n' + (q),parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'n' + (q)));
    })

    nodes_hitbox_arr = [];
    nodes_points.forEach(function (value, q, array){
        nodes_hitbox_arr.push(rsr.circle(value[0], value[1], radius_shadow).attr({id: 'h' + (q),parent: 'layer2',"font-family": 'Times New Roman',fill: '#e98074',"fill-opacity": '1',stroke: 'none','stroke-width':'1','stroke-opacity':'1',"stroke-width": '0.57',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data('id', 'h' + (q)))
        nodes_hitbox_arr[q].attr("opacity", "0")
    })

    lens_arr = new Array(nodes_points.length).fill(0).map(v => new Array(nodes_points.length).fill(0));

    distance_arr = new Array(nodes_points.length).fill(0).map(v => new Array(nodes_points.length).fill(0));

    var metric = type == metric_type_enum.MANHATTAN ? manhattan : euclidian
    var get_x_l = special == undefined ? get_x(x) : get_x_s;
    var get_y_l = special == undefined ? get_y(x): get_y_s;

    var i;
    var j;
    for (i = 0; i < nodes_points.length; i++){
        for (j = i + 1 ; j < nodes_points.length; j++){
            var id_str = "v" + (i + 1) + "-" + (j + 1);

            var location1x = nodes_points[i][0]
            var location1y = nodes_points[i][1]
            var location2x = nodes_points[j][0]
            var location2y = nodes_points[j][1]

            var path_str = "M " + location1x + "," + location1y + " " + location2x+ "," + location2y;

            lens_arr[i][j] = rsr.path(path_str).attr({
                id: id_str,
                parent: 'layer1',
                "font-family": 'Times New Roman',
                fill: 'none',
                stroke: "#000000",
                "stroke-width": '1.1',
                "stroke-linecap": 'butt',
                "stroke-linejoin": 'miter',
                "stroke-miterlimit": '10',
                "stroke-dasharray": 'none',
                "stroke-opacity": '1'
              }).data('id', id_str);

            //quick silly function to set distance labels


            lens_arr[i][j].attr("opacity", "0")
            distance_arr[i][j] = metric(get_x_l(i), get_y_l(i), get_x_l(j), get_y_l(j))
        }
    }
    //alert(JSON.stringify(distance_arr))
    num_nodes = nodes_points.length
    rsr.forEach(element => {
        element.translate(100, -50)
    })
}
function Graph_two_opt(rsr){
    Graph_Grid(rsr, 10, 10, metric_type_enum.EUCLIDIAN,  mode_heur_type_enum.RANDOM, "Part 1: Beyoncé", "two-opt-special")
}