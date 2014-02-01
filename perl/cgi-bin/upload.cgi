#! /usr/bin/perl -w

use CGI;
use strict;
use CGI::Carp qw/warningsToBrowser fatalsToBrowser/;

my $q = new CGI;

my $upload_dir = $ENV{"OPENSHIFT_DATA_DIR"};

my $filename = $q->param("pic");
my $description = $q->param("description");

if(undef $filename) {
	print $q->header();
	
	print <<"UPLOAD_FAIL";
	<html>
	<body>
	<h1>File too large</h1>
	</body>
	</html>
UPLOAD_FAIL
	exit 0;
}

print $q->header();
print <<"START_HTML";
<head>
<title>Upload Successful</title>
</head>
</body>
START_HTML

$_ = $filename;
my ($name, $ext) = /([a-z0-9-_]+).([a-z0-9-_]+)/;

if(! open(OUTFILE, "> $upload_dir/$filename"))
{
	die("Can't open $upload_dir/$filename for writing - $!");
}

my $ret = 0;
my $totalBytes = 0;
my $buffer ="";

binmode $filename;

while ( $ret = read($q->upload("pic"), $buffer, 1024))
{
	print OUTFILE $buffer;
	$totalBytes += $ret;
}

close(OUTFILE);

print "Your file has been uploaded (Size = $totalBytes bytes)<br />";
print "<h3>Image</h3><img src='../data/$filename'>";
print <<"END_HTML";
</body>
</html>
END_HTML
