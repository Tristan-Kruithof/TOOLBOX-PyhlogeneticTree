class DNA:
    def __init__(self, sequentie, ):

        self.sequentie = sequentie

    def vertalen_naar_RNA(self):
        RNA_dict = {'T' : 'U', 'G' : 'G', 'A' : 'A', 'C' : 'C'}
        RNA_list = []

        for item in self.sequentie:
            if item in RNA_dict:
                item = RNA_dict[item]
                RNA_list.append(item)
        RNA_sequentie = ''.join(RNA_list)
        return RNA_sequentie

    def __str__(self):
        return f'RNA-sequence:{'\n'}{DNA.vertalen_naar_RNA(self)}{'\n'}translated proteins:{'\n'}{DNA.vertalen_naar_eiwitten(self)}'

    def vertalen_naar_eiwitten(self):
        codon_table = {
            'AAA': 'K', 'AAC': 'N', 'AAG': 'K', 'AAT': 'N',
            'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',
            'AGA': 'R', 'AGC': 'S', 'AGG': 'R', 'AGT': 'S',
            'ATA': 'I', 'ATC': 'I', 'ATG': 'M', 'ATT': 'I',
            'CAA': 'Q', 'CAC': 'H', 'CAG': 'Q', 'CAT': 'H',
            'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCT': 'P',
            'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R',
            'CTA': 'L', 'CTC': 'L', 'CTG': 'L', 'CTT': 'L',
            'GAA': 'E', 'GAC': 'D', 'GAG': 'E', 'GAT': 'D',
            'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',
            'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
            'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V',
            'TAA': '_', 'TAC': 'Y', 'TAG': '_', 'TAT': 'Y',
            'TCA': 'S', 'TCC': 'S', 'TCG': 'S', 'TCT': 'S',
            'TGA': '_', 'TGC': 'C', 'TGG': 'W', 'TGT': 'C',
            'TTA': 'L', 'TTC': 'F', 'TTG': 'L', 'TTT': 'F',
        }
        vertaling = {}
        eiwit_list = []
        for i in range(0, len(self.sequentie), 3):
            if (self.sequentie[i:i + 3]) in codon_table:
                vertaling[self.sequentie[i:i + 3]] = codon_table[self.sequentie[i:i + 3]]
                eiwit_list.append(codon_table[self.sequentie[i:i + 3]])

        eiwit_sequentie = ''.join(eiwit_list)
        return eiwit_sequentie
DNA_sequentie = DNA('ATGCTTTTGAAGGATGCCCGGCCTTGAAGCT')
print(DNA_sequentie)

