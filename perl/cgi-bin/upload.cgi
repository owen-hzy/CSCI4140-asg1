#! /usr/bin/perl -w

use CGI;
use DBI;
use strict;
use CGI::Carp qw/warningsToBrowser fatalsToBrowser/;

do "./include.cgi";

my $q = new CGI;
# Check the session information
session_check();
###

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

# In case there is another tmp
`/bin/rm -rf \"$upload_dir/tmp\"`;
###

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
check_name_type($filename);
###

# then do the duplicate checking
check_duplicate($filename, $description);
###

# update storage		
insert_photo($filename, $description, $totalBytes);
###