# importando módulo uic para ler o arquivo UI e QtWidgets para montar os elementos
from PyQt5 import uic,QtWidgets

def funcao_principal():
    
    linha1 = formulario.lineEdit.text() # lê o que foi digitado
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()

    categoria = ""

    if formulario.radioButton.isChecked(): # verifica se o botão foi clicado
        print("Categoria Alimento selecionada")
        categoria = "Alimento"
    elif formulario.radioButton_2.isChecked():
        print("Categoria Limpeza selecionada")
        categoria = "Limpeza"
    else:
        print("Categoria Higiene selecionada")
        categoria = "Higiene"

    print("Código:", linha1) # o que foi digitado no "código" na interface gráfica, é recuperado na linha 1, e assim por diante
    print("Nome:", linha2)
    print("Preço:", linha3)

app=QtWidgets.QApplication([])
formulario=uic.loadUi("formulario.ui") # carrega o arquivo de interface feito no Qt
formulario.pushButton.clicked.connect(funcao_principal)

formulario.show()
app.exec()