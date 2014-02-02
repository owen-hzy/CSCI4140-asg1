#! /usr/bin/perl -w

use strict;
use CGI;

do "./include.cgi";
# Check the session info
session_check();
###

my $q = CGI -> new;
my $upload_dir = $ENV{"OPENSHIFT_DATA_DIR"};
my $filename = `/bin/ls \"$upload_dir/tmp\"`;

$_ = $filename;
my ($name, $ext) = /([a-z0-9-_]+).([a-z0-9-_]+)/;

print $q -> header();
print $q -> start_html(-title=>"LOGIN", -meta=>{"http-equiv"=>"content-type", "content"=>"text/html; charset=UTF-8"});


print "<section>";
print "<form method='post' action='dup_handle.cgi'>";
print "<input type='radio' name='choice' id='overwrite' value='overwrite' /><label for='overwrite'>Overwrite the exisiting file \"$filename\"</label>";
print "<br />"; 
print "<input type='radio' name='choice' id='rename' value='rename' /><label for='rename'><label for='name'>Rename the uploading file.</label></label>";
print "<br />";
print "<label for='name'>New filename:</label><input type='text' id='name' name='rename' />.\"$ext\"";
print <<"PART";
	<br />
	<input type="radio" name="choice" id="cancel" value="cancel" /><label for="cancel">Cancel the current upload.</label>
	
	<br />
	<input type="submit" value="Proceed" />
	</form>
</section>
PART

print $q -> end_html;