#! /usr/bin/perl -w

use strict;
use Digest::SHA qw/sha256_hex/;

print sha256_hex("test"), "\n";