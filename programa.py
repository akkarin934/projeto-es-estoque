
from PyQt5 import uic,QtWidgets # importando módulo uic para ler o arquivo UI e QtWidgets para montar os elementos
import mysql.connector # módulo do python que conecta com o mysql

# fazendo a conexão python com o mysql 
banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="cadastro_produtos"
)

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

    # insere no banco os dados digitados pelo usuário
    cursor = banco.cursor()
    comando_SQL = "INSERT INTO produtos (codigo,nome,preco,categoria) VALUES (%s,%s,%s,%s)"
    dados = (str(linha1),str(linha2),str(linha3),categoria)
    cursor.execute(comando_SQL,dados)
    banco.commit()

    formulario.lineEdit.setText("") # limpa o escrito após enviar
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")

def chama_segunda_tela():
    segunda_tela.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall() 

    segunda_tela.tableWidget.setRowCount(len(dados_lidos)) #linhas da tabela
    segunda_tela.tableWidget.setColumnCount(5) # número colunas da tabela é fixo 

    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            segunda_tela.tableWidget.setItem(i, j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

def excluir_dados():
    linha = segunda_tela.tableWidget.currentRow()
    segunda_tela.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM produtos WHERE id=" + str(valor_id))


numero_id = 0

def editar_dados():
    global numero_id
    linha = segunda_tela.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM produtos WHERE id="+ str(valor_id))
    produto = cursor.fetchall()
    tela_editar.show()
    
    numero_id = valor_id

    tela_editar.lineEdit.setText(str(produto[0][0]))
    tela_editar.lineEdit_2.setText(str(produto[0][1]))
    tela_editar.lineEdit_3.setText(str(produto[0][2]))
    tela_editar.lineEdit_4.setText(str(produto[0][3]))
    tela_editar.lineEdit_5.setText(str(produto[0][4]))


def salvar_editados():
    # pega o número do id
    global numero_id
    # pega o valor digitado no lineEdit (as caixas aonde o usuário digita os valores)
    codigo = tela_editar.lineEdit_2.text() # método .text() lê o que foi passado
    nome = tela_editar.lineEdit_3.text()
    preco = tela_editar.lineEdit_4.text()
    categoria = tela_editar.lineEdit_5.text()
    # atualizar no banco os dados que foram editados 
    cursor = banco.cursor()
    cursor.execute("UPDATE produtos SET codigo = '{}', nome = '{}', preco = '{}', categoria = '{}' WHERE id ={}".format(codigo,nome,preco,categoria,numero_id))
    # atualiza na tela
    tela_editar.close()
    segunda_tela.close()
    chama_segunda_tela()

app=QtWidgets.QApplication([])
formulario=uic.loadUi("formulario.ui") # carrega o arquivo de interface feito no Qt
segunda_tela=uic.loadUi("listar_produtos.ui") # carregando a tela de listagem
tela_editar=uic.loadUi("tela_editar.ui")
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_3.clicked.connect(chama_segunda_tela)
segunda_tela.pushButton.clicked.connect(excluir_dados)
segunda_tela.pushButton_2.clicked.connect(editar_dados)
tela_editar.pushButton.clicked.connect(salvar_editados)

formulario.show() 
app.exec()