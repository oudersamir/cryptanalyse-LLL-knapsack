


****************** l'implementation de sac a dos et l'attaque LLL  sur sac a dos **********************





PRESENTATION DES FICHIERS


crypt.py      :  fichier responsable de crypter  le message claire avec cryptosyteme KNAPSACK.

decrypt.py    :  fichier reseponsable de crypter le message crypter.

attack_LLL.py : fichier qui fait l'attaque avec l'algorithme LLL.

empilement.py : exemple du cours ( sac a dos ) 

  chiffrement :


	1- executez le fichier crypt.py 
	2- entrez le texte claire 
	3- le script va generer les donnees suivantes :
			       cle publique :

			- modulo : keys/public_key/modulo.txt
			- multiplicative : keys/public_key/multiplicative_to_mask.txt
				
				cle privee :
			-suite super croissante : keys/private_key/private_key.txt


			-le message de l'entrer dans : resultat/input_msg_clear.txt
			-le text chiffrer dans : resultat/output_msg_crypt.txt
  dechiffrement :
	
	1- executez le fichier decrypt.py
	2- le script il va lire les donnees necessaire le texte chiffrer et cle privee et la cle publique a partir les chemins precedente
	3- le resultat de dechiffrement sera ecrit dans le fichier  resultat/input_msg_decrypt.txt.

 application l'algorithme LLL :
  	1- executez le fichier attaque_LLL.py
	2- pour faire l'attaque on a besoin du texte claire et la cle publique  alors 
	le script va requiperer ces donnees  a partir de  resultat/output_msg_crypt.txt et keys/public_key/public_key.txt
	3- enfin le resultat sera mettre dans le fichier text_claire.txt
	
				
			

