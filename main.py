import csv
import time
from prettytable import PrettyTable

# Estrutura Hash para Jogadores
class TabelaHashJogadores:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.tabela = [None] * tamanho

    def funcao_hash(self, chave):
        return hash(chave) % self.tamanho

    def inserir(self, chave, valor):
        indice = self.funcao_hash(chave)
        if self.tabela[indice] is None:
            self.tabela[indice] = [Nodo(chave, valor)]
        else:
            self.tabela[indice].append(Nodo(chave, valor))

    def buscar(self, chave):
        indice = self.funcao_hash(chave)
        lista_encadeada = self.tabela[indice]
        if lista_encadeada is not None:
            for nodo in lista_encadeada:
                if nodo.chave == chave:
                    return nodo.valor
        return None

    def obter_informacoes_do_jogador(self, sofifa_id):
        jogador = self.buscar(sofifa_id)
        if jogador is not None:
            return jogador
        else:
            print(f"Jogador com sofifa_id {sofifa_id} não encontrado.")
            return None

# Estrutura TRIE para Nomes Longos
class TrieNode:
    def __init__(self, char):
        self.char = char
        self.is_end = False
        self.children = {}
        self.id = None

class Trie:
    def __init__(self):
        self.root = TrieNode("")

    def inserir(self, item):
        node = self.root
        word = item.long_name.lower()
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode(char)
            node = node.children[char]
        node.is_end = True
        node.id = item.sofifa_id

    def busca(self, prefixo):
        node = self.root
        ids = []
        for char in prefixo.lower():
            if char in node.children:
                node = node.children[char]
            else:
                return ids
        self.busca_profundidade(node, prefixo.lower(), ids)
        return ids

    def busca_profundidade(self, node, prefix, ids):
        if node.is_end:
            ids.append(node.id)
        for char, child in node.children.items():
            self.busca_profundidade(child, prefix + char, ids)

# Estrutura Hash para Avaliações
class TabelaHashAvaliacoes:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.tabela = [None] * tamanho

    def funcao_hash(self, chave):
        return hash(chave) % self.tamanho

    def inserir(self, chave, valor):
        indice = self.funcao_hash(chave)
        if self.tabela[indice] is None:
            self.tabela[indice] = [Nodo(chave, valor)]
        else:
            for nodo in self.tabela[indice]:
                if nodo.chave == chave:
                    nodo.valor = valor
                    return
            self.tabela[indice].append(Nodo(chave, valor))

    def buscar(self, chave):
        indice = self.funcao_hash(chave)
        lista_encadeada = self.tabela[indice]
        if lista_encadeada is not None:
            for nodo in lista_encadeada:
                if nodo.chave == chave:
                    return nodo.valor
        return None

# Estrutura Hash para Tags
class TrieNodeTags:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.sofifa_ids = set()

class TrieTags:
    def __init__(self):
        self.root = TrieNodeTags()

    def inserir(self, sofifa_id, tag):
        node = self.root
        for char in tag:
            if char not in node.children:
                node.children[char] = TrieNodeTags()
            node = node.children[char]
        node.sofifa_ids.add(sofifa_id)
        node.is_end = True

    def search(self, tag):
        node = self.root
        result = set()
        for char in tag:
            if char in node.children:
                node = node.children[char]
            else:
                return list(result)
            if node.is_end:
                result.update(node.sofifa_ids)
        return list(result)

# Classe Jogador
class Jogador:
    def __init__(self, sofifa_id, short_name, long_name, player_positions, nationality, club_name, league_name):
        self.sofifa_id = sofifa_id
        self.short_name = short_name
        self.long_name = long_name
        self.player_positions = player_positions
        self.nationality = nationality
        self.club_name = club_name
        self.league_name = league_name
        self.rating_contador = 0
        self.rating_soma = 0
        self.media_global = 0

    def calcular_media_global(self):
        if self.rating_contador > 0:
            self.media_global = self.rating_soma / self.rating_contador
        else:
            self.media_global = 0

# Nodo para armazenar chave e valor
class Nodo:
    def __init__(self, chave, valor):
        self.chave = chave
        self.valor = valor
        self.proximo_nodo = None

# Inicialização
tabela_jogadores = TabelaHashJogadores(10000)
tabela_rating = TabelaHashAvaliacoes(100000)
trie = Trie()
trietags = TrieTags()
user_rating = set()

# Processamento de arquivos
start_time_tags = time.time()
with open("tags.csv", "r") as arquivo_tags:
    leitor_tags = csv.reader(arquivo_tags, delimiter=",")
    next(leitor_tags)
    for linha in leitor_tags:
        sofifa_id, tags = linha[1], linha[2]
        trietags.inserir(sofifa_id, tags)
end_time_tags = time.time()
print(f"Tags carregado em: {end_time_tags - start_time_tags:.4f} segundos")

start_time_players = time.time()
with open("players.csv", "r") as arquivo_jogadores:
    leitor_jogadores = csv.reader(arquivo_jogadores, delimiter=",")
    next(leitor_jogadores)
    for linha in leitor_jogadores:
        sofifa_id, short_name, long_name, player_position, nationality, club_name, league_name = linha
        jogador = Jogador(sofifa_id, short_name, long_name, player_position, nationality, club_name, league_name)
        tabela_jogadores.inserir(sofifa_id, jogador)
        trie.inserir(jogador)
end_time_players = time.time()
print(f"Players carregado em: {end_time_players - start_time_players:.4f} segundos")

# Classe Rating
class Rating:
    def __init__(self, user_id):
        self.user_id = user_id
        self.jogador_avaliado = []
        self.rating = []

# Processamento de Ratings
start_time_ratings = time.time()
with open("rating.csv", "r") as arquivo_rating:
    leitor_rating = csv.reader(arquivo_rating, delimiter=",")
    next(leitor_rating)
    for linha in leitor_rating:
        user_id, sofifa_id, rating = linha[0], linha[1], float(linha[2])
        jogador = tabela_jogadores.buscar(sofifa_id)
        if jogador:
            jogador.rating_contador += 1
            jogador.rating_soma += rating
            jogador.calcular_media_global()
            if user_id not in user_rating:
                user_rating.add(user_id)
                user_instance = Rating(user_id)
                user_instance.jogador_avaliado.append(jogador)
                user_instance.rating.append(rating)
                tabela_rating.inserir(user_id, user_instance)
            else:
                user_instance = tabela_rating.buscar(user_id)
                if user_instance:
                    user_instance.jogador_avaliado.append(jogador)
                    user_instance.rating.append(rating)
end_time_ratings = time.time()
print(f"Ratings carregado em: {end_time_ratings - start_time_ratings:.4f} segundos \n")

# Função de Consulta por Tags
def consultar_tags(trieTags, tabela_jogadores, tabela_rating, tagsList):
    if isinstance(tagsList, list) and all(isinstance(tag, str) for tag in tagsList) and tagsList:
        result = trieTags.search(tagsList[0])

        for tag in tagsList[1:]:
            newTagResult = trieTags.search(tag)
            new_tag_ids_set = set(newTagResult)
            result = list(set(result).intersection(new_tag_ids_set))

        if not result:
            print(f"Nenhum jogador encontrado com as tags fornecidas: {tagsList}")
            return

        result = sorted(result, key=lambda x: tabela_jogadores.obter_informacoes_do_jogador(x).media_global, reverse=True)

        tabela_resultados = PrettyTable()
        tabela_resultados.field_names = ["Sofifa ID", "Short Name", "Long Name", "Player Positions", "Nationality", "Club Name", "League Name", "Rating", "Count"]

        for sofifa_id in result:
            jogador = tabela_jogadores.obter_informacoes_do_jogador(sofifa_id)
            rating_contador = jogador.rating_contador
            tabela_resultados.add_row([jogador.sofifa_id, jogador.short_name, jogador.long_name, jogador.player_positions, jogador.nationality, jogador.club_name, jogador.league_name, f"{jogador.media_global:.6f}", rating_contador])
        print(tabela_resultados)
    else:
        print("Entrada inválida. Por favor, forneça uma lista de tags.")

# Função de Consulta por Usuário
def consultar_usuario(tabela_rating, tabela_jogadores, user_id):
    rating_info = tabela_rating.buscar(user_id)
    if rating_info:
        resultados = []
        for i in range(len(rating_info.jogador_avaliado)):
            jogador = rating_info.jogador_avaliado[i]
            nota_usuario = rating_info.rating[i]
            media_global = jogador.media_global
            count = jogador.rating_contador
            resultados.append((jogador.sofifa_id, jogador.short_name, jogador.long_name, jogador.player_positions, jogador.nationality, jogador.club_name, jogador.league_name, nota_usuario, media_global, count))

        resultados.sort(key=lambda x: (x[7], x[8]), reverse=True)
        resultados = resultados[:20]

        tabela_resultados = PrettyTable()
        tabela_resultados.field_names = ["Sofifa ID", "Short Name", "Long Name", "Player Positions", "Nationality", "Club Name", "League Name", "User Rating", "Global Rating", "Count"]
        for resultado in resultados:
            tabela_resultados.add_row(resultado)

        print(tabela_resultados)
    else:
        print(f"Usuário com ID '{user_id}' não encontrado.")

# Loop de Entrada
while True:
    entrada = input("Digite sua consulta (ou 'sair' para encerrar): ")
    if entrada.lower() == 'sair':
        break

    if entrada.startswith("player "):
        prefixo = entrada[len("player "):].strip()
        ids_jogadores = trie.busca(prefixo)
        if ids_jogadores:
            ids_jogadores = sorted(ids_jogadores, key=lambda x: tabela_jogadores.obter_informacoes_do_jogador(x).media_global, reverse=True)
            tabela_resultados = PrettyTable()
            tabela_resultados.field_names = ["Sofifa ID", "Short Name", "Long Name", "Player Positions", "Nationality", "Club Name", "League Name", "Rating", "Count"]
            for sofifa_id in ids_jogadores:
                jogador = tabela_jogadores.obter_informacoes_do_jogador(sofifa_id)
                if jogador:
                    tabela_resultados.add_row([jogador.sofifa_id, jogador.short_name, jogador.long_name, jogador.player_positions, jogador.nationality, jogador.club_name, jogador.league_name, f"{jogador.media_global:.6f}", jogador.rating_contador])
            print(tabela_resultados)
        else:
            print(f"Nenhum jogador encontrado com o prefixo '{prefixo}'.")

    elif entrada.startswith("user "):
        user_id = entrada[len("user "):].strip()
        consultar_usuario(tabela_rating, tabela_jogadores, user_id)

    elif entrada.startswith("top "):
        partes = entrada.split()
        if len(partes) >= 3:
            N = int(partes[1])
            posicao = partes[2]
            jogadores = [jogador for jogador in tabela_jogadores.tabela if jogador and posicao in jogador.player_positions]
            jogadores.sort(key=lambda x: x.media_global, reverse=True)
            jogadores = jogadores[:N]

            tabela_resultados = PrettyTable()
            tabela_resultados.field_names = ["Sofifa ID", "Short Name", "Long Name", "Player Positions", "Nationality", "Club Name", "League Name", "Rating", "Count"]
            for jogador in jogadores:
                tabela_resultados.add_row([jogador.sofifa_id, jogador.short_name, jogador.long_name, jogador.player_positions, jogador.nationality, jogador.club_name, jogador.league_name, f"{jogador.media_global:.6f}", jogador.rating_contador])
            print(tabela_resultados)
        else:
            print("Formato de comando inválido. Use: top <N> <position>")

    elif entrada.startswith("tags "):
        tags = entrada[len("tags "):].strip().split()
        consultar_tags(trietags, tabela_jogadores, tabela_rating, tags)
    
    else:
        print("Comando inválido. Tente novamente.")
