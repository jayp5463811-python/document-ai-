# 📄 GenAI Document Analyzer & Verifier

**An intelligent web application built for the Gen AI Exchange Hackathon that uses Google's Gemini API to analyze, summarize, and answer questions about PDF documents, cross-referencing information with a custom knowledge base.**

---

## 🚀 Live Demo

Click the link below to access the live, deployed prototype. The app is fully functional and ready for testing.

**[➡️ Access the Live Prototype Here](https://gggsxqy4e4nv9k4kuejk8i.streamlit.app/)**

---

## 🎯 The Problem

In a world filled with digital documents, manually reading through lengthy PDFs to find specific information, verify details, or get a quick summary is time-consuming and inefficient. This process is prone to human error and becomes a significant bottleneck for professionals in various fields.

## ✨ The Solution

This **GenAI Document Analyzer** provides an intelligent solution by automating the entire process. Users can simply upload a PDF document and instantly receive AI-powered insights. The application leverages a simple but powerful **Retrieval-Augmented Generation (RAG)** pipeline to answer questions not only based on the document's content but also by cross-referencing it with a pre-loaded custom dataset, acting as a verification layer.

---

## ⚙️ How It Works: System Architecture

The application follows a modern, serverless architecture where the frontend and backend logic are handled by Streamlit, with AI capabilities provided by Google's Generative AI services.



```mermaid
graph TD;
    A[👨‍💻 User uploads PDF & asks a question] --> B{📄 Streamlit Frontend};
    B --> C[🐍 Python Backend Logic];
    C --> D{📚 Extract Text <br> (pypdf)};
    C --> E{🔍 Search Custom Data <br> (pandas)};
    D --> F[📝 Create "Super-Prompt"];
    E --> F;
    A --> F;
    F --> G[🧠 Google Gemini API];
    G --> H[✅ AI Response];
    H --> B;
