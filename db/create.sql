--Criando estrutura
--create database trabalhobd2;

create table logradouro(cep integer primary key, nome varchar(100), bairro varchar(40), cidade varchar(50), uf char(2));

create table usuario(id serial primary key, nome varchar(100), cpf char(11), sexo char(1), telefone varchar(11));

create table endereco_usuario(id serial primary key, usuario_id integer, cep integer, numero varchar(10), complemento varchar(50),
foreign key(usuario_id) references usuario(id), foreign key(cep) references logradouro(cep));

-- Inserindo endereços
insert into logradouro(cep, nome, bairro, cidade, uf) values
(21825320, 'Rua Engenheira Paula Lopes', 'Bangu', 'Rio de Janeiro', 'RJ'),
(20520050, 'Rua Conde de Bonfim', 'Tijuca', 'Rio de Janeiro', 'RJ'),
(21321000, 'Rua Baronesa', 'Praça Seca', 'Rio de Janeiro', 'RJ'),
(01310300, 'Avenida Paulista', 'Bela Vista', 'São Paulo', 'SP'),
(05510020, 'Rua M.M.D.C.', 'Butantã', 'São Paulo', 'SP'),
(80420090, 'Avenida do Batel', 'Batel', 'Curitiba', 'PR');
