import pymysql

# Function to connect to the database
def connect_db():
    """Connect to the MySQL database using PyMySQL."""
    return pymysql.connect(
        host="localhost",
        user="root",  
        password="9433480703", 
        database="matching_engine",
        cursorclass=pymysql.cursors.DictCursor
    )

# Function to calculate similarity between input movie and reference movie
def calculate_similarity(input_movie, reference_movie):
    """Calculate similarity score."""
    fields = ["title", "director", "release_year"]
    match_score = 0

    for field in fields:
        input_value = input_movie.get(field, "").lower()
        reference_value = str(reference_movie.get(field, "")).lower()
        if input_value and reference_value and input_value == reference_value:
            match_score += 1

    return match_score / len(fields)  # Normalize the score

# Function to search for matching movies in the database
def search_movies(input_title, input_director, input_release_year):
    db = connect_db()
    cursor = db.cursor()

    # Fetch the reference dataset from the database
    cursor.execute("SELECT title, director, release_year FROM reference_dataset")
    reference_dataset = cursor.fetchall()

    # Perform matching
    matches = []
    for ref_movie in reference_dataset:
        score = calculate_similarity(
            {"title": input_title, "director": input_director, "release_year": input_release_year},
            ref_movie
        )
        if score > 0.01:  # Only add matches with a score greater than 1%
            matches.append({"movie": ref_movie, "score": score})

    # Sort matches by the highest score
    matches = sorted(matches, key=lambda x: x["score"], reverse=True)

    cursor.close()
    db.close()

    return matches

# CLI interface
def main():
    print("Welcome to the Movie Matching Engine!")
    title = input("Enter movie title: ").strip()
    director = input("Enter director: ").strip()
    release_year = input("Enter release year (optional): ").strip()

    if not release_year:
        release_year = None

    matches = search_movies(title, director, release_year)

    if matches:
        print("\nMatching Movies Found:")
        for match in matches:
            movie = match["movie"]
            score = match["score"]
            print(f"{movie['title']} ({movie['director']}, {movie['release_year'] if movie['release_year'] else 'N/A'}) - Score: {score*100:.1f}%")
    else:
        print("No matching movies found.")

if __name__ == "__main__":
    main()
