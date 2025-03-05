# 🚀 Soluções RAG Deepseek-r1:8b

[![GitHub stars](https://img.shields.io/github/stars/JohnNeuron/rag-local-model?style=social)](https://github.com/JohnNeuron/rag-local-model/stargazers) 
[![GitHub forks](https://img.shields.io/github/forks/JohnNeuron/rag-local-model?style=social)](https://github.com/JohnNeuron/rag-local-model/network)

> **RAG (Retrieval-Augmented Generation)** que integra dados de bancos e documentos PDF do usuário  
> utilizando soluções **gratuitas** e **locais** — da infraestrutura ao servidor de aplicação.

---

## 📖 Descrição

Este repositório reúne uma coleção de projetos que implementam **RAG** para:
- **Recuperar informações** de bancos de dados e arquivos PDF;
- **Gerar respostas** e conteúdo de forma inteligente;
- Utilizar **ferramentas gratuitas** e recursos locais, garantindo uma solução econômica e escalável.

---

## ⚙️ Recursos

- **Integração de Dados:** Extração e processamento de informações de fontes variadas.
- **Soluções Completamente Gratuitas:** Da infraestrutura ao servidor, tudo utilizando recursos free.
- **Arquitetura Local:** Totalmente implementado para rodar localmente, sem dependências pagas.
- **Flexibilidade e Escalabilidade:** Adaptável a diferentes cenários e demandas.

---

## 🛠️ Tecnologias Utilizadas

- **Infraestrutura:** *Vagrant e Ansible*
- **Servidor de Aplicação:** *Ubuntu e Python*
- **Processamento de Dados:** *Deepseek-r1:8b (OLLAMA)*
- **Outras Ferramentas:** *Vanna e chromaDB*


---

## 🚀 Como Utilizar




1. **Clone o repositório:**

   ```bash
   git clone https://github.com/JohnNeuron/rag-local-model.git
   ```

2. **Instale o Vagrant**

      - [Vagrant Windows](https://developer.hashicorp.com/vagrant/install?product_intent=vagrant#windows)
      - [Vagrant Linux](https://developer.hashicorp.com/vagrant/install?product_intent=vagrant#linux)
      - [Vagrant macOS](https://developer.hashicorp.com/vagrant/install?product_intent=vagrant#darwin)




  
3. **(Opcional) Instale o VirtualBox**
      - [VirtualBox](https://www.virtualbox.org/wiki/Downloads)







4. **Suba as máquinas virtuais**
   
   Após instalar o Vagrant e clonar o repositório, você pode adentrar em cada pasta:

   - app01
   - controlnode
   - db01
   
   E executar esses comandos, pasta por pasta:

   - Para subir a máquina com a configuração do Vagrantfile

   ```bash
   vagrant up            
   ```
   - Para se conectar a máquina via SSH.

    ```bash
    vagrant ssh              
   ```





5. **Instale o ansible para a execução dos playbooks**

   - Instale o ansible na máquina controlnode
       ```bash
       sudo apt install ansible -y
       ```
       
   - Configure o roteamento no /etc/hosts

        ```bash
         sudo nano /etc/hosts 
        ```
        E adicione os endereços ips e seus hostnames:

        ```bash
         192.168.56.3 app01
         192.168.56.4 db01
        ```
        Salve o arquivo (CTRL+X, Y, Enter).
     
   - Reflita no arquivo de inventário do ansible:

        ```bash
        [APPS]
        app01
        [DBS]
        db01
        ```
       Salve o arquivo. (CTRL+X, Y, Enter).


     Agora necessitamos criar uma relação de confiança entre o controlnode e as máquinas virtuais
     que estão sendo gerenciadas, para que possamos realizar chamadas SSH sem a necessidade de senhas.


     No controlnode execute esses passos:

      - Gere a chave SSH

        ```bash
        ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa
        ```
        
      - Verifique a chave

        ```bash
        cat ~/.ssh/id_rsa.pub
        ```


     Copie a chave SSH gerada e jogue no arquivo de provisionamento (provision.sh) do app01 e do db01
      nessa parte comentada, aliás, retire os comentários:

        ![image](https://github.com/user-attachments/assets/a759fc64-f63a-4680-8c90-1daf87f5b241)


     Depois, execute um provisionamento forçado nas duas máquinas:

        ```bash
        vagrant reload --provision 
        ```
     Após isso, teste a configuração executando este comando dentro do controlnode:

        ```bash
        ansible -m ping all
        ```

     Caso a configuração seja bem sucedida deverá aparecer isto na tela:
     
     ![image](https://github.com/user-attachments/assets/41e390b2-2121-4314-94d0-75a74acc100c)

     

     Com tudo configurado podemos finalmente executar os playbooks no controlnode, primeiro devemos
     baixar a role de instalação do mysql no Galaxy:

     ```bash
     ansible-galaxy install geerlingguy.mysql
     ```

     Após isso realizamos a execução dos playbooks:

     ```bash
     ansible-playbook app.yaml 
     ```
     ```bash
     ansible-playbook db.yaml 
     ```

  



     

6.  Configuração do modelo deepseek-r1:8b 

      **OPÇÃO 1 (UTILIZANDO O MODELO NA MESMA MÁQUINA)**
      Primeiramente, instale o OLLAMA:
   
      - [Ollama Windows](https://ollama.com/download/windows)
      - [Ollama Linux](https://ollama.com/download/linux)
      - [Ollama MacOS](https://ollama.com/download/mac)
   
      Após isso, teste a instalação executando na linha de comando:
   
      ```bash
      ollama --version
      ```
   
      Seguidamente, baixe e instale o modelo deepseek-r1:8b:
   
      ```bash
      ollama run deepseek-r1:8b 
      ```
   
      **OPÇÃO 2 (UTILIZANDO O MODELO EM UMA MÁQUINA DIFERENTE)** 
   
      Você deve seguir os mesmos passos anteriores, porém adicione alguns passos posteriores como: 
   
      - Configurar o Ollama para servir em toda a rede local.
   
      ```bash
      setx OLLAMA_HOST "0.0.0.0:11434"
      ```
   
      - Servir o Ollama.
   
      ```bash
      ollama serve 
      ```
      Você pode realizar o teste da configuração dando este comando em qualquer outra linha de 
      comando: 
   
      ```bash
      curl http://ip_da_maquina:11434/ 
      ```
   
      Deverá retornar algo como: 
      
      ![image](https://github.com/user-attachments/assets/c9552698-53c8-41a7-8780-ff1833a10241)

   








7. **(Ollama em outra máquina) Configurar redirecionamento para o modelo na máquina APP01**

     Caso você tenha escolhido utilizar o modelo deepseek-r1:8b em outra máquina, você deverá
     realizar o redirecionamento das requisições internas feitas na porta 11434 para o endereço
     e porta que o seu modelo está escutando.

     Para facilitar deixei toda a parte de configuração no arquivo **provision.sh**  na pasta app01
     você deverá apenas retirar as hashtags(#), salvar e executar esse comando na linha de comando
     estando na pasta:

    

     Depois execute esse comando para forçar o provisionamento:
     ```bash
     vagrant reload --provision 
     ```
   


   Agora que as máquinas virtuais estão configuradas juntamente com o modelo, você deverá realizar os testes 
   de conexões com o seu banco de dados. 







8. **Execução das soluções**

   Na pasta /vagrant/applications da máquina virtual app01 você poderá escolher entre duas soluções:
      
      - modelo_sql: Solução que utiliza a fonte de dados através do banco de dados.
      - modelo_pdf: Solução que utiliza a fonte de dados através de documentos PDF.
  
   Adentre-a e execute o python da respectiva pasta. 🚀


Caso seja necessário, utilize o requirements.txt que está na pasta app01 para realizar a instalação 
das bibliotecas utilizadas.



     

      
   
