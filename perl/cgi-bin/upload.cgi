#! /usr/bin/perl -w

use CGI;
use DBI;
use strict;
use CGI::Carp qw/warningsToBrowser fatalsToBrowser/;

my $q = new CGI;

my $db_host =       $ENV{'OPENSHIFT_MYSQL_DB_HOST'};
my $db_username =   $ENV{'OPENSHIFT_MYSQL_DB_USERNAME'};
my $db_password =   $ENV{'OPENSHIFT_MYSQL_DB_PASSWORD'};
my $db_name =       $ENV{'OPENSHIFT_APP_NAME'};
my $upload_dir = $ENV{"OPENSHIFT_DATA_DIR"};

my $filename = $q->param("pic");
my $description = $q->param("description") || "No description";


# Detect the empty upload
if(!$filename) {
	print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/upload_form.cgi?e=1");
	exit 0;
}
###

# put the file into teporary folder
`/bin/mkdir \"$upload_dir/tmp\"`;
open(OUTFILE, "> $upload_dir/tmp/$filename") || die ("Can't open $filename for writing - $!");

my $ret = 0;
my $buffer ="";
my $totalBytes = 0;

binmode $filename;

while ( $ret = read($q->upload("pic"), $buffer, 1024))
{
	print OUTFILE $buffer;
	$totalBytes += $ret;
}

close(OUTFILE);
###

# first check file name and type 
check_name_type();
###

# then do the duplicate checking
check_duplicate();
###

# update storage		
insert_photo();
###

print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/upload_form.cgi?e=5");


sub check_name_type
{
	$_ = $filename;
	my ($name, $ext) = /([a-z0-9-_]+).([a-z0-9-_]+)/;
	
	my $result = `/usr/bin/identify \"$upload_dir/tmp/$filename\"`;
	my @type = split(/ /, $result);

	if ($name && ($type[1] eq "JPEG" || $type[1] eq "PNG" || $type[1] eq "GIF"))
	{	
		return 1;
	}else
	{
		`/bin/rm -rf \"$upload_dir/tmp"`;
		print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/upload_form.cgi?e=2");
		exit 0;
	}
}

sub check_duplicate
{
	# Connect the database
	my $db_source = "DBI:mysql:$db_name;host=$db_host";
	my $dbh = DBI -> connect($db_source, $db_username, $db_password) || die $DBI::errstr;
	###
	
	my $query = $dbh -> prepare("SELECT * FROM photos WHERE name = ?");
	$query -> execute($filename) or die $query -> errstr;
	
	if ($query -> rows != 0)
	{
		print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/duplicate.cgi");
		$dbh -> disconnect;
		exit 0;	
	}
}

sub insert_photo
{	
	`/bin/mv \"$upload_dir/tmp/$filename\" \"$upload_dir\$filename\"`;
	`/bin/rm -rf \"$upload_dir/tmp\"`;
	
	$_ = $filename;
	my ($name, $ext) = /([a-z0-9-_]+).([a-z0-9-_]+)/;
	
	my $thumb_name = $name . "_thumb." . $ext;
	`/usr/bin/convert \"$upload_dir/$filename\" -resize 30% \"$thumb_name\"`;
	
	my $time = `/bin/date +%s`;
	
	# Connect the database
	my $db_source = "DBI:mysql:$db_name;host=$db_host";
	my $dbh = DBI -> connect($db_source, $db_username, $db_password) || die $DBI::errstr;
	###
	
	my $query = $dbh -> prepare("INSERT INTO photos (name, thumb_name, size, upload_time, description) VALUES (?, ?, ?, ?, ?)");
	$query -> execute($filename, $thumb_name, $totalBytes, $time, $description) || die $query -> errstr;
	
	$dbh -> disconnect;
}