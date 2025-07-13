import logging

# Configuração básica do logger
logging.basicConfig(
    level=logging.INFO,  # Pode ser DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Salva em arquivo
        logging.StreamHandler()          # Mostra no console
    ]
)

# Instância reutilizável
logger = logging.getLogger(__name__)
