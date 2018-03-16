---
title: Three.js first trial
date: 06/26/2015
tags: 
- Technology
- Programming
- Threejs
- Graphic
---

Recently, I am very intrigued by the webGl. There are several frameworks available on the market. For example:

* Three.js
The is the framework I choice for my little project. Its concept shares that of most of the scene graph, such as ILNumerics in C# (based on openTK). You can freely manipulate an scene object, then throw them into a scene. The webGl engine will render it for you. There are a lot of cool examples on their website with source code. Such as this one.
[Three.js example](http://threejs.org/examples/#webgl_buffergeometry)

<!--more-->

Here is my practice result:

We need to create a skeleton html first:
~~~~{.html}
<html>
  <head>
    <script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" />
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r71/three.min.js"></script>
    <script type="text/javascript" src="https://dl.dropboxusercontent.com/s/g1nqz09v5v5m57m/Detector.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/stats.js/r14/Stats.min.js"></script>
    <script src="https://dl.dropboxusercontent.com/u/3587259/Code/Threejs/OrbitControls.js"></script>
    <style media="screen">
      body {
      color: #cccccc;
      font-family: Monospace;
      font-size: 13px;
      text-align: center;
      background-color: white;
      margin: 0px;
      overflow: hidden;
      }
      #info {
      position: absolute;
      top: 0px;
      width: 100%;
      padding: 5px;
      }
      a { color: #0080ff; }
      #instruction_text {
      position: absolute;
      width:100%;
      left:50%;
      visibility: hidden;
      }
      #instruction_text p {
      position: relative;
      left:-50%;
      z-index:100;
      color: black;
      }
      #axis_legend {
      position: absolute;
      left:80%;
      width:100px;
      padding: 10px 0 0 0px;
      border:2px solid black;
      }
      #axis_legend li {
      line-height:1em;
      }
    </style>
    <title>Sample Three.js</title>
  </head>
  <body>
    <nav class="navbar navbar-default">
      <div class="container-fluid">
        <!-- Brand and toggle get grouped for better mobile display -->
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
          <span class="sr-only">Toggle navigation</span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          </button>
        </div>
        <!-- Collect the nav links, forms, and other content for toggling -->
        <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
          <ul class="nav navbar-nav">
            <li><a role="button" id="print3D">SnapShot</a></li>
            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Options <span class="caret"></span></a>
              <ul class="dropdown-menu">
                <li><a role="button" id="instruction_button" class="toggle_button">Instruction</a></li>
                <li class="active"><a role="button" id="show_points_button" class="toggle_button">Points</a></li>
                <li><a role="button" id="show_wireframe_button" class="toggle_button">WireFrame</a></li>
              </ul>
            </li>
          </ul>
        </div>
        <!-- /.navbar-collapse -->
      </div>
      <!-- /.container-fluid -->
    </nav>
    <div id="instruction_text">
      <p>Hold <i>Left</i> button to rotate, <i>middle</i> button to zoom, <i>right</i> button to pan.</p>
    </div>
    <div id="axis_legend">
      <ul>
        <li>
          <p id="first" style="color:#d9534f">DR0</p>
        </li>
        <li>
          <p id="second" style="color:#5cb85c">DRF1</p>
        </li>
        <li>
          <p id="third" style="color:#337ab7">DRF2</p>
        </li>
      </ul>
    </div>
    <div id="container">
    </div>
  </body>
  <footer></footer>
</html>
~~~~

Then we can apply the following js script to the html

~~~~{.js}
(function($) {
  // I am using static data here, in reality, data should be retrived from backend service
  var plotParams = {
    "Clouds": [{
      "Color": "234, 59, 255",
      "Points": [
        (omitted...)
      ],
      "SEM": {
        "xc": 4.87739791109634,
        "xr": 1.7896974687848195,
        "yc": 7.8509696190543847,
        "yr": 1.1683497112498769,
        "zc": 1.4654439940961688,
        "zr": 1.5191657662560727
      },
      "STD": {
        "xc": 4.87739791109634,
        "xr": 7.8011104059435681,
        "yc": 7.8509696190543847,
        "yr": 5.0927183220531393,
        "zc": 1.4654439940961688,
        "zr": 6.6218900535967533
      }
    }, {
      "Color": "255, 89, 89",
      "Points": [
        (omitted...)
      ],
      "SEM": {
        "xc": -3.1344389838330717,
        "xr": 2.6483711300010198,
        "yc": -7.5412077140427147,
        "yr": 2.4544386364764503,
        "zc": -0.5604799953554821,
        "zr": 2.3632904447559637
      },
      "STD": {
        "xc": -3.1344389838330717,
        "xr": 11.236087110734403,
        "yc": -7.5412077140427147,
        "yr": 10.413301223152567,
        "zc": -0.5604799953554821,
        "zr": 10.026592196401882
      }
    }, {
      "Color": "23, 55, 239",
      "Points": [
        (omitted....)
      ],
      "SEM": {
        "xc": -3.9744006243675885,
        "xr": 3.28175602733187,
        "yc": 0.16023687172210516,
        "yr": 2.72151168659635,
        "zc": -6.50233547780321,
        "zr": 2.4017869340414957
      },
      "STD": {
        "xc": -3.9744006243675885,
        "xr": 15.038895407625862,
        "yc": 0.16023687172210516,
        "yr": 12.471533308534708,
        "zc": -6.50233547780321,
        "zr": 11.006370428401063
      }
    }],
    "Title": null
  };
  if (plotParams == null || plotParams.length == 0) {
    console.log("Probabally session time out, log back in");
  }
  // begin Code
  if (!Detector.webgl) {
    Detector.addGetWebGLMessage();
  }

  var container, stats;
  var camera, scene, renderer, controls, light;
  var particleSystem;

  init();
  animate();


  function init() {
    container = document.getElementById("container");
    scene = new THREE.Scene();
    scene.fog = new THREE.Fog(0x050505, 2000, 3500);

    camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 1, 5000);
    camera.position.z = 50;


    //TrackballControls, have to include the js
    controls = new THREE.OrbitControls(camera);
    controls.damping = 0.2;
    controls.addEventListener('change', render);

    renderer = new THREE.WebGLRenderer({
      antialias: true,
      preserveDrawingBuffer: true
    });
    renderer.setClearColor(scene.fog.color);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(0xffffff, 1);
    container.appendChild(renderer.domElement);


    for (var i = 0; i < plotParams.Clouds.length; ++i) {
      scene.add(createElipsoid(plotParams.Clouds[i].SEM, rgbStringToHex(plotParams.Clouds[i].Color)));
      scene.add(createElipsoid(plotParams.Clouds[i].STD, rgbStringToHex(plotParams.Clouds[i].Color)));

      var axes = buildAxes(100);
      scene.add(axes);
      scene.add(createPoints(plotParams.Clouds[i].Points, rgbStringToRGB(plotParams.Clouds[i].Color)));
    }

    //lightning
    light = new THREE.DirectionalLight(0xffffff);
    light.position.set(1, 1, 1);
    scene.add(light);

    light = new THREE.DirectionalLight(0x002288);
    light.position.set(-1, -1, -1);
    scene.add(light);


    light = new THREE.AmbientLight(0x222222);
    scene.add(light);

    stats = new Stats();
    stats.domElement.style.position = 'absolute';
    stats.domElement.style.top = '55px';
    container.appendChild(stats.domElement);
    window.addEventListener('resize', onWindowResize, false);

  }

  function rgbStringToHex(rgbString) {
    var result = rgbStringToRGB(rgbString);
    return rgbToHex(result[0], result[1], result[2]);
  }

  function rgbStringToRGB(rgbString) {
    var result = rgbString.split(',');
    for (var i = 0; i < result.length; ++i) {
      result[i] = parseInt(result[i]);
    }
    return result;
  }

  function componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
  }

  function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
  }

  function createElipsoid(positions, colorHex) {
    var geometry = new THREE.SphereGeometry(1, 32, 32);
    var material = new THREE.MeshLambertMaterial({
      color: colorHex,
      shading: THREE.SmoothShading,
      transparent: true,
      opacity: 0.8
    });
    //var material = new THREE.MeshBasicMaterial( {transparent: true, opacity: 1, color: colorHex, wireframe:true} );
    geometry.applyMatrix(new THREE.Matrix4().makeScale(positions.xr, positions.yr, positions.zr));
    geometry.applyMatrix(new THREE.Matrix4().makeTranslation(positions.xc, positions.yc, positions.zc));
    return new THREE.Mesh(geometry, material);
  }


  function createPoints(points, colorRGB) {

    var geometry = new THREE.BufferGeometry();

    var positions = new Float32Array(points.length);
    var colors = new Float32Array(points.length);


    var n = 1000,
      n2 = n / 2; // particles spread in the cube
    for (var i = 0; i < positions.length; i += 3) {
      // positions
      positions[i] = points[i];
      positions[i + 1] = points[i + 1];

      positions[i + 2] = points[i + 2];

      // colors
      colors[i] = colorRGB[0] / 255;
      colors[i + 1] = colorRGB[1] / 255;
      colors[i + 2] = colorRGB[2] / 255;
    }
    geometry.addAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.addAttribute('color', new THREE.BufferAttribute(colors, 3));

    geometry.computeBoundingSphere();

    var material = new THREE.PointCloudMaterial({
      size: 1,
      vertexColors: THREE.VertexColors
    });

    return new THREE.PointCloud(geometry, material);

  }

  function buildAxis(src, dst, colorHex, dashed) {
    var geom = new THREE.Geometry(),
      mat;

    if (dashed) {
      mat = new THREE.LineDashedMaterial({
        linewidth: 5,
        color: colorHex,
        dashSize: 3,
        gapSize: 3
      });
    } else {
      mat = new THREE.LineBasicMaterial({
        linewidth: 5,
        color: colorHex
      });
    }

    geom.vertices.push(src.clone());
    geom.vertices.push(dst.clone());
    geom.computeLineDistances(); // This one is SUPER important, otherwise dashed lines will appear as simple plain lines

    var axis = new THREE.Line(geom, mat, THREE.LinePieces);

    return axis;
  }

  function buildAxes(length) {
    var axes = new THREE.Object3D();
    axes.add(buildAxis(new THREE.Vector3(0, 0, 0), new THREE.Vector3(length, 0, 0), 0xd9534f, false)); // +X
    axes.add(buildAxis(new THREE.Vector3(0, 0, 0), new THREE.Vector3(-length, 0, 0), 0xd9534f, true)); // -X
    axes.add(buildAxis(new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, length, 0), 0x5cb85c, false)); // +Y
    axes.add(buildAxis(new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, -length, 0), 0x5cb85c, true)); // -Y
    axes.add(buildAxis(new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, 0, length), 0x337ab7, false)); // +Z
    axes.add(buildAxis(new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, 0, -length), 0x337ab7, true)); // -Z

    return axes;
  }


  function onWindowResize() {

    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    renderer.setSize(window.innerWidth, window.innerHeight);

    controls.handleResize();

    render();

  }

  function animate() {

    requestAnimationFrame(animate);
    controls.update();
    render();
    stats.update();

  }


  var programFill = function(context) {

    context.beginPath();
    context.arc(0, 0, 0.5, 0, PI2, true);
    context.fill();

  }

  var programStroke = function(context) {

    context.lineWidth = 0.025;
    context.beginPath();
    context.arc(0, 0, 0.5, 0, PI2, true);
    context.stroke();

  }

  function render() {
    renderer.render(scene, camera);

  }


  function onPrintButtonClick() {
    window.open(Render.domElement.toDataURL("image/png"), "Final");
    return false;
  }


  //update legend
  (function(plotParams) {
    var idxRanks = plotParams.OrderedIdx;
    var legend = $('#axis_legend');
    //#axis_legend > ul > li:nth-child(2)
    for (var i = 0; i < idxRanks.length && i < 3; ++i) {
      $("#axis_legend > ul > li:nth-child(" + (i + 1) + ") > p").text("Axis_" + idxRanks[i]);
    }
  })(plotParams);

  // event listeners
  $("#print3D").on('click', function() {
    window.open(renderer.domElement.toDataURL("image/png"), "Final");
    return false;
  });

  $('.toggle_button').on('click', function() {
    if ($(this).parent().hasClass('active')) {
      $(this).parent().removeClass('active');
    } else {
      $(this).parent().addClass('active');
    }
  });

  $('#instruction_button').on('click', function() {
    var instrText = $('#instruction_text');
    var status = instrText.css("visibility");
    instrText.css('visibility', status == 'visible' ? 'hidden' : 'visible');
  });

  $('#show_points_button').on('click', function() {
    scene.traverse(function(child) {
      if (child instanceof THREE.PointCloud) {
        child.visible = !child.visible;
      }
    });
  });

  $('#show_wireframe_button').on('click', function() {
    scene.traverse(function(child) {
      if (child instanceof THREE.Mesh && child.hasOwnProperty('material')) {
        child.material.wireframe = !child.material.wireframe;
      }
    });
  });


})(jQuery);
~~~~

* Babylon.js
This framework seems focus more on game development. I played it a bit before jumping into Three.js. It is not difficult to find a lot of good articles about it.

* x3dom
This one takes different approach compare to the previous two. Instead of creating a "cavas" then using javescript to "inject" plot into the canvas. This one is more like static svg -- you write html file then the framework will render it for you, like the example provided by their website.

~~~~{.html}
<html>
    <head>
        <title>My first X3DOM page</title>
        <script type='text/javascript' src='http://www.x3dom.org/download/x3dom.js'> </script>
        <link rel='stylesheet' type='text/css' href='http://www.x3dom.org/download/x3dom.css'></link>
    </head>
    <body>
        <h1>Hello, X3DOM!</h1>
        <p>
            This is my first html page with some 3d objects.
        </p>
    </body>
</html>
~~~~

source: http://doc.x3dom.org/tutorials/basics/hello/index.html
