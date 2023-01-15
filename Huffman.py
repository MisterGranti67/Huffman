from __future__ import annotations
import string
from typing_extensions import Self

class Huffman:
    # class HuffmanTree
    class HuffmanTree:
        def __init__(self:Self,char : str | None, freq : int,left : Huffman.HuffmanTree|None=None, right : Huffman.HuffmanTree|None=None):
            """
                constructor of HuffmanTree Node

                @Args:
                    char (str|None) : character
                    freq (int) : frequence of character 'char'
                    left (HuffmanTree) : left child
                    right (HuffmanTree) : right child
            """
            self.left = left
            self.right = right
            self.freq = freq
            self.char = char

        def isLeaf(self : Self) -> bool:
            """ renvoie True si le noeud est une feuille
            """
            if self.right:
                return False
            if self.left:
                return False
            return True
        #[-1] pour le dernier (il faut mettre la condition avant pour pouvoir l'append sinon cela plante, et attention à la liste vide aussi de mettre une condition)
    @staticmethod
    def buidFreqTable(text : str) -> list[int]:
        """ construit la table de fréquence
        """
        notre_liste : list[int] = [0 for i in range(256)]
        for t2 in text:
            if ord(t2) < 256:
                notre_liste[ord(t2)] += 1
        return notre_liste

    @staticmethod
    def insertHuffmanTreeList(tree : Huffman.HuffmanTree, list : list[Huffman.HuffmanTree]) -> list[Huffman.HuffmanTree]:
        """ insère un arbre dans une liste d’arbres triée
        """
        i=0
        mon_max = len(list)
        list2 = (i+mon_max)//2
        while i < mon_max:
            if tree.freq < list[list2].freq:
                mon_max=list2
            else:
                i = list2+1
            list2 = (i+mon_max)//2
        list.insert(i,tree)
        return list

    @staticmethod
    def buildTreeList(freqTable : list[int]) -> list[Huffman.HuffmanTree]:
        """ construit la liste triée des arbres feuilles
        """
        # print("buildTreeList")
        maliste = []
        for i in range(len(freqTable)):
            if freqTable[i]!=8:
                maliste = Huffman.insertHuffmanTreeList(Huffman.HuffmanTree(chr(i),freqTable[i]),maliste)
        return maliste


    @staticmethod
    def buildHuffmanTree(freqTable : list[int]) -> HuffmanTree:
        """ construit un arbre feuille pour chaque caractère présent
        """
        # print("buildHuffmanTree")
        feuille = Huffman.HuffmanTree 
        monarbre = Huffman.buildTreeList(freqTable)
        while len(monarbre)>1:
            nouvelarbre = Huffman.HuffmanTree(None,monarbre[0].freq+monarbre[1].freq,monarbre[0],monarbre[1])
            monarbre.remove(monarbre[0])
            monarbre.remove(monarbre[0])
            monarbre = Huffman.insertHuffmanTreeList(nouvelarbre,monarbre)
        return monarbre[0]

    
    @staticmethod
    def getCodingTable(tree : Huffman.HuffmanTree, path : str|None = None, res : dict[str,str] | None= None) -> dict[str,str]:
        """ renvoie le dictionnaire donnant le codage des caractères
        """
        if res is None:
            res = {}
        if path is None:
            path = ""
        if tree.left:
            res = Huffman.getCodingTable(tree.left,path+"0",res)
        if tree.right:
            res = Huffman.getCodingTable(tree.right,path+"1",res)
        if tree.isLeaf():
            if tree.char:
                res[tree.char] = path
                path = None
        
        return res
    @staticmethod
    def encodeHuffman(text: str) -> tuple[str, list[int]] :
        """ code un texte et renvoie le texte codé et la table de 
            fréquence

            Attention ord < 256 !!
        """
        # print("encodeHuffman")
        codage = ''
        frequence = (Huffman.buidFreqTable(text))
        arbre = Huffman.buildHuffmanTree(frequence)
        table = Huffman.getCodingTable(arbre)
    #     resultat = sorted(dico.items(), key=lambda t: t[1])
        for valeur in text:
            if ord(valeur) < 256:
                codage+=table[valeur]
        return (codage,frequence)

    @staticmethod
    def decodeHuffOne(codedText :str, i :int, huff :Huffman.HuffmanTree) -> tuple[int, str | None]:
        """ décode le i-ème caractère en fonction d’un arbre d’Huffman
        """
        tmp_huff = huff
        code = ""
        resultat = ""
        for i in codedText:
            code+=i

            if int(i)==0:
                huff=huff.left
            else:
                huff=huff.right

            if not huff.left:
                if not huff.right:
                    resultat+=huff.char
                    huff = tmp_huff
                    code = ""
        return resultat

    @staticmethod
    def decodeHuff(codedText : str,huff : HuffmanTree) -> str:
        """ decode le texte codé en fonction d’un arbre d’Huffman
        """
        codage = Huffman.decodeHuffOne(codedText,0,huff)
        return codage
    @staticmethod
    def decodeHuffman(txt: str, freqs : list[int]) -> str:
        """ décode un texte en fonction de la table de fréquence
        """
        codage = Huffman.buildHuffmanTree(freqs)
        resultat = Huffman.decodeHuff(txt,codage)
        return resultat

    @staticmethod
    def bitStream2str(myTextcoded : str) -> tuple[str,int]:
        """ convertit un stream  binaire '0'|'1' en texte 
            (codage 8 bits)

            return c'est X et len(myTextcoded)
        """
        test = ""
        text = len(myTextcoded)%8
        nombre_binaire = []
        for i in range(text,len(myTextcoded),8):
            nombre_binaire.append(myTextcoded[i:i+8])
        for i in nombre_binaire:
            test += chr(ord(chr(int(i,2))))
        return test,len(myTextcoded)
    
    @staticmethod
    def str2bitStream(txt : str, length: int) -> str:
        """ convertit un texte codé en stream '0’|'1’
        """
        nombre_binaire = []

        for i in range(len(txt)):
            nombre_binaire.append('{0:08b}'.format(ord(chr(ord(txt[i])))))
    
        nombre_binaire[0] = nombre_binaire[0][len(nombre_binaire[0])-length%8]
        return "".join(nombre_binaire)




if __name__ == '__main__':
    text_file = open("./fdm.txt","r",encoding='utf8')
    data = text_file.read()
    text_file.close()

    myText= "Souvent, pour s'amuser, les hommes d'équipage Prennent des albatros, vastes oiseaux des mers, Qui suivent, indolents compagnons de voyage, Le navire glissant sur les gouffres amers. À peine les ont-ils déposés sur les planches, Que ces rois de l'azur, maladroits et honteux, Laissent piteusement leurs grandes ailes blanches Comme des avirons traîner à côté d'eux. Ce voyageur ailé, comme il est gauche et veule ! Lui, naguère si beau, qu'il est comique et laid ! L'un agace son bec avec un brûle-gueule, L'autre mime, en boitant, l'infirme qui volait ! Le Poëte est semblable au prince des nuées Qui hante la tempête et se rit de l'archer ; Exilé sur le sol au milieu des huées, Ses ailes de géant l'empêchent de marcher."
    print(">> test Huffman: text to be encoded")
    print(">> ----------------------------------------")
    print(data)
    print(">> ----------------------------------------")

    # test = Huffman.buildTreeList(Huffman.buidFreqTable("test"))
    # print(test)
    # for i in range(len(test)):
    #     print(test[i])
    # # encoding, then convert to txt
    bitStream,freqTable  = Huffman.encodeHuffman(data)
    myTextcoded, length = Huffman.bitStream2str(str(bitStream))

    print(">> encoded text according Huffman")
    print("----------------------------------------")
    print(f'{myTextcoded}')
    print("----------------------------------------")

    # decoding : convert txt (8bits) to bit stream ‘01001’, then decode
    newBitStream = Huffman.str2bitStream(myTextcoded, length) 
    decoded = Huffman.decodeHuffman(newBitStream, freqTable)

    print(">> decoded text")
    print(">> ----------------------------------------")
    print(decoded)
    print(">> ----------------------------------------")
    print(f'>> compression ratio: {round(100*len(myTextcoded)/len(data))} %')

