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

if(!$filename) {
	print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/upload_form.cgi?e=1");
	exit 0;
}

my $check_type = "/usr/bin/identify $filename";
my $result = `$check_type`;
my @type = split(/ /, $result);

if ($type[1] ne "JPEG")
{
	#print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/upload_form.cgi?e=2");
	print $q -> header();
	print $q -> h1($check_type);
	print $q -> h2($type[1]);
	exit 0;
}

my $db_source = "DBI:mysql:$db_name;host=$db_host";
my $dbh = DBI -> connect($db_source, $db_username, $db_password) || die $DBI::errstr;

my $ifdup = check_duplicate();
$_ = $filename;
my ($name, $ext) = /([a-z0-9-_]+).([a-z0-9-_]+)/;
my $totalBytes = 0;

if ($ifdup == 1)
{
	if(! open(OUTFILE, "> $upload_dir/$filename"))
	{
		die("Can't open $upload_dir/$filename for writing - $!");
	}

	my $ret = 0;
	my $buffer ="";

	binmode $filename;

	while ( $ret = read($q->upload("pic"), $buffer, 1024))
	{
		print OUTFILE $buffer;
		$totalBytes += $ret;
	}

	close(OUTFILE);

	insert_photo();

	print $q -> header();
	print $q -> start_html(-title=>"UPLOAD", -meta=>{"http-equiv"=>"content-type", "content"=>"text/html; charset=UTF-8"});

	print "Your file has been uploaded (Size = $totalBytes bytes)<br />";
	print "<h3>Image</h3><img src='../data/$filename' title=$description>";
	print $q -> end_html;
}

sub check_duplicate
{
	my $query = $dbh -> prepare("SELECT * FROM photos WHERE name = ?");
	$query -> execute($filename) or die $query -> errstr;
	
	if ($query -> rows != 0)
	{
		$q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/dup_handle.cgi");
		$dbh -> disconnect;
		exit;	
	}else
	{
		return 1;
	}
}

sub insert_photo
{
	my $thumb_name = $name . "_thumb." . $ext;
	my $gen_thumb = "/usr/bin/convert \"../data/$filename\" -resize 30% \"../data/$thumb_name\"";
	my $cmd = `$gen_thumb`;

	my $gen_time = "/bin/date +%s";
	my $time = `$gen_time`;
	
	my $query = $dbh -> prepare("INSERT INTO photos (name, thumb_name, size, upload_time, description) VALUES (?, ?, ?, ?, ?)");
	$query -> execute($filename, $thumb_name, $totalBytes, $time, $description) || die $query -> errstr;
	
	$dbh -> disconnect;
}