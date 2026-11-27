
import streamlit as st
import json
import os
from datetime import date

st.set_page_config(
    page_title="CHEST DAY",
    page_icon="🏋️"
)

ARQUIVO = "/content/drive/MyDrive/DiarioTreino/treinos.json"

# Carrega os treinos salvos
def carregar_treinos():
    if not os.path.exists(ARQUIVO):
        return []
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except Exception:
        return []

# Salva a lista de treinos no arquivo JSON
def salvar_treinos(treinos):
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(
            treinos,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


ARQUIVO_FICHAS = "/content/drive/MyDrive/DiarioTreino/fichas.json"

def carregar_fichas():
    if not os.path.exists(ARQUIVO_FICHAS):
        return {}

    try:
        with open(ARQUIVO_FICHAS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except Exception:
        return {}

def salvar_fichas(fichas):
    with open(ARQUIVO_FICHAS, "w", encoding="utf-8") as arquivo:
        json.dump(fichas, arquivo, ensure_ascii=False, indent=4)


# Identidade visual CHEST DAY
st.markdown("""
<style>
:root {
    --cd-bg: #17191D;
    --cd-panel: #24272D;
    --cd-panel-2: #2C3038;
    --cd-wine: #701C2B;
    --cd-wine-light: #8D293B;
    --cd-text: #F2F2F3;
    --cd-muted: #A9ADB5;
}
.stApp { background: var(--cd-bg); color: var(--cd-text); }
[data-testid="stHeader"] { background: rgba(23,25,29,0.92); }
[data-testid="stSidebar"] {
    background: #202329;
    border-right: 1px solid #373B44;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 1.5rem; }
h1, h2, h3 { color: var(--cd-text) !important; letter-spacing: -0.02em; }
p, label, .stMarkdown { color: var(--cd-text); }
small, [data-testid="stCaptionContainer"] { color: var(--cd-muted) !important; }
div[data-testid="stMetric"] {
    background: var(--cd-panel);
    border: 1px solid #383D47;
    padding: 16px 18px;
    border-radius: 14px;
}
div[data-testid="stMetricLabel"] { color: var(--cd-muted) !important; }
div[data-testid="stMetricValue"] { color: #FFFFFF !important; }
.stButton > button, div[data-testid="stFormSubmitButton"] > button {
    background: var(--cd-wine);
    color: white;
    border: 1px solid var(--cd-wine-light);
    border-radius: 9px;
    font-weight: 650;
    transition: all .15s ease;
}
.stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {
    background: var(--cd-wine-light);
    border-color: #B44A5D;
    color: white;
}
.stButton > button[kind="secondary"] {
    background: var(--cd-panel-2);
    border-color: #454B56;
}
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
div[data-baseweb="textarea"] > div {
    background: var(--cd-panel) !important;
    border-color: #454B56 !important;
}
[data-testid="stExpander"] {
    background: var(--cd-panel);
    border: 1px solid #383D47;
    border-radius: 12px;
}
[data-testid="stAlert"] { border-radius: 10px; }
hr { border-color: #383D47; }
</style>
""", unsafe_allow_html=True)

catalogo = [
    ("Supino reto com barra", "Peito"),
    ("Supino inclinado com barra", "Peito"),
    ("Supino reto com halteres", "Peito"),
    ("Crossover polia alta", "Peito"),
    ("Crossover polia baixa", "Peito"),
    ("Crucifixo com halteres", "Peito"),
    ("Peck deck", "Peito"),
    ("Flexão de braço", "Peito"),
    ("Puxada frontal", "Costas"),
    ("Barra fixa", "Costas"),
    ("Remada curvada", "Costas"),
    ("Remada unilateral com halter", "Costas"),
    ("Remada baixa", "Costas"),
    ("Remada cavalinho", "Costas"),
    ("Pulldown na polia", "Costas"),
    ("Desenvolvimento com halteres", "Ombros"),
    ("Desenvolvimento com barra", "Ombros"),
    ("Elevação lateral", "Ombros"),
    ("Elevação frontal", "Ombros"),
    ("Crucifixo inverso", "Ombros"),
    ("Face pull", "Ombros"),
    ("Rosca direta", "Bíceps"),
    ("Rosca alternada", "Bíceps"),
    ("Rosca martelo", "Bíceps"),
    ("Rosca Scott", "Bíceps"),
    ("Rosca concentrada", "Bíceps"),
    ("Tríceps pulley", "Tríceps"),
    ("Tríceps corda", "Tríceps"),
    ("Tríceps testa", "Tríceps"),
    ("Tríceps francês", "Tríceps"),
    ("Tríceps coice", "Tríceps"),
    ("Agachamento livre", "Quadríceps"),
    ("Agachamento frontal", "Quadríceps"),
    ("Leg press 45 graus", "Quadríceps"),
    ("Cadeira extensora", "Quadríceps"),
    ("Agachamento búlgaro", "Quadríceps"),
    ("Hack squat", "Quadríceps"),
    ("Mesa flexora", "Posteriores de coxa"),
    ("Cadeira flexora", "Posteriores de coxa"),
    ("Stiff com barra", "Posteriores de coxa"),
    ("Levantamento terra romeno", "Posteriores de coxa"),
    ("Elevação pélvica", "Glúteos"),
    ("Coice na polia", "Glúteos"),
    ("Abdução de quadril na máquina", "Glúteos"),
    ("Agachamento sumô", "Glúteos"),
    ("Elevação de panturrilha em pé", "Panturrilhas"),
    ("Elevação de panturrilha sentado", "Panturrilhas"),
    ("Abdominal supra", "Abdômen"),
    ("Abdominal infra", "Abdômen"),
    ("Prancha abdominal", "Abdômen"),
    ("Abdominal bicicleta", "Abdômen"),
    ("Abdominal na polia", "Abdômen"),
    ("Extensão lombar", "Lombar"),
    ("Encolhimento de ombros", "Trapézio"),
    ("Rosca inversa", "Antebraços"),
    ("Adução de quadril na máquina", "Adutores")
]



with st.sidebar:
    st.markdown(
        "<div style='padding:4px 4px 18px 4px;'>"
        "<div style='font-size:13px;letter-spacing:3px;color:#B9A0A5;font-weight:700;'>TREINO • DESEMPENHO</div>"
        "<div style='font-size:30px;font-weight:900;letter-spacing:1px;color:#FFFFFF;'>CHEST <span style='color:#A93449;'>DAY</span></div>"
        "<div style='font-size:12px;color:#A9ADB5;margin-top:4px;'>Seu treino. Sua evolução.</div>"
        "</div>",
        unsafe_allow_html=True
    )
    st.markdown("---")
    pagina = st.radio(
        "NAVEGAÇÃO",
        ["Registrar treino", "Dashboard", "Minhas fichas", "Histórico", "Evolução"],
        index=0,
        label_visibility="visible"
    )
    st.markdown("---")
    st.caption("CHEST DAY • Diário de treino")

st.markdown(
    "<div style='font-size:12px;letter-spacing:2px;color:#B44A5D;font-weight:800;'>CHEST DAY</div>",
    unsafe_allow_html=True
)


if pagina == "Registrar treino":
    st.title("Registrar treino")
    st.caption("Registre sua sessão de forma rápida e acompanhe seu histórico.")
    st.header("📝 Detalhes do treino")

    modo_registro = st.radio(
        "Como deseja registrar?",
        ["Treino livre", "Usar uma ficha"],
        horizontal=True,
        key="modo_registro_unificado"
    )

    data_treino = st.date_input(
        "Data do treino",
        value=date.today(),
        key="data_treino_unificado"
    )

    registros = []

    catalogo = [
        ("Supino reto com barra", "Peito"),
        ("Supino inclinado com barra", "Peito"),
        ("Supino reto com halteres", "Peito"),
        ("Crossover polia alta", "Peito"),
        ("Crossover polia baixa", "Peito"),
        ("Crucifixo com halteres", "Peito"),
        ("Peck deck", "Peito"),
        ("Flexão de braço", "Peito"),
        ("Puxada frontal", "Costas"),
        ("Barra fixa", "Costas"),
        ("Remada curvada", "Costas"),
        ("Remada unilateral com halter", "Costas"),
        ("Remada baixa", "Costas"),
        ("Remada cavalinho", "Costas"),
        ("Pulldown na polia", "Costas"),
        ("Desenvolvimento com halteres", "Ombros"),
        ("Desenvolvimento com barra", "Ombros"),
        ("Elevação lateral", "Ombros"),
        ("Elevação frontal", "Ombros"),
        ("Crucifixo inverso", "Ombros"),
        ("Face pull", "Ombros"),
        ("Rosca direta", "Bíceps"),
        ("Rosca alternada", "Bíceps"),
        ("Rosca martelo", "Bíceps"),
        ("Rosca Scott", "Bíceps"),
        ("Rosca concentrada", "Bíceps"),
        ("Tríceps pulley", "Tríceps"),
        ("Tríceps corda", "Tríceps"),
        ("Tríceps testa", "Tríceps"),
        ("Tríceps francês", "Tríceps"),
        ("Tríceps coice", "Tríceps"),
        ("Agachamento livre", "Quadríceps"),
        ("Agachamento frontal", "Quadríceps"),
        ("Leg press 45 graus", "Quadríceps"),
        ("Cadeira extensora", "Quadríceps"),
        ("Agachamento búlgaro", "Quadríceps"),
        ("Hack squat", "Quadríceps"),
        ("Mesa flexora", "Posteriores de coxa"),
        ("Cadeira flexora", "Posteriores de coxa"),
        ("Stiff com barra", "Posteriores de coxa"),
        ("Levantamento terra romeno", "Posteriores de coxa"),
        ("Elevação pélvica", "Glúteos"),
        ("Coice na polia", "Glúteos"),
        ("Abdução de quadril na máquina", "Glúteos"),
        ("Agachamento sumô", "Glúteos"),
        ("Elevação de panturrilha em pé", "Panturrilhas"),
        ("Elevação de panturrilha sentado", "Panturrilhas"),
        ("Abdominal supra", "Abdômen"),
        ("Abdominal infra", "Abdômen"),
        ("Prancha abdominal", "Abdômen"),
        ("Abdominal bicicleta", "Abdômen"),
        ("Abdominal na polia", "Abdômen"),
        ("Extensão lombar", "Lombar"),
        ("Encolhimento de ombros", "Trapézio"),
        ("Rosca inversa", "Antebraços"),
        ("Adução de quadril na máquina", "Adutores")
    ]

    if modo_registro == "Treino livre":

        opcoes = [f"{nome} - {grupo}" for nome, grupo in catalogo]

        exercicios_selecionados = st.multiselect(
            "Selecione os exercícios realizados",
            opcoes,
            key="exercicios_livres_unificado"
        )

        for opcao in exercicios_selecionados:
            nome, grupo = opcao.split(" - ", 1)

            st.subheader(nome)

            col1, col2, col3 = st.columns(3)

            with col1:
                series = st.number_input(
                    "Séries", min_value=1, value=3,
                    key=f"unificado_livre_series_{nome}"
                )

            with col2:
                repeticoes = st.number_input(
                    "Repetições", min_value=1, value=10,
                    key=f"unificado_livre_repeticoes_{nome}"
                )

            with col3:
                carga = st.number_input(
                    "Carga (kg)", min_value=0.0, value=0.0,
                    step=1.0,
                    key=f"unificado_livre_carga_{nome}"
                )

            registros.append({
                "nome": nome,
                "grupo_muscular": grupo,
                "series": series,
                "repeticoes": repeticoes,
                "carga": carga
            })

    else:

        fichas_disponiveis = carregar_fichas()

        if len(fichas_disponiveis) == 0:
            st.info(
                "Você ainda não possui fichas. "
                "Crie uma na seção Minhas fichas de treino."
            )

        else:
            ficha_escolhida = st.selectbox(
                "Escolha sua ficha",
                list(fichas_disponiveis.keys()),
                key="ficha_unificada"
            )

            for i, exercicio in enumerate(
                fichas_disponiveis[ficha_escolhida]
            ):

                st.subheader(exercicio["nome"])
                st.caption(exercicio["grupo_muscular"])

                col1, col2, col3 = st.columns(3)

                with col1:
                    series = st.number_input(
                        "Séries", min_value=1, value=3,
                        key=f"unificado_ficha_series_{ficha_escolhida}_{i}"
                    )

                with col2:
                    repeticoes = st.number_input(
                        "Repetições", min_value=1, value=10,
                        key=f"unificado_ficha_repeticoes_{ficha_escolhida}_{i}"
                    )

                with col3:
                    carga = st.number_input(
                        "Carga (kg)", min_value=0.0, value=0.0,
                        step=1.0,
                        key=f"unificado_ficha_carga_{ficha_escolhida}_{i}"
                    )

                registros.append({
                    "nome": exercicio["nome"],
                    "grupo_muscular": exercicio["grupo_muscular"],
                    "series": series,
                    "repeticoes": repeticoes,
                    "carga": carga
                })

    if st.button(
        "Salvar treino",
        type="primary",
        key="salvar_treino_unificado"
    ):

        if len(registros) == 0:
            st.warning("Selecione pelo menos um exercício.")

        else:
            treinos = carregar_treinos()

            novo_treino = {
                "data": data_treino.strftime("%d/%m/%Y"),
                "exercicios": registros
            }

            treinos.append(novo_treino)
            salvar_treinos(treinos)

            st.success("Treino salvo com sucesso!")
            st.rerun()


elif pagina == "Histórico":
    st.title("Histórico de treinos")
    st.header("Histórico de treinos")
    treinos = carregar_treinos()

    if len(treinos) == 0:
        st.info("Nenhum treino registrado ainda.")
    else:
        datas = sorted(list(set(treino["data"] for treino in treinos)), reverse=True)
        data_filtro = st.selectbox("Filtrar por data", ["Todas as datas"] + datas)

        for treino in reversed(treinos):
            if data_filtro == "Todas as datas" or treino["data"] == data_filtro:
                with st.expander(f"Treino de {treino['data']}", expanded=True):
                    for exercicio in treino["exercicios"]:
                        st.markdown(f"**{exercicio['nome']}** ({exercicio['grupo_muscular']})")
                        st.write(f"Séries: {exercicio['series']} | Repetições: {exercicio['repeticoes']} | Carga: {exercicio['carga']} kg")
                        st.write("---")



elif pagina == "Evolução":
    st.title("Evolução")
    # ==========================================
    # EVOLUÇÃO DOS EXERCÍCIOS
    # ==========================================

    import pandas as pd
    import matplotlib.pyplot as plt

    st.header("📈 Evolução dos exercícios")

    treinos = carregar_treinos()

    if len(treinos) == 0:
        st.info("Registre alguns treinos para visualizar sua evolução.")

    else:
        # Criar lista com todos os exercícios registrados
        exercicios_disponiveis = []

        for treino in treinos:
            for exercicio in treino["exercicios"]:
                nome = exercicio["nome"]

                if nome not in exercicios_disponiveis:
                    exercicios_disponiveis.append(nome)

        # Selecionar exercício
        exercicio_escolhido = st.selectbox(
            "Selecione o exercício:",
            exercicios_disponiveis
        )

        # Organizar os dados do exercício escolhido
        dados = []

        for treino in treinos:
            for exercicio in treino["exercicios"]:

                if exercicio["nome"] == exercicio_escolhido:

                    dados.append({
                        "Data": treino["data"],
                        "Carga": exercicio["carga"]
                    })

        # Transformar os dados em tabela
        df = pd.DataFrame(dados)

        # Converter datas
        df["Data"] = pd.to_datetime(
            df["Data"],
            format="%d/%m/%Y"
        )

        # Ordenar por data
        df = df.sort_values("Data")

        # Criar gráfico
        fig, ax = plt.subplots()

        ax.plot(
            df["Data"],
            df["Carga"],
            marker="o"
        )

        ax.set_title("Evolução da carga - " + exercicio_escolhido)
        ax.set_xlabel("Data")
        ax.set_ylabel("Carga (kg)")

        ax.grid(True)

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)

        # Mostrar maior carga registrada
        maior_carga = df["Carga"].max()

        st.metric(
            "Maior carga registrada",
            str(maior_carga) + " kg"
        )


    # ==========================================

    # VOLUME DE TREINO
    # ==========================================

    st.header("🏋️ Volume de treino")

    treinos = carregar_treinos()

    if len(treinos) == 0:
        st.info("Registre treinos para visualizar o volume.")

    else:

        # Selecionar o exercício
        exercicios_disponiveis = []

        for treino in treinos:
            for exercicio in treino["exercicios"]:

                nome = exercicio["nome"]

                if nome not in exercicios_disponiveis:
                    exercicios_disponiveis.append(nome)

        exercicio_escolhido = st.selectbox(
            "Escolha um exercício para analisar o volume:",
            exercicios_disponiveis,
            key="volume_exercicio"
        )

        dados_volume = []

        # Percorrer os treinos
        for treino in treinos:

            volume = 0

            for exercicio in treino["exercicios"]:

                if exercicio["nome"] == exercicio_escolhido:

                    volume = (
                        exercicio["series"]
                        * exercicio["repeticoes"]
                        * exercicio["carga"]
                    )

                    dados_volume.append({
                        "Data": treino["data"],
                        "Volume": volume
                    })

        # Organizar os dados
        df_volume = pd.DataFrame(dados_volume)

        df_volume["Data"] = pd.to_datetime(
            df_volume["Data"],
            format="%d/%m/%Y"
        )

        df_volume = df_volume.sort_values("Data")

        # Criar gráfico
        fig, ax = plt.subplots()

        ax.bar(
            df_volume["Data"],
            df_volume["Volume"]
        )

        ax.set_title("Volume de treino - " + exercicio_escolhido)
        ax.set_xlabel("Data")
        ax.set_ylabel("Volume (kg × repetições)")

        ax.grid(axis="y")

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)

        # Estatísticas
        volume_total = df_volume["Volume"].sum()

        st.metric(
            "Volume total acumulado",
            str(volume_total) + " kg × repetições"
        )




elif pagina == "Dashboard":
    st.title("Dashboard")
    st.caption("Visão geral da sua rotina de treinos.")
    # ==========================================
    # ESTATISTICAS GERAIS
    # ==========================================

    st.header("📊 Estatísticas gerais")

    treinos = carregar_treinos()

    if len(treinos) == 0:

        st.info("Registre treinos para visualizar suas estatísticas.")

    else:

        from datetime import datetime, timedelta
        import pandas as pd
        import matplotlib.pyplot as plt

        # Organizar as informações
        total_treinos = len(treinos)

        hoje = datetime.today()
        limite = hoje - timedelta(days=7)

        treinos_semana = 0
        exercicios_realizados = []
        grupos = {}

        for treino in treinos:

            data = datetime.strptime(
                treino["data"], "%d/%m/%Y"
            )

            if limite.date() <= data.date() <= hoje.date():
                treinos_semana += 1

            for exercicio in treino["exercicios"]:

                nome = exercicio["nome"]
                grupo = exercicio["grupo_muscular"]

                if nome not in exercicios_realizados:
                    exercicios_realizados.append(nome)

                if grupo not in grupos:
                    grupos[grupo] = 0

                grupos[grupo] += 1

        # Apresentar indicadores
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Total de treinos",
                total_treinos
            )

        with col2:
            st.metric(
                "Treinos nos últimos 7 dias",
                treinos_semana
            )

        col3, col4 = st.columns(2)

        with col3:
            st.metric(
                "Exercícios diferentes",
                len(exercicios_realizados)
            )

        with col4:
            st.metric(
                "Grupos musculares",
                len(grupos)
            )

        # Gráfico de grupos musculares
        st.subheader("Distribuição por grupo muscular")

        nomes_grupos = list(grupos.keys())
        quantidades = list(grupos.values())

        fig, ax = plt.subplots()

        ax.bar(
            nomes_grupos,
            quantidades
        )

        ax.set_xlabel("Grupo muscular")
        ax.set_ylabel("Quantidade de exercícios registrados")
        ax.set_title("Grupos musculares treinados")

        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        st.pyplot(fig)

        # Mostrar informações
        st.subheader("Resumo dos grupos musculares")

        for grupo, quantidade in sorted(
            grupos.items(),
            key=lambda item: item[1],
            reverse=True
        ):

            st.write(
                grupo + ": " + str(quantidade) +
                " exercícios registrados"
            )




    # ==========================================
    # RECORDES PESSOAIS
    # ==========================================

    st.header("🏆 Recordes pessoais")

    treinos = carregar_treinos()

    if len(treinos) == 0:

        st.info("Registre treinos para descobrir seus recordes.")

    else:

        recordes = {}

        # Percorrer todos os treinos
        for treino in treinos:

            for exercicio in treino["exercicios"]:

                nome = exercicio["nome"]
                carga = exercicio["carga"]
                data = treino["data"]

                # Verificar se o exercício já possui recorde
                if nome not in recordes:

                    recordes[nome] = {
                        "carga": carga,
                        "data": data,
                        "grupo": exercicio["grupo_muscular"]
                    }

                # Atualizar caso encontre uma carga maior
                elif carga > recordes[nome]["carga"]:

                    recordes[nome] = {
                        "carga": carga,
                        "data": data,
                        "grupo": exercicio["grupo_muscular"]
                    }

        # Organizar recordes do maior para o menor
        recordes_ordenados = sorted(
            recordes.items(),
            key=lambda item: item[1]["carga"],
            reverse=True
        )

        st.subheader("Maior carga por exercício")

        for nome, informacoes in recordes_ordenados:

            with st.expander(nome):

                st.write(
                    "Grupo muscular:",
                    informacoes["grupo"]
                )

                st.metric(
                    "Maior carga registrada",
                    str(informacoes["carga"]) + " kg"
                )

                st.write(
                    "Data do recorde:",
                    informacoes["data"]
                )

        # Apresentar o maior recorde geral
        st.subheader("Maior carga registrada no histórico")

        maior_exercicio = recordes_ordenados[0]

        st.metric(
            maior_exercicio[0],
            str(maior_exercicio[1]["carga"]) + " kg"
        )



    # ==========================================

elif pagina == "Minhas fichas":
    st.title("Minhas fichas")
    # SISTEMA DE FICHAS DE TREINO
    # ==========================================

    st.header("📋 Minhas fichas de treino")

    fichas = carregar_fichas()

    # Criar nova ficha
    st.subheader("Criar ficha")

    nome_ficha = st.text_input(
        "Nome da ficha",
        placeholder="Exemplo: Treino A - Peito e Tríceps"
    )

    opcoes_fichas = [
        nome + " - " + grupo
        for nome, grupo in catalogo
    ]

    exercicios_ficha = st.multiselect(
        "Selecione os exercícios da ficha",
        opcoes_fichas,
        key="exercicios_ficha"
    )

    if st.button("Salvar ficha", type="primary"):

        if nome_ficha.strip() == "":
            st.warning("Digite um nome para a ficha.")

        elif len(exercicios_ficha) == 0:
            st.warning("Selecione pelo menos um exercício.")

        elif nome_ficha in fichas:
            st.warning("Já existe uma ficha com esse nome.")

        else:

            fichas[nome_ficha] = []

            for opcao in exercicios_ficha:

                nome, grupo = opcao.rsplit(" - ", 1)

                fichas[nome_ficha].append({
                    "nome": nome,
                    "grupo_muscular": grupo
                })

            salvar_fichas(fichas)

            st.success("Ficha cadastrada com sucesso!")
            st.rerun()


    # Visualizar fichas cadastradas
    st.subheader("Fichas cadastradas")

    fichas = carregar_fichas()

    if len(fichas) == 0:

        st.info("Nenhuma ficha cadastrada.")

    else:

        for nome, exercicios in fichas.items():

            with st.expander(nome):

                for exercicio in exercicios:

                    st.write(
                        exercicio["nome"],
                        "-",
                        exercicio["grupo_muscular"]
                    )

                if st.button(
                    "Excluir ficha",
                    key="excluir_" + nome
                ):

                    del fichas[nome]

                    salvar_fichas(fichas)

                    st.success("Ficha excluída!")
                    st.rerun()
