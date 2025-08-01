#!/bin/sh

# rbenv install 3.2.2
rbenv local 3.2.2
gem install bundler
bundle config set --local path 'vendor/bundle'
bundle install
rm -rf _site
bundle exec jekyll serve
