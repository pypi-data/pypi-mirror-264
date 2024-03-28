# ISeqDb - Identify Sequences in Databases
# version 0.0.3
# module, create_db
# Nico Salmaso, FEM, nico.salmaso@fmach.it

import os
import sys
import tarfile


def run(args):

    print('_____________________________________')
    print(' ')
    print("Database:", args.targetfasta)
    print('_____________________________________')
    print(' ')

    dirfasta, file_name_fs = os.path.split(args.targetfasta)
    datseq = file_name_fs.split('.')[0]

    if (len(dirfasta) == 0) or (len(file_name_fs) == 0):
        print("The fasta name with the full path should be provided - e.g. '/inputdir/inp.fasta'")
        print(" ")
        sys.exit()

    outdir = os.path.join(str(dirfasta), str(datseq) + '_out')

    if os.path.isdir(outdir):
        print("Cannot write an existing directory: ", outdir)
        print(" ")
        sys.exit()
    else:
        os.mkdir(outdir)

    define_cmd_1: str = (
        f'makeblastdb -in {args.targetfasta} -input_type fasta -dbtype {args.moltype} '
        f'-parse_seqids -out {dirfasta}"/"{datseq} '
    )
    os.system(define_cmd_1)

    if args.moltype == "nucl":
        chartask = ".n"
    elif args.moltype == "prot":
        chartask = ".p"
    else:
        print(" ")
        print("allowed moltype are nucl (nucleotydes) or prot (proteins)")
        sys.exit()

    elements_db = [
        ("".join([datseq, chartask, 'db'])),
        ("".join([datseq, chartask, 'hr'])),
        ("".join([datseq, chartask, 'in'])),
        ("".join([datseq, chartask, 'js'])),
        ("".join([datseq, chartask, 'og'])),
        ("".join([datseq, chartask, 'os'])),
        ("".join([datseq, chartask, 'ot'])),
        ("".join([datseq, chartask, 'sq'])),
        ("".join([datseq, chartask, 'tf'])),
        ("".join([datseq, chartask, 'to']))
    ]

    for fileelem in elements_db:
        os.rename(os.path.join(dirfasta, fileelem), os.path.join(outdir, fileelem))

    filetargz = (datseq + '.tar.gz')
    output_targz = os.path.join(dirfasta, filetargz)

    with tarfile.open(output_targz, "w:gz") as tar:
        for fileelem in elements_db:
            direl = os.path.join(outdir, fileelem)
            tar.add(direl, arcname=fileelem)
            os.remove(direl)

    os.rmdir(outdir)
