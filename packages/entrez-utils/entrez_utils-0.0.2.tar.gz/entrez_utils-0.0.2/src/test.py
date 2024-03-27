from entrez_utils import *
from IPython import embed

if __name__ == "__main__":
    man = EntrezManager("andrew.tapia@uky.edu")
    with open("../../wrasse/metadata.txt", "r") as wfile:
        accs = [l.rstrip().split()[-1] for l in wfile]
    samples = fetched(BioSample.from_sra_accessions(man, accs))
    embed()
