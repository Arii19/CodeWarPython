# popular_livros.py

from sqlalchemy.orm import Session
from database import SessionLocal
from models import Livro
from datetime import datetime

def inserir_livros_iniciais():
    db: Session = SessionLocal()

    livros = [
        Livro(id=1, nome='O Senhor dos Anéis', descricao='A Sociedade do Anel', genero='Fantasia'),
        Livro(id=2, nome='Harry Potter', descricao='A Pedra Filosofal', genero='Fantasia'),
        Livro(id=3, nome='Hábitos Atômicos', descricao='Guia prático para criar bons hábitos', genero='Desenvolvimento pessoal'),
        Livro(id=4, nome='1984', descricao='Sociedade distópica sob vigilância', genero='Distopia'),
        Livro(id=5, nome='Dom Quixote', descricao='Cavaleiro em busca de justiça', genero='Clássico / Romance'),
        Livro(id=6, nome='O Pequeno Príncipe', descricao='Viagem filosófica e poética', genero='Fábula / Filosófico'),
        Livro(id=7, nome='A Revolução dos Bichos', descricao='Sátira política com animais', genero='Sátira / Distopia'),
        Livro(id=8, nome='O Código Da Vinci', descricao='Suspense envolvendo religião e arte', genero='Suspense / Mistério'),
        Livro(id=9, nome='Moby Dick', descricao='A caça à baleia branca', genero='Aventura / Clássico'),
        Livro(id=10, nome='Crime e Castigo', descricao='Drama psicológico e culpa', genero='Drama psicológico / Clássico'),
        Livro(id=11, nome='O Alquimista', descricao='Jornada espiritual por um tesouro', genero='Ficção filosófica'),
        Livro(id=12, nome='A Guerra dos Tronos', descricao='Intrigas em Westeros', genero='Fantasia épica'),
        Livro(id=13, nome='O Morro dos Ventos Uivantes', descricao='Romance gótico e vingança', genero='Romance gótico'),
        Livro(id=14, nome='Cem Anos de Solidão', descricao='Saga da família Buendía', genero='Realismo mágico'),
        Livro(id=15, nome='A Lâmina da Assassina', descricao='Prelúdio da saga Trono de Vidro', genero='Fantasia / Jovem adulto'),
        Livro(id=16, nome='Trono de Vidro', descricao='Assassina em competição mortal', genero='Fantasia / Jovem adulto'),
        Livro(id=17, nome='Coroa da Meia-Noite', descricao='Segredos e traições', genero='Fantasia / Jovem adulto'),
        Livro(id=18, nome='Herdeira do Fogo', descricao='Poderes despertando', genero='Fantasia / Jovem adulto'),
        Livro(id=19, nome='Rainha das Sombras', descricao='Confronto com o passado', genero='Fantasia / Jovem adulto'),
        Livro(id=20, nome='Império de Tempestades', descricao='Aliados improváveis', genero='Fantasia / Jovem adulto'),
        Livro(id=21, nome='Torre do Alvorecer', descricao='Aventuras em novo continente', genero='Fantasia / Jovem adulto'),
        Livro(id=22, nome='Reino das Cinzas', descricao='Conclusão épica', genero='Fantasia / Jovem adulto'),
        Livro(id=23, nome='Corte de Espinhos e Rosas', descricao='Bela e a Fera reimaginado', genero='Fantasia / Romance / Jovem adulto'),
        Livro(id=24, nome='Corte de Névoa e Fúria', descricao='Segredos do mundo feérico', genero='Fantasia / Romance / Jovem adulto'),
        Livro(id=25, nome='Corte de Asas e Ruína', descricao='Batalha entre reinos', genero='Fantasia / Romance / Jovem adulto'),
        Livro(id=26, nome='Corte de Gelo e Estrelas', descricao='História pós-guerra', genero='Fantasia / Romance / Jovem adulto'),
        Livro(id=27, nome='Corte de Chamas Prateadas', descricao='Nova protagonista em ascensão', genero='Fantasia / Romance / New adult'),
        Livro(id=28, nome='Casa de Terra e Sangue', descricao='Mundo urbano com magia', genero='Fantasia / New adult'),
        Livro(id=29, nome='Casa de Céu e Sopro', descricao='Conflitos e revelações', genero='Fantasia / New adult'),
        Livro(id=30, nome='Casa de Chama e Sombra', descricao='Último capítulo da saga', genero='Fantasia / New adult'),
    ]

    for livro in livros:
        livro.data_inclusao = datetime.utcnow()
        db.merge(livro)  # merge evita duplicação se ID já existir

    db.commit()
    db.close()
    print("✅ Livros inseridos com sucesso.")

if __name__ == "__main__":
    inserir_livros_iniciais()
