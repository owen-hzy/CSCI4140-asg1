#! /usr/bin/perl -w

use CGI;
use DBI;
use strict;

my $q = CGI -> new;
my $action = $q -> url_param("action");
my $row = $q -> param("row") || $q -> cookie("row") || 2;
my $column = $q -> param("column") || $q -> cookie("column") || 4;
my $sort = $q -> param("sort") || $q -> cookie("sort") || "size";
my $order = $q -> param("order") || $q -> cookie("order") || "ASC";

my $cookie1 = $q -> cookie(-name => "row", -value => $row, -expires => "+1h", -path => "/cgi-bin");
my $cookie2 = $q -> cookie(-name => "column", -value => $column, -expires => "+1h", -path => "/cgi-bin");
my $cookie3 = $q -> cookie(-name => "sort", -value => $sort, -expires => "+1h", -path => "/cgi-bin");
my $cookie4 = $q -> cookie(-name => "order", -value => $order, -expires => "+1h", -path => "/cgi-bin");

print $q -> header(-cookie => $cookie1);
print $q -> header(-cookie => $cookie2);
print $q -> header(-cookie => $cookie3);
print $q -> header(-cookie => $cookie4);









