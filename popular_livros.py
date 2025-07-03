# popular_livros.py

from sqlalchemy.orm import Session
from database import SessionLocal
from models import Livro
from datetime import datetime



def inserir_livros_iniciais():
    db: Session = SessionLocal()

    livros = [
        Livro(id=1, nome='O Senhor dos Anéis', autor='J.R.R. Tolkien', descricao='A Sociedade do Anel', genero='Fantasia'),
        Livro(id=2, nome='Harry Potter', autor='J.K. Rowling', descricao='A Pedra Filosofal', genero='Fantasia'),
        Livro(id=3, nome='Hábitos Atômicos', autor='James Clear', descricao='Guia prático para criar bons hábitos', genero='Desenvolvimento pessoal'),
        Livro(id=4, nome='1984', autor='George Orwell', descricao='Sociedade distópica sob vigilância', genero='Distopia'),
        Livro(id=5, nome='Dom Quixote', autor='Miguel de Cervantes', descricao='Cavaleiro em busca de justiça', genero='Clássico / Romance'),
        Livro(id=6, nome='O Pequeno Príncipe', autor='Antoine de Saint-Exupéry', descricao='Viagem filosófica e poética', genero='Fábula / Filosófico'),
        Livro(id=7, nome='A Revolução dos Bichos', autor='George Orwell', descricao='Sátira política com animais', genero='Sátira / Distopia'),
        Livro(id=8, nome='O Código Da Vinci', autor='Dan Brown', descricao='Suspense envolvendo religião e arte', genero='Suspense / Mistério'),
        Livro(id=9, nome='Moby Dick', autor='Herman Melville', descricao='A caça à baleia branca', genero='Aventura / Clássico'),
        Livro(id=10, nome='Crime e Castigo', autor='Fiódor Dostoiévski', descricao='Drama psicológico e culpa', genero='Drama psicológico / Clássico'),
        Livro(id=11, nome='O Alquimista', autor='Paulo Coelho', descricao='Jornada espiritual por um tesouro', genero='Ficção filosófica'),
        Livro(id=12, nome='A Guerra dos Tronos', autor='George R.R. Martin', descricao='Intrigas em Westeros', genero='Fantasia épica'),
        Livro(id=13, nome='O Morro dos Ventos Uivantes', autor='Emily Brontë', descricao='Romance gótico e vingança', genero='Romance gótico'),
        Livro(id=14, nome='Cem Anos de Solidão', autor='Gabriel García Márquez', descricao='Saga da família Buendía', genero='Realismo mágico'),
        Livro(id=15, nome='A Lâmina da Assassina', autor='Sarah J. Maas', descricao='Prelúdio da saga Trono de Vidro', genero='Fantasia / Jovem adulto'),
        Livro(id=16, nome='Trono de Vidro', autor='Sarah J. Maas', descricao='Assassina em competição mortal', genero='Fantasia / Jovem adulto'),
        Livro(id=17, nome='Coroa da Meia-Noite', autor='Sarah J. Maas', descricao='Segredos e traições', genero='Fantasia / Jovem adulto'),
        Livro(id=18, nome='Herdeira do Fogo', autor='Sarah J. Maas', descricao='Poderes despertando', genero='Fantasia / Jovem adulto'),
        Livro(id=19, nome='Rainha das Sombras', autor='Sarah J. Maas', descricao='Confronto com o passado', genero='Fantasia / Jovem adulto'),
        Livro(id=20, nome='Império de Tempestades', autor='Sarah J. Maas', descricao='Aliados improváveis', genero='Fantasia / Jovem adulto'),
        Livro(id=21, nome='Torre do Alvorecer', autor='Sarah J. Maas', descricao='Aventuras em novo continente', genero='Fantasia / Jovem adulto'),
        Livro(id=22, nome='Reino das Cinzas', autor='Sarah J. Maas', descricao='Conclusão épica', genero='Fantasia / Jovem adulto'),
        Livro(id=23, nome='Corte de Espinhos e Rosas', autor='Sarah J. Maas', descricao='Bela e a Fera reimaginado', genero='Fantasia / Romance / Jovem adulto'),
        Livro(id=24, nome='Corte de Névoa e Fúria', autor='Sarah J. Maas', descricao='Segredos do mundo feérico', genero='Fantasia / Romance / Jovem adulto'),
        Livro(id=25, nome='Corte de Asas e Ruína', autor='Sarah J. Maas', descricao='Batalha entre reinos', genero='Fantasia / Romance / Jovem adulto'),
        Livro(id=26, nome='Corte de Gelo e Estrelas', autor='Sarah J. Maas', descricao='História pós-guerra', genero='Fantasia / Romance / Jovem adulto'),
        Livro(id=27, nome='Corte de Chamas Prateadas', autor='Sarah J. Maas', descricao='Nova protagonista em ascensão', genero='Fantasia / Romance / New adult'),
        Livro(id=28, nome='Casa de Terra e Sangue', autor='Sarah J. Maas', descricao='Mundo urbano com magia', genero='Fantasia / New adult'),
        Livro(id=29, nome='Casa de Céu e Sopro', autor='Sarah J. Maas', descricao='Conflitos e revelações', genero='Fantasia / New adult'),
        Livro(id=30, nome='Casa de Chama e Sombra', autor='Sarah J. Maas', descricao='Último capítulo da saga', genero='Fantasia / New adult'),
    ]

    for livro in livros:
        livro.data_inclusao = datetime.utcnow()
        db.merge(livro)  # merge evita duplicação se ID já existir

    db.commit()
    db.close()
    print("✅ Livros inseridos com sucesso.")

if __name__ == "__main__":
    inserir_livros_iniciais()
