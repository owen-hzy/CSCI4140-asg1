#! /usr/bin/perl -w

use strict;
use CGI;
use DBI;

use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;

# Get database detail
my $db_host = $ENV{"OPENSHIFT_MYSQL_DB_HOST"};
my $db_username = $ENV{"OPENSHIFT_MYSQL_DB_USERNAME"};
my $db_password = $ENV{"OPENSHIFT_MYSQL_DB_PASSWORD"};
my $db_name = $ENV{"OPENSHIFT_APP_NAME"};

#Connect to database
my $db_source = "DBI:mysql:$db_name;host=$db_host";
my $dbh = DBI -> connect($db_source, $db_username, $db_password) or die $DBI::errstr;

my $q = CGI -> new;
my $action = $q -> url_param("action");

if ($action eq "login")
{
	login();
}


sub login
{
	
	my $username = $q -> param("username");
	my $password = $q -> param("password");
	
	my $query = $dbh -> prepare("SELECT * FROM users WHERE username = ?");
	$query -> execute($username) or die $query -> errstr;
	
	if ($query -> rows == 0)
	{
		print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/login.cgi?f=1");
		$dbh -> disconnect;
		exit;
	}
	
	$dbh -> disconnect;
}

 