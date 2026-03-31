class DNA:
    def __init__(self, sequentie):

        self.sequentie = sequentie

    def vertalen_naar_RNA(self):
        RNA_dict = {'T' : 'U', 'G' : 'G', 'A' : 'A', 'C' : 'C'}
        RNA_list = []

        for item in self.sequentie:
            if item in RNA_dict:
                item = RNA_dict[item]
                RNA_list.append(item)
        string = ''.join(RNA_list)
        return string

    def __str__(self):
        return DNA.vertalen_naar_RNA(self)

DNA_sequentie = DNA('ATGCTTTTGAAGGATGCCCGGCCTTGAAGCT')

print(DNA_sequentie.vertalen_naar_RNA())
