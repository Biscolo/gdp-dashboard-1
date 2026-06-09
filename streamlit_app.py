import streamlit as str_inst  # Evitar conflito se necessário, mas usaremos 'st' por padrão
import streamlit as st

# =====================================================================
# 1. SUA CLASSE ORIGINAL (Mantida intacta, apenas corrigido o import)
# =====================================================================
class Smartphone:
    """
    Classe que representa um Smartphone.
    Aplica conceitos de POO: encapsulamento, getters, setters e métodos de ação.
    """

    def __init__(self, marca: str, modelo: str, bateria: int):
        self.__marca: str = marca
        self.__modelo: str = modelo
        self._bateria: int = max(0, min(100, bateria))
        self.__ligado: bool = False
        self.__apps_instalados: list[str] = []
        self.__historico: list[str] = []

    # ---- Getters ----
    def get_marca(self) -> str: return self.__marca
    def get_modelo(self) -> str: return self.__modelo
    def get_bateria(self) -> int: return self._bateria
    def get_ligado(self) -> bool: return self.__ligado
    def get_apps_instalados(self) -> list[str]: return list(self.__apps_instalados)
    def get_historico(self) -> list[str]: return list(self.__historico)

    # ---- Setters ----
    def set_marca(self, marca: str) -> None:
        if not marca.strip(): raise ValueError("A marca não pode ser vazia.")
        self.__marca = marca.strip()

    def set_modelo(self, modelo: str) -> None:
        if not modelo.strip(): raise ValueError("O modelo não pode ser vazio.")
        self.__modelo = modelo.strip()

    def set_bateria(self, bateria: int) -> None:
        if not (0 <= bateria <= 100): raise ValueError("O nível de bateria deve estar entre 0 e 100%.")
        self._bateria = bateria

    # ---- Métodos de ação ----
    def ligar_desligar(self) -> str:
        if not self.__ligado and self._bateria == 0:
            msg = "Sem bateria! Carregue o smartphone antes de ligá-lo."
            self.__historico.append(msg)
            return msg
        self.__ligado = not self.__ligado
        estado = "LIGADO" if self.__ligado else "DESLIGADO"
        msg = f"Smartphone {self.__marca} {self.__modelo} foi {estado}."
        self.__historico.append(msg)
        return msg

    def instalar_app(self, app: str) -> str:
        if not self.__ligado:
            msg = "O smartphone está desligado. Ligue-o para instalar aplicativos."
            self.__historico.append(msg)
            return msg
        app = app.strip()
        if not app:
            return "Digite o nome de um aplicativo válido."
        if app in self.__apps_instalados:
            msg = f"O app '{app}' já está instalado."
            self.__historico.append(msg)
            return msg
        self.__apps_instalados.append(app)
        msg = f"App '{app}' instalado com sucesso!"
        self.__historico.append(msg)
        return msg

    def desinstalar_app(self, app: str) -> str:
        if app in self.__apps_instalados:
            self.__apps_instalados.remove(app)
            msg = f"App '{app}' removido."
        else:
            msg = f"App '{app}' não encontrado."
        self.__historico.append(msg)
        return msg

    def carregar_bateria(self, quantidade: int) -> str:
        anterior = self._bateria
        self._bateria = min(100, self._bateria + quantidade)
        ganho = self._bateria - anterior
        msg = f"Bateria carregada +{ganho}%. Nível atual: {self._bateria}%."
        self.__historico.append(msg)
        return msg

    def usar_bateria(self, quantidade: int) -> str:
        if not self.__ligado:
            return "O smartphone está desligado."
        anterior = self._bateria
        self._bateria = max(0, self._bateria - quantidade)
        consumido = anterior - self._bateria
        msg = f"Bateria consumida -{consumido}%. Nível atual: {self._bateria}%."
        if self._bateria == 0:
            self.__ligado = False
            msg += " Bateria esgotada! Smartphone desligado automaticamente."
        self.__historico.append(msg)
        return msg

    def resumo(self) -> dict:
        return {
            "Marca": self.__marca,
            "Modelo": self.__modelo,
            "Bateria": f"{self._bateria}%",
            "Status": "Ligado" if self.__ligado else "Desligado",
            "Apps instalados": self.__apps_instalados if self.__apps_instalados else ["Nenhum"],
        }


# =====================================================================
# 2. INTERFACE STREAMLIT
# =====================================================================

st.set_page_config(page_title="Simulador de Smartphone", page_icon="📱", layout="centered")

st.title("📱 Simulador de Smartphone (POO)")
st.write("Crie o seu aparelho na barra lateral e controle as ações dele por aqui.")

# ---- BARRA LATERAL: Inicialização do Aparelho ----
st.sidebar.header("🛠️ Configurações Iniciais")

# Inputs para criar o objeto
marca_input = st.sidebar.text_input("Marca do Smartphone", value="Pythonic")
modelo_input = st.sidebar.text_input("Modelo do Smartphone", value="Pro Max X")
bateria_inicial = st.sidebar.slider("Bateria Inicial (%)", 0, 100, 50)

# Botão para (re)inicializar o smartphone
if st.sidebar.button("Instanciar / Reiniciar Smartphone") or "celular" not in st.session_state:
    st.session_state.celular = Smartphone(marca_input, modelo_input, bateria_inicial)
    st.sidebar.success("Smartphone criado com sucesso!")

# Instância persistente na sessão
celular = st.session_state.celular

# ---- PAINEL DE STATUS (Tela do celular) ----
st.subheader("📺 Tela do Aparelho")

# Organizando o status em colunas visuais bonitas
col1, col2, col3 = st.columns(3)

with col1:
    status_texto = "🟢 LIGADO" if celular.get_ligado() else "🔴 DESLIGADO"
    st.metric(label="Status do Aparelho", value=status_texto)

with col2:
    st.metric(label="Bateria", value=f"{celular.get_bateria()}%")

with col3:
    st.metric(label="Aparelho", value=f"{celular.get_marca()} {celular.get_modelo()}")

# Progresso visual da bateria
st.progress(celular.get_bateria() / 100)

st.markdown("---")

# ---- PAINEL DE AÇÕES ----
st.subheader("🎮 Ações do Usuário")

# Botão de Ligar/Desligar destacado
if celular.get_ligado():
    if st.button("🔴 Desligar Aparelho", use_container_width=True):
        retorno = celular.ligar_desligar()
        st.toast(retorno)
        st.rerun()
else:
    if st.button("🟢 Ligar Aparelho", use_container_width=True):
        retorno = celular.ligar_desligar()
        st.toast(retorno)
        st.rerun()

# Organizando as outras ações em Abas (Tabs) para não poluir o visual
aba_apps, aba_energia = st.tabs(["📂 Gerenciar Apps", "🔋 Energia & Bateria"])

with aba_apps:
    st.write("### Aplicativos")
    
    # Exibir apps instalados
    apps_instalados = celular.get_apps_instalados()
    st.write(f"**Instalados atualmente:** {', '.join(apps_instalados) if apps_instalados else 'Nenhum app instalado.'}")
    
    # Formulário para Instalar App
    col_ins1, col_ins2 = st.columns([2, 1])
    with col_ins1:
        novo_app = st.text_input("Nome do App para Instalar", key="input_instalar", placeholder="Ex: WhatsApp")
    with col_ins2:
        st.write("##") # Espaçador para alinhar com o input
        if st.button("Instalar", use_container_width=True):
            retorno = celular.instalar_app(novo_app)
            st.info(retorno)
            st.rerun()
            
    # Formulário para Desinstalar App
    if apps_instalados:
        col_des1, col_des2 = st.columns([2, 1])
        with col_des1:
            app_remover = st.selectbox("Escolha o App para Desinstalar", options=apps_instalados)
        with col_des2:
            st.write("##")
            if st.button("Desinstalar", use_container_width=True):
                retorno = celular.desinstalar_app(app_remover)
                st.warning(retorno)
                st.rerun()

with aba_energia:
    st.write("### Controle de Energia")
    
    col_eng1, col_eng2 = st.columns(2)
    
    with col_eng1:
        qtd_carga = st.number_input("Quantidade para Carregar (%)", min_value=1, max_value=100, value=15)
        if st.button("⚡ Carregar Bateria", use_container_width=True):
            retorno = celular.carregar_bateria(qtd_carga)
            st.success(retorno)
            st.rerun()
            
    with col_eng2:
        with col_eng1:
        qtd_carregar = st.number_input("Quantidade para Carregar (%)", min_value=1, max_value=100, value=15) # <-- Fechado aqui )
        if st.button("⚡ Carregar Bateria", use_container_width=True):
            retorno = celular.carregar_bateria(qtd_carregar)
            st.success(retorno)
            st.rerun()
            
    with col_eng2:
        qtd_uso = st.number_input("Quantidade para Consumir (%)", min_value=1, max_value=100, value=10) # <-- O SEU ERRO ESTAVA AQUI! Faltava o )
        if st.button("🎮 Jogar / Usar Celular", use_container_width=True):
            retorno = celular.usar_bateria(qtd_uso)
            st.error(retorno)
            st.rerun()
