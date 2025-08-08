# CineMatch
A modern Streamlit + MySQL powered application that matches incoming movies, TV series, and episodes to an existing reference catalog using Jaccard similarity with bigrams. Features a clean, responsive UI, advanced search capabilities, and match scoring with visual indicators.

✨ Features

- **Near Real-Time Matching**  
  Quickly matches incoming records against a large-scale reference dataset.

- **Intelligent Fuzzy Matching**  
  Uses **Jaccard Similarity on Bigrams** for robust, typo-tolerant matching.

- **Multi-Entity Support**  
  Handles Movies, TV Series, and Episodes with entity-specific key fields:
  - 🎥 Movies → Title, Director, Release Year  
  - 📺 TV Series → Title, Director  
  - 🎞 Episodes → Title, Season No., Episode No.

- **Optimized for Accuracy & Speed**  
  Implements efficient bigram indexing for fast lookups.

- **Web-Based Interface**  
  Built with Flask for interactive querying and result visualization.

 🏗 Architecture
Incoming Data ➜ Preprocessing & Bigram Tokenization ➜ Similarity Scoring ➜ Match Decision ➜ Database Update

## 🛠 Tech Stack

| Category        | Technologies |
|-----------------|--------------|
| **Backend**     | Python 3.11 |
| **Database**    | MySQL |
| **Algorithm**   | Jaccard Similarity (Bigrams) |
| **Deployment**  | Localhost |

📐 Matching Algorithm

- **Jaccard Similarity on Bigrams:-**
- 
Convert strings to lowercase.

Break into character bigrams.

Compute intersection and union sizes.

Similarity = Intersection / Union.

This approach allows for fuzzy matching and typo tolerance while maintaining efficiency.



-**Screenshots**

<img width="1913" height="973" alt="image" src="https://github.com/user-attachments/assets/80b649d6-733d-4788-a292-f116253e81bf" />
<img width="1896" height="978" alt="image" src="https://github.com/user-attachments/assets/ced9be81-b308-49ef-afec-d2f72bc4c404" />


-**Author:** Avigayan Ghosh
