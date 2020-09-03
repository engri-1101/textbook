const algorithms = require('./interactive-algorithms');

test('Test 2-opt double', () =>{
    visited = [1, 5, 3 ,4, 2, 6]
    distance_map = function(i , j){
        var dist = i - j > 0 ? i - j : j - i
        if (dist == 5){ // make last and first close
            return 1;
        } else{
            return dist
        }
    }
    expect(distance_map(1,2) < distance_map(1, 3)).toEqual(true)
    expect(algorithms.opt2(distance_map, visited)).toEqual([1,2,3,4,5,6])
});
test('Test 2-opt simple', () =>{
    visited = [1, 3, 2, 4]
    distance_map = function(i , j){
        var dist = i - j > 0 ? i - j : j - i
        if (dist == 3){ // make last and first close
            return 1;
        } else{
            return dist
        }
    }
    expect(algorithms.opt2(distance_map, visited)).toEqual([1,2,3,4])
});
test('Test 2-opt simple boundry', () =>{
    visited = [1, 3, 4, 2]
    distance_map = function(i , j){
        var dist = i - j > 0 ? i - j : j - i
        if (dist == 3){ // make last and first close
            return 1;
        } else{
            return dist
        }
    }
    expect(algorithms.opt2(distance_map, visited)).toEqual([1,4,3,2])
});