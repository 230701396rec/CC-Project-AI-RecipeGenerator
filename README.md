# Full-Stack AI Recipe Generator

A complete application that uses an LLM and Vision Model to generate recipes from ingredients or images.

## Structure
- `/backend`: FastAPI Python server containing ML inference and LLM connectivity, with SQLite for local persistence.
- `/frontend`: Vite + React UI using a vibrant, glassmorphism-based modern CSS.

## Setup Instructions

### 1. Backend Setup
1. Open a terminal and navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # Windows: .\venv\Scripts\activate
   # Mac/Linux: source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up an OpenAI API key (optional) in `backend/.env`. If you omit it, a Mock Generator will be used!
5. Start the backend:
   ```bash
   uvicorn app:app --reload
   ```

### 2. Frontend Setup
1. Open a *new* terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install NodeJS dependencies:
   ```bash
   npm install
   ```
3. Start the dev server:
   ```bash
   npm run dev
   ```

### 3. Usage
- Provide text ingredients or drag-and-drop a food image to analyze.
- The app will automatically populate ingredients and you can click "Generate Recipe".
