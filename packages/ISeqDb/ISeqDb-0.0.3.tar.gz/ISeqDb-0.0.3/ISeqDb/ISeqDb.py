#!/usr/bin/env python

# ISeqDb - Identify Sequences in Databases
# version 0.0.3
# main module
# Nico Salmaso, FEM, nico.salmaso@fmach.it

import argparse
import sys
import textwrap

from ISeqDb import find_nucl, inspect_db, create_db


def main():
    version_isdb = "0.0.3"
    description = ("ISeqDb v." + version_isdb)
    parser = argparse.ArgumentParser(prog='ISeqDb', description=description,
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent('''\
                Author: Nico Salmaso (nico.salmaso@fmach.it)
                
                ISeqDb relies on BLAST®:
                
                -   BLAST® Command Line Applications User Manual [Internet]. Bethesda (MD): National Center
                    for Biotechnology Information (US); 2008-.
                -   Camacho C., Coulouris G., Avagyan V., Ma N., Papadopoulos J., Bealer K., Madden T.L. (2008)
                    “BLAST+: architecture and applications.” BMC Bioinformatics 10:421. PubMed
                ---
                ''')
                                     )
    parser.add_argument('-v', '-V', '--version', action='version', version='%(prog)s 0.0.3')
    subparsers = parser.add_subparsers(dest='command', title='commands',
                                       description='Available commands - Use "ISeqDb [command] --help"'
                                                   ' for more information about a command')

    # find_nucl
    parser_find_nucl = subparsers.add_parser('find_nucl', help='Identify sequences in databases',
                                             formatter_class=argparse.RawDescriptionHelpFormatter,
                                             epilog=textwrap.dedent('''\

             Output legend (in square brackets, the blast codes)
                ---
                query_id:		        query/sequence identifier [qacc]
                subject_accession:	        NCBI accession number or subject identifier in the database [sacc]
                pident:			percentage of identical matches in query and subject sequences [pident]
                n_ident_match:		number of identical bases/matches [nident]
                n_diff_match:		number of different bases/matches [mismatch]
                n_gaps:			total number of gaps [gaps]
                alignment_length:	        length of the alignemnt between query and subject sequences [length]
                query_start_al:		start of alignment in query [qstart]
                query_end_al:		end of alignment in query [qend]
                subj_start_al:		start of alignment in subject [sstart]
                subj_end_al:		        end of alignment in subject [send]
                bitscore:			bit score [bitscore]
                evalue:			expect value [evalue]
                subject_seq_title:		title of subject sequence in database [stitle]
                align_query_seq:		aligned part of query sequence [qseq]
                align_subj_seq:		aligned part of subject sequence [sseq]
                ---
             ''')
                                             )
    parser_find_nucl.add_argument('queryfile', default=None,
                                  help="Input query file fasta/multi-fasta (with path) - e.g. /dir/query.fna")
    parser_find_nucl.add_argument('targetdb', default=None,
                                  help="Target database for the blast analysis (with path) - e.g. /dir/arch.tar.gz")
    parser_find_nucl.add_argument('outputfile', default=None,
                                  help="Output name file (with path) - e.g. /dir/out.txt")
    parser_find_nucl.add_argument('-k', '--task', required=False, default="megablast",
                                  choices=['megablast', 'blastn', 'blastx'],
                                  help="Task: megablast (nucl), blastn (nucl), blastx (prot); default=megablast")
    parser_find_nucl.add_argument('-m', '--maxtargseq', type=int, required=False, default=100,
                                  help="Keep max target sequences >= maxtargseq; default=100")
    parser_find_nucl.add_argument('-e', '--minevalue', type=float, required=False, default=1e-6,
                                  help="Keep hits with evalue >= minevalue; default=1e-6")
    parser_find_nucl.add_argument('-p', '--minpident', type=int, required=False, default=85,
                                  help="Keep hits with pident >= minpident (only megablast/blastn); default=85")
    parser_find_nucl.add_argument('-t', '--threads', type=int, required=False, default=1,
                                  help="Number of threads to use; default=1")
    parser_find_nucl.add_argument('-s', '--sortoutput', required=False, default="bitscore",
                                  help="Sort output by colname. eg.: bitscore, pident, alignment_length; "
                                       "default=bitscore")
    parser_find_nucl.add_argument('-d', '--delimiter', required=False, default="comma",
                                  choices=['comma', 'semicolon', 'tab'],
                                  help="Output delimiter: comma, semicolon, tab; default=comma")
    parser_find_nucl.set_defaults(func=find_nucl.run)

    # inspect_db
    parser_inspect_db = subparsers.add_parser('inspect_db', help='Inspect or save the sequence database')
    parser_inspect_db.add_argument('targetdb', default=None,
                                   help="Target database (with path) - e.g. /dir/arch.tar.gz")
    parser_inspect_db.add_argument('-d', '--savedb', required=False, default="nosave",
                                   help="Output directory (with path) - e.g. /dir/; if not indicated, default=nosave")
    parser_inspect_db.set_defaults(func=inspect_db.run)

    # create_db
    parser_create_db = subparsers.add_parser('create_db', help='Create a database from a fasta/multifasta file')
    parser_create_db.add_argument('targetfasta', default=None,
                                  help="Fasta file (with path) - e.g. /dir/arch.fasta")
    parser_create_db.add_argument('-m', '--moltype', type=str, required=True, default=None, choices=['nucl', 'prot'],
                                  help="Molecule type in fasta file, nucl (nucleotide) or prot (protein)")
    parser_create_db.set_defaults(func=create_db.run)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
