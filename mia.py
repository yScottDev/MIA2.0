from time import sleep
import importlib
import os
from os import system
from os import name, system
system('cls' if name == 'nt' else 'clear')
print("carregando...")

#codigo pra verificar se o usario tem as depdencias necessarias pra instalar o programa
dependencies = [
    "csv",
    "datetime",
    "os",
    "gtts",
    "pywebostv",
    "requests",
    "openai",
    "functools",
    "fuzzywuzzy",
    "playsound",
    "speech_recognition",
    "nltk"
]

missing_dependencies = []

for dependency in dependencies:
    try:
        importlib.import_module(dependency)
    except ImportError:
        missing_dependencies.append(dependency)

if missing_dependencies:
    print("As seguintes dependências estão ausentes:")
    for dependency in missing_dependencies:
        print(dependency)

    choice = input("Deseja instalar as dependências ausentes? (s/n): ")

    if choice.lower() == "s":
        try:
            import pip
            pip.main(["install", "--upgrade"] + missing_dependencies)
            print("As dependências foram instaladas com sucesso.")
        except Exception as e:
            print("Ocorreu um erro durante a instalação das dependências:", e)
            exit(1)
    else:
        print("O programa será encerrado.")
        exit(0)


import csv
import datetime
from gtts import gTTS
from pywebostv.discovery import *
from pywebostv.connection import *
from pywebostv.controls import *
import requests
import openai
from functools import lru_cache
from fuzzywuzzy import fuzz
import re
from playsound import playsound
import speech_recognition as sr
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.classify import NaiveBayesClassifier

ps = PorterStemmer()
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
system('cls' if name == 'nt' else 'clear')
print('Você tem todas as bibliotecas instaladas e pode rodar este código. direcionando à pagina inicial.')
sleep(5)
system('cls' if name == 'nt' else 'clear')
responses = {}
@lru_cache(maxsize=100)


def preprocess(sentence):
    sentence = sentence.lower()
    words = word_tokenize(sentence)
    words = [w for w in words if not w in stop_words and w.isalpha()]
    return words


def fl(msg):
    obj = gTTS(text=msg, lang='pt-br', slow=False)

    # Salva o arquivo de áudio
    obj.save("audio.mp3")

    # Reproduz o arquivo de áudio usando o playsound
    playsound("audio.mp3")

    #deleta o audio
    system('del audio.mp3')

def rec():
    # Crie um objeto de reconhecimento de fala
    r = sr.Recognizer()

    # Use o microfone como fonte de entrada de áudio
    with sr.Microphone() as source:
        print("Diga algo!")
        # Ajuste o ruído de fundo
        r.adjust_for_ambient_noise(source)
        # Escute o que o usuário diz
        audio = r.listen(source)

    # Tente reconhecer a fala usando o Google Speech Recognition
    try:
        fala = r.recognize_google(audio, language='pt-BR')
        return fala
    except sr.UnknownValueError:
        print("Não entendi o que você disse")
    except sr.RequestError as e:
        print("Erro ao tentar reconhecer a fala; {0}".format(e))




def generate_response(prompt):
        if prompt in responses:
            return responses[prompt]
        else:
            completions = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=2048,
            n=1,
            stop=None,
            temperature=0.7
             )
            message = completions.choices[0].text
            responses[prompt] = message.strip()
            return message.strip()



def preprocess_text(text):
    tokens = word_tokenize(text.lower()) # tokenização e conversão para minúsculas
    stems = [ps.stem(token) for token in tokens] # aplicação de stemização de Porter
    return stems

def match_command(prompt):
    max_ratio = 0.7
    best_match = None
    prompt_stems = preprocess_text(prompt)
    for command, func in commands.items():
        for cmd in command:
            cmd_stems = preprocess_text(cmd)
            ratio = fuzz.token_set_ratio(prompt_stems, cmd_stems)
            if ratio > max_ratio:
                max_ratio = ratio
                best_match = func
    return best_match


def hrs():
    hr = str(time.ctime()[11:20])
    fl(f'Mia: São {hr}')


def vlm():
    padrao = re.compile(r'\d+')
    lol = padrao.search(prompt)

    if lol:
        numero = int(lol.group())
        media.set_volume(numero)
        fl(f'volume da tv alterado para {numero}.')
    else:
        fl("Desculpe, não consegui encontrar um número no seu comando.")

# função para cadastrar um novo usuário
def cadastrar_usuario(nome, senha, cidade, key_api_tempo, key_api_openai, endereco_ip):
    with open('usuarios.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([nome, senha, cidade, key_api_tempo, key_api_openai, endereco_ip])
        
# função para verificar se o usuário já está cadastrado
def verificar_usuario(nome, senha):
    with open('usuarios.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == nome and row[1] == senha:
                return True
        return False


# função para atualizar as informações de um usuário
def atualizar_usuario(nome_antigo, senha_antiga, novo_nome=None, nova_senha=None, nova_cidade=None, nova_key_api_tempo=None, nova_key_api_openai=None, novo_endereco_ip=None):
    # abre o arquivo 'usuarios.csv' para leitura e escrita
    with open('usuarios.csv', 'r+', newline='') as csvfile:
        reader = csv.reader(csvfile)
        writer = csv.writer(csvfile)
        linhas = []
        atualizado = False
        # lê as linhas do arquivo e armazena em uma lista
        for row in reader:
            if row[0] == nome_antigo and row[1] == senha_antiga:
                # atualiza as informações do usuário se os novos valores forem diferentes dos antigos
                if novo_nome:
                    row[0] = novo_nome
                if nova_senha:
                    row[1] = nova_senha
                if nova_cidade:
                    row[2] = nova_cidade
                if nova_key_api_tempo:
                    row[3] = nova_key_api_tempo
                if nova_key_api_openai:
                    row[4] = nova_key_api_openai
                if novo_endereco_ip:
                    row[5] = novo_endereco_ip
                atualizado = True
            linhas.append(row)
        # reescreve o arquivo com as novas informações
        if atualizado:
            csvfile.seek(0)
            writer.writerows(linhas)
            csvfile.truncate()
        return atualizado


def atua_user(nome,senha):
    nome = nome
    senha = senha
    
    with open('usuarios.csv', 'r', newline='') as arquivo:
        leitor = csv.reader(arquivo)
        for row in leitor:
            if row[0] == nome and row[1] == senha:
                nome_usuario = row[0]
                senha_usuario = row[1]
                cidade_usuario = row[2]
                key_api_tempo_usuario = row[3]
                key_api_openai_usuario = row[4]
                endereco_ip_usuario = row[5]
                return nome_usuario, senha_usuario, cidade_usuario, key_api_tempo_usuario, key_api_openai_usuario, endereco_ip_usuario
        else:
            print("Usuário ou senha inválidos.")


def head_user():
    while True:
        nome = input("Digite seu nome: ")
        senha = input("Digite sua senha: ")
        
        with open('usuarios.csv', 'r', newline='') as arquivo:
            leitor = csv.reader(arquivo)
            for row in leitor:
                if row[0] == nome and row[1] == senha:
                    nome_usuario = row[0]
                    senha_usuario = row[1]
                    cidade_usuario = row[2]
                    key_api_tempo_usuario = row[3]
                    key_api_openai_usuario = row[4]
                    endereco_ip_usuario = row[5]
                    return nome_usuario, senha_usuario, cidade_usuario, key_api_tempo_usuario, key_api_openai_usuario, endereco_ip_usuario
            else:
                print("Usuário ou senha inválidos.")
                continue

system('cls' if name == 'nt' else 'clear')
while True:
    tt=input('deseja fazer um tutorial de como as coisas funcionam?(s/n): ')
    if tt.lower()=='s':
        print('''
MIA é uma inteligência artificial simples que está sendo projetada a fim de ajudar pessoas no dia a dia.
Mia pode fazer muitas coisas, desde se comunicar usando a api da openai a controlar sua Smart TV LG.
Mia é um projeto inicialmente simples, uma simulação do que pode ser uma inteligencia artificial feita em python.
você cadastra sua conta, e nela você precisará fornecer algumas informações necessarias para que o programa rode.
primeiramente, na tela de cadastro, você fornecerá:
- Seu usuário
- Sua senha
depois, você terá que fornecer algumas chaves de api que será preciso construir nestes sites:

API DE CLIMA: 
Acesse o site oficial do OpenWeatherMap em https://openweathermap.org/.

Clique em "Sign Up" (Registrar-se) no canto superior direito para criar uma nova conta. Se você já tiver uma conta, faça login.

Preencha o formulário de registro com seu endereço de e-mail, nome de usuário e senha. Você também pode optar por fazer login usando sua conta do Google, GitHub ou outras opções disponíveis.

Após o registro, faça login em sua conta OpenWeatherMap.

No painel de controle, clique em "API Keys" (Chaves de API) no menu à esquerda.

Em "Create Key" (Criar chave), forneça um nome para a chave de API no campo "Name" (Nome). Por exemplo, você pode usar "Minha Chave de API".

Selecione o tipo de plano gratuito.

Clique em "Generate" (Gerar) para criar sua chave de API.

A chave de API será gerada e exibida na tela. Copie essa chave e salve-a em um local seguro, pois você precisará dela para fazer solicitações à API do OpenWeatherMap.

API DA OPENAI:
 
Acesse o site da OpenAI em https://www.openai.com/.

No menu principal, clique em "Sign In" (entrar) para fazer login na sua conta OpenAI. Se você ainda não tiver uma conta, clique em "Sign Up" (inscrever-se) para criar uma.

Após fazer login, clique no seu nome de usuário no canto superior direito e selecione "API Keys" (chaves de API) no menu suspenso.

Na página de chaves de API, clique no botão "New Key" (nova chave).

Será exibido um formulário para criar uma nova chave de API. dê um nome à sua api e faça sua chave

Após selecionar os recursos desejados, clique em "Create" (criar) para gerar a chave de API.

Após a criação da chave, você verá um código alfanumérico. esse é o seu código de api, anote.

___________________________________________________________________________

Além disso, você também pode usar a Mia para controlar sua Smart TV LG. você será perguntado na aba de cadastro e se sim, você precisará ter em mãos o ip da sua tv, que pode ser conseguido fácilmente entrando nas configurações avançadas de rede.

LEMBRANDO:
isso é só uma leve simulação do que poderia ser uma idéia de projeto atualizado futuro da MIA. esse não é o projeto oficial, nem muito menos deve ser levado em conta. ainda existem diversos bugs, mas estou trabalhando pra resolvê-los.

divirta-se.
''')
        input('mande qualquer coisa pra continuar: ')
        break
    else:
        print('ok.')
        break


while True:
    print('''
1 - microfone
2 - por escrito
''')
    crt=int(input('deseja usar a versão com microfone ou a versão por texto?: '))
    if crt > 2 or crt <= 0:
        print('Apenas 1 e 2 são aceitos. verfique seu comando.')
        sleep(3)
        system('cls' if name == 'nt' else 'clear')
        continue
    else:
        break
system('cls' if name == 'nt' else 'clear')
print('certo, espere um pouco.')

# exemplo de uso das funções
while True:
    system('cls' if name == 'nt' else 'clear')
    login=int(input('''
deseja logar, ou cadastrar um usuario?
cadastrar - 1
login - 2
escolha: '''))
    if login == 1:
        Nick=input('Nick: ')
        Senha=input('Senha: ')
        Cidade=input('Cidade: ')
        key_clima=input('Key de Clima: ')
        key_openai=input('Key de openai: ')
        ipdatv=input('''
neste código, há um serviço de controle que controla a sua tv LG por comandos. gostaria de usá-lo?(s/n): ''')
        if ipdatv=='s':
            ip_tv=input('digite o ip da sua tv: ')
        else:
            ip_tv='não_cadastrado'
        cadastrar_usuario(Nick, Senha, Cidade, key_clima, key_openai, ip_tv)
        continue
    if login == 2:
        nome, senha, cidade, key_api_tempo, key_api_openai, endereco_ip = head_user()
        print(f'Olá, {nome}! o login foi efetuado com sucesso, um segundo..')
        API_KEY = key_api_tempo
        openai.api_key = key_api_openai
        link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&lang=pt_br"
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()
        descricao = requisicao_dic['weather'][0]['description']
        temperatura = requisicao_dic['main']['temp'] - 273.15
        break


tvss=0
if endereco_ip != 'não_cadastrado':
    TV_CODE_FILE = "tv_code.txt"

    # Check if TV code file exists
    if os.path.exists(TV_CODE_FILE):
        # Read TV code from file
        with open(TV_CODE_FILE, "r") as f:
            tv_code = f.read().strip()
        
        print(tv_code)
        # Create client and connect to TV
        store={'client_key': tv_code}
        client = WebOSClient(endereco_ip)
        client.connect()
        for status in client.register(store):
            if status == WebOSClient.PROMPTED:
                print("Porfavor, aceite a conexão na tv!")
            elif status == WebOSClient.REGISTERED:
                print('Estou conectada na sua tv')

        system1 = SystemControl(client)
        system1.notify("Olá, sou a Mia. Estou conectada na sua TV.")
        app =ApplicationControl(client)
        apps = app.list_apps()
        media = MediaControl(client)
    else:
        # Create client and discover TV
        client = WebOSClient.discover()[0]
        client.connect()

        # Register client with TV and save code to file
        store = {}
        for status in client.register(store):
            if status == WebOSClient.PROMPTED:
                print("aceite a conexão na tv.")
            elif status == WebOSClient.REGISTERED:
                tv_code = store["client_key"]
                store={'client_key': tv_code}
                with open(TV_CODE_FILE, "w") as f:
                    f.write(tv_code)
                print("TV connected and code saved to file!")
else:
    tvss=1

comandos = [
    'Ligar a TV.',
    'Desligar o ar-condicionado.',
    'Ligar as luzes da sala.',
    'Fechar as cortinas.',
    'Ligar o aspirador de pó.',
    'Aumentar o volume.',
    'Diminuir o volume.',
    'Ligar a cafeteira.',
    'Desligar a cafeteira.',
    'Ligar o ventilador.',
    'Desligar o ventilador.',
    'Ligar o aquecedor.',
    'Desligar o aquecedor.',
    'Ligar a máquina de lavar.',
    'Desligar a máquina de lavar.',
    'Ligar o secador de cabelo.',
    'Desligar o secador de cabelo.',
    'Ligar o forno.',
    'Desligar o forno.',
    'Ligar a chaleira elétrica.',
    'Desligar a chaleira elétrica.',
    'Ligar o microondas.',
    'Desligar o microondas.',
    'Ligar o ar-condicionado.',
    'Abrir a porta da garagem.',
    'Fechar a porta da garagem.',
    'Ligar a câmera de segurança.',
    'Desligar a câmera de segurança.',
    'Ligar o alarme.',
    'Desligar o alarme.',
    'como está o clima',
    'como está o tempo',
    'que dia é hoje',
    'que horas são',
    'abra o youtube',
    'abra a netflix',
    'abra o spotify',
    'mia desligue a tv',
    'mia abra o youtube na tv',
    'mia abrir spotify na tv',
    'mia abra netflix na tv',
    'mia como está o tempo',
    'mia, volume da tv em 50',
    'mia, que horas são?',
    'mia, que dia é hoje?',
    'Aumentar o volume da TV.',
    'Abrir o YouTube.',
    'Abrir a Netflix na TV.',
    'Mostrar as horas.',
    'Mostrar a data.',
    'Que horas são?',
    'Que horas são agora?',
    'mia, que horas são?',
    "Ligar a TV",
    "Desligar a TV",
    "Aumentar o volume da TV",
    "Diminuir o volume da TV",
    "Trocar para o canal 5",
    "Próximo canal",
    "Canal anterior",
    "Mostrar a previsão do tempo",
    "Qual é a temperatura atual?",
    "Como estará o clima amanhã?",
    "Mostrar a hora atual",
    "Mostrar a data atual",
    "Ler minhas mensagens",
    "Enviar uma mensagem para [contato]",
    "Ligar para [contato]",
    "Enviar um e-mail para [contato]",
    "Criar um lembrete para [data/hora]",
    "Mostrar meus compromissos para hoje",
    "Tocar música",
    "Parar a música",
    "Próxima música",
    "Música anterior",
    "Pesquisar na web por [termo de busca]",
    "Abrir o navegador",
    "Fechar o navegador",
    "Abrir o aplicativo [nome do aplicativo]",
    "Definir um alarme para [hora]",
    "Criar uma nota",
    "Ler minhas notas",
    "Traduzir [texto] para [idioma]",
    "Contar até 10"]

perguntas = [
    'Quem foi o primeiro homem a pisar na lua?',
    'Quantos planetas existem no sistema solar?',
    'Qual é a capital da França?',
    'Qual é o maior país do mundo?',
    'Quando começou a Primeira Guerra Mundial?',
    'Qual é o nome do presidente do Brasil?',
    'Quem é a atual rainha da Inglaterra?',
    'Qual é o autor de "O Pequeno Príncipe"?',
    'Qual é o nome do cientista que descobriu a lei da gravidade?',
    'Quem pintou a obra "A Última Ceia"?',
    'Qual é o nome do pintor que criou a obra "O Grito"?',
    'Qual é a maior cachoeira do mundo?',
    'Qual é o nome da maior floresta tropical do mundo?',
    'Qual é o nome do autor de "Dom Quixote"?',
    'Qual é o nome do inventor do telefone?',
    'Qual é o nome do fundador da Microsoft?',
    'Qual é o nome do fundador da Apple?',
    'Qual é o nome do fundador da Amazon?',
    'Qual é o nome do inventor da lâmpada?',
    'Qual é o nome do cientista que criou a teoria da relatividade?',
    'Qual é o nome do compositor de "A Flauta Mágica"?',
    'Qual é o nome do criador da famosa escultura "O Pensador"?',
    'Qual é o nome da atriz que interpretou Hermione na saga Harry Potter?',
    'Qual é o nome do autor de "A Divina Comédia"?',
    'Qual é o nome do fundador do Facebook?',
    'Qual é o nome do explorador português que descobriu o caminho marítimo para as Índias?',
    'Qual é o nome do famoso matemático grego conhecido como "O Pai da Geometria"?',
    'Qual é o nome do criador da obra "Guernica"?',
    'Qual é o nome do fundador da Tesla?']

comandos = [preprocess(sentence) for sentence in comandos]
perguntas = [preprocess(sentence) for sentence in perguntas]

training_data = comandos[:2] + perguntas[:2]
test_data = comandos[2:] + perguntas[2:]

def create_word_features(words):
    my_dict = dict([(word, True) for word in words])
    return my_dict

training_features = [(create_word_features(sentence), 'comando') for sentence in training_data[:2]] \
                   + [(create_word_features(sentence), 'pergunta') for sentence in training_data[2:]]

classifier = NaiveBayesClassifier.train(training_features)

def predict(sentence):
    words = preprocess(sentence)
    features = create_word_features(words)
    return classifier.classify(features)

if tvss==0:
    commands = {
        ('mia desligue a tv', 'desliga a tv', 'desligue a tv', 'mia desligue a tv'): system1.power_off,
        ('mia abra o youtube na tv', 'abrir youtube na tv', 'mia abrir youtube na tv', 'abra o youtube na tv', 'mia youtube'): lambda: app.launch([x for x in apps if "youtube" in x["title"].lower()][0]),
        ('mia abrir spotify na tv', 'mia abra o spotify na tv', 'mia Spotify'): lambda: app.launch([x for x in apps if "spotify - músicas e podcasts" in x["title"].lower()][0]),
        ('mia abra netflix na tv', 'abra a netflix na tv', 'mia abra a netflix na tv', 'mia abrir netflix na tv', 'mia Netflix'): lambda: app.launch([x for x in apps if "netflix" in x["title"].lower()][0]),
        ('mia como está o tempo', 'mia como está o clima', 'e como está o clima'): lambda: fl(f'Mia: {descricao}, {temperatura}'),
    ('mia, volume da tv em 50', 'mia, quero o volume da tv em 15', 'mia, coloque o volume da tv em 30', 'quero o volume ds tv', 'volume da tv'): vlm,
    ('mia, que horas são?', 'que horas são agora', 'que horas?'): lambda: fl(f'são {datetime.datetime.now()}'),
    ('mia, que dia é hoje?', 'que dia é hoje?','que dia?', 'dia', 'que data é hoje?', 'que data é hoje, mia?'): lambda: fl(f'são {datetime.datetime.now().date()}')
    }
else:
    commands = {
    ('mia como está o tempo', 'mia como está o clima', 'e como está o clima'): lambda: fl(f'Mia: {descricao}, {temperatura}'),
   ('mia, volume da tv em 50', 'mia, quero o volume da tvS em 15', 'mia, coloque o volume da tv em 30', 'quero o volume ds tv', 'volume da tv'): vlm,
   ('mia, que horas são?', 'que horas são agora', 'que horas?'): lambda: fl(f'são {datetime.datetime.now()}'),
   ('mia, que dia é hoje?', 'que dia é hoje?','que dia?', 'dia', 'que data é hoje?', 'que data é hoje, mia?'): lambda: fl(f'são {datetime.datetime.now().date()}')
}

print('Pronto.')
time.sleep(1)
system('cls' if name == 'nt' else 'clear')
print('funções definidas, iniciando..')
sleep(0.5)
while True:
    system('cls' if name == 'nt' else 'clear')
    try:
        if crt == 1:
            print(f'''
Bem-vindo, {nome}
para acessar ou mudar as informações da conta, diga "configurações".
''')
            fl1 = rec()
            prompt = str(fl1)
            prompt=prompt.lower()
            if prompt == 'configurações':
                print(f'''
Você está na aba de configurações da sua conta.
Seus dados são:
1 - Nick: {nome}
2 - Senha: {senha}
3 - Cidade: {cidade}
4 - Key de API do Tempo: {key_api_tempo}
5 - Key de API da OpenAI: {key_api_openai}
6 - Endereço IP da TV (se estiver cadastrado): {endereco_ip}
7 - Sair
''')

                opcao = int(input('Escolha uma das opções: '))

                if opcao == 1:
                    novo_nome = input("Novo nome: ")
                    atualizar_usuario(nome, senha, novo_nome=novo_nome)
                    nome, senha, cidade, key_api_tempo, key_api_openai, endereco_ip = atua_user(novo_nome,senha)
                    continue
                elif opcao == 2:
                    nova_senha = input("Nova senha: ")
                    atualizar_usuario(nome, senha, nova_senha=nova_senha)
                    nome, senha, cidade, key_api_tempo, key_api_openai, endereco_ip = atua_user(nome,nova_senha)
                    continue
                elif opcao == 3:
                    nova_cidade = input("Nova cidade: ")
                    atualizar_usuario(nome, senha, nova_cidade=nova_cidade)
                    nome, senha, cidade, key_api_tempo, key_api_openai, endereco_ip = atua_user(nome,senha)
                    continue
                elif opcao == 4:
                    nova_key_api_tempo = input("Nova Key de API do Tempo: ")
                    atualizar_usuario(nome, senha, nova_key_api_tempo=nova_key_api_tempo)
                    nome, senha, cidade, key_api_tempo, key_api_openai, endereco_ip = atua_user(nome,senha)
                    continue
                elif opcao == 5:
                    nova_key_api_openai = input("Nova Key de API da OpenAI: ")
                    atualizar_usuario(nome, senha, nova_key_api_openai=nova_key_api_openai)
                    nome, senha, cidade, key_api_tempo, key_api_openai, endereco_ip = atua_user(nome,senha)
                    continue
                elif opcao == 6:
                    novo_endereco_ip = input("Novo endereço IP da TV: ")
                    atualizar_usuario(nome, senha, novo_endereco_ip=novo_endereco_ip)
                    nome, senha, cidade, key_api_tempo, key_api_openai, endereco_ip = atua_user(nome,senha)
                    continue
                elif opcao == 7:
                    # Sair do programa ou executar outra ação
                    continue
                else:
                    print("Opção inválida.")
                    continue

        else:
            print(f'''
Bem-vindo, {nome}
para acessar ou mudar as informações da conta, digite "config".
''')
            prompt=input('digite um comando: ')
            prompt=prompt.lower()
            if prompt == 'config':
                print(f'''
Você está na aba de configurações da sua conta.
Seus dados são:
1 - Nick: {nome}
2 - Senha: {senha}
3 - Cidade: {cidade}
4 - Key de API do Tempo: {key_api_tempo}
5 - Key de API da OpenAI: {key_api_openai}
6 - Endereço IP da TV (se estiver cadastrado): {endereco_ip}
7 - Sair
''')

                opcao = int(input('Escolha uma das opções: '))

                if opcao == 1:
                    novo_nome = input("Novo nome: ")
                    atualizar_usuario(nome, senha, novo_nome=novo_nome)
                    nome, senha, cidade, key_api_tempo, key_api_openai, endereco_ip = atua_user(novo_nome,senha)
                    continue
                elif opcao == 2:
                    nova_senha = input("Nova senha: ")
                    atualizar_usuario(nome, senha, nova_senha=nova_senha)
                    nome, senha, cidade, key_api_tempo, key_api_openai, endereco_ip = atua_user(nome,nova_senha)
                    continue
                elif opcao == 3:
                    nova_cidade = input("Nova cidade: ")
                    atualizar_usuario(nome, senha, nova_cidade=nova_cidade)
                    nome, senha, cidade, key_api_tempo, key_api_openai, endereco_ip = atua_user(nome,senha)
                    continue
                elif opcao == 4:
                    nova_key_api_tempo = input("Nova Key de API do Tempo: ")
                    atualizar_usuario(nome, senha, nova_key_api_tempo=nova_key_api_tempo)
                    nome, senha, cidade, key_api_tempo, key_api_openai, endereco_ip = atua_user(nome,senha)
                    continue
                elif opcao == 5:
                    nova_key_api_openai = input("Nova Key de API da OpenAI: ")
                    atualizar_usuario(nome, senha, nova_key_api_openai=nova_key_api_openai)
                    nome, senha, cidade, key_api_tempo, key_api_openai, endereco_ip = atua_user(nome,senha)
                    continue
                elif opcao == 6:
                    novo_endereco_ip = input("Novo endereço IP da TV: ")
                    atualizar_usuario(nome, senha, novo_endereco_ip=novo_endereco_ip)
                    nome, senha, cidade, key_api_tempo, key_api_openai, endereco_ip = atua_user(nome,senha)
                    continue
                elif opcao == 7:
                    # Sair do programa ou executar outra ação
                    continue               
        if 'none' in prompt:
            fl('não entendi, poderia repetir?')
        print(f'você disse: {prompt}')
        result = predict(prompt)
        if result == 'comando' or 'horas' in prompt or 'clima' in prompt or 'tempo' in prompt:
            print('isso foi um comando.')
            match = match_command(prompt)
            if match:
                try:
                    match()
                except NameError:
                    print('''
Sua conta não tem essa disponibilidade, para alterar sua conta, entre em configurações.
voltando a aba inicial.''')
                    sleep(6.5)
        else:
            print('pergunta')
            response = generate_response(prompt)
            fl(f'Mia: {response}')
            continue
        if prompt == 'Mia' or prompt == 'mia?':
            fl('Olá, estou aqui! em que posso ajudar?')
            continue
    except KeyboardInterrupt:
        print('''                                                                                                                             
saindo.
''')
        exit()