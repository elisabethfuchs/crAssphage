# We're using make to generate alignments and trees because, well why not!

PRIMER = C

.PHONY: clean help reverse_complement reverse_complement_tree mafft align

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "\tvol_date\tcreate a tree and rename the leaves using both the volunteer and date tags"
	@echo "\tvolunteer_tree\tcreate a tree and rename the leaves using the volunteer= tag in the fasta def line"
	@echo "\tdate_tree\tcreate a tree and rename the leaves using the date= tag in the fasta def line"
	@echo "\ttree\t\tmake a tree named with the label of the sequences"
	@echo "\treverse_complement_tree\tReverse complement sequences as below and make an alignment and tree of them"
	@echo "\treverse_complement\tReverse complement sequences as required and filter to only those that match crassphage"
	@echo "\tblastn\t\tblast all the sequences against crAssphage (e.g. to check orientation)"
	@echo "\talign\t\talign the sequences using the default aligner (mafft)"
	@echo "\tseqs.fa\t\tassemble the DNA sequences into a single fasta file"
	@echo "\trenum\t\trenumber the fasta file and create a separate id.map"
	@echo "\tclustalw\trun a clustalw alignment on the sequences"
	@echo "\tmafft\t\trun a mafft alignment on the sequences (this makes a phylip format output used for building the trees)"
	@echo "\tmafft_fa\trun a mafft alignment but write the alignment in fasta format"
	@echo "\tmafft_fa_name\trun a mafft alignment but write the alignment in fasta format and rename the sequences"
	@echo "\treverse_complement\trenumber the sequences, run a blast to match them, and reverse complement ones in the wrong orientation"
	@echo ""
	@echo "You probably want to start with vol_date, as it will create the sequences, build an alignment, rename the sequences, etc etc"

vol_date: seqs.$(PRIMER).tree
	python3 ../../../bin/rename_trees.py -t seqs.$(PRIMER).tree -i id.$(PRIMER).map -n volunteer -n date > seqs.$(PRIMER).volunteerdate.tree

date_tree: seqs.$(PRIMER).tree
	python3 ../../../bin/rename_trees.py -t seqs.$(PRIMER).tree -i id.$(PRIMER).map -n date > seqs.$(PRIMER).date.tree

vol_tree: seqs.$(PRIMER).tree
	python3 ../../../bin/rename_trees.py -t seqs.$(PRIMER).tree -i id.$(PRIMER).map -n volunteer > seqs.$(PRIMER).volunteer.tree

tree: seqs.$(PRIMER).tree
	python3 ../../../bin/rename_trees.py -t seqs.$(PRIMER).tree -i id.$(PRIMER).map > seqs.$(PRIMER).named.tree

seqs.$(PRIMER).tree: seqs.$(PRIMER).trim.aln
	FastTreeDbl -nt seqs.$(PRIMER).trim.aln > seqs.$(PRIMER).tree

blastn: seqs.$(PRIMER).fa
	blastn -task blastn -db ../../../data/JQ995537.fna -query seqs.$(PRIMER).fa -out seqs.$(PRIMER).crassphage.blastn -outfmt '6 std qlen slen' -evalue 1e-12


seqs.$(PRIMER).trim.aln: seqs.$(PRIMER).aln
	python3 ../../../bin/trim_fasta_alignment.py -f seqs.$(PRIMER).aln -c 0.9 > seqs.$(PRIMER).trim.aln

seqs.all.aln:
	muscle -in seqs.all.renum.fa -out seqs.all.aln -maxiters 2 -diags

align: mafft

mafft: seqs.$(PRIMER).aln

seqs.$(PRIMER).aln: seqs.$(PRIMER).fa id.$(PRIMER).map metadata.$(PRIMER).tsv
	mafft --adjustdirectionaccurately --localpair  --maxiterate 16 --reorder seqs.$(PRIMER).renum.fa > seqs.$(PRIMER).aln


phylipoutput:
	mafft --adjustdirectionaccurately --localpair  --maxiterate 16 --phylipout --reorder seqs.$(PRIMER).renum.fa > seqs.$(PRIMER).aln

mafft_fa: seqs.$(PRIMER).fa id.$(PRIMER).map
	mafft --adjustdirectionaccurately --localpair  --maxiterate 16 --reorder seqs.$(PRIMER).renum.fa > seqs.$(PRIMER).faln

clustalw: seqs.$(PRIMER).fa
	clustalw seqs.$(PRIMER).fa -OUTFILE=seqs.$(PRIMER).clustalw

reverse_complement_tree: seqs.$PRIMER.rc.trim.tree

seqs.$PRIMER.rc.trim.tree: seqs.$(PRIMER).renum.rc.fa
	@echo "Running muscle may take a while. You might want to run these steps on the cluster"
	muscle -in seqs.$(PRIMER).renum.rc.fa -out seqs.$(PRIMER).renum.rc.aln -maxiters 2 -diags
	python3 ../../../bin/trim_fasta_alignment.py -f seqs.$(PRIMER).renum.rc.aln -c 0.9 -r 0.8 -v > seqs.$(PRIMER).rc.trim.aln
	fasttree -nt seqs.$(PRIMER).rc.trim.aln > seqs.$(PRIMER).rc.trim.tree

reverse_complement: seqs.$(PRIMER).renum.rc.fa

seqs.$(PRIMER).renum.rc.fa: id.$(PRIMER).map metadata.$(PRIMER).tsv
	blastn -task blastn -db ../../../data/JQ995537.fna -query seqs.$(PRIMER).renum.fa -out seqs.$(PRIMER).crassphage.blastn -outfmt '6 std qlen slen' -evalue 0.001
	python3 ../../../bin/reverse_complement.py -f seqs.$(PRIMER).renum.fa -b seqs.$(PRIMER).crassphage.blastn -o seqs.$(PRIMER).renum.rc.fa

metadata.$(PRIMER).tsv: id.$(PRIMER).map
	python3 ../../../bin/metadata.py -i id.$(PRIMER).map -o metadata.$(PRIMER).tsv
		
renum: id.$(PRIMER).map

id.$(PRIMER).map: seqs.$(PRIMER).fa
	python3 ../../../bin/rename_fasta.py -f seqs.$(PRIMER).fa -o seqs.$(PRIMER).renum.fa -i id.$(PRIMER).map -t volunteer -t date

seqs.$(PRIMER).fa:
	cat ../../Sequences/Primer$(PRIMER)/*.fasta > seqs.$(PRIMER).fa

clean:
	rm -f *.aln *.dnd seqs.*.fa seqs.?.renum.fa id.*.map seqs.*.dnadist  seqs.*.neighbor  seqs.*.tree seqs.aln.*.full seqs.*.faln  seqs.?.named.tree seqs.?.nonneg.tree
	rm -f seqs.$(PRIMER).sitedate.tree seqs.$(PRIMER).date.tree seqs.$(PRIMER).site.tree seqs.$(PRIMER).crassphage.blastn seqs.$(PRIMER).renum.rc.fa metadata.$(PRIMER).tsv
