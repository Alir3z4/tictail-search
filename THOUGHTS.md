Thoughts
=========

## Zepto

First and first, there's no `Zepto` on client code, it's `jQuery`.

## Loading, Modeling, Handling and Abstracting data

Data files are in `CSV` format, they're not big to be scary, the only real 
challenge goes for data structure which is was handled by `server.models` 
module. `server.models.ModelObjectManager` and `server.models.Model` are 
tight together to make accessing and data in less painful way by providing
the data in objects and behave like objects and keep the relation 
between each data as simple as possible. For instance `server.models.Products`
has `shop_id` attribute which is related to it's parent shop and each 
instance of `server.models.Products` has a `server.models.Shops` instance
set on its `shop` attributes. In the case of `server.models.Tag` and
`server.models.Taggings` no relation is specified and therefore
`server.models.ModelObjectManager` is not able to tight these two models
together since defining *Many to Many* would bring more complexity to the
implementation and slower data binding. Although demoralization is an option 
that can be implemented and it could be defined in each `server.models.Model`
to gain data demoralization in matter of many to many relationship handling.


## Spatial Search

For spatial search, we have the module `server.search.Search` which 
uses ``scipy.spatial.cKDTree`` to query the data for neighbor locations/shops.
In `server.search.Search` demoralisation has been tried to be used and keeping
memory and cpu happy was one the goal. `server.search.Search` will not not 
start any data indexing or demoralization util a list of `server.models.Shops`
has been passed to `server.search.Search.set_shops` method. After setting the 
data it will start building an index of `server.models.Shops` with their 
`lat` and `lng` attributes as their hash key.

## API Endpoint
`server.api.search` has been considered as the only place of the view logic,
where all of the above mentioned modules will get crafted into and provide 
the data in a flexible way.`server.api.search` is able to handle tagging, 
limiting, radius and location and filter the products to be given.

## Practices

In the making of this tiny cool project, below ideas and practise has been used.

* Exceptional Programming 
* Object Oriented Programming
* MVC
* Polymorphism
* DRY
* TDD
* Duck Typing

### Exceptional Programming

In all the place of the code reasonable amount of ``try: except`` bock has 
been used and each part of the code will raise related `Exceptions`. All the
custom build exception that are being used in this task are defined in 
`server.exceptions`.

#### Custom Defined Exceptions

* `ObjectDoesNotExist`: Should be raised when looked up object does not exist.
* `FieldDoesNotExist`: Should be raised when an filed is being passed object 
which doesn't exists on the `server.models.Model`
* `LookupIsNotAllowed`: Should be raised when an invalid lookup is being used on filtering.
* `InvalidSortKey`: Should be raised when the sort key is invalid and doesn't exists on model.
A sort key is obviously a field on the `server.models.Model`.


### MVC

The logic or controller has been tried to be kept in `server.api` as much as 
possible where dealing with data and models are in `server.models` and
`server.search`. As for the view `client/index.html` can be considered as 
such.

### Object Oriented Programming & Polymorphism

In the making the project following best practising of Object Oriented 
Programming and Polymorphism was a leading key. `server.models` module 
speaks in objects and work with objects although there's a mixture of 
duck typing as well.

### DRY

Code has been written to be DRY as possible, in some places to reduce development
time *Make it Work, Make it Right, Make it Fast* has been followed as well, 
that made some places of code to be tiny bit WET with considering some space 
for future DRY job.


### TDD

Test Driven Development has been used to make the whole application possible.
Each part of code contains small, short and one task per method that are 
prefect fit for unit-testing.

This task came with `pytest` battery included, which has been removed to use
Python unittest standard library. For testing Flask's views `Flask-Testing` 
has been used.

### Duck Typing

Duck typing is crafted into `server.models.Model` and data loader.
