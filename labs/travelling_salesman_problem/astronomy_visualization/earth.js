import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.121.1/examples/jsm/controls/OrbitControls.js';
import { CSS2DRenderer, CSS2DObject } from 'https://cdn.jsdelivr.net/npm/three@0.121.1/examples/jsm/renderers/CSS2DRenderer.js';
import { GUI } from 'https://cdn.jsdelivr.net/npm/lil-gui@0.17/+esm';

const params = new Proxy(new URLSearchParams(window.location.search), {
    get: (searchParams, prop) => searchParams.get(prop),
  });
// Holds path to solution data
let solutionPath = params.solution;
console.log(solutionPath);
if (!(solutionPath === 'data/solution.csv' || solutionPath === 'data/solution_infeasible.csv')){
    solutionPath = 'data/solution.csv';
}
let dayLength = params.day;
dayLength = parseFloat(dayLength);
if (isNaN(dayLength)){
    // Determines how long a 'day' is in seconds
    dayLength = 120.0
}
console.log(dayLength);

var currentTime = 0.0;
// How long the dot should wait at each star
var waitTime = dayLength * 0.25/180.0;
// Earth rotation to start at
var startRadians = Math.PI;

// Scene Initialization
var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );
var clock = new THREE.Clock();

var renderer = new THREE.WebGLRenderer({antialias: true});
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );

let labelRenderer = new CSS2DRenderer();
labelRenderer.setSize( window.innerWidth, window.innerHeight );
labelRenderer.domElement.style.position = 'absolute';
labelRenderer.domElement.style.top = '0px';
document.body.appendChild( labelRenderer.domElement );

// Create the mesh
var geometry = new THREE.SphereGeometry( 1, 32, 32 );
var material = new THREE.MeshPhongMaterial();
var earthmesh = new THREE.Mesh( geometry, material );
scene.add( earthmesh );

// Texture the mesh
// Textures from http://planetpixelemporium.com/earth.html
material.map    = new THREE.TextureLoader().load('images/earthmap1k.jpg');
material.bumpMap   = new THREE.TextureLoader().load('images/earthbump1k.jpg');     
material.bumpScale = 0.05;

material.specularMap = new THREE.TextureLoader().load('images/earthspec1k.jpg');
material.specular  = new THREE.Color('grey');

// Lighting
const directionalLight = new THREE.DirectionalLight( 0xffffff, 0.5 );
directionalLight.position.set(0,0,1)
directionalLight.target = earthmesh;
scene.add( directionalLight );

const light = new THREE.AmbientLight( 0x404040, 0.75 );
scene.add( light );

// Camera positioning
camera.position.z = -3;
const controls = new OrbitControls(camera, labelRenderer.domElement);
controls.target = earthmesh.position;
controls.minDistance = 1.4;
controls.maxDistance = 3.0;
controls.enablePan = false;

var labels = [];
var labelsOn = true;
var starLocation = new THREE.Vector3();
function UpdateLabels() {
    if (labelsOn) {
        labels.forEach(label =>{
            label.parent.getWorldPosition(starLocation)
            label.visible = camera.position.distanceTo(starLocation) <= 2.3;
        });
    }  
}
controls.addEventListener('change', UpdateLabels);

// Load star data
var data;
var locationDict = {};
var nameDict = {};
var line;
var currentPoint = 0;
var ballmesh;
var ballPath = [];
var speed;
$.get('data/formatted_data.csv', function (CSVdata){
    data = $.csv.toArrays(CSVdata);
    data.shift();
    let furthest_dist = Math.max(...data.map((star) => star[3] * 3.1415 / 180));

    // Uncomment to place a red star for testing purposes
    // var row = [3, 3, 'Test', 0, 0, 0, 0, 0, 180, 0]
    // data.push(row)

    // Draw stars
    data.forEach(item =>{
        if (item[0] === '') {return;}
        var id = item[1];
        var proper = item[2];
        var dist = item[3] * 3.1415 / 180;
        var roh = 0.5 * dist/furthest_dist + 1.25;
        var theta = item[8] * 3.1415 / 180;
        var phi = (90-item[9]) * 3.1415 / 180;

        // Create star
        var geometry = new THREE.SphereGeometry( 0.01, 32, 32 );
        var material = new THREE.MeshPhongMaterial({emissive: 'white'});
        if (item[2] === 'Test') {material = new THREE.MeshPhongMaterial({color: 'red'});}
        var starmesh = new THREE.Mesh( geometry, material );
        earthmesh.add(starmesh);

        // Position star
        var x = roh * Math.cos(theta) * Math.sin(phi);
        var y = roh * Math.sin(theta) * Math.sin(phi);
        var z = roh * Math.cos(phi);
        starmesh.position.set(y,z,x);
        // Update location in dictionary
        locationDict[id] = [y,z,x];
        nameDict[id] = proper;

        // Create star name
        starmesh.layers.enable(1);
        const starDiv = document.createElement( 'div' );
        starDiv.className = 'label';
        starDiv.textContent = proper;
        starDiv.style.marginTop = '-1em';
        const starLabel = new CSS2DObject( starDiv );
        starLabel.position.set( 0, 0.01, 0 );
        starmesh.add( starLabel );
        labels.push(starLabel);
        starLabel.visible = false;
    });
    $('div').css('color','#FFF');
    $('div').css('font-size','15px');

    // Load solution csv and render line accordingly
    var solutions;
    $.get(solutionPath, function (SolutionData){
        solutions = $.csv.toArrays(SolutionData);
        // Remove non-point row
        solutions.shift();
        // Line wraps back to first point
        solutions.push(solutions[0]);

        material = new THREE.LineBasicMaterial({
            color: 0xff0000
        });
        
        const points = [];
        solutions.forEach(id => {
            var p = locationDict[id];
            const point = new THREE.Vector3(p[0], p[1], p[2]);
            points.push(point);
            ballPath.push(point);
        });
        
        ballPath.pop();
        const geometry = new THREE.BufferGeometry().setFromPoints( points );
        
        line = new THREE.Line( geometry, material );
        earthmesh.add( line );

         // Create ball to trace the path
        var geometry2 = new THREE.SphereGeometry( 0.02, 32, 32 );
        var material2 = new THREE.MeshPhongMaterial({emissive: 'cyan'});
        ballmesh = new THREE.Mesh( geometry2, material2 );
        earthmesh.add(ballmesh);
        var point = ballPath[currentPoint];
        currentPoint += 1;
        ballmesh.position.set(point.x, point.y, point.z);
        var totalDistance = 0;
        for (let i = 0; i < ballPath.length - 1; i++) {
            const p1 = ballPath[i];
            const p2 = ballPath[i+1];
            var dist = p1.distanceTo(p2);
            totalDistance += dist;
        }
        speed = totalDistance / (dayLength - waitTime * (ballPath.length + 1));
        earthmesh.rotateY(startRadians);
    });
    UpdateLabels();
});


// Controls for name labels
let gui;
var moving = true;
const layers = {

    'Toggle Names': function () {
        labelsOn = !labelsOn;
        if (!labelsOn) {
            labels.forEach(label =>{
                label.visible = false;
            });
        } else {
            UpdateLabels();
        }
    },

    'Toggle Path': function () {
        line.visible = !line.visible;
    },

    'Toggle Rotation': function () {
        moving = !moving;
    },
}

function initGui(){
    gui = new GUI();
	gui.add( layers, 'Toggle Names' );
    gui.add( layers, 'Toggle Path' );
    gui.add(layers, 'Toggle Rotation');
}

initGui();

// Handle resizing
window.addEventListener( 'resize', onWindowResize );
function onWindowResize() {

    camera.aspect = window.innerWidth / window.innerHeight;

    camera.updateProjectionMatrix();

    renderer.setSize( window.innerWidth, window.innerHeight );

    labelRenderer.setSize( window.innerWidth, window.innerHeight );

}

// Handle moving the ball along the path
// var waiting = true;
// var currentWaitTime = 0.0;
var lastPointTime = 0.0;
function moveBall(deltaTime) {
    if (ballmesh === undefined){
        return;
    }
    currentTime += deltaTime;
    var previousPoint;
    if (currentPoint == 0) {
        previousPoint = ballPath[ballPath.length - 1]
    } else {
        previousPoint = ballPath[currentPoint - 1]
    }
    
    if (currentTime >= dayLength) {
        currentTime = 0.0;
        currentPoint = 0;
        var point = ballPath[currentPoint]
        ballmesh.position.set(point.x, point.y, point.z);

        lastPointTime = 0.0;

        var quat = new THREE.Quaternion();
        quat.identity();
        earthmesh.rotation.setFromQuaternion(quat);
        earthmesh.rotateY(startRadians);
    }
    var nextMoveTime = lastPointTime + waitTime + previousPoint.distanceTo(ballPath[currentPoint])/speed;
    var nextWaitTime = nextMoveTime - waitTime;
    if (currentTime <= nextWaitTime) {
        // Move ball to next point
        var currentPosition = ballmesh.position;
        var target = ballPath[currentPoint];
        var delta = new THREE.Vector3();
        delta.subVectors(target, currentPosition);
        delta.normalize();
        delta.multiplyScalar(speed * deltaTime);
        var nextPosition = new THREE.Vector3();
        nextPosition.addVectors(currentPosition, delta);
        ballmesh.position.set(nextPosition.x, nextPosition.y, nextPosition.z);
    } else if (currentTime <= nextMoveTime) {
        var target = ballPath[currentPoint];
        ballmesh.position.set(target.x, target.y, target.z);
    }
    if (currentTime >= nextMoveTime) {
        lastPointTime = nextMoveTime;
        var target = ballPath[currentPoint];
        ballmesh.position.set(target.x, target.y, target.z);
        currentPoint += 1;
        if (currentPoint >= ballPath.length){
            currentPoint = 1;
        }
    }

    // Rotate Earth
    var rotationSpeed = 2 * Math.PI / dayLength;
    earthmesh.rotateY(-1 * rotationSpeed * deltaTime);
    UpdateLabels();

}

// Render Loop
function render() {
    requestAnimationFrame( render );
    renderer.render( scene, camera );
    labelRenderer.render(scene, camera);

    if (moving) {
        moveBall(clock.getDelta());
    }
}
render();