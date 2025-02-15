import streamlit as st
import duckdb 


if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "📚 Livres"


def switch_tab():
    st.session_state["active_tab"] = st.session_state["selected_tab"]


with st.sidebar:
    st.title("😺")
    st.radio(
        "Choisissez une catégorie",
        ["📚 Livres", "🎬 Films et Séries", "🖼 Expositions"],
        index=["📚 Livres", "🎬 Films et Séries", "🖼 Expositions"].index(st.session_state["active_tab"]),
        key="selected_tab",
        on_change=switch_tab  # Met à jour `st.session_state["active_tab"]`
    )


con_books = duckdb.connect(database="books.db", read_only=False)
con_films = duckdb.connect(database="films.db", read_only=False)
con_expo = duckdb.connect(database="expo.db", read_only=False)

con_books.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    genre TEXT,
    date_read DATE,
    rating INTEGER,
    comments TEXT
);
''')

con_films.execute('''
CREATE TABLE IF NOT EXISTS films (
    id INTEGER PRIMARY KEY,
    title TEXT,
    realisator TEXT,
    genre TEXT,
    date_watch DATE,
    rating INTEGER,
    comments TEXT
);
''')

con_expo.execute('''
CREATE TABLE IF NOT EXISTS expo (
    id INTEGER PRIMARY KEY,
    title TEXT,
    place TEXT,
    artist TEXT,
    date_visit DATE,
    rating INTEGER,
    comments TEXT
);
''')


if st.session_state["active_tab"] == "📚 Livres":

    with st.sidebar:
        st.header("Ajouter un Livre")
        with st.form("book_form"):
            title = st.text_input("Titre")
            author = st.text_input("Auteur ou Autrice")
            genre = st.selectbox("Genre", ["Classique", "Horreur", "SF", "Fantasy", "Policier", "Romance", "Fiction Historique"])
            date_read = st.date_input("Date de Lecture")
            rating = st.slider("Note (1-5)", 1, 5, 3)
            comments = st.text_area("Commentaires")
            submitted = st.form_submit_button("Ajouter le Livre")

            if submitted:
                max_id = con_books.execute("SELECT MAX(id) FROM books").fetchone()[0]
                new_id = max_id + 1 if max_id is not None else 1
                con_books.execute("INSERT INTO books (id, title, author, genre, date_read, rating, comments) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                  (new_id, title, author, genre, date_read, rating, comments))
                st.success("📖 Nouveau livre ajouté !")

    books_df = con_books.execute("SELECT * FROM books").fetch_df()
    st.subheader("📚 Mes Livres")
    st.dataframe(books_df)

elif st.session_state["active_tab"] == "🎬 Films et Séries":

    with st.sidebar:
        st.header("Ajouter un Film/Série")
        with st.form("films_form"):
            title = st.text_input("Titre")
            realisator = st.text_input("Réalisateur ou Réalisatrice")
            genre = st.selectbox("Genre", ["Classique", "Horreur", "SF", "Fantasy", "Policier", "Romance", "Fiction Historique", "Comédie"])
            date_watch = st.date_input("Date de Visionnage")
            rating = st.slider("Note (1-5)", 1, 5, 3)
            comments = st.text_area("Commentaires")
            submitted = st.form_submit_button("Ajouter le Film/Série")

            if submitted:
                max_id = con_films.execute("SELECT MAX(id) FROM films").fetchone()[0]
                new_id = max_id + 1 if max_id is not None else 1
                con_films.execute("INSERT INTO films (id, title, realisator, genre, date_watch, rating, comments) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                  (new_id, title, realisator, genre, date_watch, rating, comments))
                st.success("🎬 Nouveau film/série ajouté !")

    films_df = con_films.execute("SELECT * FROM films").fetch_df()
    st.subheader("🎬 Mes Films et Séries")
    st.dataframe(films_df)

elif st.session_state["active_tab"] == "🖼 Expositions":

    with st.sidebar:
        st.header("Ajouter une Exposition")
        with st.form("expo_form"):
            title = st.text_input("Nom de l'Exposition")
            place = st.text_input("Lieu")
            artist = st.text_input("Artiste(s) ou Sujet(s)")
            date_visit = st.date_input("Date de visite de l'Exposition")
            rating = st.slider("Note (1-5)", 1, 5, 3)
            comments = st.text_area("Commentaires")
            submitted = st.form_submit_button("Ajouter l'Exposition")

            if submitted:
                max_id = con_expo.execute("SELECT MAX(id) FROM expo").fetchone()[0]
                new_id = max_id + 1 if max_id is not None else 1
                con_expo.execute("INSERT INTO expo (id, title, place, artist, date_visit, rating, comments) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                 (new_id, title, place, artist, date_visit, rating, comments))
                st.success("🖼 Nouvelle exposition ajoutée !")

    expo_df = con_expo.execute("SELECT * FROM expo").fetch_df()
    st.subheader("🖼 Mes Expositions")
    st.dataframe(expo_df)
