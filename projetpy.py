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
    if (not name.isalpha()) or (name==""):
        QMessageBox.critical(fen, "Error", "Vérifiez votre nom")
        fen.num_supprim.setText("")
        fen.num_supprim.setFocus()
    else :
        tous_les_contact = [nom for nom in csv.reader(open("projetpython.csv"))]
        trouve = False
        index = 0
        for contact in tous_les_contact:
            if name == contact[0]:
                trouve = True
                tous_les_contact = tous_les_contact[:index] + tous_les_contact[index+1:]
                break
            index += 1
        with open('projetpython.csv','w') as file:
            csv_writer = csv.writer(file)
            for contact in tous_les_contact:
                csv_writer.writerow(contact)
        QMessageBox.information(fen, "Cool", "suppression effectuer avec succes")
        fen.num_supprim.clear()


def aff():
    name=fen.num_aff.text()
    fen.table.setRowCount(0)
    for contact in  open ('projetpython.csv','r'):
        [nom,email,tel] = contact.split(',')
        if(name==nom):
            row = fen.table.rowCount()
            fen.table.insertRow(row)
            fen.table.setItem(row,0,QTableWidgetItem(nom))
            fen.table.setItem(row,1,QTableWidgetItem(email))
            fen.table.setItem(row,2,QTableWidgetItem(tel.strip()))
    fen.num_aff.setText("")

        
        
        

app = QApplication([])
fen = loadUi("interface.ui")
fen.show()
fen.ajouter.clicked.connect(ajout)
fen.supprimer.clicked.connect(supprim)
fen.afficher.clicked.connect(aff)

app.exec_()
