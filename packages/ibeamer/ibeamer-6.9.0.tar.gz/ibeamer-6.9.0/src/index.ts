// A simple jupyter lab/notebook front-end extension for writing beamer-style environments using CSS classes

import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
} from '@jupyterlab/application';

import {
  DOMUtils
} from '@jupyterlab/apputils';

import {
  Widget
} from '@lumino/widgets';

const ilambda_Anchor_CSS_CLASS = 'jp-ilambda-Anchor';

/**
 * Initialization data for the iBeamer extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'ibeamer:plugin',
  description: 'A simple .css Beamer/LaTeX Environment Extension for Jupyter Lab/Notebooks',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('ibeamer is activated!');

    // Create the ilambda logo wiget
    var node;
    // If the node doesn't exist, create it
    node = document.createElement("div");
    node.innerHTML = "<a href='https://www.lambda.joburg' target='_blank'><img src='https://lambda.joburg/assets/images/index/logo/lambda_logo.svg'></a>";
    const widget = new Widget({node}); // constructor for creating a widget from a DOM element
    
    widget.id = DOMUtils.createDomID();
    widget.id = "ilambda-logo";

    // provide a class for styling
    widget.addClass(ilambda_Anchor_CSS_CLASS);

    // add the widget to the DOM
    app.shell.add(widget, 'top', {rank: 1000}); // rank - move widget to right-most position in top area panel    
    
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

export default plugin;