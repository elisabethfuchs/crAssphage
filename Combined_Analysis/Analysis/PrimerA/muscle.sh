export PRIMER=A
/home3/redwards/opt/muscle/muscle -in seqs.$PRIMER.renum.rc.fa -out seqs.$PRIMER.renum.rc.aln -maxiters 2 -diags
python3 ../../../bin/trim_fasta_alignment.py -f seqs.$PRIMER.renum.rc.aln -c 0.9 -r 0.8 -v > seqs.$PRIMER.rc.trim.aln
