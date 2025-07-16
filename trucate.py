from sqlalchemy import text
from postgre import SessionLocal

def truncate_livros():
    db = SessionLocal()
    try:
        db.execute(text("TRUNCATE TABLE livros"))
        db.commit()
        print("Tabela livros truncada com sucesso.")
    except Exception as e:
        db.rollback()
        print(f"Erro ao truncar tabela: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    truncate_livros()