#! /usr/bin/perl -w

use CGI;
use DBI;

my $q = CGI -> new;
my $action = $q -> url_param("action");
my $row = $q -> param("row") || 2;
my $column = $q -> param("column") || 4;
my $sort = $q -> param("sort") || "size";
my $order = $q -> param("order") || "ascending";

# Database Info
my $db_host =       $ENV{'OPENSHIFT_MYSQL_DB_HOST'};
my $db_username =   $ENV{'OPENSHIFT_MYSQL_DB_USERNAME'};
my $db_password =   $ENV{'OPENSHIFT_MYSQL_DB_PASSWORD'};
my $db_name =       $ENV{'OPENSHIFT_APP_NAME'};
###
	
# Connect the database
my $db_source = "DBI:mysql:$db_name;host=$db_host";
my $dbh = DBI -> connect($db_source, $db_username, $db_password) || die $DBI::errstr;
###


