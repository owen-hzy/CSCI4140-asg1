#! /usr/bin/perl -w

use strict;
use CGI;

do "./include.cgi";
# Check the session info
session_check();
###

my $q = CGI -> new;
