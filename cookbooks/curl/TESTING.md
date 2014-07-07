# Testing the Cookbook #

This cookbook uses [bundler](http://gembundler.com/) and [berkshelf](http://berkshelf.com/) to isolate dependencies and run tests.

Tests are defined in the Rakefile, which in turn calls rubocop, foodcritic and chefspec.

To run all of the tests:

    $ rake

## Rubocop  ##

[Rubocop](https://github.com/bbatsov/rubocop) is a static Ruby code analyzer, based on the community [Ruby style guide](https://github.com/bbatsov/ruby-style-guide).

## Foodcritic ##

[Foodcritic](http://acrmp.github.io/foodcritic/) is a lint tool for Chef cookbooks.

## Chefspec

[ChefSpec](http://code.sethvargo.com/chefspec/) is a unit testing framework for testing Chef cookbooks. ChefSpec makes it easy to write examples and get fast feedback on cookbook changes without the need for virtual machines or cloud servers.
