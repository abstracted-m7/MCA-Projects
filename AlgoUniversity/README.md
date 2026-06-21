# AI Product Intelligence System

A Gen AI Bootcamp Day 2 project that uses **CLIP embeddings** and **FAISS vector search** to power three smart e-commerce features on top of a fashion product catalog:

1. **Smart Product Recommendation Engine** — suggests complementary products
2. **Unique Product Catalog Creation** — automatically removes duplicate/near-duplicate product listings
3. **Reverse Product Search** — search for products using plain text instead of an image

---

## 📌 Overview

Traditional product search relies on manually written tags and categories. This project instead converts every product **image** into a 512-number vector ("embedding") using OpenAI's **CLIP** model. Products that look visually similar end up with similar vectors — which makes searching, comparing, and grouping products possible without any manual labeling.

```
Dataset Images  →  CLIP Vision Encoder  →  Image Embeddings  →  FAISS Index
```

That single embedding index is then reused to power all three features.

---

## 🗂️ Dataset

This project uses the **Fashion Product Images (Small)** dataset from Kaggle:
🔗 https://www.kaggle.com/code/sahandakramipour/fashion-product-images-small

You will need:
- `styles.csv` — product metadata (id, gender, category, article type, color, display name, etc.)
- `images/` — a folder of product photos named `<product_id>.jpg`

Place both in the project's root folder before running the notebook.

---

## ⚙️ Setup

### Requirements

- Python 3.9+
- Jupyter Notebook

### Install dependencies

```bash
pip install transformers torch faiss-cpu pandas pillow tqdm scikit-learn matplotlib
```

| Library | Purpose |
|---|---|
| `transformers` | Loads and runs the CLIP model |
| `torch` | Backend for running CLIP |
| `faiss-cpu` | Fast similarity search across embeddings |
| `pandas` / `numpy` | Data handling |
| `pillow` (PIL) | Image loading |
| `tqdm` | Progress bars while processing images |
| `scikit-learn` | DBSCAN clustering for duplicate detection |
| `matplotlib` | Displaying result images |

---

## 🏗️ Project Structure

```
.
├── task2.ipynb                  # Main notebook — all 3 tasks
├── styles.csv                   # Product metadata (from Kaggle dataset)
├── images/                      # Product photos (from Kaggle dataset)
├── product_embeddings.npy       # Generated: CLIP embeddings for all products
├── product_metadata.csv         # Generated: cleaned metadata aligned with embeddings
├── fashion_index.faiss          # Generated: FAISS vector index
└── README.md
```

The three files marked **"Generated"** are created automatically the first time you run the notebook — you don't need to create them yourself.

---

## ▶️ How to Run

Open `task2.ipynb` in Jupyter and run the cells **in order, top to bottom**. The notebook is organized into clear sections:

### 1. Build the Embeddings (run once)
Loads `styles.csv`, runs every product image through CLIP, and saves:
- `product_embeddings.npy` — a (N × 512) matrix of image embeddings
- `product_metadata.csv` — matching product info for each embedding

> ⏱️ This step processes the full dataset and can take a while (~35–40 minutes for ~44,000 images on CPU). It only needs to be run once — after that, the saved `.npy` and `.csv` files are reused.

### 2. Build the FAISS Index (run once)
Loads the saved embeddings and builds a FAISS index (`fashion_index.faiss`) for fast nearest-neighbor search.

### 3. Task 1 — Recommendation Engine
Run the `recommend(category)` function with any category name (e.g., `"Shoes"`) to get a list of complementary product categories.

```python
recommend("Shoes")
# → ['Socks', 'Fitness Watch', 'Water Bottle']
```

### 4. Task 2 — Unique Product Catalog
Runs DBSCAN clustering on the embeddings to group visually similar/duplicate products, then builds a catalog with one representative item per group. Displays a sample grid of the resulting catalog.

### 5. Task 3 — Reverse Product Search
Type any text query into the `query` variable (e.g., `"blue casual shirt"`) and run the search cell to get the top 5 closest-matching products, along with similarity scores and a visual preview.

```python
query = "blue casual shirt"
# → Top 5 matches displayed with similarity scores
```

---

## 🧠 How Each Feature Works

### 1. Smart Product Recommendation Engine
Uses a simple, transparent **category → complementary categories** rule map (e.g., Shoes → Socks, Fitness Watch, Water Bottle). This keeps the logic fast, explainable, and easy to extend without needing purchase-history data.

### 2. Unique Product Catalog Creation
Applies **DBSCAN clustering** (cosine similarity) on the CLIP embeddings to automatically group visually similar products — without needing to know the number of groups in advance. One representative product is kept per cluster to form the final catalog.

### 3. Reverse Product Search
CLIP can encode **both images and text into the same vector space**. A typed search phrase is converted into a 512-number vector using CLIP's text encoder, then compared against all stored image embeddings using FAISS to retrieve the closest matches.

---

## 📊 Results Summary

| Task | Result |
|---|---|
| Recommendation Engine | `recommend("Shoes")` → Socks, Fitness Watch, Water Bottle ✅ matches expected example |
| Catalog Deduplication | 15,596 products scanned → 45 unique catalog groups → 15,551 duplicates removed |
| Reverse Search | Query `"blue casual shirt"` → top 5 results were all genuinely blue, casual-style shirts |

A full write-up with screenshots is available in the accompanying project report (`AI_Product_Intelligence_Report.docx`).

---

## 🔧 Tech Stack

- **CLIP** (`openai/clip-vit-base-patch32`) via Hugging Face Transformers
- **FAISS** (`IndexFlatIP`) for vector similarity search
- **DBSCAN** (scikit-learn) for duplicate/near-duplicate clustering
- **Pandas / NumPy** for data handling
- **Matplotlib / PIL** for visualizing results

---

## 🚀 Future Improvements

- Replace the rule-based recommendation map with a model trained on real co-purchase data
- Tune the DBSCAN `eps` parameter for tighter, more precise duplicate detection
- Add a simple web interface (e.g., Streamlit) for live, interactive text search
- Cache the CLIP model load across tasks to avoid reloading it multiple times in the notebook

---

## 📄 License

This project was built as part of a Gen AI Bootcamp homework challenge. Dataset credit: [Fashion Product Images (Small)](https://www.kaggle.com/code/sahandakramipour/fashion-product-images-small) on Kaggle.
