from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMessageBox,QTableWidgetItem
import csv
import os


def is_valid_email(email):
    if "@" in email and "." in email:
        parts = email.split("@")
        if len(parts) == 2:
            domain_parts = parts[1].split(".")
            if len(domain_parts) >= 2:
                return True
    return False

def ajout():
    name = fen.name.text()
    mail = fen.mail.text()
    tel = fen.tel.text()
    
    if (not name.isalpha()) or (name==""):
        QMessageBox.critical(fen, "Error", "Vérifiez votre nom")
        fen.name.setText("")
        fen.name.setFocus()
    elif (is_valid_email(mail)==False) or (mail==""):
        QMessageBox.critical(fen, "Error", "Vérifiez votre mail")
        fen.mail.setText("")
        fen.mail.setFocus()
    elif(len(tel)!=8) or (tel.isnumeric()==False):
        QMessageBox.critical(fen, "Error", "Vérifiez votre tel")
        fen.tel.setText("")
        fen.tel.setFocus()
    else:
        user = [name, mail, tel]
        file_exists = os.path.isfile("projetpython.csv")
        with open("projetpython.csv", "a", newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                fields = ["nom", "mail", "tel"]
                writer.writerow(fields)
                
            writer.writerow(user)
        QMessageBox.information(fen, "Cool", "Ajout effectuer avec succes")
        fen.name.setText("")
        fen.mail.setText("")
        fen.tel.setText("")
        fen.name.setFocus()

def supprim():
    name = fen.num_supprim.text()
    if not name.isalpha() or name == "":
        QMessageBox.critical(fen, "Error", "Vérifiez votre nom")
        fen.num_supprim.setText("")
        fen.num_supprim.setFocus()
    else:
        liste = []
        test = False
        f = open("projetpython.csv", "r", newline='')
        file = csv.reader(f)
        for ligne in file:
            if name != ligne[0]:
                liste.append(ligne)
            else:
                test = True
        f.close()

        if not test:
            error(test)
            return

        f = open("projetpython.csv", "w", newline='')
        file = csv.writer(f)
        for ligne in liste:
            file.writerow(ligne)
        f.close()

        QMessageBox.information(None, "Notice", "Suppression avec succès")

def error(found):
    if not found:
        QMessageBox.critical(None, "Error", "NOM INEXISTANT")


def modification():
    nom = fen.num_modif.text()
    new_mail = fen.nouv_mail.text()
    new_tel = fen.nouv_num.text()
    
    d = []
    found = False
    with open("projetpython.csv","r") as f:
        file = csv.reader(f)
        for data in file:
            if data[0] == nom:
                data[1] = new_mail
                data[2] = new_tel
                found = True
            d.append(data)
    
    if not found:
        error(found)
        return
    
    with open("projetpython.csv","w",newline='') as f:
        file = csv.writer(f)
        for data in d:
            file.writerow(data)
            
    QMessageBox.information(None,"Notice","Modification effectuée avec succes")
    

def aff():
    name=fen.num_aff.text()
    fen.table.setRowCount(0)
    for contact in open('projetpython.csv','r'):
        [nom,email,tel] = contact.split(',')
        if(name==nom):
            row = fen.table.rowCount()
            fen.table.insertRow(row)
            fen.table.setItem(row,0,QTableWidgetItem(nom))
            fen.table.setItem(row,1,QTableWidgetItem(email))
            fen.table.setItem(row,2,QTableWidgetItem(tel.strip()))
            
    fen.num_aff.setText("")
    
        
def afftout():
    fen.table.setRowCount(0)
    for contact in open("projetpython.csv","r"):
        [nom,email,tel] = contact.split(',')
        row = fen.table.rowCount()
        if nom != "nom" and email != "mail" and tel != "tel":
            fen.table.insertRow(row)
            fen.table.setItem(row,0,QTableWidgetItem(nom))
            fen.table.setItem(row,1,QTableWidgetItem(email))
            fen.table.setItem(row,2,QTableWidgetItem(tel.strip()))
        

app = QApplication([])
fen = loadUi("interface.ui")
fen.show()
fen.ajouter.clicked.connect(ajout)
fen.supprimer.clicked.connect(supprim)
fen.afficher.clicked.connect(aff)
fen.modifier.clicked.connect(modification)
fen.afficher_t.clicked.connect(afftout)
app.exec_()
