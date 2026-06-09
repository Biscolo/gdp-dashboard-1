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

    def get_marca(self) -> str:
        return self.__marca

    def get_modelo(self) -> str:
        return self.__modelo

    def get_bateria(self) -> int:
        return self._bateria

    def get_ligado(self) -> bool:
        return self.__ligado

    def get_apps_instalados(self) -> list[str]:
        return list(self.__apps_instalados)

    def get_historico(self) -> list[str]:
        return list(self.__historico)

    # ---- Setters ----

    def set_marca(self, marca: str) -> None:
        if not marca.strip():
            raise ValueError("A marca não pode ser vazia.")
        self.__marca = marca.strip()

    def set_modelo(self, modelo: str) -> None:
        if not modelo.strip():
            raise ValueError("O modelo não pode ser vazio.")
        self.__modelo = modelo.strip()

    def set_bateria(self, bateria: int) -> None:
        if not (0 <= bateria <= 100):
            raise ValueError("O nível de bateria deve estar entre 0 e 100%.")
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
