import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * Initialization data for the jupyterlab-poul-theme extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-poul-theme:plugin',
  description: 'JupyterLab POuL theme',
  autoStart: true,
  requires: [IThemeManager],
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    const style = 'jupyterlab-poul-theme/index.css';

    manager.register({
      name: 'JupyterLab POuL',
      isLight: false,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });
  }
};

export default plugin;
