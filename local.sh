#!/bin/sh

rbenv install 3.2.2
rbenv local 3.2.2
gem install bundler
bundle config set --local path 'vendor/bundle'
bundle install
bundle exec jekyll serve
