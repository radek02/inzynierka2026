# Deploy PostgreSQL to Cloud SQL (Quick Guide)

## 1. Setup GCP

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud services enable sqladmin.googleapis.com
```

## 2. Create Database Instance

```bash
gcloud sql instances create interactions-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=europe-central2 \
  --storage-size=10GB \
  --storage-auto-increase
```

Takes 5-10 minutes.

## 3. Set Password & Create Database

```bash
# Set password
gcloud sql users set-password postgres \
  --instance=interactions-db \
  --password=postgres # TODO: think of a proper way

# Create database
gcloud sql databases create interactions \
  --instance=interactions-db
```

## 4. Allow all IPs
Temporary solution, ideally we would use Cloud SQL proxy and rely on IAM.

```bash
# Add it to authorized networks
gcloud sql instances patch interactions-db \
  --authorized-networks=0.0.0.0/0 # unsafe, but anyway
```

## 5. Get Connection Info

```bash
# Get public IP
gcloud sql instances describe interactions-db \
  --format="value(ipAddresses[0].ipAddress)"
```

## 6. Update .env

Edit `proj/Database/.env`:

```env
POSTGRES_HOST=<IP_FROM_ABOVE>
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<YOUR_PASSWORD>
POSTGRES_DB=interactions
```

## 7. Load Data

```bash
cd proj/Database
source ../.venv/bin/activate
python load_interactions.py
```

## 8. Verify

```bash
gcloud sql connect interactions-db --user=postgres

# In psql:
\c book_recommendations
SELECT * FROM interaction_stats;
```

## Cost

~$10-15/month for `db-f1-micro`

## Cleanup

```bash
gcloud sql instances delete book-recommendations-db
```
