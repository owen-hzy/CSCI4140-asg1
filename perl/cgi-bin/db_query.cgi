#!/usr/bin/perl -w

use DBI;
use CGI;
use strict;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use Digest::SHA qw/sha256_hex/;
# Get database detail
my $db_host =       $ENV{'OPENSHIFT_MYSQL_DB_HOST'};
my $db_username =   $ENV{'OPENSHIFT_MYSQL_DB_USERNAME'};
my $db_password =   $ENV{'OPENSHIFT_MYSQL_DB_PASSWORD'};
my $db_name =       $ENV{'OPENSHIFT_APP_NAME'};             # Default database name is same as application name
my $hashed_password = sha256_hex("test");
my $name = "hzy";
my $q = CGI -> new;

print $q -> header();

print '<html><body>';

# Connect to database

my $db_source = "DBI:mysql:$db_name;host=$db_host";

my $db_handle =
    DBI -> connect($db_source, $db_username, $db_password)
    or die $DBI::errstr;

# Connected to database

print 'Connected! <br />';

# Query detail
my $query_str = 'INSERT INTO users VALUES (?, ?)';

my $query = $db_handle -> prepare($query_str);

$query -> execute($name, $hashed_password) or die $query -> errstr;

#while (my @data = $query -> fetchrow_array) {
 #   print $data[0].', '.$data[1].'<br />';
#}

# Disconnect after your job

$db_handle -> disconnect;

print 'Disconncted. DONE <br />';

print '</html></body>';


