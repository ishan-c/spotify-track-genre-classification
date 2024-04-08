# Spotify Track Genre Classification

## Project Overview
This project aims to develop a machine learning model capable of classifying Spotify tracks into genres based on audio features obtained via the Spotify API. The objective is to explore the predictability of genres from these features and to refine my skills in data collection, processing, visualization, and the application of machine learning techniques. No portion of this project, including the dataset, models, and findings will now or in the future be used for commercial purpose; this is a purely a learning exercise.

Exploratory data analysis (EDA) was performed using Pandas and Seaborn to understand the organize and visualize the Spotify-provided features and assess their suitability for training. The primary challenge of the dataset is the development of a useful label, as genre tags are only provided at the artist level and the tags exhibit very high cardinality. In other words, there are many highly-specific genres which greatly increases the sparsity of labels.

Utilities from pandas, scikit-learn, and scikit-multilearn were leveraged for feature engineering and label representation, the latter of which was achieved through hierarchical clustering.

Presently, several modeling options from scikit-learn are being evaluated and future development will include using neural network models for prediction. There are no plans for deployment or maintaining the model, as the end goal is to learn from and compare the performance of the various modeling options.

### Status
This project is a work-in-progress. EDA, feature engineering, and some initial modeling is complete. Model selection and tuning is in progress. Building and tuning neural network models will be the next step.

## Data Source and Collection
The dataset used in this project was obtained through the Spotify Web API. I acknowledge that all data are the intellectual property of Spotify and their respective parties, such as recording artists and labels. As previously stated, the analyses, models, and findings from this project are intended exclusively for academic exploration and carry no commercial intent. In this spirit, none of the datasets or models will be publicly released, and only project findings are shared here for educational purposes.

To create the dataset, the Spotify search was used to identify large (50+ tracks) and popular playlists for various musical genres, starting with broad "fundamental" genres such as "rock" and then for large sub-genres or regional genres such as "metal" or "Bollywood", as respective examples. The name of the genre was the search query in the Spotify playlist search in all cases. A total of 103 playlist IDs were compiled and served as the initial input to a custom data ingestion script.

The data ingestion script first iterates over each playlist id, and then each track id within the playlists, ignoring repeats. For each track it queries the track data endpoint for general information such as titles and duration, as well as the audio features endpoint for musical characteristics such as tempo, volume, and energy. If a track's artist or artists are new to the dataset, the artist endpoint is also queried for artist-level data such as follower count and most importantly genre tags. This process yielded a dataset of 11,489 tracks associated with 7,346 artists, encompassing a wide array of audio features and metadata. For a detailed breakdown of the dataset and the specific features collected, please refer to the EDA notebook.

## Technology Stack
Please see the environment.yml file for an up-to-date and full set of dependencies.
- **Language**: python, Jupyter Notebook
- **Data Processing and Visualization**: Pandas, Seaborn
- **Modeling**: scikit-learn, scikit-multilearn, PyTorch (planned)

## Project Structure

### Data Storage
- **Ingest**: The `/integrations/spotify` subdirectory contains the scripts used to ingest the dataset. These handle API authentication as well as HTTP requests, file creation, and logging. 
- **Raw Data**: raw data consists of four files in `/data` (not public). These include two files keeping track of known track and artist ids, as well as two files with the raw track and artist level data.
- **Processed Data**: After conducting Exploratory Data Analysis (EDA), preliminary data is also saved in the `/data`, as is the pickled custom `Dataset` object resulting from feature engineering. A few manual data transforms were also conducted in the process of clustering genre labels, and those can be found in the `/clustering` directory.

### Notebooks
- **EDA and Preprocessing**: Key insights, visualizations, and early transformations from EDA are documented in `/notebooks/eda.ipynb`.
- **Feature Engineering**: The `/notebooks` directory also contains notebooks for more in-depth feature transformations in `feature_engineering.ipynb`. This is also where a baseline modeling and evaluation scheme is introduced in order to test the relative contributions of features. This process also introduces and motivates the need for developing custom labels for the dataset, documented in `label_clustering.ipynb`
- **Model Exploration**: The evaluation, tuning, and comparison of various modeling options is being conducted in `model_exploration.ipynb`. As this process continues, this notebook may be split into smaller, more specific notebooks.

### Models, Experiments, and Other Utilities
- The `/models` directory includes `setup.py` to create and initialize estimators as specified in `config.py`. The latter will likely be split into multiple files for clarity and scalability as the number of modeling options expands.
- The `/evaluation` directory contains definitions for custom classes, including: 
  - `Experiment`: Stores a set of trained models alongside their associated dataset and metrics.This class also logs relevant information from these entities to MLFlow experiment tracking. Local copies of some instances are pickled and stored in `/experiments` (not publicly shared).
  - `Metrics`: A utility class to calculate, store, and present metrics relevant to the model runs of this project. Instances of this class are stored in the attributes of the `Experiment` class.
- The `utils` directory contains the `Dataset` class, which is used to store and split datasets used for modeling, as well as relevant metadata. The classification task is being treated as a multi-label problem, so the process of splitting the dataset is a bit more complicated than normal. An instance of `Dataset` is produced by the feature engineering notebook and these are also stored in instances of `Experiment`. 
- As the project continues, additional classes or processing steps are expected in order to improve or expand workflows as needed.

## Methodology

This project is being conducted in iterative phases, with each stage building upon the insights and outputs of the previous ones, although work across these phases is interrelated and not strictly sequential.

1. **Data Acquisition**: The initial stage involved the planning and execution of a comprehensive and representative dataset using the Spotify API, aiming for diversity in musical genres and audio features.

2. **Data Exploration**: Exploratory data analysis using Pandas and Seaborn was crucial for understanding both the features and labels of the dataset. Identifying patterns and relationships within and between these fields laid the initial groundwork for subsequent modeling efforts.

3. **Feature Engineering**: Leveraging insights from EDA, this process selects and transforms fields in the raw dataset into a format more suitable and useful for modeling. Special emphasis was placed on transforming label data to mitigate challenges posed by its high-dimensional and sparse nature.

4. **Model Selection and Development** (In Progress): This iterative process involves testing, evaluating, and tuning models from scikit-learn to gauge their relative efficacy for capturing the relationship between the features and labels.  Future work will extend into developing and fine-tuning neural network models to explore their potential advantages for this task.

5. **Reporting** (Future): The culmination of the project will involve the analysis and discussion of the modeling outcomes, detailing the performance of various approaches, notable findings, and key takeaways. This phase will also reflect on the project’s methodology, highlighting improvements, challenges encountered, and potential applications of the learned insights to similar problems in the music domain or beyond.
