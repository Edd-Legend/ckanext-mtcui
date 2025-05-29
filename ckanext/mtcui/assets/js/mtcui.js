ckan.module("mtcui-module", function ($, _) {
  "use strict";
  return {
    options: {
      debug: false,
    },
    initialize: function () {}
  };
});

"use strict";
/* example_theme_popover
*
* This JavaScript module adds a Bootstrap popover with some extra info about a
* dataset to the HTML element that the module is applied to. Users can click
* on the HTML element to show the popover.
*
* title- the title of the dataset
* license- the title of the dataset's copyright license
* num_resources- the number of resources that the dataset has.
*
*/
"use strict";

ckan.module('example_theme_popover', function ($) {
  return {
    initialize: function () {
      $.proxyAll(this, /_on/);
      this.el.popover({
        title: this.options.title,
        html: true,
        content: this._('Loading...'),
        placement: 'left'
      });
      this.el.on('click', this._onClick);
    },

    _onClick: function(event) {
      if (!this._snippetReceived) {
        this.sandbox.client.getTemplate(
          'example_theme_popover.html',
          this.options,
          this._onReceiveSnippet
        );
        this._snippetReceived = true;
      }
    },

    _snippetReceived: false,

    _onReceiveSnippet: function(html) {
      this.el.popover('destroy');
      this.el.popover({
        title: this.options.title,
        html: true,
        content: html,
        placement: 'left'
      });
      this.el.popover('show');
    }
  };
});