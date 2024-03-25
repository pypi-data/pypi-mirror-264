"use strict";
(self["webpackChunkibeamer"] = self["webpackChunkibeamer"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
// A simple jupyter lab/notebook front-end extension for writing beamer-style environments using CSS classes


const ilambda_Anchor_CSS_CLASS = 'jp-ilambda-Anchor';
/**
 * Initialization data for the iBeamer extension.
 */
const plugin = {
    id: 'ibeamer:plugin',
    description: 'A simple .css Beamer/LaTeX Environment Extension for Jupyter Lab/Notebooks',
    autoStart: true,
    activate: (app) => {
        console.log('ibeamer is activated!');
        // Create the ilambda logo wiget
        var node;
        // If the node doesn't exist, create it
        node = document.createElement("div");
        node.innerHTML = "<a href='https://www.lambda.joburg' target='_blank'><img src='https://lambda.joburg/assets/images/index/logo/lambda_logo.svg'></a>";
        const widget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget({ node }); // constructor for creating a widget from a DOM element
        widget.id = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.DOMUtils.createDomID();
        widget.id = "ilambda-logo";
        // provide a class for styling
        widget.addClass(ilambda_Anchor_CSS_CLASS);
        // add the widget to the DOM
        app.shell.add(widget, 'top', { rank: 1000 }); // rank - move widget to right-most position in top area panel    
        // let logos = document.getElementsByClassName(ilambda_Anchor_CSS_CLASS);
        // console.log(logos);
        // if there are multiple ilambda extensions installed,
        // each will contribute its own logo, so do the following
        // if (logos.length >= 2) {
        //   // remove all the ilambda-logo widgets from the DOM, except the first
        //   for (let i = 1; i < logos.length; i++) {
        //     logos[i].remove();
        //   }
        // }
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.4fbdccf9b33fd694973e.js.map