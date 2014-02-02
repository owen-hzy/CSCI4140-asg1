#! /usr/bin/perl -w

use strict;
use CGI;
use DBI;

my $q = CGI -> new;
my $db_host =       $ENV{'OPENSHIFT_MYSQL_DB_HOST'};
	my $db_username =   $ENV{'OPENSHIFT_MYSQL_DB_USERNAME'};
	my $db_password =   $ENV{'OPENSHIFT_MYSQL_DB_PASSWORD'};
	my $db_name =       $ENV{'OPENSHIFT_APP_NAME'};
	my $db_source = "DBI:mysql:$db_name;host=$db_host";
	my $dbh = DBI -> connect($db_source, $db_username, $db_password) || die $DBI::errstr;
	my $description = "hello";
	my $sessid = 9871271073;
	
	my $query = $dbh -> prepare("UPDATE sessions SET desc = ? WHERE sessid = ?");
		$query -> execute("$description", "$sessid") || die $query -> errstr;
		$query -> finish;
		$dbh -> disconnect;
		
		print $q -> header();
		print $q -> h3("hello ok!");