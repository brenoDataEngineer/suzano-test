# suzano-test
repository for suzano data engineer test

Para iniciar o desafio, vou quebrar a arquitetura em etapas para poder melhor explicar os desafios e ferramentas e cada etapa...

## Extração

Para extração temos algumas opções:

A melhor delas e mais automática seria extrair os dados diretamente de APIs, contudo o provedor do website não possui APIs liberadas para uso, mesmo investigando pelas ferramentas do desenvolvedor (do navegador) e encontrando o endereço das APIs, a requisição precisa ser autenticada com isso impossibilita de que possamos extrair diretamente da fonte ou da origem que o site usa para estruturar seus dados e sua página.

A segunda opção que temos seria buscar alguma ferramenta externa ou de terceiros, uma biblioteca ou algo do tipo que possa ler as APIs do cliente, ou seja, a API que ele usa no website já fazendo uma requisição autenticada ou alguma biblioteca feita para extrair dados diretamente do website ou dados similares dos mesmos índices econômicos por exemplo. 

Observação: encontrei ao pesquisar uma biblioteca python chamada Investpy e outra chamada Investiny ambas libs são do mesmo desenvolvedor e servem especificamente pra extrair dados diretamente das APIs origem do site investing.com.
Contudo esse serviço parou de funcionar em meados de 2022 pois o site investing.com em um ponto com mudou suas políticas de segurança, criptografia e autenticação das APIs e não permitiu mais acessos públicos com isso ficamos impossibilitados de extrair os dados de forma automática do site

Contudo quando limitamos a consulta dos dados a esse site (investing.com) e percebemos que não podemos fazer nenhum dos desses dois tipos de extração de dados que seria mais automática, temos que chegar numa terceira opção mais complexa.

A terceira opção seria utilizar de bibliotecas do Python que lêem dinamicamente o conteúdo do site e nesse caso simulam cliques e navegações na página pra poder navegar pelo conteúdo e capturar os dados das tabelas e dos gráficos presente dentro do site.

A última maneira mais perto de automática seria utilizando bibliotecas do python como Selenium, que criaria a possibilidade de extrair esses dados como se fosse um usuário indo lá e dando control C control V. Isso funciona bem pra página do indíce da moeda chinesa, mais para as outras páginas não funcionaria muito bem pois lá nós temos calendários e alguns elementos HTML um pouco mais complexos de serem simulados os cliques movimentações e afins. 
E para que nós possamos abrir aquele range de datas do calendário e conseguir extrair o período completo esses movimentos que teriamos que simular, o código ficaria muito complexo e o processo também para realizar a extração.
Então quando fossemos for consultar o site enfrentariamos alguns problemas pra carregar. Um problema por exemplo seriam os os anúncios, o site possui um pop up de um anúncio inscreva-se em nosso portal e esse anúncio ele vai servir geralmente na maioria das vezes pra que usuários se inscrevam no site então não tem como tirar isso e esse anúncio é do bloqueia aas ações do usuário e obriga a interagir com o pop up, o que quebra a execução da rotina do Selenium porque o mesmo abre a página da internet com driver do Google Chrome e imita um usuário mexendo na página só que a gente não consegue prever quando o anúncio vai aparecer, então esse pop up acabaria atrapalhando em diversos momentos.

Fazendo um breve resumo o código para poder extrair os dados da página chinesa tem esse problema do pop up mas não é sempre que acontece, contudo para as outras páginas teria que navegar dentro do Calendário que já é bem mais complexo, o código começa a ficar num nível de complexidade muito grande então essa automação entre aspas começa a se tornar problemática porque eu posso ter um dia que aparece um pop up e trava, eu posso ter um dia que dá um problema ali ele não consegue ler e mesmo mesmo pra navegar nesse calendário é complexo teria que fazer muitas etapas, muitas processos, muitos testes. 
Então é uma implementação de muitas horas e que acaba sendo um hard code, pouco automático que poderia ocasionar erros e necessitaria de muitos testes e possíveis execuções manuais. 

Então iremos partir pra uma solução mais elegante que vai ser utilizar de uma arquitetura completamente automática e orquestrada, contudo vamos utilizar um ponto manual, que seria o download dos dados.
Então vamos pegar os dados por mês considerando o inicio do período passado até o dia de hoje. 
Vamos considerar que nós precisamos desses dados até o dia de hoje, nós teriamos que baixar os dados manualmente todos os dias, o que não é o ideal, mas serviria ao propósito.
Contudo ao baixar os dados manualmente, arquiteturariamos um pipeline que que pudesse fazer essa ingestão de forma automático.

Infelizmente não parece possivel para mim encontrar uma alternativa pra processar mais automático esses dados de forma que a gente consiga consiga automatizar completamente o processo porque o cliente não forneceu APIs e pelo cliente não fornecer APIs impossbilita a extração dos dados de forma automática. 

Para resumir, a nossa solução mais elegante seria automatizar todo processo menos a parte de extração dos dados, não conseguimos por hora automatizar mais do que isso.
Se estivessemos em um cenário da vida real, ambiente produtivo etc, teriamos três opções para trabalhar:

1- Seria buscar alguma outra fonte dos mesmos dados, dos mesmos índices que liberasse uma API ou acesso à alguma base, alguma coisa do tipo para que pudessemos extrair os índices em tempo real.
2- Um site que já mostrasse todos os índices, todos dados histórico, em que usuário não tivesse que ficar interagindo para buscar os dados específicos  
3- A outra opção seria pedir a esse site (investing.com) que liberasse um tokem e o acesso a APIs para que os dados pudessem ser extraidos, pois se precisamos desses dados possívelmente estamos falando de uma corretora de investimentos ou um banco, alguém que precisa desses dados de índice pra tomar decisões na bolsa de valores ou alguma coisa do tipo.

Então provavelmente teriamos que fazer um pedido de uma integração de sistema ou API que já faz esse acesso automático, teria que existir uma colaboração entre os times dos desenvolvedores do site e o nosso sistema. Esse seria o cenário da vida real que não seria extrair os dados na mão, teriamos que tentar automatizar pra poder conectar nas APIs do cliente. 

Não foi citado aqui no desafio por exemplo a volumetria, latência de dados, mas vamos supor que o índice precisasse atualizar por segundo, por exemplo eu precisasse ver o índice da moeda por segundo (eu acredito que não seja o caso), mas se eu precisasse ver por segundo o índice da moeda eu já teria um problema, pois eu teria que ter um usuário entrando e baixando a pasta, planilha (o CSV) a cada segundo e colocando no sistema pra rodar cada segundo, com isso já teriamos um problema, então o caminho certo seria a automação no caso do nosso exemplo que eu acredito não ter como automatizar mais devido aos problemas citados. 

Eu deixei um exemplo de um código com o Selenio, da moeda chinesa que vai ser utilizado só pra vocês entenderem mais ou menos como seria um código desse, então eu estruturei o código para que ele consiga extrair os dados chineses, porque o tipo de página permite, contudo a página dos outros dois índices já é bem mais complexa e precisa navegar dentro de um calendário como comentado... Com isso acabamos ficando bloqueados ali de fazer essas extraçoes.

## Transformação e Carga dos Dados

Agora seguimos para a parte de transformação e carga dos dados. 

Irei apresentar três arquiteturas de referência para o restante nosso cenário, que são elas: Streaming, Batch e Near Real Time.
Contudo, podemos entender rapidamente que o cenário proposto não se trata de um cenário Streaming, mas de qualquer maneira fica o desenho e arquitetura de referência.

### Cenário 01 - Streaming de dados

O cenário aborda uma possível troca de fonte de csv (exportado manualmente) para um serviço de mensageria, ilustrado com o kafka.
Com isso nos habilita a pensar em um cenário onde consumimos os dados do tópico (que dentro do pub sub podemos usar por exemplo deadletters para reter mensagens não processadas) e processamos via Dataflow, cascateando em uma latência baixa para tabelas Streaming do BigQuery e usando terraform para orquestrar a infraestrutura.

<img width="1111" alt="image" src="https://github.com/user-attachments/assets/1af3f24d-5010-49db-8650-0ad1124b2e50">


### Cenário 02 - Batch

O cenário traz uma abordagem mais próxima da realidade do nosso exemplo, que com certeza seria uma boa escolha para processar os dados históricos.
Trazemos como orquestrador o Composer (Apache Airflow) e o mesmo sendo responsável por rodar a dag em um momento do dia (d-1) para processar os dados históricos que vai extrair do Google Cloud Storage para dentro do seu código e em seguida inserir no BigQuery.
(Podemos também inverter a ordem, onde o dataproc extrai os dados da origem para o Google Cloud Storage e usariamos um template do Airflow para criar um job de inserção no BigQuery diretamente do Google Cloud Storage)

<img width="1103" alt="image" src="https://github.com/user-attachments/assets/ce096d7c-7393-4d03-b145-53864916884d">


### Cenário 03 - Near Real Time (Que iremos executar)

O cenário traz como objetivo a criação de um microserviço (API) com uma rota de processamento que faz a ingestão dos dados em toda as tabelas.
Onde temos o Cloud Scheduler como responsável por engatilhar a execução da rota sempre que o horário estipulado chegar.
Ele envia um payload para a respectiva rota daquele serviço contendo os parametros necessários para a requisição.
Com isso a rota executa seu processamento, que lê os dados do bucket do Cloud Storage e insere na tabela do BigQuery.

<img width="1106" alt="image" src="https://github.com/user-attachments/assets/23267888-938e-44f2-8ee6-801da3ece597">


## Dados do cenário realizado (infos do gcp)

BigQuery: https://console.cloud.google.com/bigquery?referrer=search&project=suzano-poc&ws=!1m4!1m3!3m2!1ssuzano-poc!2sfinancial_data

Storage: https://console.cloud.google.com/storage/browser/suzano-financial-data?pageState=(%22StorageObjectListTable%22:(%22f%22:%22%255B%255D%22))&project=suzano-poc

Cloud Run: https://console.cloud.google.com/run/detail/us-central1/financial-api/metrics?project=suzano-poc

Cloud Build: https://console.cloud.google.com/cloud-build/builds?referrer=search&project=suzano-poc

Cloud Scheduler: https://console.cloud.google.com/cloudscheduler?project=suzano-poc

## Como testar?

Temos duas opções para testar o serviço:

### Localmente:

Collection postman com os bodys de requisição para as três tabelas:
[suzano.postman_collection.json](https://github.com/user-attachments/files/17392889/suzano.postman_collection.json)

Basta copiar a collection e executar as requisições, pode acompanhar pelo link do ambiente que deixei acima para ver a mágica acontecer.

### Via Cloud Scheduler:

Pode ser rodado via Cloud Scheduler (recurso também disponibilizado acima): https://console.cloud.google.com/cloudscheduler?project=suzano-poc

usd-cny: Roda a requisição para a tabela usd-cny.

chinese-caixin: Roda a requisição para a tabela chinese-caixin.

bcom: Roda a requisição para a tabela bcom.

*INFOS:
Endpoint Cloud Run (aberto para internet): https://financial-api-266949854628.us-central1.run.app 

Rota cloud Run: POST: /load-data

Caso queira clonar, fazer alguma alteração e rodar o cloud build, basta abrir seu terminal na pasta raiz de onde clonou o repositório e rodar: 'gcloud builds submit --config cloudbuild.yaml .'

Automaticamente o comando identifica nosso yaml e começa a subida (PS: rodar sem aspas).

# Conclusão:
Para finalizar, temos os dados extraidos e carregados na origem, a arquitetura poderia evoluir para inlcuir particinamento nas tabelas, modelagens específicas etc, contudo o desafio propôs apenas o que apresentamos...

Estou liberando o acesso do projeto do gcp para o MANUELD@suzano.com.br poder validar diretamente o que está por lá.
O código está no repositório onde vocês lêem esse arquivo.

Fico a disposição para quaisquer dúvidas posteriores.



# EXTRA

Para matar a curiosidade do sample do código com Selenium que comentei acima, vou colocar embaixo o código e como rodar...

(PS: sei que não valia sqlite, mas como é só um exemplo e não está atrelado de maneira alguma a solução do desafio original, da um desconto ;) )

## Chinese Seleniu exemplo

```
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
import sqlite3
import time

service = Service('./chromedriver') 
driver = webdriver.Chrome(service=service)

url = 'https://br.investing.com/economic-calendar/chinese-caixin-services-pmi-596'
driver.get(url)

WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, 'showMoreHistory596')))

actions = ActionChains(driver)

while True:
    try:
        button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, 'showMoreHistory596')))
        
        actions.move_to_element(button).perform()
        
        button.click()
        
        time.sleep(5) 
        
    except (NoSuchElementException, TimeoutException):
        print("No more 'Show More' button found or it's not clickable. Exiting loop.")
        break

soup = BeautifulSoup(driver.page_source, 'html.parser')

data_table = soup.find('table', {'class': 'genTbl openTbl ecHistoryTbl'})

conn = sqlite3.connect('economic_data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS economic_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        value TEXT,
        additional_info TEXT
    )
''')

if data_table:
    rows = data_table.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 3:
            date = cells[0].text.strip()
            value = cells[1].text.strip()
            additional_info = cells[2].text.strip() 
            
            cursor.execute('''
                INSERT INTO economic_data (date, value, additional_info) VALUES (?, ?, ?)
            ''', (date, value, additional_info))

conn.commit()
conn.close()
print("Data stored in the SQLite database.")

driver.quit()
```

### Etapas:

1- Salve o arquivo como chinese.py (ou outro nome...)

2- Baixe o seu chromedriver respectivo (driver sua versão de navegador/tipo de navegador)

3- Disponibilize o chromedriver.exe (no meu caso uso o Google Chrome) na pasta raiz de onde decidir criar o arquivo chinese.py

4- Execute python3 chinese.py e veja a mágica acontecer...

Obs: Ele vai abrir seu navegador no site, e simular movimentos de um usuário para que possa ser mostrada na tela (dentro das tags html de tabela) todo o conteúdo de dados históricos, onde ele captura com o próprio código os dados presentes dentro dessas tags de tabela e salva eles na sqlite...

5- Depois que rodar completo, só mandar um SELECT * no banco para ver seus resultados (vide exemplo python abaixo)

```
import sqlite3

conn = sqlite3.connect('economic_data.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM economic_data')

rows = cursor.fetchall()

for row in rows:
    print(f"ID: {row[0]}, Date: {row[1]}, Value: {row[2]}, Additional Info: {row[3]}")

conn.close()
```

_______________


Breno Carlo Piccoli - Engenheiro de dados Senior GCP.








