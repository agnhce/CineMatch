import re
import pymysql  # ✅ Use pymysql consistently

def preprocess(text):
    """Normalize and preprocess text for bigram matching."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text

def generate_bigrams(text):
    """Generate bigrams from a given text."""
    text = preprocess(text)
    tokens = text.split()
    bigrams = set()
    for token in tokens:
        bigrams.update([token[i:i+2] for i in range(len(token) - 1)])
    return bigrams

def calculate_similarity(bigrams1, bigrams2):
    """Calculate Jaccard similarity between two bigram sets."""
    intersection = len(bigrams1 & bigrams2)
    union = len(bigrams1 | bigrams2)
    return intersection / union if union > 0 else 0

def fetch_records_from_db(cursor, table_name):
    """Fetch records from the specified table."""
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def match_record(incoming_record, reference_records):
    """Find the best match for an incoming record."""
    best_match = None
    best_score = 0

    incoming_text = " ".join(str(incoming_record.get(field, "")) for field in ["title", "director", "release_year"])
    incoming_bigrams = generate_bigrams(incoming_text)

    for ref_record in reference_records:
        ref_text = " ".join(str(ref_record.get(field, "")) for field in ["title", "director", "release_year"])
        ref_bigrams = generate_bigrams(ref_text)

        score = calculate_similarity(incoming_bigrams, ref_bigrams)

        if score > best_score:
            best_score = score
            best_match = ref_record

    return best_match, best_score

def matching_engine():
    """Match all incoming records to the reference dataset."""
    try:
        db = pymysql.connect(
            host="localhost",
            user="root",
            password="9433480703",  # ✅ Replace with your actual password
            database="matching_engine"
        )
        cursor = db.cursor()

        # Fetch records
        incoming_catalog = fetch_records_from_db(cursor, "incoming_catalog")
        reference_dataset = fetch_records_from_db(cursor, "reference_dataset")

        print("\n--- Matching Results ---\n")

        # Perform matching
        for incoming_record in incoming_catalog:
            match, score = match_record(incoming_record, reference_dataset)

            print(f"Incoming Movie: {incoming_record['title']} ({incoming_record['director']}, {incoming_record['release_year']})")
            if match and score > 0.01:
                print(f"  → Matched With: {match['title']} ({match['director']}, {match['release_year']})")
                print(f"  → Similarity Score: {score * 100:.2f}%\n")
            else:
                print("  → No good match found.\n")

        cursor.close()
        db.close()
    except pymysql.MySQLError as e:
        print("❌ Database Error:", e)

if __name__ == "__main__":
    matching_engine()
