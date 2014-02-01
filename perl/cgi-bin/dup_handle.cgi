#! /usr/bin/perl -w

use strict;
use CGI;

my $q = CGI -> new;
print $q -> header();
print $q -> h3("this is duplicate handling panel");