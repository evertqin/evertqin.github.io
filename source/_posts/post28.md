---
title: Making a Ajax file structure browser with ReactJs Flux Pattern
date: 12/16/2015
tag: 
- Technology
- Javascript
- ReactJS
- Flux
---
Consider the following scenario, we are creating a set of dropdowns each displays a series folders in a file system. User will click a dropdown to view all the folders (or files), then make a selection. After selection is made, all the dropdowns following the one user interacted with will change to show the subfolders (or files, if there are any) in the folder the user has selected.

<!--more-->

An apparent solution to that scenario is by using an cascading event structure. The figure below demonstrate this simple structure:

![Demo](http://i.imgur.com/rMInLfF.jpg=242x455)

From the figure, we can see a change event from the controls higher in the hierarchy triggers data change in the control lower in the hierarchy, which will then triggers the change of its lower hierarchical controls. This process will continue until there is no more downstream controls. There are nothing wrong with this approach, since it is very straightforward and simple. We essentially chain a unidirectional events together.

Does "unidirectional" ring a bell? Yes, we keep this word in heart when we are practicing [Flux Pattern](https://facebook.github.io/flux/docs/overview.html). The different is, in flux, it emchews a MVC pattern, ReactJS views are actually view-controllers whose responsiblities include retrieving data from stores and propagate them to children. Actions are usually user interactions with the views and they are propagated to the dispatchers who execute callbacks registered to that action to interact with corresponding store(s).

My initial reaction is: we can use Flux pattern to create this structure, we can fit our scenario perfectly into Flux pattern. The following figures shows the modified Flux structure.

![Modified Flux](http://i.imgur.com/vmev9q0.png)

Data flow is no different from the standard Flux. My change is: instead of creating separate store and view from different options, the stores can be derived from a single base store. If we are storing data of similar format, we event don't need to create separate store, we can just use the base store directly. 

The views are derived from a single base view, and to achieve the chaining, instead of binding event listeners, we do this by class inheritance. For example, view0 has a method _onChange which does some ajax requests to fetch fresh data. View1 will inherit everything from view0 (which has everything already setup), and bind its own event handler to the events emitter of view0, such as `var BaseComponent = require('./AppComponent1');`(You will see this in [Create ReactJs Components](#create-reactjs-components))

First everything I am doing here can be found on my GitHub ([https://github.com/evertqin/flux-reactjs-chain-reactions](https://github.com/evertqin/flux-reactjs-chain-reactions)). To run the demo, checkout everything then run

~~~
npm install
~~~
then
~~~
npm start
~~~
then navigate to `http://localhost:3000` to see the result.


To start from scratch, make sure you have nodejs installed, for demo purpose, I am using express to generate web scaffold, feel free to choose other types of frameworks as long as it is able to provide endpoints that is capable of returning JSON.

# Setup backend services

#### Install Express and scaffoldding the web application.
First make sure express generator is installed:

~~~
sudo npm install express-generator -g
~~~

Then type

~~~
express myapp
~~~

Replace "myapp" with the the name of your app.

You also need to add some dependencies to `package.json` besides those added by express. 

~~~{.json}
{
 "name": "nodejs-react-flux",
 "version": "0.0.0",
 "private": true,
 "scripts": {
  "start": "node ./bin/www",
  "build": "grunt",
  "test": "jest"
 },
 "dependencies": {
  "body-parser": "~1.13.2",
  "cookie-parser": "~1.3.5",
  "debug": "~2.2.0",
  "express": "~4.13.1",
  "jade": "~1.11.0",
  "morgan": "~1.6.1",
  "serve-favicon": "~2.3.0",
  "flux": "^2.1.1",
  "grunt": "^0.4.5",
  "jquery": "^2.1.4",
  "keymirror": "^0.1.1",
  "object-assign": "^4.0.1",
  "object-is": "^1.0.1"
 },
 "devDependencies": {
  "babel-preset-es2015": "^6.3.13",
  "babel-preset-react": "^6.1.18",
  "babelify": "^7.2.0",
  "browserify": "^12.0.1",
  "grunt-browserify": "^4.0.1",
  "grunt-contrib-sass": "^0.9.2",
  "grunt-contrib-watch": "^0.6.1",
  "grunt-react": "^0.12.3",
  "jest-cli": "^0.8.2",
  "babel-jest": "*",
  "react": "^0.14.3",
  "react-dom": "^0.14.3"
 },
 "jest": {
  "modulePathIgnorePatterns": [
   "/node_modules/"
  ],
  "rootDir": "",
  "scriptPreprocessor": "<rootDir>/node_modules/babel-jest",
  "testFileExtensions": ["es6", "js"],
  "moduleFileExtensions": ["jsx","js", "json", "es6"],
   "testPathDirs": [
   "<rootDir>/public/js"
  ],
  "unmockedModulePathPatterns": [
   "<rootDir>/node_modules/react",
   "<rootDir>/node_modules/react-dom",
   "<rootDir>/node_modules/react-addons-test-utils",
   "<rootDir>/node_modules/fbjs"
  ]
 },
 "author": "Ruogu Qin",
 "license": "MIT"
}
~~~

The file can also be found on my GitHub ([https://github.com/evertqin/flux-reactjs-chain-reactions/blob/master/package.json](https://github.com/evertqin/flux-reactjs-chain-reactions/blob/master/package.json)).

After adding necessary dependencies, run `npm install`.

#### Setup grunt for automation. 
I used browserify to compile js/jsx/es6 files, I also used jest(which is the default testing framework provided in official flux example)

Install grunt by typing:

~~~
sudo npm install grunt-cli -g
~~~

Modify the `gruntfile.js` according to [https://github.com/evertqin/flux-reactjs-chain-reactions/blob/master/gruntfile.js](https://github.com/evertqin/flux-reactjs-chain-reactions/blob/master/gruntfile.js), 

~~~{.json}
/*
This file in the main entry point for defining grunt tasks and using grunt plugins.
Click here to learn more. http://go.microsoft.com/fwlink/?LinkID=513275&clcid=0x409
*/
module.exports = function(grunt) {
  grunt.initConfig({
  pkg: grunt.file.readJSON('package.json'),
  
  browserify: {
   dist: {
       options: {
          transform: [
            ["babelify", {
              presets: ["react", "es2015"]
            }]
          ],
          noParse: ["~/node_modules/jquery/**/*", "~/node_modules/react/**/*", "~/node_modules/react-dom/**/*"],
          browserifyOptions: {
            debug: true
          }
        },
        files: {
          "public/build/js/app-bundle.js": ["public/js/app.jsx"]
        }
      }

    },

    sass: {
      dynamic_mapping: {
        files: [{
          expand: true,
          cwd: 'public/stylesheets',
          src: ['*.scss'],
          dest: 'public/build/stylesheets',
          ext: '.css',
        }]
      }
    },

    watch: {
      js: {
        files: ["public/js/**/*.jsx", "public/js/**/*.js", "!public/build/**/*", "!public/js/**/__tests__/*"],
        tasks: ["browserify"]
      },
      css: {
        files:["public/stylesheets/**/*.scss"],
        tasks: ["sass"]
      }
    }
  });

  grunt.registerTask('default', ['watch']);
  grunt.registerTask('build', ['browserify', 'sass']);
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-browserify');
  grunt.loadNpmTasks('grunt-contrib-watch');

};
~~~
the default task is registed as watch, you can build your browserify bundle by typing `grunt build`.

#### Add routes
I add three endpoints to the express router. Because I want to demonstrate populating three dropdowns, so each of these endpoints returns an array in JSON format. 

~~~{.javascript}
var express = require('express');
var url = require('url');
var querystring = require('querystring');
var fs = require('fs');
var path = require('path');
var router = express.Router();
var HOME = process.env[(process.platform == 'win32') ? 'USERPROFILE' : 'HOME'];

/* GET home page. */

router.get('/', function(req, res) {
 res.render('index', {
  title: 'Express'
 });
});

router.get('/Analysis/root', function(req, res, next) {
 fs.readdir(HOME, function(err, files) {
  if (err) {
   res.send([]);
   return;
  }

  if (files) {
   files = files.filter(function(item) {
    return fs.lstatSync(path.join(HOME, item)).isDirectory();
   });
   res.send(files);
  } else {
   res.send([]);
  }
 });
});

router.get('/Analysis/level0', function(req, res, next) {
 var selected = req.query.root;
 fs.readdir(path.join(HOME, selected), function(err, files) {
  if (err) {
   res.send([]);
   return;
  }
  if (files) {
   files = files.filter(function(item) {
    return fs.lstatSync(path.join(HOME, selected, item)).isDirectory();
   });
   res.send(files);
  } else {
   res.send([]);
  }
 });
});

router.get('/Analysis/level1', function(req, res, next) {
 var root = req.query.root;
 var level0 = req.query.level0;

 fs.readdir(path.join(HOME, root, level0), function(err, files) {
  if (err) {
   res.send([]);
  } else {
   res.send(files);
  }
 });
});

module.exports = router;
~~~


Please check the file on GitHub ([https://github.com/evertqin/flux-reactjs-chain-reactions/blob/master/routes/index.js](https://github.com/evertqin/flux-reactjs-chain-reactions/blob/master/routes/index.js)).

Now we have created all the backend services we need, we can try to test it here. Navigate to the root directory of "myapp" then type `npm start`. It everything is correct, you should see Express Hello world page.

# Setup flux and reactjs 

Next, we are moving to creating frontend code. It is important to setup folder structures for your ReactJs and flux application, the resultant directory tree should be more or less like this:

~~~
myapp
|-actions
|-components
|-configs
|-constants
|-dispatcher
|-stores
|-utils
~~~

## Setup dispatcher

Since we are not making any customize modification for now, I using the default dispatcher.

~~~
var Dispatcher = require('flux').Dispatcher;
module.exports = new Dispatcher();
~~~
[Flux ToDo List Tutorial](https://facebook.github.io/flux/docs/todo-list.html#creating-a-dispatcher) gives more detailed insight about the dispatcher.


## Create Actions
Depends on the type of the actions, the approperate dispatcher is called to trigger the invocation of a registered callback. I generalize this part assuming our application is doing one thing, getting an action type, wait for all the upstream actions to finish, then broadcast this action as event.

~~~{.javascript}
var AppDispatcher = require('../dispatcher/AppDispatcher');
var Constants = require('../constants/constants');
var ActionTypes = require('./Actions');

var Actions = {
	excute: function(actionType, value) {
		AppDispatcher.dispatch({
			actionType: actionType,
			value: value,
		});
	}
};

module.exports = Actions;
~~~

## Setup stores

Instead of creating one store for each of the component (which is how the official tutorial do it). I am generalizing stores and use a store manager to manage data and events for all the stores. A store config file is used to tell the store manager what stores will be initialized and how they are initialized.

The following `Config.js` is located under configs folder
~~~{.javascript}
'use strict';
var Config = [{
	name: 'AppComponent0',
	class: require('../stores/Store'),
}, {
	name: 'AppComponent1',
	class: require('../stores/Store'),
},{
	name: 'AppComponent2',
	class: require('../stores/Store'),
} ];

module.exports = Config;
~~~
Storemanager will read the above file and populate an array of store object:

~~~
"use strict";

var AppDispatcher = require('../dispatcher/AppDispatcher');
var storesConfig = require('../configs/Config');

class StoresManager {
	constructor() {
		this._stores = {};
		this._order = [];
	}

	add(store) {
		if (!!store) {
			if (!(store in this._stores)) {
				this._stores[store.name] = store;
				this._order.push(store);
			}
		}

		// we need to handle all the previous stores
		store.dispatchToken = AppDispatcher.register(function(payload) {
			var index = -1;
			for(var i = 0; i < this._order.length; ++i){
				if(this._order[i].name === payload.actionType){
					index = i;
					break;
				}
			}

			var storeIndex = this._order.indexOf(store);

			if(index > storeIndex){
				// higher hirachy actions will not cause any change in the lower 
				// hirachy stores
				return;
			}

			var pre = this._order.slice(0, index);

			AppDispatcher.waitFor(pre.map(s=>{return s.dispatchToken;}));
			store.dispatch(payload);	
			store.emitChange();
		}.bind(this));
	}

	remove(store) {
		var index = this._order.indexOf(store.name);

		if (index > -1) {
			this._stores.splice(index, 1);
		}

		if (store.name in this._stores) {
			delete this._stores[store.name];
		}
	}

	get allStores() {
		return this._order;
	}

	getStoreState(name) {
		return this._stores[name].state;
	}

	addListener(name, callback) {
		var store = this._stores[name];

		if(store){
			store.addChangeListener(callback);
		}
	}

	removeListener(name, callback){
		var store = this._stores[name];

		if(store){
			store.removeChangeListener(callback);
		}
	}

	printAllStores() {
		console.log(this._stores);
	}

	static init() {
		var storesManager = new StoresManager();

		for(var i = 0; i < storesConfig.length; ++i){
			var store = new storesConfig[i].class(storesConfig[i].name);
			storesManager.add(store);
		}
		return storesManager;

	}

}

module.exports = StoresManager.init();
~~~

Stores are added to the manager by the order they are specified in the config file and this order reflects the dependency among dropdowns. So in this case, AppComponent2 will depend on AppComponent1 which depends on AppComponent0. These stores are added to the manager in such as way that when a new store is added to the end of this hierarchy, it will register itself to the dispatcher and waitFor all the upstream stores to finish their excusion.

Single stores generally follow the same pattern, I created a generic `Store` class. Specific stores can be created by subclassing this one or by their own.

~~~{.js}
'use strict';

var EventEmitter = require('events').EventEmitter;

class Store extends EventEmitter {
	constructor(name) {
		super();

		if (!name) {
			throw new TypeError('You must provide the name of the store');
		}

		this.name = name ? name : 'Store';
		this.state = {
			list: ['Universal'],
      selected: 'Universal'
		};
		this.dispatchToken = {};
	}

	update(value){
		console.log("Updating " + value);
		for(let tag in value){
			if(value.hasOwnProperty(tag)){
				this.state[tag] = value[tag];
			}
		}
	}

	dispatch(action) {
		console.log("Dispatching \"" + this.name + "\"." );
		if(!Object.is(action.value, this.state)) {
			this.update(action.value);
		}
	}

	emitChange() {
		console.log("Emitting " + this.name);
		super.emit(this.name);
	}

	addChangeListener(callback) {
		super.on(this.name, callback);
	}

	removeChangeListener(callback) {
		super.removeListener(this.name, callback);
	}


}

module.exports = Store;
~~~

## <a name="create-reactjs-components"></a>Create ReactJs Components
This is the key part, to get the application running, we need to create ReactJs UI component. We start with a base component.

~~~{.js}
'use strict';

var React = require('react');
var StoresManager = require('../stores/StoresManager');
var Actions = require('../actions/Actions');
var UserControls = require('./UserControls.jsx');
var utils = require('../utils/AjaxUtils');

var ajaxGet = utils.ajaxGet;

class BaseComponent extends React.Component {
	constructor(props) {
		super(props);
		this.state = StoresManager.getStoreState(props.name);
		// we need to manually bind this to custom methods
		//https://github.com/goatslacker/alt/issues/283
		this._onChange = this._onChange.bind(this);
	}

	componentDidMount() {
		console.log("calling base componentDidMount");
		ajaxGet.call(this, this.props.url, {}).then(this._onChange);

	}

	componentWillUnmount() {
		// AnalysisInputStores.removeChangeListener(this._onChange);
	}

	_onChange(value) {
		Actions.excute(this.props.name, value);
		this.setState(StoresManager.getStoreState(this.props.name));
	}

	render() {
		return React.createElement(UserControls.AnalysisDropDown, {
			dataSource: this.state.list,
			selected: this.state.selected,
			selectChange: this._onChange
		});
	}
}

BaseComponent.propTypes = {
	name: React.PropTypes.string.isRequired,
	url: React.PropTypes.string.isRequired
};

BaseComponent.defaultProps = {
	name: 'BaseComponent', // change this
	url: '/Analysis/root'
};

module.exports = BaseComponent;
~~~
The initial data is populated by doing an ajax request to the backend. Then the _onChange event is triggered so the internal state of this component and that stored in its corresponding store are synced.

For the rest of the components, we just need to subclass its predecessors (which is the component lower in the hierarchy), and provide a customized event handler as shown below:

For example, for the first component (`AppComponent0`):

~~~{.javascript}
'use strict';

var React = require('react');
var StoresManager = require('../stores/StoresManager');
var Actions = require('../actions/Actions');
var UserControls = require('./UserControls.jsx');
var BaseComponent = require('./BaseComponent');
var utils = require('../utils/AjaxUtils');

var ajaxGet = utils.ajaxGet;

class AppComponent0 extends BaseComponent {
	constructor(props) {
		super(props);
		this.state = StoresManager.getStoreState(props.name);
	}

	render() {
		return React.createElement(UserControls.AnalysisDropDown, {
			dataSource: this.state.list,
			selected: this.state.selected,
			selectChange: this._onChange
		});
	}
}

AppComponent0.propTypes = {
	name: React.PropTypes.string.isRequired,
	url: React.PropTypes.string.isRequired
};

AppComponent0.defaultProps = {
	name: 'AppComponent0', // change this
	url: '/Analysis/root'
};

module.exports = AppComponent0;
~~~

for the second component (`AppComponent1`):
~~~{.javascript}
'use strict';

var React = require('react');
var StoresManager = require('../stores/StoresManager');
var Actions = require('../actions/Actions');
var UserControls = require('./UserControls.jsx');
var BaseComponent = require('./AppComponent0');
var utils = require('../utils/AjaxUtils');

var ajaxGet = utils.ajaxGet;

class AppComponent1 extends BaseComponent {
	constructor(props) {
		super(props);
		this.state = StoresManager.getStoreState(props.name);
		// we need to manually bind this to custom methods
		//https://github.com/goatslacker/alt/issues/283
		this._onRootChange = this._onRootChange.bind(this);
	}

	componentDidMount() {
		//Here should attach event listener to upstream store
		StoresManager.addListener(BaseComponent.name, this._onRootChange);
	}

	componentWillUnmount() {
		StoresManager.removeListener(BaseComponent.name, this._onRootChange);
	}

	_onRootChange() {
		ajaxGet.call(this, this.props.url, {
			root: StoresManager.getStoreState(BaseComponent.name).selected
		}).then(this._onChange);
	}

	render() {
		return React.createElement(UserControls.AnalysisDropDown, {
			dataSource: this.state.list,
			selected: this.state.selected,
			selectChange: this._onChange
		});
	}
}

AppComponent1.propTypes = {
	name: React.PropTypes.string.isRequired,
	root: React.PropTypes.string.isRequired,
	url: React.PropTypes.string.isRequired
};

AppComponent1.defaultProps = {
	name: 'AppComponent1', // change this
	root: '.android',
	url: '/Analysis/level0',
};

module.exports = AppComponent1;
~~~
And et cetera... to create more component in the chain, just inherit, add own event handler then register the event handler to lower hierarchical control's event emitter, and that's it!

Refer to [https://github.com/evertqin/flux-reactjs-chain-reactions/tree/master/public/js/components](https://github.com/evertqin/flux-reactjs-chain-reactions/tree/master/public/js/components) for other components necessary for creating this application.

Finally, compile the js with `npm build`, then you can check the result with http://localhost:3000

The result should look like this:

![Display Grid](http://i.imgur.com/iYVvuxh.gif)