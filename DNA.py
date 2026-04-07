import sys
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

    #def __str__(self):
     #   return DNA.bestand_schrijven(self)

    def dictionary_maken(self):
        """
        Maakt een dictionary met de headers van het fasta-bestand als key en de bijbehorende mRNA-sequenties als value

        :Param: regels: list
        :Return: RNA_dict: dictionary
        """

        RNA_dict = {}

        for regel in self.sequentie:
            if regel.startswith('>'):
                # als een regel met < begint, dan is het een header

                header = regel.replace('\n', '')
            elif not regel.startswith('>') and regel != '\n':
                sequentie = regel.replace('\n', '')
                RNA_dict.setdefault(header, []).append(sequentie)
                # maakt keys van de headers van het fasta-bestand en values van de mRNA-sequenties in RNA-dict

        for header, sequentie in RNA_dict.items():
            gekoppelde_sequentie = ''.join(sequentie)
            RNA_dict[header] = gekoppelde_sequentie
            # zorgt ervoor dat de losse regels van de sequenties aan elkaar gekoppeld worden als één enkele string

        return RNA_dict

    def nucleotiden_vertalen(self, RNA_dict):
        """
        Verdeelt de sequenties van het fasta-bestand in codons en vertaalt de codons naar eiwitten. De headers en eiwitten worden overgeschreven naar een nieuw bestand.

        :param RNA_dict: dictionary
        :Param: startpositie: string

        :return: vertaling: dictionary
        """
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

        for header, sequentie in RNA_dict.items():
            for i in range(0, len(sequentie), 3):
                codons = sequentie[i:i + 3]
                # verdeelt de mRNA-sequenties in codons

                if codons in codon_table:
                    vertaling.setdefault(header, []).append(codon_table[codons])
                    # vertaalt de codons naar de eiwitten waar ze voor coderen

                if len(codons) != 3:
                    print(f'{len(codons)} nucleotiden blijven over aan het einde van de sequentie van {header}')
                # zorgt voor een melding als er aan het einde van de sequentie 1 of 2 nucleotiden overblijven

            for header, codon in vertaling.items():
                vertaling[header] = ''.join(codon)
                # zorgt ervoor dat de losse eiwitten per sequentie als één enkele string worden weergegeven

        return vertaling

    def resultaat_wegschrijven(vertaling, output_file):
        """
        Schrijft de headers en vertaalde sequenties over naar een nieuw bestand
        :Param: vertaling: dictionary
        :Param: output_file: string
        :Return:
        """

        with open(output_file, 'w') as file_output:
            for header, sequentie in vertaling.items():
                file_output.write(f'{header}{'\n'}')
                for i in range(0, len(sequentie), 70):
                    juiste_lengte = sequentie[i:i + 70]
                    file_output.write(f'{juiste_lengte}{'\n'}')

                file_output.write('\n')



