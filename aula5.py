from flask import Flask, request, render_template_string

app = Flask(__name__)

usuarios_senhas = {
    'miguel': '22401032', 
    'dolga': 'cotemig2026',
    'janaina': 'cotemig2026',
    'antonio': 'cotemig2026'
}

def show_the_login_form():
    return render_template_string("""
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #6a11cb, #2575fc);
                color: #fff;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            form {
                background: rgba(255, 255, 255, 0.1);
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
                text-align: center;
                backdrop-filter: blur(10px);
            }
            input {
                width: 100%;
                padding: 12px;
                margin: 10px 0;
                border: none;
                border-radius: 5px;
                background: rgba(255, 255, 255, 0.2);
                color: #fff;
                font-size: 16px;
            }
            input::placeholder {
                color: #ddd;
            }
            input:focus {
                outline: none;
                background: rgba(255, 255, 255, 0.3);
            }
            button {
                background-color: #ff7f50;
                color: white;
                padding: 12px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                transition: background-color 0.3s ease;
            }
            button:hover {
                background-color: #ff5722;
            }
            h2 {
                margin-bottom: 20px;
            }
        </style>
        <h2>Login</h2>
        <form method="POST">
            <input type="text" name="usuario" placeholder="Usuário"><br><br>
            <input type="password" name="senha" placeholder="Senha"><br><br>
            <button type="submit">Entrar</button>
        </form>
    """)
def do_the_login():
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')

    if usuario in usuarios_senhas and usuarios_senhas[usuario] == senha:
        return render_template_string(f"""
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #43cea2, #185a9d);
                    color: #fff;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }}
                .welcome {{
                    text-align: center;
                    background: rgba(255, 255, 255, 0.1);
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
                    backdrop-filter: blur(10px);
                }}
                h1 {{
                    margin-bottom: 20px;
                }}
                a {{
                    color: #ff7f50;
                    text-decoration: none;
                    font-weight: bold;
                }}
                a:hover {{
                    color: #ff5722;
                }}
            </style>
            <div class="welcome">
                <h1>Bem-vindo, {usuario}!</h1>
                <a href="/">Voltar para o login</a>
            </div>
        """)
    else:
        return "<h1>Login inválido</h1>"

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()

if __name__ == "__main__":
    app.run(debug=True)