"""
Given a fasta file and a list of sequence IDs, write the whole file out but with those sequence IDs reverse complemented.
"""

import os
import sys
import argparse
import gzip

def stream_fasta(fastafile):
    """
    Stream a fasta file, one read at a time. Saves memory!

    :param fastafile: The fasta file to stream
    :type fastafile: str
    :return:A single read
    :rtype:str, str
    """

    try:
        if fastafile.endswith('.gz'):
            f = gzip.open(fastafile, 'rb')
        else:
            f = open(fastafile, 'r', encoding='utf-8')
    except IOError as e:
        sys.stderr.write(str(e) + "\n")
        sys.stderr.write("Message: \n" + str(e.message) + "\n")
        sys.exit("Unable to open file " + fastafile)

    posn = 0
    while f:
        # first line should start with >
        idline = f.readline()
        if not idline:
            break
        if not idline.startswith('>'):
            sys.exit("Do not have a fasta file at: {}".format(idline))
        idline = idline.strip().replace('>', '', 1)
        posn = f.tell()
        line = f.readline()
        seq = ""
        while not line.startswith('>'):
            seq += line.strip()
            posn = f.tell()
            line = f.readline()
            if not line:
                break
        f.seek(posn)
        yield idline, seq


def rc(dna):
    """
    Reverse complement a DNA sequence

    :param dna: The DNA sequence
    :type dna: str
    :return: The reverse complement of the DNA sequence
    :rtype: str
    """
    complements = str.maketrans('acgtrymkbdhvACGTRYMKBDHV', 'tgcayrkmvhdbTGCAYRKMVHDB')
    rcseq = dna.translate(complements)[::-1]
    return rcseq


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Reverse complement some sequences')
    parser.add_argument('-f', help='fasta file of sequences', required=True)
    parser.add_argument('-i', help='file with list of IDs, one per line', required=True)
    parser.add_argument('-o', help='output file', required=True)
    parser.add_argument('-v', help='verbose output', action='store_true')
    args = parser.parse_args()

    torc = set()
    with open(args.i) as idF:
        for l in idF:
            torc.add(l.strip())

    with open('args.o', 'w', encoding='utf-8') as out:
        for ids, seq in stream_fasta(args.f):
            name = ids.split(" ")[0]
            if name in torc:
                seq = rc(seq)
            out.write(">{}\n{}\n".format(ids, seq))
