"use strict";
(self["webpackChunkihide"] = self["webpackChunkihide"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__);
// The functionality for hiding cell source and output
// is already a built-in feature in Jupyter Lab/Notebooks
// https://github.com/jupyterlab/jupyterlab/pull/5968


/**
 * Initialization data for the ihide extension.
 */
let ihide_cell = "ihide_cell";
let ihide_source = "ihide_source";
let ihide_output = "ihide_output";
const plugin = {
    id: 'ihide:plugin',
    description: 'A jupyter lab/notebook front-end extension for hiding cells after execution by specifying metadata "ihide": true',
    autoStart: true,
    activate: (app, notebook) => {
        console.log('JupyterLab extension ihide is activated!');
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.executed.connect((_, args) => {
            var _a;
            const { cell } = args;
            const { success } = args;
            console.log("isCodeCellMode(cell.model) === " + (0,_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__.isCodeCellModel)(cell.model));
            if ((0,_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__.isCodeCellModel)(cell.model)) {
                if (success) {
                    // get cell metadata
                    let md = cell.model.sharedModel.getMetadata();
                    console.log(md);
                    if (ihide_cell in md) {
                        console.log("ihide_cell: " + ihide_cell);
                        cell.hide();
                    }
                    if (ihide_source in md) {
                        console.log("ihide_source: " + ihide_source);
                        (_a = cell.inputArea) === null || _a === void 0 ? void 0 : _a.node.classList.add("jp-inputArea-hidden-cell");
                        // cell.inputHidden = true;
                        // cell.model.sharedModel.setMetadata("source_hidden", true);
                    }
                    if (ihide_output in md) {
                        console.log("ihide_output: " + ihide_output);
                        cell.model.outputs.clear();
                        // cell.model.clearExecution();
                        // cell.model.sharedModel.setMetadata("collapsed", true);
                        // cell.model.sharedModel.setMetadata("outputs_hidden", true);
                        // let codeCellModel = <CodeCellModel>cell.model;
                        // codeCellModel.sharedModel.setOutputs;
                    }
                }
            }
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.5a158fc134045726682f.js.map