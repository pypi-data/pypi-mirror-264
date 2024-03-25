// The functionality for hiding cell source and output
// is already a built-in feature in Jupyter Lab/Notebooks
// https://github.com/jupyterlab/jupyterlab/pull/5968

import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
} from '@jupyterlab/application';

import {
  NotebookActions,
  Notebook,
} from '@jupyterlab/notebook';

import {
  // CodeCellModel,
  isCodeCellModel,
} from '@jupyterlab/cells';

/**
 * Initialization data for the ihide extension.
 */

let ihide_cell = "ihide_cell";
let ihide_source = "ihide_source";
let ihide_output = "ihide_output";

const plugin: JupyterFrontEndPlugin<void> = {
  id: 'ihide:plugin',
  description: 'A jupyter lab/notebook front-end extension for hiding cells after execution by specifying metadata "ihide": true',
  autoStart: true,
  activate: (app: JupyterFrontEnd, notebook: Notebook) => {
    console.log('JupyterLab extension ihide is activated!');

    NotebookActions.executed.connect((_, args) => {
      
      const { cell } = args;
      const { success } = args;

      console.log("isCodeCellMode(cell.model) === " + isCodeCellModel(cell.model));

      if (isCodeCellModel(cell.model)) {

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
            cell.inputArea?.node.classList.add("jp-inputArea-hidden-cell");
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

export default plugin;
