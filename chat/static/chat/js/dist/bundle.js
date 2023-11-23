/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./src/main.js":
/*!*********************!*\
  !*** ./src/main.js ***!
  \*********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _modules_home_serverPage__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./modules/home/serverPage */ \"./src/modules/home/serverPage.js\");\n/* harmony import */ var _modules_room_roomPage__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./modules/room/roomPage */ \"./src/modules/room/roomPage.js\");\n\n\n\nfunction initialize() {\n    console.log(\"Sanity check from main.js.\");\n    const currentPage = window.location.pathname;\n\n    console.log(currentPage);\n    \n    if(currentPage.match(/^\\/chat\\/server\\/\\d+\\/$/)) {\n        (0,_modules_home_serverPage__WEBPACK_IMPORTED_MODULE_0__.serverPage)(currentPage);\n    }\n    else if(currentPage.match(/^\\/chat\\/server\\/\\d+\\/\\w+\\/$/)) {\n        (0,_modules_room_roomPage__WEBPACK_IMPORTED_MODULE_1__.roomPage)();\n    }\n    else {\n        console.log(\"Page not found.\");\n    }\n}\n\nwindow.onload = initialize;\n\n//# sourceURL=webpack:///./src/main.js?");

/***/ }),

/***/ "./src/modules/home/serverPage.js":
/*!****************************************!*\
  !*** ./src/modules/home/serverPage.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   serverPage: () => (/* binding */ serverPage)\n/* harmony export */ });\nfunction serverPage(currentURL) {\n    console.log(\"Sanity check from homePage().\");\n\n    // focus 'roomInput' when user opens the page\n    document.querySelector(\"#roomInput\").focus();\n    \n    // submit if the user presses the enter key\n    document.querySelector(\"#roomInput\").onkeyup = function(e) {\n        if (e.keyCode === 13) {  // enter key\n            document.querySelector(\"#roomConnect\").click();\n        }\n    };\n    \n    // redirect to '/room/<roomInput>/'\n    document.querySelector(\"#roomConnect\").onclick = function() {\n        let roomName = document.querySelector(\"#roomInput\").value;\n        window.location.pathname = currentURL + roomName + \"/\";\n    }\n    \n    // redirect to '/room/<roomSelect>/'\n    document.querySelector(\"#roomSelect\").onchange = function() {\n        let roomName = document.querySelector(\"#roomSelect\").value.split(\" (\")[0];\n        window.location.pathname = currentURL + roomName + \"/\";\n    }    \n}\n\n\n//# sourceURL=webpack:///./src/modules/home/serverPage.js?");

/***/ }),

/***/ "./src/modules/room/roomPage.js":
/*!**************************************!*\
  !*** ./src/modules/room/roomPage.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   roomPage: () => (/* binding */ roomPage)\n/* harmony export */ });\nfunction roomPage() {\n    console.log(\"Sanity check from roomPage().\");\n\n    const roomName = JSON.parse(document.getElementById('roomName').textContent);\n\n    let chatLog = document.querySelector(\"#chatLog\");\n    let chatMessageInput = document.querySelector(\"#chatMessageInput\");\n    let chatMessageSend = document.querySelector(\"#chatMessageSend\");\n    let onlineUsersSelector = document.querySelector(\"#onlineUsersSelector\");\n\n    // adds a new option to 'onlineUsersSelector'\n    function onlineUsersSelectorAdd(value) {\n        if (document.querySelector(\"option[value='\" + value + \"']\")) return;\n        let newOption = document.createElement(\"option\");\n        newOption.value = value;\n        newOption.innerHTML = value;\n        onlineUsersSelector.appendChild(newOption);\n    }\n\n    // removes an option from 'onlineUsersSelector'\n    function onlineUsersSelectorRemove(value) {\n        let oldOption = document.querySelector(\"option[value='\" + value + \"']\");\n        if (oldOption !== null) oldOption.remove();\n    }\n\n    // focus 'chatMessageInput' when user opens the page\n    chatMessageInput.focus();\n\n    // submit if the user presses the enter key\n    chatMessageInput.onkeyup = function(e) {\n        if (e.keyCode === 13) {  // enter key\n            chatMessageSend.click();\n        }\n    };\n\n    chatMessageSend.onclick = function() {\n        if (chatMessageInput.value.length === 0) return;\n        // Forward the message to the WebSocket\n        chatSocket.send(JSON.stringify({\n            \"message\": chatMessageInput.value,\n        }));\n        // Clear the 'chatMessageInput'\n        chatMessageInput.value = \"\";\n    };\n\n    //=== Websocket communication ===//\n\n    let chatSocket = null;\n\n    function connect(){\n        chatSocket = new WebSocket(\"ws://\" + window.location.host + \"/ws/chat/\" + roomName + \"/\");\n        \n        chatSocket.onopen = function(e) {\n            console.log(\"Successfully connected to the Websocket.\")\n        }\n\n        chatSocket.onclose = function(e) {\n            console.log(\"Websocket connection closed unexpectedly. Trying to reconnect in 2s...\");\n            setTimeout(function() {\n                console.log(\"Reconnecting...\");\n                connect();\n            }, 2000);\n        }\n\n        chatSocket.onmessage = function(e) {\n            const data = JSON.parse(e.data);\n            console.log(data);\n\n            switch(data.type) {\n                case \"chat_message\":\n                    chatLog.value += data.user + \": \" + data.message + \"\\n\";\n                    break;\n                case \"user_list\":\n                    for (let i = 0; i < data.users.length; i++) {\n                        onlineUsersSelectorAdd(data.users[i]);\n                    }\n                    break;\n                case \"user_join\":\n                    chatLog.value += data.user + \" joined the room.\\n\";\n                    onlineUsersSelectorAdd(data.user);\n                    break;\n                case \"user_leave\":\n                    chatLog.value += data.user + \" left the room.\\n\";\n                    onlineUsersSelectorRemove(data.user);\n                    break;\n                case \"private_message\":\n                    chatLog.value += \"PM from \" + data.user + \": \" + data.message + \"\\n\";\n                    break;\n                case \"private_message_delivered\":\n                    chatLog.value += \"PM to \" + data.target + \": \" + data.message + \"\\n\";\n                    break;\n                default:\n                    //console.error(\"Unknown message type !\");\n                    console.error(\"Unknown message type ! \\n(data.type = \" + data.type + \")\");\n                    break;\n            }\n        }\n\n        // Scroll 'chatLog' to the bottom\n        chatLog.scrollTop = chatLog.scrollHeight;\n\n        chatSocket.onerror = function(err) {\n            console.log(\"Websocket encountered an error: \" + err.message);\n            console.log(\"Closing the socket\");\n            chatSocket.close();\n        }    \n    }\n\n    connect();\n\n    onlineUsersSelector.onchange = function() {\n        chatMessageInput.value = \"/pm \" + onlineUsersSelector.value + \" \";\n        onlineUsersSelector.value = null;\n        chatMessageInput.focus();\n    }\n}\n\n//# sourceURL=webpack:///./src/modules/room/roomPage.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = __webpack_require__("./src/main.js");
/******/ 	
/******/ })()
;