#! /usr/bin/perl -w

use strict;
use CGI;

my $q = CGI -> new;
print $q -> header();
print $q -> start_html(-title => "Duplicate-Handling", -meta => {"http-equiv"=>"content-type", "content"=>"text/html; charset=UTF-8"});

print $q -> h1("test");

print $q -> end_html;