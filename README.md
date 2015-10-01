# Глас

*Work in progress.*

[![License GPL 3](https://img.shields.io/badge/license-GPL_3-green.svg)](http://www.gnu.org/licenses/gpl-3.0.txt)

This a minimalistic (essentially text-only) forum written in Python using
Django web framework. It's possible to use it in production after some
further refinement, but it's currently not the aim of this project.

Aim of the project is to practice Python/Django development. This does not
mean, however, that this is a primitive toy project. This one was approached
seriously and with certain enthusiasm, so I guess doesn't suck too badly in
what it tries to achieve.

## Features

Here is list of features that should help you understand what is this about.

* Users can register on the site.

* Once registered, user can create tagged topics.

* Other users can filter all existing topics by tag and possibly by other
  criteria; this way they can find a topic of interest.

* Every topic has introducing post. Just like any other post, it can be
  upvoted. Upvoting is reversible, but a post cannot be downvoted. Its
  rating can be used to order topics, etc.

* Although every post can be “upvoted”, there is *no* such thing as karma
  (sum of all upvotes from all posts by particular user) that would grant
  additional privileges to users. This way we avoid inequality on the site,
  while users still can see what others deem important or otherwise
  noticeable.

* Users can post in any topic of course. Standard markdown is used. User can
  only edit or delete his/her post when it's the latest post in thread.

* There is notion of user profile, which is useful if you want to edit your
  own profile but is currently quite boring if you want to take a look at
  other people's profiles. Although you can see their recent postings.

* Many other little goodish things like decent pagification, links per post,
  etc., start development server and see for yourself.

## Dependencies

There should be `requirements.txt` for your convenience, by the way.

* Python 3

* Django 1.8

* Django Registration Redux 1.2

* Django Markdown 0.8.4

## License

Copyright © 2015 Mark Karpov

Distributed under GNU GPL, version 3.
