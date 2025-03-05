from vanna.chromadb import ChromaDB_VectorStore 
from vanna.flask import VannaFlaskApp
from vanna.ollama import Ollama



#Classe para inicialização do LLM e ChromaDB 
class MyVanna(ChromaDB_VectorStore, Ollama):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Ollama.__init__(self, config=config)

#Passando como argumento o modelo que está configurado no "ollama serve". 
vn = MyVanna(config={
    'model': 'deepSeek-r1:8b'
})

#Realizando a conexão com o banco. 
vn.connect_to_mysql(host='ip_banco', dbname='banco_ficticio', user='user', password='password', port=12345)

#Realizando o treinamento do modelo com base no resultado SQL.
vn.train(sql="SELECT * FROM estoqueProdutos WHERE rownum < 1000")


#Setando o App Flask do Vanna
app = VannaFlaskApp(vn)

#Rodando Vanna na rede local
app.run(host = '0.0.0.0', port = 8010,debug = True)