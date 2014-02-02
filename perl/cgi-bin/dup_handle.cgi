#! /usr/bin/perl -w

use strict;
use CGI;
use DBI;

do "./include.cgi";
# Check the session info
session_check();
###

my $q = CGI -> new;
my $choice = $q -> param("choice") || "No choice";
$choice =~ tr/a-z/A-Z/;

my $db_host =       $ENV{'OPENSHIFT_MYSQL_DB_HOST'};
my $db_username =   $ENV{'OPENSHIFT_MYSQL_DB_USERNAME'};
my $db_password =   $ENV{'OPENSHIFT_MYSQL_DB_PASSWORD'};
my $db_name =       $ENV{'OPENSHIFT_APP_NAME'};
my $upload_dir = $ENV{"OPENSHIFT_DATA_DIR"};

my $filename = `/bin/ls \"$upload_dir/tmp\"`;
$filename = chomp($filename);
$_ = $filename;
my ($name, $ext) = /([a-z0-9-_]+).([a-z0-9-_]+)/;
my $thumb_name = $name . "_thumb." . $ext;

if ($choice eq "OVERWRITE")
{
	
	`/bin/rm -f \"$upload_dir/$filename\"`;
	`/bin/rm -f \"$upload_dir/$thumb_name\"`;
	
	# Read the file size, do not use identify cause it's not accurate
	open(OUTFILE, "> $upload_dir/$filename") || die ("Can't open $filename for writing - $!");

	my $ret = 0;
	my $buffer ="";
	my $totalBytes = 0;

	binmode $filename;
	open(INFILE, "$upload_dir/tmp/$filename");
	
	while ( $ret = read(INFILE, $buffer, 1024))
	{
		print OUTFILE $buffer;
		$totalBytes += $ret;
	}
	###
	close(INFILE);
	close(OUTFILE);
	
	
	# Connect DB to get the description
	my $db_source = "DBI:mysql:$db_name;host=$db_host";
	my $dbh = DBI -> connect($db_source, $db_username, $db_password) || die $DBI::errstr;
	###
	my $sessid = $q -> cookie("SESSID");
	
	my $query = $dbh -> prepare("SELECT description FROM sessions WHERE sessid = ?");
	$query -> execute($sessid) || die $query -> errstr;
	my @description = $query -> fetchrow_array;
	
	$query -> finish;
	$dbh -> disconnect;
	
	update_photo($filename, $description[0], $totalBytes);
}
