from flask import Flask

app = Flask(__name__)

@app.route('/')
def resume():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Currículo</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #6a11cb, #2575fc);
                color: #fff;
                text-align: center;
                animation: backgroundFade 10s infinite alternate;
            }
            @keyframes backgroundFade {
                0% { background: linear-gradient(135deg, #6a11cb, #2575fc); }
                100% { background: linear-gradient(135deg, #ff7e5f, #feb47b); }
            }
            .container {
                padding: 50px;
            }
            h1 {
                font-size: 3.5em;
                animation: fadeIn 2s ease-in-out;
            }
            h2 {
                font-size: 2.5em;
                margin: 20px 0;
                animation: slideIn 2s ease-in-out;
            }
            p {
                font-size: 1.2em;
                line-height: 1.5;
                animation: fadeIn 3s ease-in-out;
            }
            .skills, .experience, .education, .contact, .projects {
                margin-top: 30px;
                text-align: left;
                padding: 20px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                animation: fadeIn 3s ease-in-out;
                transition: transform 0.3s, box-shadow 0.3s;
            }
            .skills:hover, .experience:hover, .education:hover, .contact:hover, .projects:hover {
                transform: scale(1.05);
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
            }
            .skills ul, .experience ul, .education ul, .projects ul {
                list-style: none;
                padding: 0;
            }
            .skills li, .experience li, .education li, .projects li {
                margin: 10px 0;
                transition: color 0.3s;
            }
            .skills li:hover, .experience li:hover, .education li:hover, .projects li:hover {
                color: #ffcc00;
            }
            .contact {
                margin-top: 40px;
                padding: 20px;
                background: rgba(255, 255, 255, 0.3);
            }
            a {
                color: #fff;
                text-decoration: none;
                transition: color 0.3s, text-shadow 0.3s;
            }
            a:hover {
                color: #ffcc00;
                text-shadow: 0 0 10px #ffcc00;
            }
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            @keyframes slideIn {
                from { transform: translateY(-50px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Currículo</h1>
            <h2>Ansur Nikolas Anthony Miguel Braga Brum Cornélio de Paiva Drummond Marco Proti Amorin Diniz Azevedo Duarte II</h2>
            <p>Desenvolvedor Full Stack com experiência em Python, Flask, e JavaScript. Apaixonado por criar soluções inovadoras e eficientes.</p>
            
            <div class="skills">
                <h2>Habilidades</h2>
                <ul>
                    <li>Python</li>
                    <li>Flask</li>
                    <li>JavaScript</li>
                    <li>HTML & CSS</li>
                    <li>Banco de Dados (MySQL, PostgreSQL)</li>
                    <li>Git e Controle de Versão</li>
                    <li>Docker e Kubernetes</li>
                    <li>Metodologias Ágeis (Scrum, Kanban)</li>
                </ul>
            </div>
            
            <div class="experience">
                <h2>Experiência Profissional</h2>
                <ul>
                    <li><strong>Desenvolvedor Full Stack</strong> - Empresa X (2020 - Presente)
                        <p>Desenvolvimento de aplicações web utilizando Flask e React. Integração com APIs RESTful e otimização de desempenho.</p>
                    </li>
                    <li><strong>Estagiário de Desenvolvimento</strong> - Empresa Y (2018 - 2020)
                        <p>Criação de scripts em Python para automação de tarefas e suporte ao time de desenvolvimento.</p>
                    </li>
                </ul>
            </div>
            
            <div class="education">
                <h2>Educação</h2>
                <ul>
                    <li><strong>Bacharelado em Ciência da Computação</strong> - Universidade Z (2015 - 2019)</li>
                    <li><strong>Curso de Desenvolvimento Web</strong> - Plataforma Online (2020)</li>
                    <li><strong>Certificação em Docker e Kubernetes</strong> - Escola de Tecnologia (2021)</li>
                </ul>
            </div>
            
            <div class="projects">
                <h2>Projetos</h2>
                <ul>
                    <li><strong>Gerenciador de Tarefas</strong> - Aplicação web para organização de tarefas pessoais.</li>
                    <li><strong>API de Clima</strong> - API RESTful para consulta de dados meteorológicos.</li>
                    <li><strong>Blog Pessoal</strong> - Blog desenvolvido com Flask e Bootstrap.</li>
                </ul>
            </div>
            
            <div class="contact">
                <h2>Contato</h2>
                <p>Email: joao.silva@email.com</p>
                <p>Telefone: (11) 99999-9999</p>
                <p>LinkedIn: <a href="https://linkedin.com/in/joaosilva">linkedin.com/in/joaosilva</a></p>
                <p>GitHub: <a href="https://github.com/joaosilva">github.com/joaosilva</a></p>
                <p>Portfólio: <a href="https://joaosilva.dev">joaosilva.dev</a></p>
            </div>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)