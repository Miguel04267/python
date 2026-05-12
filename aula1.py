from flask import Flask

app = Flask(__name__)

@app.route('/') 
def info():
    return '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Decorators em Python</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            background-color: #f4f4f9;
            color: #333;
            margin: 0;
            padding: 0;
        }
        header {
            background: #6200ea;
            color: #fff;
            padding: 20px 10px;
            text-align: center;
        }
        main {
            padding: 20px;
            max-width: 800px;
            margin: 20px auto;
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        h1, h2 {
            color: #6200ea;
        }
        p {
            margin: 10px 0;
        }
        footer {
            text-align: center;
            padding: 10px;
            background: #6200ea;
            color: #fff;
            position: fixed;
            bottom: 0;
            width: 100%;
        }
    </style>
</head>
<body>
    <header>
        <h1>Decorators em Python</h1>
    </header>
    <main>
        <h2>O que são Decorators?</h2>
        <p>Decorators são uma funcionalidade poderosa e flexível do Python que permitem modificar o comportamento de funções ou métodos. Eles são amplamente utilizados para adicionar funcionalidades a funções existentes de forma limpa e reutilizável.</p>
        <h2>Como funcionam?</h2>
        <p>Um decorator é essencialmente uma função que recebe outra função como argumento e retorna uma nova função com comportamento modificado. Eles são aplicados usando o símbolo <code>@</code> antes da definição da função.</p>
        <h2>Exemplo:</h2>
        <pre>
<code>
def meu_decorator(func):
    def wrapper():
        print("Algo antes da função original.")
        func()
        print("Algo depois da função original.")
    return wrapper

@meu_decorator
def minha_funcao():
    print("Essa é a função original.")

minha_funcao()
</code>
        </pre>
        <p>No exemplo acima, o decorator <code>meu_decorator</code> modifica o comportamento da função <code>minha_funcao</code>, adicionando mensagens antes e depois da execução.</p>
    </main>
    <footer>
        <p>Feito com ❤️ para aprender Python</p>
    </footer>
</body>
</html>'''

@app.route('/hello')
def sobre():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)