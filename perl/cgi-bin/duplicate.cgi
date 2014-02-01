#! /usr/bin/perl -w

use strict;
use CGI;

my $q = CGI -> new;
my $filename = "hello";
my $ext = "jpg";

print $q -> header();
print $q -> start_html(-title=>"LOGIN", -meta=>{"http-equiv"=>"content-type", "content"=>"text/html; charset=UTF-8"});


print "<section>";
print "<form method='post' action='dup_handle.cgi'>";
print "<input type='radio' name='choice' id='overwrite' value='overwrite' /><label for='overwrite'>Overwrite the exisiting file \"$filename\"</label>";
print "<br />"; 
print "<input type='radio' name='choice' id='rename' value='rename' /><label for='rename'>Rename the uploading file.</label>";
print "<br />";
print "<label for='name'>New filename:</label><input type='text' name='rename' />.\"$ext\"";
print <<"PART";
	<br />
	<input type="radio" name="choice" id="cancel" value="cancel" /><label for="cancel">Cancel the current upload.</label>
	
	<br />
	<input type="submit" value="Proceed" />
	</form>
</section>
PART

print $q -> end_html;