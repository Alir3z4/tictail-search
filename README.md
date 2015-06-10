Backend Recruiting Task
=======================

[![Build Status](https://secure.travis-ci.org/Alir3z4/tictail-search.png)](http://travis-ci.org/Alir3z4/tictail-search)
[![Coverage Status](https://coveralls.io/repos/Alir3z4/tictail-search/badge.svg)](https://coveralls.io/r/Alir3z4/tictail-search)


The story
---------

At Tictail we organize bi-annual Demo Weeks where we hack on creative projects. It's a
good way to get that side project going or validate an idea for a new feature. One of the
ideas for the upcoming Demo Week is spatial search for Tictail products around you. You
will be building the backend for that!


Provided goodies
----------------

1. A server boilerplate using `Flask`. To run the server:

  ```
  $ python runserver.py
  ```

2. A rudimentary client so you can visualize the results more easily. The client does not
have any way to communicate with the API so you will need to implement that. To run the
client:

  ```
  $ cd client
  $ python -m SimpleHTTPServer
  ```

3. Four datasets in CSV format: `shops.csv`, `products.csv`, `tags.csv` and `taggings.csv`.


What you need to do
-------------------

1. Implement the `Searcher.search()` method in the client so it can communicate with your
API. We've included `zepto` on the page so you can use that if you like.

2. Build an endpoint that returns a number of most popular products given some coordinates,
a search radius and, optionally, some tags. The number of products to return should be
given as a parameter as well. You can use popular Python libraries to your aid but you
can't use any external databases or search engines (e.g PostGIS, Elasticsearch, etc).

3. Document your design and thought process in `THOUGHTS.md`. Keep it short :-)

*You should deliver your solution as a `git` repository, preferably hosted on GitHub.*

Things to consider
------------------

1. **Quality & design:** Imagine that your solution will be delivered to production as-is,
and maintained by your fellow engineers. What are the things you need to consider to make
it production-quality?

2. **Performance:** In real-life the datasets will be big enough to cause problems to a
simple brute-force approach, so your solution should account for that. Can you do any
preprocessing or use specialized data structures?

Good luck!

*N.B: Your code is provided solely for the purposes of this exercise and will not be used by
Tictail under any circumstances.*
