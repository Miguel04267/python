import os
import sqlite3
import json
from functools import wraps
from urllib.error import URLError
from urllib.request import urlopen

from flask import Flask, flash, g, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao")
app.config["DATABASE"] = os.path.join(app.root_path, "tarefas.db")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(_error=None):
    db = g.pop("db", None)
    if db:
        db.close()


def init_db():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'Pendente'
                CHECK(status IN ('Pendente', 'Em andamento', 'Concluída')),
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        );
    """)
    db.commit()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Faça login para continuar.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


def tarefa_do_usuario(tarefa_id):
    tarefa = get_db().execute(
        "SELECT * FROM tarefas WHERE id = ? AND usuario_id = ?",
        (tarefa_id, session["usuario_id"]),
    ).fetchone()
    return tarefa


@app.route("/")
def inicio():
    return redirect(url_for("dashboard" if "usuario_id" in session else "login"))


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        if not nome or not email or len(senha) < 6:
            flash("Preencha tudo; a senha deve ter pelo menos 6 caracteres.", "danger")
        else:
            try:
                db = get_db()
                db.execute(
                    "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
                    (nome, email, generate_password_hash(senha)),
                )
                db.commit()
                flash("Cadastro realizado. Agora faça login.", "success")
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                flash("Este e-mail já está cadastrado.", "danger")
    return render_template("registro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        usuario = get_db().execute(
            "SELECT * FROM usuarios WHERE email = ?", (email,)
        ).fetchone()
        if usuario and check_password_hash(usuario["senha"], request.form.get("senha", "")):
            session.clear()
            session["usuario_id"] = usuario["id"]
            session["usuario_nome"] = usuario["nome"]
            return redirect(url_for("dashboard"))
        flash("E-mail ou senha inválidos.", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    tarefas = get_db().execute(
        "SELECT * FROM tarefas WHERE usuario_id = ? ORDER BY id DESC",
        (session["usuario_id"],),
    ).fetchall()
    return render_template("dashboard.html", tarefas=[dict(t) for t in tarefas])

@app.route("/nova_tarefa", methods=["GET", "POST"])
@login_required
def nova_tarefa():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        if not titulo:
            flash("Informe um título.", "danger")
        else:
            get_db().execute(
                "INSERT INTO tarefas (titulo, descricao, status, usuario_id) VALUES (?, ?, ?, ?)",
                (titulo, request.form.get("descricao", "").strip(),
                 request.form.get("status", "Pendente"), session["usuario_id"]),
            )
            get_db().commit()
            flash("Tarefa criada.", "success")
            return redirect(url_for("dashboard"))
    return render_template("tarefa_form.html", tarefa=None)


@app.route("/editar/<int:tarefa_id>", methods=["GET", "POST"])
@login_required
def editar(tarefa_id):
    tarefa = tarefa_do_usuario(tarefa_id)
    if not tarefa:
        flash("Tarefa não encontrada.", "danger")
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        if titulo:
            get_db().execute(
                "UPDATE tarefas SET titulo=?, descricao=?, status=? WHERE id=? AND usuario_id=?",
                (titulo, request.form.get("descricao", "").strip(),
                 request.form.get("status", "Pendente"), tarefa_id, session["usuario_id"]),
            )
            get_db().commit()
            flash("Tarefa atualizada.", "success")
            return redirect(url_for("dashboard"))
        flash("Informe um título.", "danger")
    return render_template("tarefa_form.html", tarefa=tarefa)


@app.post("/excluir/<int:tarefa_id>")
@login_required
def excluir(tarefa_id):
    get_db().execute(
        "DELETE FROM tarefas WHERE id=? AND usuario_id=?",
        (tarefa_id, session["usuario_id"]),
    )
    get_db().commit()
    flash("Tarefa excluída.", "success")
    return redirect(url_for("dashboard"))


@app.post("/concluir/<int:tarefa_id>")
@login_required
def concluir(tarefa_id):
    get_db().execute(
        "UPDATE tarefas SET status='Concluída' WHERE id=? AND usuario_id=?",
        (tarefa_id, session["usuario_id"]),
    )
    get_db().commit()
    return redirect(url_for("dashboard"))


@app.get("/api/tarefas")
@login_required
def api_tarefas():
    status = request.args.get("status", "Todas")
    sql = "SELECT * FROM tarefas WHERE usuario_id = ?"
    parametros = [session["usuario_id"]]
    if status in ("Pendente", "Em andamento", "Concluída"):
        sql += " AND status = ?"
        parametros.append(status)
    sql += " ORDER BY id DESC"
    return jsonify([dict(t) for t in get_db().execute(sql, parametros).fetchall()])


@app.get("/api/progresso")
@login_required
def api_progresso():
    linhas = get_db().execute(
        "SELECT status, COUNT(*) quantidade FROM tarefas WHERE usuario_id=? GROUP BY status",
        (session["usuario_id"],),
    ).fetchall()
    dados = {"Pendente": 0, "Em andamento": 0, "Concluída": 0}
    dados.update({linha["status"]: linha["quantidade"] for linha in linhas})
    return jsonify(dados)


@app.get("/progresso")
@login_required
def progresso():
    return render_template("progresso.html")


with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
