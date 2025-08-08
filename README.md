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
