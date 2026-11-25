
import streamlit as st
import json
import os
from datetime import date

st.set_page_config(
    page_title="Treino",
    page_icon="💪"
)

ARQUIVO = "treinos.json"

# Carrega os treinos salvos
def carregar_treinos():
    if not os.path.exists(ARQUIVO):
        return []

    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    except (json.JSONDecodeError, OSError) as erro:
        st.error(f"Erro ao carregar os treinos: {erro}")
        st.stop()
# Salva a lista de treinos no arquivo JSON
def salvar_treinos(treinos):
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(
            treinos,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

st.title("💪 Diário de Treino")
st.write("Registre seus treinos e acompanhe seu histórico.")

st.header("Registrar treino")

data_treino = st.date_input("Data do treino", value=date.today())

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

opcoes = [f"{nome} - {grupo}" for nome, grupo in catalogo]

exercicios_selecionados = st.multiselect(
    "Selecione os exercícios realizados",
    opcoes
)

registros = []

for opcao in exercicios_selecionados:
    nome, grupo = opcao.split(" - ", 1)
    st.subheader(nome)
    col1, col2, col3 = st.columns(3)

    with col1:
        series = st.number_input("Séries", min_value=1, value=3, step=1, key=f"series_{nome}")
    with col2:
        repeticoes = st.number_input("Repetições", min_value=1, value=10, step=1, key=f"repeticoes_{nome}")
    with col3:
        carga = st.number_input("Carga (kg)", min_value=0.0, value=0.0, step=1.0, key=f"carga_{nome}")

    registros.append({
        "nome": nome,
        "grupo_muscular": grupo,
        "series": series,
        "repeticoes": repeticoes,
        "carga": carga
    })

if st.button("Salvar treino", type="primary"):
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

st.header("Histórico de treinos")
treinos = carregar_treinos()

if len(treinos) == 0:
    st.info("Nenhum treino registrado ainda.")
else:
    datas = sorted(
    list(set(treino["data"] for treino in treinos)),
    key=lambda d: datetime.strptime(d, "%d/%m/%Y"),
    reverse=True
)
    data_filtro = st.selectbox("Filtrar por data", ["Todas as datas"] + datas)

    for treino in reversed(treinos):
        if data_filtro == "Todas as datas" or treino["data"] == data_filtro:
            with st.expander(f"Treino de {treino['data']}", expanded=True):
                for exercicio in treino["exercicios"]:
                    st.markdown(f"**{exercicio['nome']}** ({exercicio['grupo_muscular']})")
                    st.write(f"Séries: {exercicio['series']} | Repetições: {exercicio['repeticoes']} | Carga: {exercicio['carga']} kg")
                    st.write("---")
