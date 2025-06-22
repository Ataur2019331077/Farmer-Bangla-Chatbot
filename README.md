# 🌾 Bengali Farmer Assistant Chatbot

This project is a **context-aware Bengali question-answering system** for farmers. It uses **multilingual semantic search** (via the E5 embedding model), **MongoDB vector search**, and **Gemini LLM** to respond to agricultural queries with precise, context-driven answers.

---

## 📌 Features

- 🧠 **Semantic Search** using [`intfloat/multilingual-e5-base`](https://huggingface.co/intfloat/multilingual-e5-base)
- 💬 **Query Understanding** in Bengali (or other supported languages)
- 🔍 **MongoDB Vector Search** for paragraph retrieval
- 🤖 **Response Generation** using Google's Gemini API
- 📄 **Text Ingestion Pipeline** that splits, embeds, and stores agricultural content
- 🔁 Interactive command-line chatbot

---

## ⚙️ Technologies Used

- Python 3.11+
- HuggingFace Transformers
- PyTorch
- MongoDB Atlas (with vector search index)
- Gemini API (Google's Generative Language Model)
- dotenv (for secure key management)

---

## 📁 Project Structure

```plaintext
BanglaBot/
├── .env                      # Environment variables
├── rice.txt                  # Input Bengali agricultural text
├── bot.py                    # Main chatbot loop
├── embed.py                  # Embedding and MongoDB storage logic
├── search.py                 # Semantic search using MongoDB
└── README.md                 # Project documentation
```

---

## 🚀 Work Procedure & Flow

### 🔹 Step 1: Text Ingestion and Embedding

1. Read a Bengali text document (`rice.txt`).
2. Split it into paragraphs using regex.
3. Use `intfloat/multilingual-e5-base` model to generate embeddings (mean-pooled CLS vectors).
4. Store each paragraph and its vector in MongoDB with the following structure:

```json
{
  "text": "বীজতলা তৈরি করার জন্য...",
  "embedding": [0.123, -0.456, ...]
}
```

---

### 🔹 Step 2: MongoDB Vector Search Setup

1. Use MongoDB Atlas with **Vector Search** enabled.
2. Create a vector index (`embedding_knn_index`) with:
   - Field: `embedding`
   - Similarity: `cosine`
   - Dimensions: `768`
   - Type: `knnVector`

---

### 🔹 Step 3: Query Workflow

When a user types a Bengali query like:
```
কীভাবে বীজতলা তৈরি করব?
```

The system follows this flow:

1. **Convert Query to Embedding**:
   - Prefixed with `"query: "` before passing to the E5 model.
2. **Vector Search in MongoDB**:
   - Top 5 similar paragraphs are retrieved using `$vectorSearch`.
3. **Generate Response**:
   - The paragraphs are combined into a context string.
   - A prompt is built and passed to the **Gemini API**.
4. **Display Answer**:
   - Only the direct answer is returned, without extra information.

---

## 🔐 .env Format

Create a `.env` file at the root with:

```env
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
GEMINI_KEY=your_gemini_api_key
```

---

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/BanglaBot.git
cd BanglaBot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Prepare Environment Variables
Create `.env` as shown above.

### 4. Load and Store Text Embeddings
```bash
python main.py
```

### 5. Start the Chatbot
```bash
python bot.py
```

---

## 🧠 Sample Q&A

**Query**: `কীভাবে বীজতলা তৈরি করব?`

**Response**:
> দোআঁশ ও এটেল মাটি যেখানে প্রচুর আলো বাতাস আছে এমন জমি বীজতলার জন্য উপযোগী। বীজতলার জমি উর্বর হওয়া প্রয়োজন। তবে অনুর্বর জমি হলে প্রতি বর্গমিটার ২ কেজি হারে জৈব সার প্রয়োগ করতে হবে। এর পর জমিতে ৫-৬ সে.মি. পানি দিয়ে দু-তিনটি চাষ ও মই দিয়ে ৭-১০ দিন পানি বদ্ধ অবস্থায় রেখে দিতে হবে। জমিতে ব্যবহৃত জৈব সার পচে গেলে পুনরায় চাষ ও মই দিয়ে জমি তৈরি করতে হবে। একটি আদর্শ বীজতলায় ৪টি বেড থাকবে। প্রতিটি জমির দৈর্ঘ্য বরাবর এক মিটার চওড়া বেড তৈরি করতে হবে এবং দু-বেডের মাঝে ২৫-৩০ সে.মি. ফাঁকা জায়গা রাখতে হবে। বেডের উপরের মাটি কাঠ বা বাঁশ দিয়ে সমান করে নিতে হয়। মৌসুম ভেদে ধানের চারা উৎপাদনের জন্য চার ধরনের বীজতলা তৈরি করা যায়। যেমন- (১) শুকনো বীজতলা (২) কাদাময় বীজতলা (৩) ভাসমান বীজতলা ও (৪) ডাপোগ বীজতলা।

---

## ✅ To-Do / Improvements

- [ ] Add Bengali spell-checker
- [ ] Web or mobile frontend
- [ ] Fine-tune E5 model on Bengali agricultural domain
- [ ] Improve Gemini prompt formatting

---

## 📜 License

This project is licensed under the [MIT License](./LICENSE).

---

## 🙏 Acknowledgments

- [HuggingFace Transformers](https://huggingface.co/)
- [MongoDB Atlas Vector Search](https://www.mongodb.com/docs/atlas/atlas-search/vector/)
- [Gemini Language Models](https://ai.google.dev/gemini-api)

---

## 📬 Contact

If you have any questions or feedback, feel free to reach out to [your-email@example.com].