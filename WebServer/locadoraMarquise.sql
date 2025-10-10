CREATE DATABASE locadora_marquise;
USE locadora_marquise;

-- criação das tabelas
CREATE TABLE diretor (
	id_diretor INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    sobrenome VARCHAR(255) NOT NULL,
    genero ENUM('Feminino','Masculino','Outro') NOT NULL
);

INSERT INTO diretor (nome,sobrenome,genero) VALUES
('Lucas', 'Almeida', 'Masculino'),
('Mariana', 'Souza', 'Outro'),
('André', 'Mendes', 'Masculino'),
('Carla', 'Pereira', 'Feminino'),
('Felipe', 'Costa', 'Masculino'),
('Juliana', 'Oliveira', 'Outro'),
('Rafael', 'Nascimento', 'Masculino'),
('Isabela', 'Fernandes', 'Feminino'),
('Thiago', 'Lima', 'Masculino'),
('Camila', 'Ribeiro', 'Feminino'),
('Eduardo', 'Gomes', 'Masculino'),
('Patrícia', 'Carvalho', 'Feminino'),
('Gustavo', 'Martins', 'Masculino'),
('Aline', 'Barbosa', 'Feminino'),
('Rodrigo', 'Silva', 'Outro'),
('Fernanda', 'Araújo', 'Feminino'),
('João', 'Castro', 'Masculino'),
('Natália', 'Dias', 'Feminino'),
('Bruno', 'Teixeira', 'Masculino'),
('Alex', 'Campos', 'Outro');

SELECT * FROM diretor;

-- criação da tabela filme
CREATE TABLE filme (
	id_filme INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    atores VARCHAR(255) NOT NULL,
    diretor VARCHAR(255) NOT NULL,
    ano YEAR NOT NULL,
    genero VARCHAR(255) NOT NULL,
    produtora VARCHAR(255) NOT NULL,
    sinopse TEXT(500) NOT NULL
);

INSERT INTO filme (titulo,atores,diretor,ano,genero,produtora,sinopse) VALUES
('A Origem', 'Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page', 'Christopher Nolan', 2010, 'Ficção Científica', 'Warner Bros.', 'Um ladrão que invade os sonhos das pessoas para roubar segredos corporativos enfrenta sua missão mais perigosa: implantar uma ideia na mente de alguém.'),
('Titanic', 'Leonardo DiCaprio, Kate Winslet', 'James Cameron', 1997, 'Romance', 'Paramount Pictures', 'Durante a viagem inaugural do Titanic, um jovem artista e uma mulher da alta sociedade vivem um amor proibido.'),
('Vingadores: Ultimato', 'Robert Downey Jr., Chris Evans, Scarlett Johansson', 'Anthony Russo, Joe Russo', 2019, 'Ação', 'Marvel Studios', 'Os heróis restantes unem forças para reverter o estalo de Thanos e restaurar o equilíbrio do universo.'),
('O Senhor dos Anéis: O Retorno do Rei', 'Elijah Wood, Viggo Mortensen, Ian McKellen', 'Peter Jackson', 2003, 'Fantasia', 'New Line Cinema', 'A batalha final pela Terra Média acontece enquanto Frodo e Sam tentam destruir o Um Anel.'),
('Harry Potter e a Pedra Filosofal', 'Daniel Radcliffe, Emma Watson, Rupert Grint', 'Chris Columbus', 2001, 'Fantasia', 'Warner Bros.', 'Um garoto descobre ser um bruxo e começa sua jornada na Escola de Magia e Bruxaria de Hogwarts.'),
('Jurassic Park', 'Sam Neill, Laura Dern, Jeff Goldblum', 'Steven Spielberg', 1993, 'Aventura', 'Universal Pictures', 'Cientistas recriam dinossauros em um parque temático, mas a experiência sai do controle.'),
('Forrest Gump', 'Tom Hanks, Robin Wright, Gary Sinise', 'Robert Zemeckis', 1994, 'Drama', 'Paramount Pictures', 'A vida de um homem simples que, sem perceber, influencia eventos históricos dos EUA.'),
('Matrix', 'Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss', 'Lana Wachowski, Lilly Wachowski', 1999, 'Ficção Científica', 'Warner Bros.', 'Um programador descobre que vive em uma simulação controlada por máquinas e se junta à resistência.'),
('Coringa', 'Joaquin Phoenix, Robert De Niro', 'Todd Phillips', 2019, 'Drama', 'Warner Bros.', 'A história da transformação de Arthur Fleck em um dos maiores vilões de Gotham.'),
('Pantera Negra', 'Chadwick Boseman, Michael B. Jordan, Lupita Nyong', 'Ryan Coogler', 2018, 'Ação', 'Marvel Studios', 'O rei T\'Challa precisa defender Wakanda de ameaças internas e externas.'),
('A Teoria de Tudo', 'Eddie Redmayne, Felicity Jones', 'James Marsh', 2014, 'Biografia', 'Working Title Films', 'A história de Stephen Hawking, seu amor e suas descobertas revolucionárias sobre o tempo.'),
('O Rei Leão', 'Matthew Broderick, James Earl Jones, Jeremy Irons', 'Roger Allers, Rob Minkoff', 1994, 'Animação', 'Walt Disney Pictures', 'Um jovem leão foge de seu reino após a morte do pai, mas precisa retornar para assumir seu lugar.'),
('Gladiador', 'Russell Crowe, Joaquin Phoenix', 'Ridley Scott', 2000, 'Ação', 'DreamWorks Pictures', 'Um general romano traído busca vingança contra o imperador que destruiu sua família.'),
('Homem-Aranha: Sem Volta Para Casa', 'Tom Holland, Zendaya, Benedict Cumberbatch', 'Jon Watts', 2021, 'Ação', 'Marvel Studios', 'Peter Parker enfrenta as consequências de sua identidade revelada e inimigos de outros universos.'),
('Frozen: Uma Aventura Congelante', 'Idina Menzel, Kristen Bell, Josh Gad', 'Chris Buck, Jennifer Lee', 2013, 'Animação', 'Walt Disney Animation Studios', 'Duas irmãs enfrentam uma maldição de gelo e descobrem o verdadeiro poder do amor.'),
('Avatar', 'Sam Worthington, Zoe Saldana, Sigourney Weaver', 'James Cameron', 2009, 'Ficção Científica', '20th Century Fox', 'Um ex-fuzileiro se envolve em uma guerra entre humanos e nativos de Pandora.'),
('O Poderoso Chefão', 'Marlon Brando, Al Pacino, James Caan', 'Francis Ford Coppola', 1972, 'Drama', 'Paramount Pictures', 'A saga da família Corleone e sua luta pelo poder no mundo do crime organizado.'),
('Interestelar', 'Matthew McConaughey, Anne Hathaway, Jessica Chastain', 'Christopher Nolan', 2014, 'Ficção Científica', 'Paramount Pictures', 'Exploradores viajam por um buraco de minhoca em busca de um novo lar para a humanidade.'),
('O Espetacular Homem-Aranha', 'Andrew Garfield, Emma Stone', 'Marc Webb', 2012, 'Ação', 'Columbia Pictures', 'Peter Parker ganha poderes e descobre a verdade sobre a morte de seus pais.'),
('Divertidamente', 'Amy Poehler, Phyllis Smith, Bill Hader', 'Pete Docter', 2015, 'Animação', 'Pixar Animation Studios', 'As emoções de uma garota ganham vida e precisam trabalhar juntas durante uma mudança importante.');

SELECT * FROM filme;
