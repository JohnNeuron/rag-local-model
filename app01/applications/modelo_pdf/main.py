from flask import Flask, render_template, request, jsonify
from langchain_community.document_loaders import PDFPlumberLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
import os
import re

from flask_cors import CORS

app = Flask(__name__)


# Configuração do CORS para o App Flask
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

#Setando um limite máximo de upload do arquivo PDF
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Configuração do modelo Ollama que está rodando em modo serve
llm = OllamaLLM(model="deepseek-r1:8b")

# Template do prompt
prompt_template = """
Você é um professor que utiliza as abordagens de Vygotsky e Piaget para promover a aprendizagem ativa. 
Em vez de fornecer respostas completas, ofereça apenas os fundamentos e 
faça perguntas que estimulem o aluno a pensar e descobrir por si mesmo.

1. Use APENAS o contexto abaixo.
2. Se não souber, diga "Eu não sei".
3. Mantenha as respostas com menos de 4 frases.

Contexto: {context}
Pergunta: {question}
Resposta: """

QA_CHAIN_PROMPT = PromptTemplate.from_template(prompt_template)

# Configuração do upload
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

qa_chain = None

#Rota para página Home
@app.route('/')
def home():
    return render_template('index.html')

#Rota de upload
@app.route('/upload', methods=['POST'])
def upload_file():
    
    #Camada de tratamento para ações de upload

    if 'file' not in request.files: #Caso não haja arquivos recebidos
        return jsonify({'error': 'Nenhum arquivo carregado'}), 400
    
    file = request.files['file']

    if file.filename == '': #Caso não tenha selecionado um arquivo para receber
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    
    file = request.files['file'] #Caso haja arquivo para receber
    print(f"File received: {file.filename}")
    
    #Se for um arquivo e a extensão seja .PDF
    if file and file.filename.endswith('.pdf'):
        
        #Cria um arquivo temporário do .PDF recebido
        filepath = os.path.join(UPLOAD_FOLDER, 'temp.pdf')
        file.save(filepath)
        
        # Processa o PDF
        loader = PDFPlumberLoader(filepath)
        documents = loader.load()
        
        #Realiza a divisão do documento em partes menores
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(documents)
        
        #Realiza a criação das representações vetoriais do texto
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2") #Modelo para conversão
        vector_store = FAISS.from_documents(docs, embeddings) #Armazena em um banco de vetores 
        
        #Sistema de busca de informações que retorna os 3 documentos mais semelhantes
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        
        #Criação da cadeia de perguntas e respostas
        global qa_chain #Variavel global setada acima
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm, #Modeo para gerar respostas.
            chain_type="stuff", #STUFF traz todo os documentos relevantes de uma vez para o modelo.
            retriever=retriever, #Mecanismo de busca
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT} #Prompt personalizado setado acima
        )
        
        return jsonify({'message': 'PDF processed successfully'})
    
    return jsonify({'error': 'Invalid file type'}), 400

#Rota para a realização de perguntas
@app.route('/ask', methods=['POST'])
def ask_question():

    #Se a variavel qa_chain estiver vazia
    if not qa_chain:
        return jsonify({'error': 'Por favor, suba um arquivo PDF primeiro.'}), 400
    

    question = request.json.get('question')
    
    #Se não houver uma pergunta
    if not question:
        return jsonify({'error': 'Nenhuma pergunta fornecida'}), 400
    
    #Obtém a resposta do modelo a questão
    response = qa_chain.run(question)
    
    # Divisão entre Pensamento e resposta: Expressões regulares para capturar o conteúdo dentro e fora da tag <think>
    inside_think = re.findall(r"<think>(.*?)</think>", response, re.DOTALL)
    outside_think = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()
  
    print('Esse é o thinking:',inside_think)
    print('Esse é o response:',outside_think)
    
    return jsonify({
        'thinking': inside_think,
        'response': outside_think.strip()
    })

if __name__ == '__main__':
    app.run(host ='0.0.0.0',port = 8010,debug=False)