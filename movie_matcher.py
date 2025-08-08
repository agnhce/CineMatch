import streamlit as st
import mysql.connector
from streamlit.components.v1 import html
import random
import pymysql
# Custom CSS for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Database connection function (same as before)
def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="9433480703",
        database="matching_engine",
        cursorclass=pymysql.cursors.DictCursor  # ✅ THIS enables dictionary-like rows
    )

# Similarity calculation function (same as before)
def calculate_similarity(input_movie, reference_movie):
    """Calculate similarity score."""
    fields = ["title", "director", "release_year"]
    match_score = 0

    for field in fields:
        input_value = str(input_movie.get(field, "")).lower() if field != "release_year" else input_movie.get(field, "")
        reference_value = str(reference_movie.get(field, "")).lower() if field != "release_year" else reference_movie.get(field, "")
        
        if input_value and reference_value:
            if field == "release_year":
                # For years, consider exact matches or close matches
                if input_value == reference_value:
                    match_score += 1
                elif abs(int(input_value) - int(reference_value)) <= 2:  # Consider years within 2 years as partial match
                    match_score += 0.5
            else:
                # For text fields, exact match
                if input_value == reference_value:
                    match_score += 1

    return match_score / len(fields)  # Normalize the score

# Search function (same as before)
def search_movies(input_title, input_director, input_release_year):
    db = connect_db()
    cursor = db.cursor()

    # Convert year to int if it exists
    try:
        release_year = int(input_release_year) if input_release_year else None
    except (ValueError, TypeError):
        release_year = None

    cursor.execute("SELECT title, director, release_year FROM reference_dataset")
    reference_dataset = cursor.fetchall()

    matches = []
    for ref_movie in reference_dataset:
        score = calculate_similarity(
            {"title": input_title, "director": input_director, "release_year": release_year},
            ref_movie
        )
        if score > 0.01:
            matches.append({"movie": ref_movie, "score": score})

    matches = sorted(matches, key=lambda x: x["score"], reverse=True)

    cursor.close()
    db.close()

    return matches

# Main Streamlit app
def main():
    # Load custom CSS
    local_css("D:/MatchingEngineProject/style.css")    
    # App header
    st.markdown("""
    <div class="header">
        <h1>CineMatch</h1>
        <p class="subtitle">Discover matching movies from our extensive database</p>
    </div>
    """, unsafe_allow_html=True)

    # Search form
    with st.form("search_form"):
        st.markdown("<h2 class='search-title'>Find Movie Matches</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        title = st.text_input("Movie Title", placeholder="Enter movie title", key="title")
        director = col1.text_input("Director", placeholder="Enter director name", key="director")
        year = col2.number_input("Release Year", min_value=1900, max_value=2023, step=1, 
                                placeholder="Enter release year", key="year")
        
        submitted = st.form_submit_button("Find Matches", use_container_width=True)
    
    # Process form submission
    if submitted:
        with st.spinner('Searching for matches...'):
            matches = search_movies(title, director, year if year else None)
        
        if matches:
            st.markdown("<h2 class='results-title'>Matching Results</h2>", unsafe_allow_html=True)
            
            # Display results in columns
            cols = st.columns(2)
            for i, match in enumerate(matches):
                movie = match["movie"]
                score = match["score"]
                
                with cols[i % 2]:
                    st.markdown(f"""
                    <div class="match-card">
                        <h3 class="match-title">{movie['title']}</h3>
                        <p class="match-director">Directed by {movie['director']}</p>
                        <p class="match-year">Released in {movie['release_year'] if movie['release_year'] else 'N/A'}</p>
                        <div class="score-meter">
                            <div class="score-fill" style="width: {score * 100}%"></div>
                        </div>
                        <span class="match-score">{score * 100:.1f}% Match</span>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="no-results">
                No matching movies found. Try different search terms.
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()