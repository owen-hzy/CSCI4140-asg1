#! /usr/bin/perl -w

use CGI;
use DBI;
use strict;
use CGI::Carp qw/warningsToBrowser fatalsToBrowser/;

do "./include.cgi";

my $q = new CGI;
# Check the session info
if (session_check() == 1)
{
	print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/login.cgi?e=3");
	exit;
}
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

# Escape the spacial character
$description =~ s/&/&amp;/g;
$description =~ s/</&lt;/g;
$description =~ s/>/&gt;/g;
$description =~ s/"/&quot;/g;
$description =~ s/'/&#39;/g;
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

### Check the file size
if ($totalBytes > 1000000)
{
	`/bin/rm -f \"$upload_dir/tmp\"`;
	print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/upload_form.cgi?e=1");
	exit 0;
}

# first check file name and type 
check_name_type($filename);
###

# then do the duplicate checking
check_duplicate($filename, $description, $totalBytes);
###

# update storage		
insert_photo($filename, $description, $totalBytes);
###