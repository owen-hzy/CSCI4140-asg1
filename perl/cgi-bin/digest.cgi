#! /usr/bin/perl -w

use strict;
use Digest::SHA qw/sha256_hex/;
use CGI;

my $q = CGI -> new;
print $q -> header();
print sha256_hex("test"), "\n";