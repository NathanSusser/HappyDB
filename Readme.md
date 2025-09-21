# The Structure of Happy Experiences Repository Structure

This document provides a comprehensive overview of the repository structure and the purpose of each directory and file for academic publication.

## Repository Overview

This repository contains code and data for analyzing happiness moments from the HappyDB corpus using various psychological scales and computational methods. The analysis pipeline involves data cleaning, psychological coding via OpenAI's GPT models, factor analysis, and situational analysis.

## Directory Structure

```
happyDB/
├── data_Cleaning/                    # Data preprocessing and cleaning scripts
├── dataframes/                      # Processed datasets in CSV format
├── factor_correlation analysis/     # Factor analysis and correlation studies
├── happydb/                        # Original HappyDB corpus data
├── OpenAI/                         # GPT-based psychological coding pipeline
├── Ratings data/                   # Rating matrices and filtered data
├── situation analysis/             # Situational context analysis
└── README.md                       # Original repository documentation
```

---

## Detailed Directory Documentation

### `data_Cleaning/`
Contains Python scripts for data preprocessing and transformation.

#### Files:
- **`change_items.py`**: Cleans and standardizes item text by removing prefixes (e.g., "How much does this experience indicate") and renaming columns for consistency across psychological scales.

- **`remove_random_columns_pwb.py`**: Data cleaning utility that removes unnecessary columns (Unnamed: 3-7) from PWB (Psychological Well-Being) scale data.

- **`reverse_coded.py`**: Handles reverse-coded items in psychological scales by:
  - Identifying items that require reverse coding
  - Applying reverse transformation (scale_max + 1 - original_value)
  - Creating datasets with proper directional scoring

### `dataframes/`
Processed datasets ready for analysis.

#### Files:
- **`clean_sentences.csv`**: Clean happiness moments extracted from HappyDB with hmid, reflection_period, and cleaned_hm columns
- **`scales_df.csv`**: Combined psychological scale items from all instruments (PERMA, PWB, SWLS, etc.) with standardized format

### `factor_correlation analysis/`
Statistical analysis of psychological factors and their relationships.

#### Files:
- **`clustering and networks.ipynb`**: Network analysis and clustering of psychological constructs and items
- **`correlation_factors.ipynb`**: Analysis of correlations between extracted factors
- **`factor_analysis.ipynb`**: Main factor analysis including:
  - Dimensionality reduction of psychological ratings
  - Factor extraction and rotation
  - Interpretation of psychological dimensions

- **`get_results.ipynb`**: Results compilation and summary statistics
- **`inter_scale_correlation.ipynb`**: Correlation analysis between different psychological scales
- **`intra_scale_correlation.ipynb`**: Within-scale correlation analysis
- **`merge_more_items.ipynb`**: Integration of additional psychological items into analysis
- **`numbers and sentences.ipynb`**: Analysis connecting numerical ratings to textual content
- **`remove_failed_sentences.ipynb`**: Quality control by removing sentences that failed processing
- **`reverse_column_names.py`**: Generates standardized column names for reverse-coded items
- **`rotate_factor_analysis.ipynb`**: Factor rotation techniques for improved interpretability

### `happydb/`
Original HappyDB corpus data.

#### Structure:
```
happydb/data/
├── cleaned_hm.csv          # Clean happiness moments with metadata
├── demographic.csv         # Participant demographic information  
├── original_hm.csv         # Raw happiness moments before cleaning
├── senselabel.csv         # Linguistic annotations and supersense labels
├── topic_dict/            # Topic-specific word dictionaries
│   ├── entertainment-dict.csv
│   ├── exercise-dict.csv
│   ├── family-dict.csv
│   ├── food-dict.csv
│   ├── people-dict.csv
│   ├── pets-dict.csv
│   ├── school-dict.csv
│   ├── shopping-dict.csv
│   └── work-dict.csv
└── vad.csv                # Valence, Arousal, Dominance ratings
```

### `OpenAI/`
GPT-based psychological coding pipeline for rating happiness moments.

#### Main Scripts:
- **`batch_gpt_coding.py`**: Main batch processing script that:
  - Uploads JSONL files to OpenAI batch API
  - Creates and manages batch jobs for psychological coding
  - Handles rate limiting and error recovery

- **`batch_processing_creation.py`**: Creates batch request files by:
  - Loading happiness moments and psychological items
  - Generating structured prompts for GPT rating tasks
  - Splitting large datasets into manageable batches (10MB limit)

- **`check_batches.py`**: Monitors batch processing status by:
  - Checking completion status of all submitted batches
  - Identifying failed or invalid batches
  - Parallel processing for efficient status checking

- **`check_file_size.py`**: Utility for verifying batch file sizes before submission

- **`failed_responses_gpt_coding.py`**: Recovery system for handling failed API responses:
  - Reprocesses sentences that failed initial batch processing
  - Uses direct API calls for failed items
  - Maintains data integrity and completeness

- **`retrieve_batches.py`**: Downloads completed batch results from OpenAI API and saves to local files

#### `OpenAI/More Items/` Subdirectory:
Extended psychological coding with additional constructs.

- **`check_input.py`**: Validates input data for extended coding tasks
- **`code - gpt.py`**: Interactive GPT coding for extended psychological dimensions
- **`combine_outputs.py`**: Merges multiple output files from extended coding runs
- **`parralel_code_gpt.py`**: Parallel processing implementation for extended coding with:
  - Concurrent API calls for faster processing
  - Resume functionality for interrupted runs
  - Real-time progress tracking

### `Ratings data/`
Final rating matrices and processed psychological data.

#### Files:
- **`filtered_ratings.csv`**: Quality-controlled ratings after removing invalid responses
- **`ratings_matrix.csv`**: Complete matrix of psychological ratings (sentences × items)

### `situation analysis/`
Analysis of situational contexts in happiness moments.

#### Files:
- **`sit_analysis.ipynb`**: Comprehensive situational analysis including:
  - Contextual factor extraction from happiness moments
  - Relationship between situation and psychological ratings
  - Predictive modeling of happiness from situational features

## Data Processing Pipeline

### 1. Data Preparation
- Clean and standardize happiness moments from HappyDB corpus
- Prepare psychological scale items from multiple validated instruments
- Handle reverse-coded items and ensure proper scoring direction

### 2. Psychological Coding
- Use OpenAI's GPT models to rate happiness moments on psychological dimensions
- Batch processing for efficiency and cost management
- Quality control and error recovery for failed responses

### 3. Factor Analysis
- Extract underlying psychological factors from ratings
- Analyze correlations between factors and scales  
- Validate factor structure and interpretability

### 4. Situational Analysis
- Analyze contextual factors in happiness experiences
- Model relationships between situations and psychological outcomes

## Research Applications

This repository supports research in:
- Computational psychology and well-being measurement
- Natural language processing for psychological assessment  
- Factor analysis of happiness and psychological constructs
- Situational influences on emotional experiences
- Large-scale text analysis using AI models

## Technical Dependencies

- **Python Libraries**: pandas, numpy, scikit-learn, factor_analyzer, openai
- **APIs**: OpenAI GPT-4 and GPT-4-mini models
- **Data Formats**: CSV, JSONL
- **Computing**: Batch processing, parallel execution, concurrent API calls

---

*This documentation supports the academic publication and reproducibility of the The Structure of Happy Experiences.*
