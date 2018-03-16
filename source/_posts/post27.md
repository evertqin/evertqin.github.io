---
title: How to setup ReactJS dev enviornment with Browserify, Babel and grunt
date: 11/24/2015
tags: 
- Technology
- Javascript
- ReactJS
- Babel
- Grunt
---

Major change has been made to ReactJS: JSXTransformer was deprecated, [Babel with Browserify](https://facebook.github.io/react/docs/getting-started.html) is now the recommended way to transcribe the jsx files. I am documenting the setup process hoping it will be helpful in the future.

<!--more-->

1. Setup project folder
    * nodejs is required, as well as npm because all of our packages depends on it.
    * cd into project folder, and run:
      ~~~
  npm init
      ~~~
2.  Install Required Software      
    * Run the following command anywhere to install browserify as a global node_module
      ~~~
  sudo npm install -g browserify
      ~~~

    * Install ReactJS related npm packages by running
      ~~~
  npm install --save react react-dom
      ~~~

    * Install Babel related modules
      ~~~
  npm install --save babelify babel-preset-reactbabel-preset-react
      ~~~
    * Install grunt and its modules. First grunt client is required:
      ~~~
  sudo npm install -g grunt-cli
      ~~~
      Then install grunt and some modules
      ~~~
  npm install --save-dev grunt grunt-contrib-uglify grunt-contrib-clean grunt-babel babel-preset-es2015 grunt-contrib-watch grunt-browserify
      ~~~
    * Optional grunt package(s)
      ~~~
  npm install --save-dev grunt-env
      ~~~
    The final package.json file under the project folder should look resemble following:
      ~~~~{.json}
  {
    "name": "react-editor",
    "version": "1.0.0",
    "description": "This is the text editor using reactjs",
    "main": "index.js",
    "dependencies": {
      "babel-preset-react": "^6.1.18",
      "babelify": "^7.2.0",
      "install": "^0.3.0",
      "npm": "^3.4.1",
      "react": "^0.14.3",
      "react-dom": "^0.14.3"
    },
    "devDependencies": {
      "babel-plugin-uglify": "^1.0.2",
      "babel-preset-es2015": "^6.1.18",
      "grunt": "^0.4.5",
      "grunt-babel": "^6.0.0",
      "grunt-browserify": "^4.0.1",
      "grunt-contrib-clean": "^0.7.0",
      "grunt-contrib-uglify": "^0.11.0",
      "grunt-contrib-watch": "^0.6.1",
      "grunt-env": "^0.4.4"
    },
    "scripts": {
      "test": "echo \"Error: no test specified\" && exit 1"
    },
    "keywords": [
      "react",
      "editor",
      "blog"
    ],
    "author": "Ruogu Qin",
    "license": "MIT"
  }
      ~~~~
    Okay, now you are all set to go to the next step.

3. setup grunt config file Gruntfile.js under your project root
      ~~~~{.javascript}
  module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    clean:['public/build'],
    env: {
      build: {
        NODE_ENV: 'production'
      }
    },
    browserify: {
      dev: {
        files:{
          'public/build/js/main.js':['public/js/**/*.js'] // Change this path to your source file folder
        },
        options:{
          debug: true,
          transform:['babelify']
        }
      },
      build: {
        files:{
          'public/build/js/main.js':['public/js/**/*.js'] // Change this path to your source file folder
        },
        options:{
          debug: false,
          transform:['babelify']
        }
      }
    },
    uglify: {
      build:{
        files:[
          {
            expand:true,
            src:'public/build/js/**/*.js', // Change this path to your source file folder
            dest:'.', // here I overwrite the babel generated js file with minified file.
            ext:'.js',
            extDot: 'last'
          }
        ]
      },
      options:{
        debug:false
      }
    },
    watch:{
      browserify: {
        files: ['public/js/**/*.js'], // Change this path to your source file folder
        tasks: ['browserify:dev'],
        options: {
          spawn: true,
        }
      }
    }
  });

  // Load the plugin that provides the "uglify" task.
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-browserify');
  grunt.loadNpmTasks('grunt-env');

  grunt.registerTask('default', ['watch']);
  grunt.registerTask('dev', ['env:dev', 'browserify:dev']);
  grunt.registerTask('build',  ['env:build', 'browserify:build', 'uglify:build']);
    };
    ~~~~
