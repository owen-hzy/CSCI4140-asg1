#! /usr/bin/perl -w

use strict;
use CGI;

my $q = CGI -> new;
my $error = $q -> url_param("e") || 5;

print $q -> header();
print $q -> start_html(-title=>"UPLOAD", -meta=>{"http-equiv"=>"content-type", "content"=>"text/html; charset=UTF-8"});

if ($error == 1)
{
	print $q -> h3("File too large or missed!");
}
elsif ($error == 2)
{
	print $q -> h3("Filetype is not valid!");
}
elsif ($error == 3)
{
	print $q -> h3("Please choose another photo!");
}
elsif ($error = 0)
{
	print $q -> h3("Upload Successfully!");
}

print <<"MAIN_BODY";
<section>

<form enctype="multipart/form-data" action="upload.cgi" method="POST">
    <label for="pic">Choose an image (.jpg .gif .png):</label>
    <input type="file" id="pic" name="pic" accept="image/gif, image/jpeg, image/png" required="true" />
    <br />
    <label for="desc">Description (50 bytes max)</label>
    <input type="text" id="desc" name="description" maxlength="50" />
    <br />
    <input type="submit" value="Upload" />
</form>
</section>

<section>
	<a href="display.cgi">Back to display panel</a>
</section>
MAIN_BODY

print $q -> end_html;
