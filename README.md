# FIFA21 Players Search System - Data Sorting and Searching Final Project

## Overview

This project, developed for the Data Sorting and Searching course under Professor João Comba, implements a sophisticated search system for the FIFA21 Players dataset, sourced from Kaggle and extracted from https://sofifa.com. The dataset includes comprehensive player data from FIFA 15 to FIFA 21, covering 18,944 players, 24,188,078 user ratings, and 362,700 free-text tags. The project demonstrates advanced data structures and sorting algorithms to enable efficient queries, highlighting the importance of optimized data retrieval in large-scale datasets.

The significance of this project lies in its real-world applicability, simulating a recommendation or analysis system for sports data. It integrates complex data structures (Hash Tables, TRIE, and custom indexing) with sorting mechanisms to handle large datasets efficiently, preparing students for challenges in data science, database management, and algorithmic optimization. The project also encourages innovation through optional graphical interfaces and new query types, fostering creativity and practical problem-solving.

## Project Structure

The project processes three main datasets:
- **players.csv**: Contains details for 18,944 players (sofifa_id, short/long names, positions, nationality, club, league).
- **rating.csv**: Includes 24,188,078 user ratings (1-5) for players, with a smaller `minirating.csv` for testing.
- **tags.csv**: Contains 362,700 free-text tags (e.g., "Brazil", "Speedster") associated with players.

The system operates in two phases:
1. **Preprocessing**: Builds data structures within a 3-minute limit (bonus for under 1 minute).
2. **Query Processing**: Handles interactive console-based queries for player data.

### Data Structures Implemented
1. **Hash Table for Players (Estrutura 1)**:
   - Stores player data with `sofifa_id` as the key.
   - Includes computed fields like global rating average and rating count from `rating.csv`.
   - Uses open addressing with chaining to handle collisions, ensuring O(1) average-case lookup.

2. **TRIE for Long Names (Estrutura 2)**:
   - Supports prefix-based searches on players' long names.
   - Stores `sofifa_id` at leaf nodes to link to player data.
   - Enables efficient retrieval of players matching a name prefix, critical for autocomplete-like functionality.

3. **Hash Table for User Ratings (Estrutura 3)**:
   - Indexes user ratings by `user_id`, storing lists of rated players and their scores.
   - Facilitates queries about players rated by a specific user, with sorting by user rating and global average.

4. **TRIE for Tags (Estrutura 4)**:
   - Indexes tags from `tags.csv`, mapping each tag to a set of `sofifa_id`s.
   - Supports intersection queries to find players associated with multiple tags.
   - Optimizes tag-based searches, handling free-text annotations efficiently.

### Sorting Algorithms Implemented
The project incorporates sorting algorithms to order query results, ensuring clarity and relevance:
- **Merge Sort (or Python's Timsort)**: Used for sorting query results by global rating (descending), user rating (primary), or secondary criteria (e.g., global rating for tie-breaking). Timsort, Python’s built-in sorting algorithm, provides O(n log n) performance with stability, ideal for handling large result sets.
- **Custom Comparator**: Implements multi-level sorting (e.g., primary by user rating, secondary by global rating) for queries like `user` and `tags`.
- **Filtering**: Applied in queries like `top`, where players are filtered by position and minimum rating count (1,000) before sorting, reducing computational overhead.

These sorting mechanisms ensure that query outputs are presented in a user-friendly, tabulated format using the `PrettyTable` library, with precise formatting (e.g., 6-decimal global ratings).

## Queries Supported
The system supports four query types, each leveraging specific data structures and sorting:
1. **Player Prefix Search (`player <prefix>`)**:
   - Uses TRIE to find players whose long names start with the given prefix.
   - Returns player details sorted by global rating (descending).
   - Example: `player FER` lists players like Fernando Torres.

2. **User Ratings Search (`user <userID>`)**:
   - Retrieves up to 20 players rated by a user, sorted by user rating (primary) and global rating (secondary).
   - Uses the user ratings Hash Table for fast lookup.
   - Example: `user 106180` shows rated players with their scores.

3. **Top Players by Position (`top <N> <position>`)**:
   - Returns the top N players for a position with at least 1,000 ratings, sorted by global rating.
   - Filters players by position before sorting for efficiency.
   - Example: `top 10 ST` lists top strikers.

4. **Tag Intersection Search (`tags <list of tags>`)**:
   - Finds players associated with all specified tags, sorted by global rating.
   - Uses TRIE for tags to compute intersections of player IDs.
   - Example: `tags Brazil Dribbler` lists Brazilian dribblers.

## Implementation

The code is implemented in **Python**, emphasizing custom data structures and algorithms:
- **Hash Tables**: Custom implementation with chaining for collision resolution, used for players and ratings.
- **TRIE**: Built from scratch for name and tag searches, supporting prefix and exact matching.
- **File Processing**: Reads CSV files efficiently, with timing logs to monitor preprocessing performance.
- **Query Interface**: Console-based input loop with tabulated outputs via `PrettyTable`.
- **Sorting**: Leverages Python’s sorting with custom comparators for multi-criteria ordering.

### Key Features
- **Efficiency**: Preprocessing completes within 3 minutes, with potential for a 5% bonus if under 1 minute.
- **Modularity**: Separates data structure initialization, query processing, and output formatting for maintainability.
- **Error Handling**: Validates inputs and handles edge cases (e.g., missing players or tags).
- **Custom Implementation**: Avoids high-level libraries (e.g., dictionaries, databases) as per requirements, ensuring all structures are built from scratch.

## Importance of the Project

This project is a cornerstone of the Data Sorting and Searching course, demonstrating the practical application of advanced data structures and algorithms. It mirrors real-world systems like sports analytics platforms, search engines, or recommendation systems, where efficient data retrieval and sorting are critical. By handling a large dataset (over 400MB for ratings), it prepares students for big data challenges, emphasizing:
- **Scalability**: Managing millions of records with optimized structures.
- **Performance**: Balancing preprocessing and query response times.
- **Algorithmic Thinking**: Combining multiple data structures (Hash, TRIE) and sorting techniques for complex queries.
- **Innovation**: Encouraging bonuses for fast preprocessing, graphical interfaces, or new queries, fostering creativity.

The project’s complexity—integrating multiple data structures, large-scale data processing, and precise sorting—makes it a significant academic and practical achievement, equipping students with skills for data-intensive applications.

## How to Run

1. **Prerequisites**: Python 3.x with `prettytable` installed (`pip install prettytable`).
2. **Input Files**: Place `players.csv`, `rating.csv`, and `tags.csv` in the same directory as the script.
3. **Execution**:
   ```bash
   python fifa21_search.py
