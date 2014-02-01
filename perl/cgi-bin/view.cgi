#! /usr/bin/perl -w

use strict;
use CGI;

my $q = CGI -> new;
print $q -> header();
print h1("This is ablum view panel");