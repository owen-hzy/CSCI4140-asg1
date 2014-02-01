#! /usr/bin/perl -w

use strict;
use CGI;

my $q = CGI -> new;
print $q -> header();
print "This is ablum view panel";