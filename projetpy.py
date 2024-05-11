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

def distinct(cin):
    try:
        for i in open("projetpython.csv","r"):
            [cin_test,nom,email,tel] = i.split(',')
        
            if cin_test == cin:
                return False
    
        return True
    except:
        return True


def ajout():
    cin = fen.cin.text()
    name = fen.name.text()
    mail = fen.mail.text()
    tel = fen.tel.text()
    if not distinct(cin) or not cin.isnumeric():
        QMessageBox.critical(fen, "Error", "CIN non DISTINCT ou incorrect")
        fen.cin.setText("")
        fen.cin.setFocus()
    elif not cin.isnumeric() or cin == "":
        QMessageBox.critical(fen, "Error", "Vérifiez votre cin")
        fen.name.setText("")
        fen.name.setFocus()
    elif (not name.isalpha()) or (name==""):
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
        user = [cin,name, mail, tel]
        file_exists = os.path.isfile("projetpython.csv")
        with open("projetpython.csv", "a", newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                fields = ["cin","nom", "mail", "tel"]
                writer.writerow(fields)
                
            writer.writerow(user)
        QMessageBox.information(fen, "Notice", "Ajout effectuer avec succes")
        fen.name.setText("")
        fen.mail.setText("")
        fen.tel.setText("")
        fen.cin.setText("")
        fen.cin.setFocus()

def supprim():
    cin = fen.num_supprim.text()
    if not cin.isnumeric() or cin == "":
        QMessageBox.critical(fen, "Error", "Vérifiez votre nom")
        fen.num_supprim.setText("")
        fen.num_supprim.setFocus()
    else:
        liste = []
        test = False
        f = open("projetpython.csv", "r", newline='')
        file = csv.reader(f)
        for ligne in file:
            if cin != ligne[0]:
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

        QMessageBox.information(fen, "Notice", "Suppression avec succès")

def error(found):
    if not found:
        QMessageBox.critical(fen, "Error", "CIN INEXISTANT")


def modification():
    cin = fen.num_modif.text()
    new_mail = fen.nouv_mail.text()
    new_tel = fen.nouv_num.text()
    
    d = []
    found = False
    with open("projetpython.csv","r") as f:
        file = csv.reader(f)
        for data in file:
            if data[0] == cin:
                data[2] = new_mail
                data[3] = new_tel
                found = True
            d.append(data)
    
    if not found:
        error(found)
        return
    
    with open("projetpython.csv","w",newline='') as f:
        file = csv.writer(f)
        for data in d:
            file.writerow(data)
            
    QMessageBox.information(fen,"coool","Modification effectuée avec succes")
    

def aff():
    name=fen.num_aff.text()
    fen.table.setRowCount(0)
    test=True
    for contact in open('projetpython.csv','r'):
        [cin,nom,email,tel] = contact.split(',')
        if(name==nom):
            test=False
            row = fen.table.rowCount()
            fen.table.insertRow(row)
            fen.table.setItem(row,0,QTableWidgetItem(cin))
            fen.table.setItem(row,1,QTableWidgetItem(nom))
            fen.table.setItem(row,2,QTableWidgetItem(email))
            fen.table.setItem(row,3,QTableWidgetItem(tel.strip()))
        if(name==""):
            QMessageBox.information(fen,"error","nom obligatoire")
            
        else:
            QMessageBox.information(fen,"error","nom non existant")
            
            
            
    fen.num_aff.setText("")
    
        
def afftout():
    fen.table.setRowCount(0)
    for contact in open("projetpython.csv","r"):
        [cin,nom,email,tel] = contact.split(',')
        row = fen.table.rowCount()
        if cin != "cin" and nom != "nom" and email != "mail" and tel != "tel":
            fen.table.insertRow(row)
            fen.table.setItem(row,0,QTableWidgetItem(cin))
            fen.table.setItem(row,1,QTableWidgetItem(nom))
            fen.table.setItem(row,2,QTableWidgetItem(email))
            fen.table.setItem(row,3,QTableWidgetItem(tel.strip()))
def vider():
    if fen.password.text() != "0000":
        QMessageBox.critical(fen,"error","Mot de passe incorrect")
        return
    with open("projetpython.csv",'w') as file:
        writer=csv.writer(file)
    fen.table.setRowCount(0)
        
    
        

app = QApplication([])
fen = loadUi("interface.ui")
fen.show()
fen.ajouter.clicked.connect(ajout)
fen.supprimer.clicked.connect(supprim)
fen.afficher.clicked.connect(aff)
fen.modifier.clicked.connect(modification)
fen.afficher_t.clicked.connect(afftout)
fen.vider_file.clicked.connect(vider)
app.exec_()
