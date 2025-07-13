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
<<<<<<< HEAD
logger = logging.getLogger(__name__)
=======
logger = logging.getLogger(__name__)
>>>>>>> 8ae12fd747836ae3404bea8c71fd6926ae48fbec
