#!/usr/bin/perl -w

use DBI;
use CGI;

use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;

# Get database detail
my $db_host =       $ENV{'OPENSHIFT_MYSQL_DB_HOST'};
my $db_username =   $ENV{'OPENSHIFT_MYSQL_DB_USERNAME'};
my $db_password =   $ENV{'OPENSHIFT_MYSQL_DB_PASSWORD'};
my $db_name =       $ENV{'OPENSHIFT_APP_NAME'};             # Default database name is same as application name

my $q = CGI -> new;

print $q -> header();

print '<html><body>';

# Connect to database

my $db_source = "DBI:mysql:$db_name;host=$db_host";

my $dbh =
    DBI -> connect($db_source, $db_username, $db_password)
    or die $DBI::errstr;

# Connected to database

print 'Connected! <br />';

# Disconnect immediately ...

my $table = "sessions";
my $query = $dbh -> prepare("SELECT 1 FROM $table");
$query -> execute() || die $query -> errstr;
@data = $query -> fetchrow_array;

$query -> finish;


$dbh -> disconnect;

foreach my $item (@data)
{
	print "$item\n";
}

print 'Disconncted. DONE <br />';

print '</html></body>';

