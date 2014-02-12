#! /usr/bin/perl -w

use strict;
use CGI;
use DBI;

my $q = CGI -> new;
do "./include.cgi";

# Check the session info
if (session_check() == 1)
{
	print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/login.cgi?e=3");
	exit;
}
###

my $choice = $q -> param("choice") || "No choice";
$choice =~ tr/a-z/A-Z/;

my $db_host =       $ENV{'OPENSHIFT_MYSQL_DB_HOST'};
my $db_username =   $ENV{'OPENSHIFT_MYSQL_DB_USERNAME'};
my $db_password =   $ENV{'OPENSHIFT_MYSQL_DB_PASSWORD'};
my $db_name =       $ENV{'OPENSHIFT_APP_NAME'};
my $upload_dir = $ENV{"OPENSHIFT_DATA_DIR"};

my $filename = `/bin/ls \"$upload_dir/tmp\"`;
chomp($filename);
$_ = $filename;
my ($name, $ext) = /([a-z0-9-_]+).([a-z0-9-_]+)/;
my $thumb_name = $name . "_thumb." . $ext;

if ($choice eq "OVERWRITE")
{
	
	`/bin/rm -f \"$upload_dir/$filename\"`;
	`/bin/rm -f \"$upload_dir/$thumb_name\"`;
	
	`/bin/mv \"$upload_dir/tmp/$filename\" \"$upload_dir\$filename\"`;
	`/bin/rm -rf \"$upload_dir/tmp\"`;
	
	# Read the file size, do not use identify cause it's not accurate
	my $ret = 0;
	my $buffer ="";
	my $totalBytes = 0;

	open(INFILE, "$upload_dir/$filename");
	
	while ( $ret = read(INFILE, $buffer, 1024))
	{
		$totalBytes += $ret;
	}
	close(INFILE);	
	###
	
	# Connect DB to get the description
	my $db_source = "DBI:mysql:$db_name;host=$db_host";
	my $dbh = DBI -> connect($db_source, $db_username, $db_password) || die $DBI::errstr;
	###
	my $sessid = $q -> cookie("SESSID");
	
	my $query = $dbh -> prepare("SELECT * FROM sessions WHERE sessid = ?");
	$query -> execute($sessid) || die $query -> errstr;
	my @result = $query -> fetchrow_array;
	
	$query -> finish;
	$dbh -> disconnect;
	
	update_photo($filename, $result[3], $totalBytes);
}

if ($choice eq "RENAME")
{
	my $rename = $q -> param("rename");
	if(!$rename)
	{
		print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/duplicate.cgi?e=1");
		exit 0;
	}
	
	my $fullname = $rename . "." . $ext;
	`/bin/mv \"$upload_dir/tmp/$filename\" \"$upload_dir/tmp/$fullname\"`;
	
	check_name_type($fullname);
	
	# Connect DB to get the description
	my $db_source = "DBI:mysql:$db_name;host=$db_host";
	my $dbh = DBI -> connect($db_source, $db_username, $db_password) || die $DBI::errstr;
	###
	my $sessid = $q -> cookie("SESSID");
	
	my $query = $dbh -> prepare("SELECT * FROM sessions WHERE sessid = ?");
	$query -> execute($sessid) || die $query -> errstr;
	my @result = $query -> fetchrow_array;
	
	$query -> finish;
	$dbh -> disconnect;
	
	check_duplicate($fullname, $result[3], $result[4]);
	
	insert_photo($fullname, $result[3], $result[4]);
}

if ($choice eq "CANCEL")
{
	`/bin/rm -rf \"$upload_dir/tmp\"`;
	
	print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/upload_form.cgi?e=4");
	
}
