# otree_slider

![Slider animation](https://gitlab.com/gr0ssmann/otree_slider/-/raw/main/sample.gif)

This is an oTree template for sliders without anchoring and with feedback. Inspired by [Victor van Pelt's solution](https://www.accountingexperiments.com/post/sliders/), but with completely original code. Works in Firefox and on smartphones/tablets. Allows for multiple sliders on the same page. Uses compatible JavaScript (technically ES5).

See `slider/SliderPage.html` for the code of the page and `mgslider.js` for the JavaScript library. Before use, do the following:

1. Put `mgslider.js` into your project's `_static` folder.
2. Peruse and customize `slider/SliderPage.html`, especially lines 29–45.

The directory `slider` contains a complete oTree 5+ app, but the code itself is compatible with all oTree versions.

The API provides several additional features not included in the sample app. See `mgslider.js` for details. For example, one can customize the "Your value" text by writing

```javascript
slider1.yourvalue = "Your price";
```

To display currencies, one can do something like

```javascript
slider1.f2s = function (val) {
    return '$' + val.toFixed(2);
}
```

In German-language experiments, something like

```javascript
slider1.f2s = function (val) {
    return val.toFixed(2).replace('.', ',') + '&thinsp;&euro;';
}
```

should be done if currencies are to be printed.

You can customize the appearance using CSS and JavaScript. See `slider/SliderPage.html` for an example. You can hide the feedback with

```css
.mgslider-feedback {
    display: none;
}
```

## Attribution

Please see [here](https://max.pm/posts/attribution/) for information on attribution. Thank you.

## License

All code is © [Max R. P. Grossmann](https://max.pm), 2024. It is licensed under LGPLv3+. Please see LICENSE for details.

This program is distributed in the hope that it will be useful, but **without any warranty**; without even the implied warranty of **merchantability** or **fitness for a particular purpose**. See the GNU Lesser General Public License for more details.
