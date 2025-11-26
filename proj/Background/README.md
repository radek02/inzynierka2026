# Overview
Worker services, now consitst of scripts, in future scripts will be used with cloud first aproach and managed by GCP.

All scripts have common .env file, which must be located in Background/ directory and should be fullfilled according to .env.example template.

# To run script

## .env
Create .env file in Background\ directory, fill .env file according to .env.example

## Install dependencyes
Run the following command from Background\ directory:
```
pip install -r requirements.txt
```    
## Run script
```
python {script_folder}\main.py
```

# Current scripts

## UploadToVectorDb
This script insert user and item embeddings which was previosly generated and stored at local machine into vector database (we chose Qdrant database). Script insert all embeddings and create indexing.

To run this script you should call following command from Background\ directory:
```
python .\UploadToVectorDb\main.py
```