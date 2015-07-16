select 
	u.id, 
	u.nome, 
	u.cpf, 
	u.sexo, 
	u.telefone, 
	l.nome as rua, 
	eu.numero, 
	eu.complemento, 
	l.bairro,
	l.cidade, 
	l.uf
from 
	usuario u
	left join endereco_usuario eu on (eu.usuario_id = u.id)
	left join logradouro l on (l.cep = eu.cep);
