#! /usr/bin/perl -w

use strict;
use CGI;
use DBI;

my $q = CGI -> new;
my $choice = $q -> param("choice") || 0;

if ($choice == 1)
{
	my $db_host =       $ENV{'OPENSHIFT_MYSQL_DB_HOST'};
	my $db_username =   $ENV{'OPENSHIFT_MYSQL_DB_USERNAME'};
	my $db_password =   $ENV{'OPENSHIFT_MYSQL_DB_PASSWORD'};
	my $db_name =       $ENV{'OPENSHIFT_APP_NAME'};
	
	my $upload_dir = $ENV{"OPENSHIFT_DATA_DIR"};
	
	my $db_source = "DBI:mysql;$db_name;host=$db_host";
	my $dbh = DBI -> connect($db_source, $db_username, $db_password) || die DBI::errstr;
	
	my $query = $dbh -> prepare("DROP TABLE sessions");
	$query -> execute() || die $query -> errstr;
	
	$query -> finish;
	
	$query = $dbh -> prepare("DROP TABLE photos");
	$query -> execute() || die $query -> errstr;
	
	$query -> finish;
	
	$query = $dbh -> prepare("DROP TABLE users");
	$query -> execute() || die $query -> errstr;
	
	$query -> finish;
	
	
	
}