from flask_sqlalchemy import SQLAlchemy

# Inicializamos um objeto SQLAlchemy que irá
# Fazer uma ligação com nosso app
# E ele irá verificar em todos os objetos que indicarmos
# E então ele irá nos permitir mapear esses objetos
# Em forma de "rows" em um banco de dados
# Por exemplo:
# Quando criarmos um objeto do tipo ItemModel
# Com uma coluna "name" e outra "price"
# Este objeto "db" do tipo SQLAlchemy irá nos permitir
# Colocar, facilmente, o objeto criado em um BD

db = SQLAlchemy()