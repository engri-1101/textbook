const algorithms = require('./interactive-algorithms.js')

const num_nodes = 4;

beforeEach(() => {
    algorithms.set_up_test()
    algorithms.set_up_value_map()
})

test('Test parent_index', () =>{
    expect(algorithms.parent_index(2)).toEqual(0);
    expect(algorithms.parent_index(1)).toEqual(0);
    expect(algorithms.parent_index(0)).toEqual(-1)
});

test('Test min heap insert basic', () =>{

    algorithms.min_heap["insert"](algorithms.min_heap["heap"], 1);
    expect(algorithms.min_heap["heap"]).toEqual([1]);
});

test('Test heapify_up', () =>{
    algorithms.min_heap["insert"](algorithms.min_heap["heap"], 1);
    algorithms.min_heap["insert"](algorithms.min_heap["heap"], 2, );
    expect(algorithms.min_heap["heap"]).toEqual([2, 1]);
});

test('Test min heap insert advanced', () =>{
    algorithms.min_heap["insert"](algorithms.min_heap["heap"], 1, );
    algorithms.min_heap["insert"](algorithms.min_heap["heap"], 2, );
    algorithms.min_heap["insert"](algorithms.min_heap["heap"], 3, );
    expect(algorithms.min_heap["heap"]).toEqual([3,1,2]);
});

test('Test min heap decreaseKey special', () =>{
    algorithms.set_up_test();
    algorithms.init_special()
    //expect(algorithms.get_item()).toEqual(algorithms.min_heap.heap);
    algorithms.min_heap["decreaseKey"](algorithms.min_heap["heap"], 1, 0, );
    expect(algorithms.min_heap["heap"]).toEqual([4,1,3,2]);
});

test('Test min heap decreaseKey', () =>{
    algorithms.min_heap["insert"](algorithms.min_heap["heap"], 1);
    algorithms.min_heap["insert"](algorithms.min_heap["heap"], 2);
    algorithms.min_heap["insert"](algorithms.min_heap["heap"], 3);
    algorithms.min_heap["insert"](algorithms.min_heap["heap"], 4);
    expect(algorithms.min_heap["heap"]).toEqual([3,1,2,4]);
    algorithms.min_heap["decreaseKey"](algorithms.min_heap["heap"], 2, 1);
    expect(algorithms.min_heap["heap"]).toEqual([2,1,3,4]);
    algorithms.min_heap["decreaseKey"](algorithms.min_heap["heap"], 4, 0);
    expect(algorithms.min_heap["heap"]).toEqual([4,2,3,1]);
    algorithms.min_heap["decreaseKey"](algorithms.min_heap["heap"], 1, 0);
    expect(algorithms.min_heap["heap"]).toEqual([4,1,3,2]);
});

test('Test left,right', () =>{
    var array = [1, 2, 3]
    expect(algorithms.left_index(array, 0)).toEqual(1)
    expect(algorithms.right_index(array, 0)).toEqual(2);
});

test('Test heapify_down', () =>{
    algorithms.min_heap["insert"](algorithms.min_heap["heap"], 1, );
    algorithms.min_heap["insert"](algorithms.min_heap["heap"], 2, );
    algorithms.min_heap["insert"](algorithms.min_heap["heap"], 3, );
    expect(algorithms.min_heap["heap"]).toEqual([3,1,2]);
    algorithms.min_heap["decreaseKey"](algorithms.min_heap["heap"], 2, 1)
    algorithms.heapify_down(algorithms.min_heap["heap"],  0);
    expect(algorithms.min_heap["heap"]).toEqual([2, 1, 3])
});

test('Test extract min', () =>{
    algorithms.min_heap["insert"](algorithms.min_heap["heap"], 1, );
    algorithms.min_heap["insert"](algorithms.min_heap["heap"], 2, );
    algorithms.min_heap["insert"](algorithms.min_heap["heap"], 3, );
    expect(algorithms.min_heap["heap"]).toEqual([3,1,2]);
    expect(algorithms.min_heap["extractMin"](algorithms.min_heap["heap"], )).toEqual(3)
    expect(algorithms.min_heap["heap"]).toEqual([2,1]);
});

test('Test diikstra', () => {
    algorithms.init_dijkstra();
    var ret_value = algorithms.dijkstra();
    expect(ret_value["node"]).toEqual(2);
    ret_value = algorithms.dijkstra();
    expect(ret_value["node"]).toEqual(3);
    ret_value = algorithms.dijkstra();
    expect(ret_value["node"]).toEqual(4);
})

