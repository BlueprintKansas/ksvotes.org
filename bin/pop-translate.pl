#!/usr/bin/env perl
use strict;
use warnings;
use Text::CSV_XS;
use Data::Dump qw( dump );
use Locale::PO;

my $usage = "$0 translations.csv";

# read translations
my %translations;
my $translations_csv = shift @ARGV or die $usage;
my $en_po_file       = 'app/translations/en/LC_MESSAGES/messages.po';
my $es_po_file       = 'app/translations/es/LC_MESSAGES/messages.po';

my $csv = Text::CSV_XS->new( { binary => 1, auto_diag => 1 } );
open my $fh, "<:encoding(utf8)", $translations_csv
    or die "$translations_csv: $!";
while ( my $row = $csv->getline($fh) ) {
    my $ref    = $row->[2];
    my $en_txt = $row->[4];
    my $es_txt = $row->[5] || $en_txt;    # TODO
    $translations{$ref} = { en => $en_txt, es => $es_txt };
}
close $fh;

#dump \%translations;

# populate english
my $en_locale_po = Locale::PO->load_file_ashash( $en_po_file, 'utf8' );
my $es_locale_po = Locale::PO->load_file_ashash( $es_po_file, 'utf8' );

for my $msgid ( sort keys %translations ) {
    my $en_po = Locale::PO->new(
        -msgid  => $msgid,
        -msgstr => $translations{$msgid}->{en}
    );
    my $es_po = Locale::PO->new(
        -msgid  => $msgid,
        -msgstr => $translations{$msgid}->{es}
    );
    $en_locale_po->{qq{"$msgid"}} = $en_po;
    $es_locale_po->{qq{"$msgid"}} = $es_po;
}

Locale::PO->save_file_fromhash( $en_po_file, $en_locale_po, 'utf8' );
Locale::PO->save_file_fromhash( $es_po_file, $es_locale_po, 'utf8' );
