
var nodes;
var kruskals_button;
var prims_button;
var rkruskals_button;
var hint_button;
var fast_foward_button;
var restart_button;
//var swap_graph_button;
var sensitivity_button;
var restore_button;

var nodes;
var nodes_hitboxes;
var lens;
var lens_hitboxes;

var line_texts;

var primary_text;
var secondary_text;

var len_data;
var len_value;
var nodes_centers;
let Graph1 = function(rsr){
    //Graph has nodes, lens, 7 buttons, and a next_text, clickboxes on nodes and lens
    nodes_centers = [
        [6,75],
        [20,87],
        [72,115],
        [111,154],
        [194,154],
        [178,108],
        [199,60],
        [205,50],
        [207,40],
        [198,43],
        [165,49],
        [157,62],
        [162,34],
        [144,34],
        [127,49],
        [189,53]
    ]

    len_data = new Array(nodes_centers.length).fill([]).map(x => new Array(nodes_centers.length).fill(false));
    len_data[0][1] = true
    len_data[1][2] = true
    len_data[2][3] = true
    len_data[3][4] = true
    len_data[4][5] = true
    len_data[5][6] = true
    len_data[6][15] = true
    len_data[9][15] = true
    len_data[7][9] = true
    len_data[6][7] = true
    len_data[7][8] = true
    len_data[8][9] = true
    len_data[9][10] = true
    len_data[10][11] = true
    len_data[11][12] = true
    len_data[12][13] = true
    len_data[13][14] = true
    len_data[0][14] = true
    len_data[12][14] = true
    len_data[11][13] = true
    len_data[11][14] = true
    len_data[2][11] = true
    len_data[5][11] = true
    len_data[3][5] = true
    len_data[10][15] = true
    len_data[2][14] = true
    len_data[1][14] = true
    len_data[3][11] = true

    len_value = new Array(nodes_centers.length).fill([]).map(x => new Array(nodes_centers.length).fill(undefined));
    len_value[0][1] = 4
    len_value[1][2] = 12
    len_value[2][3] = 10
    len_value[3][4] = 14
    len_value[4][5] = 12
    len_value[5][6] = 14
    len_value[6][15] = 3
    len_value[9][15] = 4
    len_value[7][9] = 2
    len_value[6][7] = 3
    len_value[7][8] = 1
    len_value[8][9] = 2
    len_value[9][10] = 6
    len_value[10][11] = 4
    len_value[11][12] = 8
    len_value[12][13] = 4
    len_value[13][14] = 6
    len_value[0][14] = 24
    len_value[12][14] = 10
    len_value[11][13] = 8
    len_value[11][14] = 8
    len_value[2][11] = 25
    len_value[5][11] = 14
    len_value[3][5] = 18
    len_value[10][15] = 6
    len_value[2][14] = 20
    len_value[1][14] = 19
    len_value[3][11] = 18



    let obtain_graphics = function(rsr){

        //refactor below

        len_text_pos = new Array(nodes_centers.length).fill([]).map(x => new Array(nodes_centers.length).fill(undefined));

        len_text_pos[11][13] = [144.46245 + 3,52.525051 - 2.7]
        len_text_pos[2][14] = [90.953278,81.311958]
        len_text_pos[11][14] = [138.0491,60.806751 - 2]
        len_text_pos[12][14] = [152.33624 + 3,43.873405 - 3]
        len_text_pos[2][11] = [139.10745 - 8,78.798416 + 5]
        len_text_pos[1][14] = [54.96994,79.592163]
        len_text_pos[0][14] = [29.040806,66.098419]
        len_text_pos[5][11] = [161.33249 + 3,90.969246 - 2]
        len_text_pos[3][5] = [148.10327,134.89011]
        len_text_pos[1][2] = [38.565804,105.25674]
        len_text_pos[2][3] = [82.486633 + 4,137.5359]
        len_text_pos[0][1] = [5.2283015 + 5,84.619247]
        len_text_pos[3][4] = [157.09914,160.81923 - 3]
        len_text_pos[5][6] = [191.49504 + 2,84.09008]
        len_text_pos[4][5] = [187.26169 + 3,129.06923]
        len_text_pos[10][15] = [172.97415 + 3,56.573418 - 2]
        len_text_pos[9][10] = [178.26582,42.285912]
        len_text_pos[8][9] = [197.84503 + 3,38.052582]
        len_text_pos[6][7] = [202.60739 + 2.5,62.394249 - 5]
        len_text_pos[7][8] = [204.19502 + 5,57.631752 - 12]
        len_text_pos[6][15] = [188.71683 + 2,61.865086 - 2]
        len_text_pos[7][9] = [195.99283 + 3,51.28175 - 2.3]
        len_text_pos[9][15] = [184.61578 + 3.7,49.694252 - 1.7]
        len_text_pos[13][14] = [130.37608,41.227589]
        len_text_pos[10][11] = [161.59697 + 1,59.483837]
        len_text_pos[11][12] = [162.12619 + 2,42.285912]
        len_text_pos[12][13] = [151.03227,33.311237 - 3]
        len_text_pos[3][11] = [121.11575 + 3,115.3109]


        buttons = [
            "Prim's",
            "Kruskal's",
            "R-Kruskal's",
            "Fast Foward",
            "Hint",
            //"Swap Graph",
            "Sensitivity",
            "Restart",
            "Restore"
        ]
        next_graph = "Swap Graph"
        primary_text = "Click the first node to start!"
        secondary_text = "Cost so far"
        var i= 0;
        var node_labels_data = new Array(nodes_centers.length).fill(0).map(x => "" + (++i) )
        let graph = {
            nodes_loc: nodes_centers,
            text_label_data : len_value,
            text_loc: [],
            line_labels: len_text_pos,
            lines_valid: len_data,
            text_label_size : "5",
            nodes_size: 3,
            lines_thickness: '2',
            nodes_labels: node_labels_data,
            label_size: '3',
            nodes_has_label: true,
            line_has_label: true,
            is_directed: false,
            is_double: false
        }
        let controler = {
            title_text : primary_text,
            second_text : secondary_text,
            next_text : next_graph,
            ButtonTexts : buttons
        }
        let data = {
            Graph : graph,
            Controler : controler
        }
        return Graph_Data(ParentFrameTypeEnum.SINGLE, FrameTypeEnum.CONTINUOUS_GRAPH, undefined, data , undefined, rsr)
    }

    let graphics = obtain_graphics(rsr).Data

    let graph_graphics = graphics.Graph

    let controler_graphics = graphics.Controler

    line_texts = graph_graphics.LineTexts

    prims_button = controler_graphics.ControlButtons[0]
    kruskals_button = controler_graphics.ControlButtons[1]
    rkruskals_button = controler_graphics.ControlButtons[2]
    fast_foward_button = controler_graphics.ControlButtons[3]
    hint_button = controler_graphics.ControlButtons[4]
    sensitivity_button = controler_graphics.ControlButtons[5];
    restart_button = controler_graphics.ControlButtons[6]
    //swap_graph_button = controler_graphics.ControlButtons[6]
    restore_button = controler_graphics.ControlButtons[7];


    nodes = graph_graphics.Nodes;
    nodes_hitboxes = graph_graphics.NodeHitboxes
    lens = graph_graphics.Lines;
    lens_hitboxes = graph_graphics.LineHitboxes;

    primary_text = controler_graphics.PrimaryText;
    secondary_text = controler_graphics.SecondaryText;
}