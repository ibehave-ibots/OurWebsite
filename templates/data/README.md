## What's this folder for?

This data is accessible in jinja templates via the "site" variable.  For example: `/templates/data/navbar` would be referenced as `{{ site.navbar }}`

  
## Why not just put it in `/data`?

Because `/data` should be completely agnostic to the website (in other words, the website depends on the structure and content of data).

On the other hand, jinja templating is really helpful for managing things, so some kind of data structure to reduce the amount of html code would be very nice.  We need, then, a data structure that depends on the website's code.  We could have a `/site_data` folder or something, but I thought it might be best to make it clear that this isn't some kind of global dataset.  Thus, `/templates/data`, which puts that data close to the templates html files that are using them and farther from the pages files that shouldn't use them.


