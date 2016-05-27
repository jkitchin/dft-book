The zen and zen-based themes are very customizable, so to make these themes work, you have to use this [conf.py](https://github.com/damianavila/damian_blog/blob/master/conf.py), obviously with your custom changes ;-)

More info about the zen themes family [here](http://www.damian.oquanta.info/posts/nikolas-zen-theme-finally-released.html).

Enjoy!

Damián

**WARNING:** 
The zen themes are LESS-powered (not less... because it is more-powered ;-))
If you use webassests (USE_BUNDLES = True in your conf.py), the theme will use compiled css files, so don't worry at all...
But, if you want to build the css files from the zen LESS files, you have to use USE_BUNDLES = False, and have installed the `lessc` (official LESS compiler). 
Additionaly, you have a LESS plugin available in the Nikola plugins repo to automatically build the LESS files inside `nikola build` command.
You can easily install it just doing: `nikola plugin -i less`.

