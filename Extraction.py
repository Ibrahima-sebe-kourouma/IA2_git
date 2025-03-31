import face_recognition
import cv2
import numpy as np
import os

def extraction_carac():
    chemin_dossier = "./capture/"
    liste_image=[]
    liste_nom=[]

    liste_fichier=os.listdir(chemin_dossier)
    #print(liste_fichier)

    #Chargement des images
    for Nom_fichier in liste_fichier:
        #print(f'{chemin_dossier}{Nom_fichier}')
        image=cv2.imread(f'{chemin_dossier}{Nom_fichier}')
        liste_image.append(image)
        #Extraction des noms
        nom_sans_extension=os.path.splitext(Nom_fichier)[0]
        #print(nom_sans_extension)
        liste_nom.append(nom_sans_extension)

    def extractionCaracteristique(L_images,L_nom):
        liste_caracteristique=[]
        compteurs=1
        for image,nom in zip(L_images,L_nom):
            image_rgb=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            encodage=face_recognition.face_encodings(image_rgb)[0]
            encodage=encodage.tolist()+[nom]
            print(encodage)
            liste_caracteristique.append(encodage)
            progression=int(compteurs/len(L_images)*100)
            print(f'{progression}%')
            compteurs+=1
        array_caracteristique=np.array(liste_caracteristique)
        np.save('Signature.npy',array_caracteristique)
        print('Extraction et sauvegarde terminée')

    extractionCaracteristique(liste_image,liste_nom)



