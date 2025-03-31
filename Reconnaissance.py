import face_recognition
import cv2
import numpy as np
import os

from deepface import DeepFace

existe=False
nom_utilisateur=''

def reco():
    # chargement du fichier de signature
    signature_fichier=np.load('Signature.npy')
    signature=signature_fichier[:,:-1].astype(float) #extraction des caracteristiques
    nom=signature_fichier[:,-1] #extraction des noms
    #print(signature)

    capture=cv2.VideoCapture(0)

    while True:
        reponse,image=capture.read()
        if reponse:
            img_reduit=cv2.resize(image,(0,0),None,0.25,0.25)
            img_reduit=cv2.cvtColor(img_reduit,cv2.COLOR_BGR2RGB)
            emplacement_face=face_recognition.face_locations(img_reduit)
            caracteristique_face=face_recognition.face_encodings(img_reduit,emplacement_face)
            #Comparer la capture avec les signatures
            for encodage,loc in zip (caracteristique_face,emplacement_face):
                match=face_recognition.compare_faces(signature,encodage)
                distance_face=face_recognition.face_distance(signature,encodage)
                min_dist=np.argmin(distance_face)
                y1,x2,y2,x1=loc
                y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
                
                if match[min_dist]==True:
                    cv2.rectangle(image,(x1,y1),(x2,y2),(0,255,0),2)
                    nomS=nom[min_dist]
                    cv2.putText(image,nomS,(x1,y1-10),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                    global existe
                    existe=True
                    global nom_utilisateur
                    nom_utilisateur=nomS
                    break
                else:
                    cv2.rectangle(image,(x1,y1),(x2,y2),(0,255,0),2)
                    nomS='inconnue'
                    cv2.putText(image,nomS,(x1,y1-10),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                    
                    

            
            #Deep face (emotions,genre,age, ...)
            try:
                face_image=image[y1:y2,x1:x2]
                analyse= DeepFace.analyze(face_image,actions=['emotion'],enforce_detection=True)
                if isinstance (analyse,list):
                    analyse=analyse[0]
                emotion_dominante=analyse.get('dominant_emotion','Non_detectee')
                cv2.putText(image,emotion_dominante,(x1,y2+25),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            except Exception as e:
                print(f'Erreur: {e}')


        
            cv2.imshow("Reconnaissance",image)  

            if cv2.waitKey(20)==ord('q'):
                break
        else:
            break

    capture.release()
    cv2.destroyAllWindows()


def get_existence():
    return existe

def get_nom_utilisateur():
    return nom_utilisateur