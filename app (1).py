import json
import os
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import streamlit as st

# ============================================================
# CHEST DAY - Aplicativo de registro e acompanhamento de treinos
# Armazenamento local em JSON (treinos.json e fichas.json)
# ============================================================

st.set_page_config(page_title="CHEST DAY", page_icon="💪", layout="wide")

ARQUIVO_TREINOS = Path("treinos.json")
ARQUIVO_FICHAS = Path("fichas.json")

CATALOGO = {
    "Peito": ["Supino reto com barra", "Supino inclinado com barra", "Supino reto com halteres", "Crossover polia alta", "Crossover polia baixa", "Crucifixo com halteres", "Peck deck", "Flexão de braço"],
    "Costas": ["Puxada frontal", "Barra fixa", "Remada curvada", "Remada unilateral com halter", "Remada baixa", "Remada cavalinho", "Pulldown na polia"],
    "Ombros": ["Desenvolvimento com halteres", "Desenvolvimento com barra", "Elevação lateral", "Elevação frontal", "Crucifixo inverso", "Face pull"],
    "Bíceps": ["Rosca direta", "Rosca alternada", "Rosca martelo", "Rosca Scott", "Rosca concentrada"],
    "Tríceps": ["Tríceps pulley", "Tríceps corda", "Tríceps testa", "Tríceps francês", "Tríceps coice"],
    "Quadríceps": ["Agachamento livre", "Agachamento frontal", "Leg press 45 graus", "Cadeira extensora", "Agachamento búlgaro", "Hack squat"],
    "Posteriores de coxa": ["Mesa flexora", "Cadeira flexora", "Stiff com barra", "Levantamento terra romeno"],
    "Glúteos": ["Elevação pélvica", "Coice na polia", "Abdução de quadril na máquina", "Agachamento sumô"],
    "Panturrilhas": ["Elevação de panturrilha em pé", "Elevação de panturrilha sentado"],
    "Abdômen": ["Abdominal supra", "Abdominal infra", "Prancha abdominal", "Abdominal bicicleta", "Abdominal na polia"],
    "Lombar": ["Extensão lombar"],
    "Trapézio": ["Encolhimento de ombros"],
    "Antebraços": ["Rosca inversa"],
    "Adutores": ["Adução de quadril na máquina"],
}

# ------------------------- Dados -----------------------------
def carregar_json(caminho, padrao):
    if not caminho.exists():
        return padrao.copy() if isinstance(padrao, (list, dict)) else padrao
    try:
        with caminho.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        return dados if isinstance(dados, type(padrao)) else padrao.copy()
    except (json.JSONDecodeError, OSError, TypeError):
        return padrao.copy() if isinstance(padrao, (list, dict)) else padrao


def salvar_json(caminho, dados):
    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)


def carregar_treinos():
    dados = carregar_json(ARQUIVO_TREINOS, [])
    # Mantém compatibilidade com o formato antigo do projeto.
    for treino in dados:
        treino.setdefault("exercicios", [])
        treino.setdefault("data", date.today().strftime("%d/%m/%Y"))
    return dados


def data_para_objeto(valor):
    for formato in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(str(valor), formato).date()
        except (ValueError, TypeError):
            pass
    return date.today()


def volume_exercicio(exercicio):
    try:
        return float(exercicio.get("series", 0)) * float(exercicio.get("repeticoes", 0)) * float(exercicio.get("carga", 0))
    except (TypeError, ValueError):
        return 0.0


def preparar_dataframe(treinos):
    linhas = []
    for treino in treinos:
        data_treino = data_para_objeto(treino.get("data", ""))
        for ex in treino.get("exercicios", []):
            linhas.append({
                "Data": data_treino,
                "Exercício": ex.get("nome", "Exercício"),
                "Grupo muscular": ex.get("grupo_muscular", "Não informado"),
                "Séries": float(ex.get("series", 0) or 0),
                "Repetições": float(ex.get("repeticoes", 0) or 0),
                "Carga (kg)": float(ex.get("carga", 0) or 0),
                "Volume (kg)": volume_exercicio(ex),
            })
    return pd.DataFrame(linhas)

# ------------------------- Estilo ----------------------------
st.markdown("""
<style>
    .stApp { background: #111114; color: #f2f2f2; }
    [data-testid="stHeader"] { background: rgba(17,17,20,0.96); }
    [data-testid="stSidebar"] { background: #19191e; border-right: 1px solid #34343b; }
    h1, h2, h3 { color: #f5f5f5 !important; }
    .brand { color: #b51f3b; font-weight: 900; letter-spacing: 4px; font-size: 15px; }
    .hero { background: linear-gradient(115deg,#25151b,#19191e 70%); border: 1px solid #51212d; padding: 25px 28px; border-radius: 15px; margin-bottom: 22px; }
    .hero-title { font-size: 34px; font-weight: 900; letter-spacing: 2px; color: #ffffff; margin: 0; }
    .hero-sub { color: #b9b9c0; margin-top: 5px; }
    div.stButton > button[kind="primary"] { background: #9f1832; border: 1px solid #bd2947; color: white; font-weight: 700; }
    div.stButton > button[kind="primary"]:hover { background: #bd2947; border-color: #df4965; }
    [data-testid="stMetric"] { background: #1b1b21; border: 1px solid #34343b; padding: 15px; border-radius: 12px; }
    [data-testid="stMetricValue"] { color: #ffffff; }
    .section-note { color: #a7a7b0; font-size: 13px; }
    div[data-baseweb="tab-list"] { gap: 8px; }
    button[data-baseweb="tab"] { background: #1b1b21; border-radius: 8px 8px 0 0; }
    hr { border-color: #34343b; }
</style>
""", unsafe_allow_html=True)

# ------------------------- Cabeçalho -------------------------
st.markdown('<div class="brand">CHEST DAY / TRAINING TRACKER</div>', unsafe_allow_html=True)
st.markdown('''<div class="hero"><p class="hero-title">TREINE. REGISTRE. EVOLUA.</p><div class="hero-sub">Seu histórico de treino, organizado em um só lugar.</div></div>''', unsafe_allow_html=True)

treinos = carregar_treinos()
fichas = carregar_json(ARQUIVO_FICHAS, [])
df = preparar_dataframe(treinos)

# ------------------------- Navegação -------------------------
abas = st.tabs(["⚡ Registro rápido", "📊 Dashboard", "📅 Histórico", "🏋️ Minhas fichas", "🏆 Recordes"])

# ========================= REGISTRO ==========================
with abas[0]:
    st.subheader("Registrar treino")
    st.caption("Selecione os exercícios e informe séries, repetições e carga.")
    col_data, col_grupo = st.columns([1, 2])
    with col_data:
        data_treino = st.date_input("Data do treino", value=date.today(), key="data_registro")
    with col_grupo:
        grupos = st.multiselect("Filtrar catálogo por grupo muscular", list(CATALOGO.keys()), default=[])

    exercicios_disponiveis = []
    grupos_para_mostrar = grupos if grupos else list(CATALOGO.keys())
    for grupo in grupos_para_mostrar:
        exercicios_disponiveis.extend([(nome, grupo) for nome in CATALOGO[grupo]])
    mapa_opcoes = {f"{nome} — {grupo}": (nome, grupo) for nome, grupo in exercicios_disponiveis}
    selecionados = st.multiselect("Exercícios realizados", list(mapa_opcoes.keys()), key="exercicios_registro")

    registros = []
    if selecionados:
        st.markdown("---")
        for indice, opcao in enumerate(selecionados):
            nome, grupo = mapa_opcoes[opcao]
            st.markdown(f"**{nome}**  ·  <span style='color:#b83a53'>{grupo}</span>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                series = st.number_input("Séries", min_value=1, max_value=30, value=3, step=1, key=f"s_{indice}_{nome}")
            with c2:
                repeticoes = st.number_input("Repetições", min_value=1, max_value=100, value=10, step=1, key=f"r_{indice}_{nome}")
            with c3:
                carga = st.number_input("Carga (kg)", min_value=0.0, max_value=1000.0, value=0.0, step=1.0, key=f"c_{indice}_{nome}")
            registros.append({"nome": nome, "grupo_muscular": grupo, "series": int(series), "repeticoes": int(repeticoes), "carga": float(carga)})

    if st.button("SALVAR TREINO", type="primary", use_container_width=True):
        if not registros:
            st.warning("Selecione pelo menos um exercício antes de salvar.")
        else:
            treinos.append({"data": data_treino.strftime("%d/%m/%Y"), "exercicios": registros})
            salvar_json(ARQUIVO_TREINOS, treinos)
            st.success("Treino salvo com sucesso!")
            st.rerun()

# ========================= DASHBOARD =========================
with abas[1]:
    st.subheader("Visão geral")
    if df.empty:
        st.info("Ainda não há treinos registrados. Comece pela aba Registro rápido.")
    else:
        total_treinos = len(treinos)
        total_exercicios = len(df)
        volume_total = df["Volume (kg)"].sum()
        grupos_trabalhados = df["Grupo muscular"].nunique()
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Treinos registrados", total_treinos)
        m2.metric("Exercícios realizados", total_exercicios)
        m3.metric("Volume acumulado", f"{volume_total:,.0f} kg".replace(",", "."))
        m4.metric("Grupos musculares", grupos_trabalhados)

        st.markdown("---")
        esquerda, direita = st.columns(2)
        with esquerda:
            st.markdown("#### Volume por treino")
            volume_data = df.groupby("Data")["Volume (kg)"].sum().sort_index()
            st.line_chart(volume_data)
        with direita:
            st.markdown("#### Volume por grupo muscular")
            volume_grupo = df.groupby("Grupo muscular")["Volume (kg)"].sum().sort_values(ascending=False)
            st.bar_chart(volume_grupo)

        st.markdown("#### Evolução da carga por exercício")
        exercicios_com_carga = sorted(df.loc[df["Carga (kg)"] > 0, "Exercício"].unique().tolist())
        if exercicios_com_carga:
            exercicio_escolhido = st.selectbox("Escolha um exercício", exercicios_com_carga, key="grafico_exercicio")
            evolucao = df[df["Exercício"] == exercicio_escolhido].sort_values("Data")
            st.line_chart(evolucao.set_index("Data")["Carga (kg)"])
        else:
            st.caption("Registre cargas maiores que zero para visualizar a evolução.")

# ========================= HISTÓRICO =========================
with abas[2]:
    st.subheader("Histórico de treinos")
    if not treinos:
        st.info("Nenhum treino registrado ainda.")
    else:
        datas = sorted({data_para_objeto(t.get("data", "")) for t in treinos}, reverse=True)
        opcoes_datas = ["Todas as datas"] + [d.strftime("%d/%m/%Y") for d in datas]
        filtro = st.selectbox("Filtrar por data", opcoes_datas)
        for indice, treino in reversed(list(enumerate(treinos))):
            data_texto = treino.get("data", "Data não informada")
            if filtro != "Todas as datas" and data_texto != filtro:
                continue
            exercicios_treino = treino.get("exercicios", [])
            volume = sum(volume_exercicio(ex) for ex in exercicios_treino)
            with st.expander(f"Treino de {data_texto}  ·  {len(exercicios_treino)} exercícios  ·  volume {volume:,.0f} kg".replace(",", ".")):
                if not exercicios_treino:
                    st.caption("Nenhum exercício neste registro.")
                for ex in exercicios_treino:
                    st.markdown(f"**{ex.get('nome', 'Exercício')}** — {ex.get('grupo_muscular', 'Grupo não informado')}")
                    st.write(f"{ex.get('series', 0)} séries × {ex.get('repeticoes', 0)} repetições · Carga: {ex.get('carga', 0)} kg")
                if st.button("Excluir este treino", key=f"excluir_{indice}"):
                    treinos.pop(indice)
                    salvar_json(ARQUIVO_TREINOS, treinos)
                    st.rerun()

# ========================= FICHAS ============================
with abas[3]:
    st.subheader("Minhas fichas de treino")
    st.caption("Monte modelos de treino para consultar e reutilizar depois.")
    with st.expander("＋ Criar nova ficha", expanded=not fichas):
        nome_ficha = st.text_input("Nome da ficha", placeholder="Ex.: Treino A — Peito e tríceps")
        grupos_ficha = st.multiselect("Grupos musculares", list(CATALOGO.keys()), key="grupos_ficha")
        opcoes_ficha = []
        for grupo in grupos_ficha:
            opcoes_ficha.extend([f"{nome} — {grupo}" for nome in CATALOGO[grupo]])
        exercicios_ficha = st.multiselect("Exercícios da ficha", opcoes_ficha, key="exercicios_ficha")
        if st.button("SALVAR FICHA", type="primary"):
            if not nome_ficha.strip() or not exercicios_ficha:
                st.warning("Informe um nome e selecione pelo menos um exercício.")
            else:
                nova_ficha = {"nome": nome_ficha.strip(), "exercicios": []}
                for item in exercicios_ficha:
                    nome, grupo = item.split(" — ", 1)
                    nova_ficha["exercicios"].append({"nome": nome, "grupo_muscular": grupo})
                fichas.append(nova_ficha)
                salvar_json(ARQUIVO_FICHAS, fichas)
                st.success("Ficha criada!")
                st.rerun()

    if fichas:
        for indice, ficha in enumerate(fichas):
            with st.expander(f"📋 {ficha.get('nome', 'Ficha sem nome')} · {len(ficha.get('exercicios', []))} exercícios"):
                for ex in ficha.get("exercicios", []):
                    st.write(f"• {ex.get('nome', 'Exercício')} — {ex.get('grupo_muscular', '')}")
                if st.button("Excluir ficha", key=f"excluir_ficha_{indice}"):
                    fichas.pop(indice)
                    salvar_json(ARQUIVO_FICHAS, fichas)
                    st.rerun()
    else:
        st.info("Você ainda não criou nenhuma ficha.")

# ========================= RECORDES ==========================
with abas[4]:
    st.subheader("Recordes pessoais")
    if df.empty:
        st.info("Seus recordes aparecerão aqui depois que você registrar treinos.")
    else:
        validos = df[df["Carga (kg)"] > 0]
        if validos.empty:
            st.info("Registre cargas maiores que zero para acompanhar seus recordes.")
        else:
            recordes = validos.loc[validos.groupby("Exercício")["Carga (kg)"].idxmax()]
            recordes = recordes.sort_values("Carga (kg)", ascending=False)
            st.caption("Maior carga registrada para cada exercício.")
            for _, linha in recordes.iterrows():
                a, b, c = st.columns([3, 1, 2])
                a.markdown(f"**{linha['Exercício']}**")
                b.markdown(f"### {linha['Carga (kg)']:g} kg")
                c.caption(f"{linha['Data'].strftime('%d/%m/%Y')} · {linha['Grupo muscular']}")
                st.divider()

st.markdown("<div style='text-align:center;color:#686871;font-size:12px;padding:25px 0 5px'>CHEST DAY · ORGANIZE SEU TREINO</div>", unsafe_allow_html=True)
