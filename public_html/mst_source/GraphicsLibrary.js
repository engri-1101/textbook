//Data reference:


//HOW THIS WORKS: You input data as to how you want your page to be (DOUBLE.LEFT or double) and also which
//subtype the left or right will be, and then the frame inputs the correct framing values to each of the 
//subfunctions, which will take the frame and produce the pictures and return the references that you can use 
//to manipulate everything. 

let ParentFrameTypeEnum = {
    DOUBLE : "double",
    SINGLE : "single"
}
let FrameTypeEnum = {
    MATH_GRAPH : "math",
    CONTINUOUS_GRAPH : "cont",
    GRID_GRAPH : "grid",
    CHART_GRAPH : "chart",
    FLOW_GRAPH : "flow"
}

// let DataChart =  {
//     num_rows : 0,
//     num_columns : 0,
//     space : 50,
//     label_rows : [],
//     label_columns : [],
// }

// let DataGridGraph = {
//     num_rows : 2,
//     num_columns : 2,
//     exception_array: [[]],
//     is_full: true,
//     nodes_size: 0,
//     node_shadow_size,
//     lines_thickness: '',

// }

// let ContinuousGraphData = {
//     nodes_loc: nodes_centers,
//     text_loc: [],
//     line_labels: len_text_pos,
//     lines_valid: len_data,
//     text_label_size : "6",
//     nodes_size: 3,
//     lines_thickness: '2',
//     nodes_labels: [],
//     label_size: '',
//     nodes_has_label: false,
//     line_has_label: true,
//     is_directed: false,
//     is_double: false
// }

// let ControlerData = {
//     title_text : "",
//     second_text : "",
//     next_text : "",
//     ButtonTexts : []
// }
// let BundleData = {
//     Graph : undefined,
//     Controler : undefined
// }


//Need to implement clickboxes option... :(
//Next graph has to be set manually because of length 
let FrameConsts = {
    SINGLE: {INFO_COR: [112.75 + 82, 0.746574 + 5], SECOND_COR: [112.75 + 82, 15.426506 + 5],
         CONTROL_X: [90, 310], CONTROL_Y : [195, 210], GRAPH_X: [70, 330], GRAPH_Y: [40, 175]},
    DOUBLE: {
        LEFT : {INFO_COR: [103.49885, 7.746574], SECOND_COR: [103.49885, 23.746574],
    CONTROL_X: [20, 190], CONTROL_Y : [190, 220], GRAPH_X: [20, 190], GRAPH_Y: [35, 180]},
        RIGHT: {INFO_COR: [295.49885, 7.746574], SECOND_COR: [295.49885, 23.746574],
            CONTROL_X: [210, 380], CONTROL_Y : [190, 220], GRAPH_X: [210, 380], GRAPH_Y: [35, 180]}}
}
//The size of the frame is between 0 and 400 on the x-axis and 0 and 227 on the y-axis.
let Graph_Data = function(FrameType, Left, Right, Left_Data, Right_Data, rsr){
    let get_graphics_left = function(FrameConsts, Left_Data, rsr){
        switch (Left) {
            case FrameTypeEnum.CONTINUOUS_GRAPH: return {Graph : Graph_type_continuous(FrameConsts.DOUBLE.LEFT, Left_Data.Graph, rsr)
                , Controler : Controler_type(FrameConsts.DOUBLE.LEFT, Left_Data.Controler, rsr) } 
            case FrameTypeEnum.GRID_GRAPH: return {Graph : Graph_type_grid(FrameConsts.DOUBLE.LEFT, Left_Data.Graph, rsr)
                , Controler : Controler_type(FrameConsts.DOUBLE.LEFT, Left_Data.Controler, rsr)}
            case FrameTypeEnum.CHART_GRAPH: return Graph_chart(FrameConsts.DOUBLE.LEFT, Left_Data, rsr);
            case FrameTypeEnum.FLOW_GRAPH: return {Graph : Graph_type_continuous(FrameConsts.DOUBLE.LEFT, Left_Data.Graph, rsr) }
        }
    }
    let get_graphics_right = function(FrameConsts, Right_Data, rsr){
        switch (Right) {
            case FrameTypeEnum.CONTINUOUS_GRAPH: return {Graph : Graph_type_continuous(FrameConsts.DOUBLE.RIGHT, Right_Data.Graph, rsr)
                , Controler:  Controler_type(FrameConsts.DOUBLE.RIGHT, Right_Data.Controler, rsr) }
            case FrameTypeEnum.GRID_GRAPH: return  {Graph : Graph_type_grid(FrameConsts.DOUBLE.RIGHT, Right_Data.Graph, rsr)
                , Controler:  Controler_type(FrameConsts.DOUBLE.RIGHT, Right_Data.Controler, rsr) }
            case FrameTypeEnum.CHART_GRAPH: return Graph_chart(FrameConsts.DOUBLE.RIGHT, Right_Data.Graph, rsr);
            case FrameTypeEnum.FLOW_GRAPH : return {Graph: Graph_type_flow_right(FrameConsts.DOUBLE.RIGHT, Right_Data.Graph, rsr) ,
                Controler : Controler_type(FrameConsts.DOUBLE.RIGHT, Right_Data.Controler, rsr)};
        }
    }
    let get_graphics_single = function(FrameConsts, Left_Data, rsr){
        switch (Left) {
            case FrameTypeEnum.CONTINUOUS_GRAPH: return {Graph : Graph_type_continuous(FrameConsts.SINGLE, Left_Data.Graph, rsr)
                , Controler : Controler_type(FrameConsts.SINGLE, Left_Data.Controler, rsr) } 
            case FrameTypeEnum.GRID_GRAPH: return {Graph : Graph_type_grid(FrameConsts.SINGLE, Left_Data.Graph, rsr)
                , Controler : Controler_type(FrameConsts.SINGLE, Left_Data.Controler, rsr)}
            case FrameTypeEnum.CHART_GRAPH: return Graph_chart(FrameConsts.SINGLE, Left_Data.Graph, rsr);
        }
    }

    if (FrameType == ParentFrameTypeEnum.DOUBLE){
        return {Left : get_graphics_left(FrameConsts, Left_Data, rsr), Right : get_graphics_right(FrameConsts, Right_Data, rsr)}
    } else {
        return {Data : get_graphics_single(FrameConsts, Left_Data, rsr)}
    }
}

let ChartFunctions = {
    drawline : function(location1x, location1y, location2x, location2y, shift_x_vec, shift_y_vec, rsr){
        var path_str = "M " + location1x + "," + location1y + " " + location2x+ "," + location2y;
          rsr.path(path_str).attr({
                                id: path_str,
                                "font-family": 'Times New Roman',
                                fill: 'none',
                                stroke: "#000000",
                                "stroke-width": '1',
                                "stroke-linecap": 'butt',
                                "stroke-linejoin": 'miter',
                                "stroke-miterlimit": '10',
                                "stroke-dasharray": 'none',
                                "stroke-opacity": '1',
                                }).translate(shift_x_vec, shift_y_vec)
    },
    //chart_height is one third the size of the area
    drawTable : function(chart_width, chart_height, shift_x_vec, shift_y_vec, num_rows, num_columns, start_space, color, type,
        title, font_size, column_labels, row_labels, data, rsr){
        var shift = type == "TOP" ? chart_height / 2 : chart_height * 2;
        let delta_x = (chart_width - start_space) / (num_columns);
        let delta_y = chart_height / (num_rows + 1);
        
        let text_x = chart_width / 2
        let text_y = type == "TOP" ? chart_height / 4 : (chart_height * 7) / 4
        var title = rsr.text(text_x, text_y, title).attr("font-size", font_size)
        
        rsr.rect(0, 0 + shift, chart_width, delta_y).attr("fill", color)
        rsr.rect(0, 0 + shift, start_space, chart_height).attr("fill", color)
        var i;
        var sum_x = start_space
        
        for (i = 0; i < num_columns + 1 ;i ++){
            ChartFunctions.drawline(sum_x, 0 + shift, sum_x, chart_height + shift, shift_x_vec, shift_y_vec, rsr)
            sum_x = sum_x + delta_x
        }
        var sum_y = delta_y + shift
        for (i = 0; i < num_rows + 1; i ++){
            ChartFunctions.drawline(0, sum_y, chart_width, sum_y, shift_x_vec, shift_y_vec, rsr)
            sum_y = sum_y + delta_y
        }
        sum_y = shift
        for (i = 0; i < num_rows + 1; i ++){
            rsr.text(start_space / 2, sum_y + delta_y / 2, row_labels[i]).translate(shift_x_vec, shift_y_vec)
            sum_y = sum_y + delta_y
        }
        sum_x = start_space
        for (i = 0; i < num_columns; i ++){
            rsr.text(sum_x + delta_x / 2, shift + delta_y / 2 , column_labels[i]).translate(shift_x_vec, shift_y_vec)
            sum_x = sum_x + delta_x
        }
        sum_x = start_space
        sum_y = shift + delta_y
        
        var data_graphics = new Array(num_rows).fill(0).map(x => new Array(num_columns).fill(undefined))
        
        var j;
        for (i = 0; i < num_rows; i++){
            for (j = 0; j < num_columns; j++){
                data_graphics[i][j] = rsr.text(sum_x + delta_x / 2, sum_y + delta_y / 2 , data[i][j]).translate(shift_x_vec, shift_y_vec)
            sum_x = sum_x + delta_x
            }
            sum_x = start_space;
            sum_y = sum_y + delta_y
        }
        return {Title: title, Data: data_graphics}
    }
}

let Graph_chart = function(Frame, DataChart, rsr){
    default_entry_data = new Array(num_rows).fill([]).map(x => new Array(num_columns).fill(22))
    default_title_1 = "Table 1"
    default_title_2 = "Table 2"
    header_color = "#8E8D8A"
    font_size_title = "15"

    chart_width = Frame.GRAPH_X[1] - Frame.GRAPH_X[0]
    chart_height = Frame.GRAPH_Y[1] - Frame.GRAPH_Y[0]
    shift_x = Frame.GRAPH_X[0]
    shift_y = Frame.GRAPH_Y[0]

    var graphics1 = drawTable(chart_width, chart_height, shift_x, shift_y, DataChart.num_rows, DataChart.num_columns, DataChart.space, header_color,
         "TOP", default_title_1, font_size_title, Data.label_columns, Data.label_rows, default_entry_data, rsr)

    var graphics2 = drawTable(chart_width, chart_height, shift_x, shift_y, DataChart.num_rows, DataChart.num_columns, DataChart.space, header_color,
         "Bottom", default_title_2, font_size_title, Data.label_columns, Data.label_rows, default_entry_data, rsr)
    return {Title1: graphics1.Title, Title2 : graphics2.Title, Entries1: graphics1.Data, Entries2: graphics2.Data }  
}

let Graph_type_grid = function(Frame, Data, rsr){
    //(rsr, x, y, type, heuristic, part_name_next, special)
    rsr.clear();

    var left_point = Frame.GRAPH_X[0]
    var right_point = Frame.GRAPH_X[1]
    var upper_point = Frame.GRAPH_Y[0]
    var lower_point = Frame.GRAPH_Y[1]
    var horizontal_delta = (right_point - left_point) / (x - 1)
    var vertical_delta = (upper_point - lower_point) / (y - 1)
    var nodes_points = [];
    var radius_circle = Data.nodes_size;
    var radius_shadow = Data.node_shadow_size;
    var i;
    var j;
    var exception_array = Data.exception_array
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

    lens_arr = new Array(nodes_points.length).fill(0).map(v => new Array(nodes_points.length).fill(undefined));
    
    var i;
    var j;
    for (i = 0; i < nodes_points.length; i++){
        for (j = i + 1 ; j < nodes_points.length; j++){
            var id_str = (i + 1) + "-" + (j + 1);

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
            
            
            lens_arr[i][j].attr("opacity", "0")
        }
    }
    return {Nodes: nodes_arr, NodesShadow: nodes_hitbox_arr, Lens : lens_arr}
}

let ContinuousFunctions = {
    //(min_x, min_y,max_x, max_y
    //, Frame.GRAPH_X[0], Frame.GRAPH_Y[0], Frame.GRAPH_X[1], Frame.GRAPH_Y[1], locations, rsr)
    MODE_ENUM_TRANSFORM  : {Node : "node", Text : "text", Text2 : "text2"},
    transform_algorithm : function(minx, miny, maxx, maxy, framex1, framey1, framex2, framey2, locations, rsr, Mode){
        var c_shift = function (minx, miny, framex, framey){
            var deltaX = framex - minx;
            var deltaY = framey - miny;
            return {X: deltaX, Y: deltaY}
        }
        var c_streach = function (minx, miny, maxx, maxy, framex1, framey1, framex2, framey2){
            var factorX = (maxx - minx) / (framex2 - framex1)
            var factorY = (maxy - miny) / (framey2 - framey1)
            return {X: factorX, Y: factorY}
        }
        var factor_v = c_streach(minx, miny, maxx, maxy, framex1, framey1, framex2, framey2)
        var shift_v = c_shift(minx, miny, framex1, framey1)

        var shift = function(point){
            if (point != undefined){
                var new_point = [0,0]
                new_point[0] = shift_v.X + point[0]
                new_point[1] = shift_v.Y + point[1]
                return new_point
            } else {
                return point
            }
        }
        var streach = function(point){
            if (point != undefined){
                var new_point = [0, 0]
                new_point[0] = (1 / factor_v.X ) * (point[0] - framex1) + framex1
                new_point[1] = (1 / factor_v.Y) * (point[1] - framey1) + framey1
                return new_point;
            } else {
                return point
            }
        }
        return Mode == ContinuousFunctions.MODE_ENUM_TRANSFORM.Node ? locations.map(shift).map(streach)
        : locations.map(function(row) {return row.map(shift).map(streach)})
    },
    make_nodes_pre : function(nodes_loc, nodes_size, opacity, rsr){
        var nodes = new Array(nodes_loc.size).fill(undefined)
        var i = 0;
        nodes_loc.forEach(element => {
            nodes[i] = rsr.circle(element[0], element[1], nodes_size).attr({parent: 'layer1',fill: '#e98074',"fill-opacity": opacity,stroke: 'none','stroke-width':'1','stroke-opacity':opacity,"stroke-width": '0.79',"stroke-miterlimit": '4',"stroke-dasharray": 'none',"stroke-opacity": '1'}).data("id", "n" + (i + 1))
            i++;
        })
        return nodes;
    },
    make_nodes : function(nodes_loc, nodes_size, rsr){
        return ContinuousFunctions.make_nodes_pre(nodes_loc, nodes_size, "1", rsr);
    },
    make_node_hitboxes : function(nodes_loc, nodes_size, rsr){
        return ContinuousFunctions.make_nodes_pre(nodes_loc, nodes_size + 0.5, "0", rsr)
    },
    make_node_texts : function(nodes_loc, nodes_labels, label_size, rsr){
        nodes_texts = new Array(nodes_loc.length).fill(undefined)
        nodes_labels.forEach(function(value, index, array){
            nodes_texts[index] = rsr.text(nodes_loc[index][0], nodes_loc[index][1], value).attr("font-size", label_size)
        })
        return nodes_texts;
    },
    make_line_texts : function(line_loc, text_label_data, label_size, rsr){
        line_texts = new Array(line_loc.length).fill([]).map(x => new Array(line_loc[0].length).fill(undefined))
        var i;
        var j;
        for (i = 0; i < line_loc.length; i++){
            for (j = 0; j < line_loc.length; j++){
                if (line_loc[i][j] != undefined && line_loc[i][j] != null){
                    line_texts[i][j] = rsr.text(line_loc[i][j][0], line_loc[i][j][1], text_label_data[i][j]).attr("font-size", label_size).attr("fill", "8E8D8A")
                }
            }
        }
        return line_texts;
    },

    // //By default lower to higher is valid if not directed, if not either is valid.
    // //This is not enforced, this must be a property of the data
    make_lines_pre : function(lines_valid, double, directed, thickness, nodes_loc, opacity, rsr){
        var lines = new Array(nodes_loc.length).fill(0).map(x => new Array(nodes_loc.length).fill(undefined))
        var i;
        var j;
        if (double){
            for (i = 0; i < nodes_loc.length; i++){
                for (j = 0; j < nodes_loc.length; j++){
                    if (lines_valid[i][j] == true){
                        var location1x = nodes_loc[i][0]
                        var location1y = nodes_loc[i][1]
                        var location2x = nodes_loc[j][0]
                        var location2y = nodes_loc[j][1]

                        var vectorx = location2x - location1x;
                        var vectory = location2y - location1y;
                        var length = Math.sqrt( vectorx * vectorx + vectory * vectory)
                        function rotate_vec(x, y){
                            xprime = x * Math.cos(Math.PI / 2) - y * Math.sin(Math.PI / 2)
                            yprime = x * Math.sin(Math.PI / 2) + y * Math.cos(Math.PI / 2)
                            return {X : xprime, Y : yprime}
                        }
                        var vector = rotate_vec(1.5 * vectorx / length, 1.5 * vectory / length)

                        //sets a particular (arbitrary) direction for one side of matrix symmetry line

                        location1x = location1x + vector.X
                        location2x = location2x + vector.X
                        location2y = location2y + vector.Y
                        location1y = location1y + vector.Y

                        var path_str = "M " + location1x + "," + location1y + " " + location2x+ "," + location2y;

                        var id_str = (i + 1) + "-" + (j + 1);
                        if (directed){
                            var length = Math.sqrt(Math.pow(location1x - location2x, 2) + Math.pow(location1y - location2y, 2))
                            var deltax = (location2x - location1x) / length;
                            var deltay = (location2y - location1y) / length;
                            deltax = deltax * -12;
                            deltay = deltay * -12;
                            location2x = deltax + location2x// + location2x;
                            location2y = deltay + location2y// + location2y;
                            var path_str = "M " + location1x + "," + location1y + " " + location2x+ "," + location2y;

                            lines[i][j] = rsr.path(path_str).attr({
                                id: id_str,
                                parent: 'layer1',
                                "font-family": 'Times New Roman',
                                fill: 'none',
                                stroke: "#8E8D8A",
                                "stroke-width": thickness,
                                "stroke-linecap": 'butt',
                                "stroke-linejoin": 'miter',
                                "stroke-miterlimit": '10',
                                "stroke-dasharray": 'none',
                                "stroke-opacity": opacity,
                                "arrow-end": "classic-narrow-short" 
                                }).data("id", id_str)
                        } else {
                            lines[i][j] = rsr.path(path_str).attr({
                                id: id_str,
                                parent: 'layer1',
                                "font-family": 'Times New Roman',
                                fill: 'none',
                                stroke: "#8E8D8A",
                                "stroke-width": thickness,
                                "stroke-linecap": 'butt',
                                "stroke-linejoin": 'miter',
                                "stroke-miterlimit": '10',
                                "stroke-dasharray": 'none',
                                "stroke-opacity": opacity,
                                }).data("id", id_str)
                        }
                    }
                }
            }
        } else
            for (i = 0; i < nodes_loc.length; i++){
                for (j = 0; j < nodes_loc.length; j++){
                    if (lines_valid[i][j] == true){
                        var location1x = nodes_loc[i][0]
                        var location1y = nodes_loc[i][1]
                        var location2x = nodes_loc[j][0]
                        var location2y = nodes_loc[j][1]

                        var path_str = "M " + location1x + "," + location1y + " " + location2x+ "," + location2y;
                        var id_str = (i + 1) + "-" + (j + 1);
                        
                        if (directed){
                            var length = Math.sqrt(Math.pow(location1x - location2x, 2) + Math.pow(location1y - location2y, 2))
                            var deltax = (location2x - location1x) / length;
                            var deltay = (location2y - location1y) / length;
                            deltax = deltax * -2.5;
                            deltay = deltay * -2.5;
                            location2x = deltax + location2x// + location2x;
                            location2y = deltay + location2y// + location2y;
                            var path_str = "M " + location1x + "," + location1y + " " + location2x+ "," + location2y;
                            lines[i][j] = rsr.path(path_str).attr({
                                id: id_str,
                                parent: 'layer1',
                                "font-family": 'Times New Roman',
                                fill: 'none',
                                stroke: "#8E8D8A",
                                "stroke-width": thickness,
                                "stroke-linecap": 'butt',
                                "stroke-linejoin": 'miter',
                                "stroke-miterlimit": '10',
                                "stroke-dasharray": 'none',
                                "stroke-opacity": opacity,
                                "arrow-end": "classic" // differing line
                                })
                        } else{
                            lines[i][j] = rsr.path(path_str).attr({
                                "font-family": 'Times New Roman',
                                fill: 'none',
                                stroke: "#8E8D8A",
                                "stroke-width": thickness,
                                "stroke-linecap": 'butt',
                                "stroke-linejoin": 'miter',
                                "stroke-miterlimit": '10',
                                "stroke-dasharray": 'none',
                                "stroke-opacity": opacity
                                }).data("id", id_str)
                        }
                    }
                }
            }
        return lines;
    },
    make_lines : function(lines_valid, double, directed, thickness, nodes_loc, rsr){
        return ContinuousFunctions.make_lines_pre(lines_valid, double, directed, thickness, nodes_loc, "1", rsr)
    },
    make_line_hitboxes : function(lines_valid, double, directed, thickness, nodes_loc, rsr){
        return ContinuousFunctions.make_lines_pre(lines_valid, double, false, (parseInt(thickness) + 2) + "", nodes_loc, "0", rsr)
    }
}
let ApplyTransformBase = function(Frame, min_x, min_y, max_x, max_y, rsr, transforme, Mode ){
    
    return ContinuousFunctions.transform_algorithm(min_x, min_y,max_x, max_y
        , Frame.GRAPH_X[0], Frame.GRAPH_Y[0], Frame.GRAPH_X[1], Frame.GRAPH_Y[1], transforme, rsr, Mode)
}

let transformBasic = function(Frame, locations, text_locations, rsr, Mode){
    
    var min_x = locations[0][0]
    var min_y = locations[0][1]
    locations.forEach(element => {
    if (element[0] < min_x){
        min_x = element[0]
    }
    if (element[1] < min_y){
        min_y = element[1]
    }
    })
    text_locations.forEach(element2 => {
        if (element2 != null && element2 != undefined){
            element2.forEach(element => {
                if (element != null && element != undefined){
                    if (element[0] < min_x){
                        min_x = element[0]
                    }
                    if (element[1] < min_y){
                        min_y = element[1]
                    }
                }
            })
        }
    })
    var max_x = locations[0][0]
    var max_y = locations[0][1]
    locations.forEach(element => {
        if (element[0] > max_x){
            max_x = element[0]
        }
        if (element[1] > max_y){
            max_y = element[1]
        }
    })
    text_locations.forEach( element => {
        if (element != null && element != undefined){
            element.forEach(element2 => {
                if (element2 != null && element2 != undefined){
                    if (element2[0] > max_x){
                        max_x = element2[0]
                    }
                    if (element2[1] > max_y){
                        max_y = element2[1]
                    }
                }
            })
        }
    })
    return {Min_x : min_x, Max_x : max_x, Min_y : min_y, Max_y : max_y};
}
let transformAdvanced = function(Frame, locations, text_locations1, text_locations2, rsr, Mode){
    structure = transformBasic(Frame, locations, text_locations1, rsr, Mode);
    var min_x = structure.Min_x;
    var max_x = structure.Max_x;
    var min_y = structure.Min_y;
    var max_y = structure.Max_y;
    text_locations2.forEach( element => {
        if (element != null && element != undefined){
            element.forEach(element2 => {
                if (element2 != null && element2 != undefined){
                    if (element2[0] > max_x){
                        max_x = element2[0]
                    }
                    if (element2[1] > max_y){
                        max_y = element2[1]
                    }
                }
            })
        }
    })
    return {Min_x : min_x, Max_x : max_x, Min_y : min_y, Max_y : max_y};
}

let ApplyTransform = function(Frame, locations,text_locations, rsr, Mode){
    
    structure = transformBasic(Frame, locations, text_locations, rsr, Mode);
    var min_x = structure.Min_x;
    var max_x = structure.Max_x;
    var min_y = structure.Min_y;
    var max_y = structure.Max_y; 

    var new_locations = Mode == ContinuousFunctions.MODE_ENUM_TRANSFORM.Node ?
    ApplyTransformBase(Frame, min_x, min_y,max_x, max_y, rsr, locations, Mode)
    : ApplyTransformBase(Frame, min_x, min_y,max_x, max_y, rsr, text_locations, Mode)

    return new_locations;
}
let ApplyTransform2 = function(Frame, locations,text_locations1, text_locations2, rsr, Mode){
    structure = transformAdvanced(Frame, locations, text_locations1, text_locations2, rsr, Mode);
    var min_x = structure.Min_x;
    var max_x = structure.Max_x;
    var min_y = structure.Min_y;
    var max_y = structure.Max_y;
    if (Mode == ContinuousFunctions.MODE_ENUM_TRANSFORM.Node){
        return ApplyTransformBase(Frame, min_x, min_y,max_x, max_y, rsr, locations, Mode)
    } else if (Mode == ContinuousFunctions.MODE_ENUM_TRANSFORM.Text){
        return ApplyTransformBase(Frame, min_x, min_y,max_x, max_y, rsr, text_locations1, Mode)
    } else if (Mode) {
        return ApplyTransformBase(Frame, min_x, min_y,max_x, max_y, rsr, text_locations2, Mode)
    }
}

let Graph_type_continuous = function(Frame, Data, rsr){

    
    //Send texts and nodes
    
    var new_nodes_loc = ApplyTransform(Frame, Data.nodes_loc, Data.line_labels, rsr, ContinuousFunctions.MODE_ENUM_TRANSFORM.Node)
    
    var new_text_loc = ApplyTransform(Frame, Data.nodes_loc, Data.line_labels, rsr, ContinuousFunctions.MODE_ENUM_TRANSFORM.Text)
    

    var lines = ContinuousFunctions.make_lines(Data.lines_valid, Data.is_double, Data.lines_directed, Data.lines_thickness, new_nodes_loc, rsr)
    var nodes = ContinuousFunctions.make_nodes(new_nodes_loc, Data.nodes_size, rsr)
    var node_texts = Data.nodes_has_label ? ContinuousFunctions.make_node_texts(new_nodes_loc, Data.nodes_labels, Data.label_size, rsr) : undefined
    var line_hitboxes = ContinuousFunctions.make_line_hitboxes(Data.lines_valid, Data.is_double, Data.lines_directed, Data.lines_thickness, new_nodes_loc, rsr)
    var node_hitboxes = ContinuousFunctions.make_node_hitboxes(new_nodes_loc, Data.nodes_size, rsr)
    var line_texts = ContinuousFunctions.make_line_texts(new_text_loc, Data.text_label_data, Data.text_label_size, rsr)

    nodes.forEach(element => {
        //element.attr("opacity", "0")
    })
    return {Nodes : nodes, Labels : node_texts, Lines : lines, LineHitboxes : line_hitboxes, NodeHitboxes : node_hitboxes, LineTexts : line_texts}
}

let Graph_type_flow_right = function(Frame, Data, rsr){
    var new_nodes_loc = ApplyTransform2(Frame, Data.nodes_loc, Data.line_labels, Data.line_labels2, rsr, ContinuousFunctions.MODE_ENUM_TRANSFORM.Node)
    var new_text_loc = ApplyTransform2(Frame, Data.nodes_loc, Data.line_labels,  Data.line_labels2, rsr, ContinuousFunctions.MODE_ENUM_TRANSFORM.Text)
    var new_text_loc2 = ApplyTransform2(Frame, Data.nodes_loc, Data.line_labels2,  Data.line_labels2, rsr, ContinuousFunctions.MODE_ENUM_TRANSFORM.Text2)
    

    var lines = ContinuousFunctions.make_lines(Data.lines_valid, Data.is_double, Data.lines_directed, Data.lines_thickness, new_nodes_loc, rsr)
    var nodes = ContinuousFunctions.make_nodes(new_nodes_loc, Data.nodes_size, rsr)
    var node_texts = Data.nodes_has_label ? ContinuousFunctions.make_node_texts(new_nodes_loc, Data.nodes_labels, Data.label_size, rsr) : undefined
    var line_hitboxes = ContinuousFunctions.make_line_hitboxes(Data.lines_valid, Data.is_double, Data.lines_directed, Data.lines_thickness, new_nodes_loc, rsr)
    var node_hitboxes = ContinuousFunctions.make_node_hitboxes(new_nodes_loc, Data.nodes_size, rsr)
    var line_texts = ContinuousFunctions.make_line_texts(new_text_loc, Data.text_label_data, Data.text_label_size, rsr)
    var line_texts2 = ContinuousFunctions.make_line_texts(new_text_loc2, Data.text_label_data2, Data.text_label_size, rsr)
    return {Nodes : nodes, Labels : node_texts, Lines : lines, LineHitboxes : line_hitboxes, NodeHitboxes : node_hitboxes, LineTexts : line_texts, LineTexts2 : line_texts2}
}


let Controler_type = function(Frame, Data, rsr){
    //Next graph has to be et manually because of length 
    //8 spots for a controler on a DOUBLE.LEFT, 6 on a double
    var instructxt = rsr.text(Frame.INFO_COR[0], Frame.INFO_COR[1], Data.title_text).attr("font-size", "12").attr("fill", "8E8D8A")
    var costtxt = rsr.text(Frame.SECOND_COR[0], Frame.SECOND_COR[1], Data.second_text).attr("fill", "8E8D8A").attr("font-size", "10")
    //var nexttext = rsr.text(Frame.INFO_COR[0], Frame.CONTROL_Y[1] + 12, Data.next_text).attr("fill", "8E8D8A")
    var Buttons = new Array(Data.ButtonTexts.length).fill(undefined)
    var num_row1_buttons = Math.ceil(Data.ButtonTexts.length / 2)
    var num_row2_buttons = Math.floor(Data.ButtonTexts.length / 2)
    var i;
    var total = Frame.CONTROL_X[0]
    var delta = (Frame.CONTROL_X[1] - Frame.CONTROL_X[0]) / num_row1_buttons
    var shift = delta / 2;
    var q = 0;
    for (i = 0; i < num_row1_buttons ; i ++){
        Buttons[q] = rsr.text(total + shift, Frame.CONTROL_Y[0], Data.ButtonTexts[q]).attr("font-size", "9").attr("fill", "8E8D8A")
        q++
        total += delta;
    }
    total = Frame.CONTROL_X[0]
    delta = (Frame.CONTROL_X[1] - Frame.CONTROL_X[0]) / num_row2_buttons
    shift = delta / 2
    for (i = 0; i < num_row2_buttons; i++){
        Buttons[q] = rsr.text(total + shift, Frame.CONTROL_Y[1], Data.ButtonTexts[q]).attr("font-size", "9").attr("fill", "8E8D8A")
        q++
        total += delta;
    }
    return {ControlButtons : Buttons, PrimaryText : instructxt, SecondaryText : costtxt}
}


