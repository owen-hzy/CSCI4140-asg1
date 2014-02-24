#! /usr/bin/perl -w

use strict;
use CGI;
use DBI;
use Digest::SHA qw/sha256_hex/;

my $q = CGI -> new;
my $choice = $q -> param("choice") || 0;

if ($choice == 1)
{
	my $db_host =       $ENV{'OPENSHIFT_MYSQL_DB_HOST'};
	my $db_username =   $ENV{'OPENSHIFT_MYSQL_DB_USERNAME'};
	my $db_password =   $ENV{'OPENSHIFT_MYSQL_DB_PASSWORD'};
	my $db_name =       $ENV{'OPENSHIFT_APP_NAME'};
	
	my $upload_dir = $ENV{"OPENSHIFT_DATA_DIR"};
	
	my $db_source = "DBI:mysql:$db_name;host=$db_host";
	my $dbh = DBI -> connect($db_source, $db_username, $db_password) || die $DBI::errstr;
	my @table = ("users, sessions, photos");
	
	foreach my $table_name (@table)
	{
		
		my $drop_if_exist = "DROP TABLE IF EXISTS $table_name";
		my $query = $dbh -> do($drop_if_exist) || die "Couldn't execute '$drop_if_exist':" . $dbh -> errstr;
	}
	
	my $create1 = <<"CREATE_SESSIONS";
	CREATE TABLE sessions (id VARCHAR(100) NOT NULL PRIMARY KEY, sessid VARCHAR(100), expire BIGINT, description TEXT, size INT)
CREATE_SESSIONS
 	my $create2 = <<"CREATE_PHOTOS";
 	CREATE TABLE photos (name VARCHAR(50) NOT NULL PRIMARY KEY, thumb_name VARCHAR(50) NOT NULL, size INT NOT NULL, upload_time INT NOT NULL, description TEXT)
CREATE_PHOTOS
	my $create3 = <<"CREATE_USERS";
	CREATE TABLE users (username VARCHAR(20) NOT NULL PRIMARY KEY, password VARCHAR(100) NOT NULL)
CREATE_USERS
	
	my @create = ($create1, $create2, $create3);
	
	foreach my $create (@create)
	{
		my $result = $dbh -> do($create) || die("Cannot create table: " . $dbh -> errstr);
	}
	
	open(INFILE, "users.conf") || die ("Can't open users.conf for reading - $!");
	my $input = "";
	while ($input = <INFILE>)
	{
		chomp($input);
		my @array = split(/:/, $input);
		
		my $hashed_password = sha256_hex($array[1]);
		my $query = $dbh -> prepare("INSERT INTO users VALUES (?, ?)");
		$query -> execute($array[0], $hashed_password) || die $query -> errstr;
		
		$query -> finish;
	}
	
	$dbh -> disconnect;
	
	`/bin/rm -rf \"$upload_dir\"`;
	`/bin/mkdir \"$upload_dir\"`;
	`/bin/chmod 750 \"$upload_dir\"`;
	
	print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/done.html");
}
else
{
	print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/login.cgi");
}