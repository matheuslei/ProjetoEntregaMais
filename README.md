### Projeto Entrega Mais

Bem-vindo ao projeto Entrega Mais! 
Este é um sistema de gestão de entregas, onde clientes podem cadastrar produtos para serem entregues e entregadores podem pegar esses produtos e realizar as entregas.

Este projeto faz parte da iniciativa da Mais1Code, que tem como missão "Reprogramar a Quebrada" através do ensino de tecnologia de qualidade para jovens de baixa renda, ajudando a transformar a realidade das comunidades periféricas.

Mais1Code visa capacitar programadores da quebrada, proporcionando oportunidades de crescimento e desenvolvimento profissional.

## Funcionalidades

- **Cadastro de Usuário**: Permite que novos usuários (clientes e entregadores) se cadastrem no sistema.
- **Login de Usuário**: Usuários cadastrados podem fazer login.
- **Dashboard do Cliente**: Clientes podem adicionar novos produtos e visualizar produtos cadastrados.
- **Dashboard do Entregador**: Entregadores podem visualizar produtos disponíveis para entrega, pegar produtos e marcar produtos como entregues.
- **Gerenciamento de Sessões**: Suporte a login e logout de usuários.
- **Status de Produtos**: Controle de status dos produtos (Aguardando entregador, Pacote com entregador, Produto Entregue, Pedido Finalizado).

## Tecnologias Utilizadas

- **Flask**: Framework web utilizado para desenvolver o backend.
- **SQLite**: Banco de dados utilizado para armazenar as informações dos usuários e produtos.
- **Flask-Login**: Extensão Flask utilizada para gerenciar a autenticação do usuário.
- **Werkzeug**: Biblioteca para hashing de senhas e segurança.

## Como Rodar o Projeto

1. Clone o repositório:
    ```bash
    git clone https://github.com/matheuslei/ProjetoEntregaMais.git
    cd ProjetoEntregaMais
    ```

2. Crie um ambiente virtual e ative-o:
    ```bash
    python -m venv venv
    source venv/bin/activate   # No Windows use `venv\Scripts\activate`
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Configure o banco de dados:
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

5. Rode a aplicação:
    ```bash
    flask run
    ```

6. Acesse a aplicação no navegador:
    ```text
    http://127.0.0.1:5000
    ```

## Imagens do Projeto

### Página Inicial
![image](https://github.com/matheuslei/ProjetoEntregaMais/assets/65515537/4cde5c50-f5a5-497e-9e22-dacff402becc)
![image](https://github.com/matheuslei/ProjetoEntregaMais/assets/65515537/612255f6-ac22-47b8-be0a-811a5c2256ee)


## Estrutura do Projeto

```
ProjetoEntregaMais/
├── app.py
├── templates/
│   ├── index.html
│   ├── cadastro.html
│   ├── login.html
│   ├── cliente.html
│   ├── entregador.html
│   ├── detalhes_produto.html
├── static/
│   ├── img/
│       ├── ...
│   ├── style.css
│   ├── style_index.css
├── README.md
├── requirements.txt
```

## Contribuição

Se você deseja contribuir com este projeto, por favor siga os passos abaixo:

1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b minha-feature`).
3. Commit suas alterações (`git commit -am 'Adicionei uma nova feature'`).
4. Faça um push para a branch (`git push origin minha-feature`).
5. Crie um novo Pull Request.

## Licença

Este projeto está licenciado sob os termos da licença MIT.

---

Espero que você goste de usar o **Entrega Mais**! Se tiver alguma dúvida ou sugestão, sinta-se à vontade para abrir uma issue no repositório.
