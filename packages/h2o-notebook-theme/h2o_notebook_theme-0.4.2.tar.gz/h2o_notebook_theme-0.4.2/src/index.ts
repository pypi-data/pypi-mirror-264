import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * This is hacky, but it works. I did not find a way how to load a static file from the Jupyter extension. But I use the
 * favicon SVG in CSS and CSS files are loaded through Webpack and uses url-loader. The Webpack loader do not work in
 * this file, it seems it only runs for the `../style` directory. I'm inexperienced with the Jupyter build system, but I
 * know Webpack, so I overrided the loader in CSS to not inline the logo as Base64 and not change the name of the logo,
 * so I can reference it here.
 * TLDR; the CSS loads the file and this function uses loosely path to the file on the server, it is fragile, but works.
 */
const replaceFavicon = () => {
  const favicon = document.head.querySelector(
    'link[rel=icon]'
  ) as HTMLLinkElement;
  favicon.href = 'lab/api/themes/h2o-notebook-theme/logo.svg';
  favicon.type = 'image/svg+xml';
};

const changeTitle = () => {
  document.title = 'Notebook Lab | H2O AI Cloud';
  // The Jupyter changes the title once in the while, to prevent that, we make
  // the title read-only 👅
  Object.defineProperty(document, 'title', {
    writable: false
  });
};

const loadHeadp = () => {
  /* eslint-disable */
  // @ts-ignore
  // prettier-ignore
  window.heap = window.heap || [], heap.load = function (e, t) { window.heap.appid = e, window.heap.config = t = t || {}; var r = document.createElement("script"); r.type = "text/javascript", r.async = !0, r.src = "https://cdn.heapanalytics.com/js/heap-" + e + ".js"; var a = document.getElementsByTagName("script")[0]; a.parentNode.insertBefore(r, a); for (var n = function (e) { return function () { heap.push([e].concat(Array.prototype.slice.call(arguments, 0))) } }, p = ["addEventProperties", "addUserProperties", "clearEventProperties", "identify", "resetIdentity", "removeEventProperty", "setEventProperties", "track", "unsetEventProperty"], o = 0; o < p.length; o++)heap[p[o]] = n(p[o]) }
  // @ts-ignore
  heap.load('1090178399');
  var re = /\/user\/.+@h2o.ai\//gm;
  // @ts-ignore
  heap.addEventProperties({
    is_h2o_internal_use: re.test(window.location.pathname),
    product: 'Notebook Lab'
  });
  /* eslint-enable */
};

/**
 * Initialization data for the h2o-notebook-theme extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'h2o-notebook-theme:plugin',
  description: 'H2O.ai JupyterLab Theme',
  autoStart: true,
  requires: [IThemeManager],
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    console.log('JupyterLab extension h2o-notebook-theme is activated!');
    const style = 'h2o-notebook-theme/index.css';

    manager.register({
      name: 'H2O',
      isLight: false,
      load: () => {
        changeTitle();
        replaceFavicon();
        loadHeadp();
        return manager.loadCSS(style);
      },
      unload: () => Promise.resolve(undefined)
    });
  }
};

export default plugin;
