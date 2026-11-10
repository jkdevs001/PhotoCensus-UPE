import sys
from pathlib import Path

# Configuração do caminho para importar o módulo da pasta kit
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

try:
    from kit import black_box
except ImportError:
    print("Erro: Não foi possível importar o módulo 'black_box' da pasta 'kit'.")
    print("Certifique-se de que a estrutura do repositório se mantém intacta.")
    sys.exit(1)


# --- Funções Auxiliares Manuais (sem sum, max, min) ---

def calcular_total(lista_valores):
    """Calcula a soma dos elementos de uma lista manualmente."""
    total = 0
    for valor in lista_valores:
        total += valor
    return total


def encontrar_maior(lista_valores):
    """Determina o valor máximo de uma lista manualmente."""
    if not lista_valores:
        return 0
    maior = lista_valores[0]
    for valor in lista_valores:
        if valor > maior:
            maior = valor
    return maior


def contar_ocorrencias(lista_itens):
    """Conta a frequência de cada elemento devolvendo duas listas: itens e contagens."""
    itens_unicos = []
    contagens = []
    for item in lista_itens:
        if item in itens_unicos:
            indice = itens_unicos.index(item)
            contagens[indice] += 1
        else:
            itens_unicos.append(item)
            contagens.append(1)
    return itens_unicos, contagens


# --- Operações do Sistema ---

def processar_imagem():
    """Solicita o caminho de uma imagem e executa a deteção."""
    caminho = input("\nIntroduza o caminho relativo ou absoluto da imagem: ").strip()
    
    if not caminho:
        print("Aviso: Caminho inválido.")
        return None, []

    ficheiro = Path(caminho)
    if not ficheiro.is_file():
        print(f"Erro: O ficheiro '{caminho}' não foi encontrado.")
        return None, []

    print("A processar imagem com a caixa-preta...")
    try:
        # Chamada da função de deteção fornecida no kit
        detecoes = black_box.detect(str(ficheiro))
        print(f"Sucesso: {len(detecoes)} objeto(s) detetado(s).")
        return str(ficheiro), detecoes
    except Exception as e:
        print(f"Ocorreu um erro durante o processamento: {e}")
        return None, []


def exibir_relatorio(caminho_imagem, detecoes):
    """Apresenta a listagem detalhada e o gráfico de barras em modo texto."""
    if not detecoes:
        print("\nNenhum objeto detetado ou nenhuma imagem processada até ao momento.")
        return

    print("\n" + "=" * 50)
    print(f"RELATÓRIO DE CENSO VISUAL: {Path(caminho_imagem).name}")
    print("=" * 50)

    classes, contagens = contar_ocorrencias(detecoes)
    total_objetos = calcular_total(contagens)
    maior_contagem = encontrar_maior(contagens)

    print(f"Total de objetos identificados: {total_objetos}\n")
    print(f"{'Classe':<20} | {'Qtd':<5} | Distribuição")
    print("-" * 50)

    # Definição da escala do gráfico (comprimento máximo da barra: 25 carateres)
    largura_maxima = 25
    for i in range(len(classes)):
        classe = classes[i]
        qtd = contagens[i]
        
        if maior_contagem > 0:
            tamanho_barra = int((qtd / maior_contagem) * largura_maxima)
        else:
            tamanho_barra = 0
            
        barra = "█" * tamanho_barra
        print(f"{classe:<20} | {qtd:<5} | {barra}")

    print("=" * 50)


# --- Menu Principal ---

def menu():
    caminho_atual = None
    detecoes_atuais = []

    while True:
        print("\n" + "#" * 35)
        print("      PHOTOCENSUS - GRUPO 03")
        print("#" * 35)
        print("1. Processar nova imagem")
        print("2. Ver relatório e gráfico de barras")
        print("3. Limpar dados em memória")
        print("0. Sair")
        print("#" * 35)

        opcao = input("Selecione uma opção: ").strip()

        if opcao == "1":
            caminho, detecoes = processar_imagem()
            if caminho is not None:
                caminho_atual = caminho
                detecoes_atuais = detecoes
        elif opcao == "2":
            exibir_relatorio(caminho_atual, detecoes_atuais)
        elif opcao == "3":
            caminho_atual = None
            detecoes_atuais = []
            print("Memória limpa com sucesso.")
        elif opcao == "0":
            print("\nA encerrar o PhotoCensus. Até breve!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()