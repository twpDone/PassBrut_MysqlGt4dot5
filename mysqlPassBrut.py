#!/usr/bin/python
# -*- coding: utf8-*-

import hashlib

def strToMysqlPassword(str):
    """
        Calcule le hash de la meme facon que la fonction Password de mysql
        @note Mysql doit etre de version >4.5
        @note ----
        @note Le calcul du hash dans mysql s'obtient avec :
        @note   SHA1(UNHEX(SHA1(chaine)
        @param str chaine a hasher
        @return Le hash dans sa representation hexadecimale.
    """
    return hashlib.sha1(hashlib.sha1(str).digest()).hexdigest()

def brutMysqlHash(len,hash):
    """
    Brute force sur 'len' caracteres pour trouver le 'hash' passé en argument.
    Utilise strToMysqlPassword pour calculer le hash.

    @param len Longueur de la chaine à bruteforcer
    @param hash Hash mysql a trouver
    @return None si le hash n'est pas trouvé
    @return Un bytearray contenant la chaine correspondant au hash
    @see strToMysqlPassword
    """ 
    str=bytearray("") 
    # Initialisation du bytearray
    # chaque byte est initialisé avec char(32) (espace)
    for i in range(0,len):
        str+=chr(32)
    
    # Tant qu'on ne rends rien, continuer le traitement
    while 1:
        # faire varier la derniere lettre 
        # avec chaque caractere asscii afichable 32-127(exclu)
        #  (ne prends pas les accents)
        for ord in range(32,127):
            str[len-1]=chr(ord)
            #si le hash correspond on rends le bytearray
            if strToMysqlPassword(str)==hash:
                return str
        # pour chaque byte du bytearray
        # (parcours de len-1 a 0)
        for index in range(len-1,-1,-1):
            byte=str[index]
            # si on est a la derniere valeur ascii affichable (126)
            if byte==126:
                # si le premier byte est a 126, 
                # nous avons teste toutes le possibilites
                if index==0:
                    return None
                # sinon comme on est a 126 on remet le byte a chr(32) 
                # pour recommencer un tour de boucle
                str[index]=chr(32)
                # On incremente le caractere ascii 
                # a l'index precedent celui 
                # sur lequel on viens d epuiser toutes les possibilitees
                # en verifiant que l'index n'est pas < a 0 
                # (index out of range)
                if index-1>=0:
                    byte=str[index-1]
                    str[index-1]=chr(byte+1)

    
