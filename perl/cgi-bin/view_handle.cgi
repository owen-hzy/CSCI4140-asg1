#! /usr/bin/perl -w

use CGI;
use DBI;
use strict;

my $q = CGI -> new;
my $action = $q -> url_param("action");
my $row = $q -> param("row") || 2;
my $column = $q -> param("column") || 4;
my $sort = $q -> param("sort") || "size";
my $order = $q -> param("order") || "DESC";

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

my $cookie1 = $q -> cookie(-name => "row", -value => $row, -expires => "+1h", -path => "/cgi-bin/view.cgi");
my $cookie2 = $q -> cookie(-name => "column", -value => $column, -expires => "+1h", -path => "/cgi-bin/view.cgi");
my $cookie3 = $q -> cookie(-name => "sort", -value => $sort, -expires => "+1h", -path => "/cgi-bin/view.cgi");
my $cookie4 = $q -> cookie(-name => "order", -value => $order, -expires => "+1h", -path => "/cgi-bin/view.cgi");

#print $q -> header(-cookie => $cookie1);
#print $q -> header(-cookie => $cookie2);
#print $q -> header(-cookie => $cookie3);
#print $q -> header(-cookie => $cookie4);

sub get_data
{
	my @data = ();
	my $query = $dbh -> prepare("SELECT name FROM photos ORDER BY $sort $order");
	$query -> execute() || die $query -> errstr;
	
	while (my @result = $query -> fetchrow_array)
	{
		push(@data, $result[0]);
	}
	
	$query -> finish;
	$dbh -> disconnect;
	
	return @data;
}

print $q -> header();
my @array = get_data();
foreach my $item (@array)
{
	print "$item\n";
}




