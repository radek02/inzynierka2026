# inzynierka2026

- info od MINI: https://ww2.mini.pw.edu.pl/studia/dziekanat/dla-dyplomantow-i-promotorow/
- strona tytułowa w Latex-ie: https://www.overleaf.com/7716428695mdnjbntsnrfg#d61846
- praca [WIP] w Latex-ie: https://www.overleaf.com/5289876111rwckkmxhscjm#8ab58c

# Zadania proponowane przez pana Małysza w zgłoszeniu:

## 1. Data Familiarization & Loading
- Download JSONL files and load key tables:
  - Ratings  
  - Reviews  
  - Books  
  - Shelves  

## 2. Exploratory Data Analysis (EDA)
- Examine rating distributions  
- Analyze user activity levels  
- Assess shelf popularity  

## 3. Data Preparation
- Clean review texts:
  - Remove stop words  
  - Remove special characters  
- Extract features:
  - TF-IDF vectors  
  - Text embeddings (Sentence-BERT)  
  - Encode shelves as categorical features  
- Filter users with fewer than 5 ratings to reduce data sparsity  
- Subsample 10% of the dataset for initial experiments, scaling to the full dataset for final evaluation  

## 4. Algorithm Implementation
- **Collaborative Filtering:** e.g., SVD, ALS  
- **Content-Based:** cosine similarity on descriptions/reviews, comparing TF-IDF with Sentence-BERT  
- **Hybrid:** weighted combination of CF and CB, or a simple neural network combining latent factors and text embeddings  
- *(Optional)*: Construct a bipartite user–book graph and apply node embeddings  

## 5. Model Evaluation
- Define a validation protocol:
  - Temporal train–test split (80% training, 20% testing) based on rating timestamps  
- Compute metrics:
  - Precision@5, Precision@10  
  - Recall@5, Recall@10  
  - NDCG@10  
- Compare model performances and visualize results (e.g., comparative plots)  

## 6. Optimization & Tuning
- Tune hyperparameters (e.g., latent-space dimensionality, regularization strength)  
- Explore dimensionality reduction techniques (e.g., SVD, PCA)  
- Pre-compute TF-IDF vectors/embeddings and store in compressed formats  

## 7. Documentation & Presentation
- Document methodology in a report, including a flowchart of the pipeline (data processing, training, evaluation)  
- Present experimental results, conclusions, and future work directions  
- Deliver documented code, a written report, and a presentation  
