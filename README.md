# MediAlertHub

**MediAlertHub** is a healthcare logistics & emergency response system that connects doctors’ disease reports with supply chain management to ensure timely resource distribution during outbreaks.

---

## Overview

Licensed doctors can upload real-time data on recently detected diseases at their health posts, which is then collected in a centralized database. This data enables management personnel to analyze outbreak trends and swiftly dispatch necessary medical supplies to affected regions, ensuring timely healthcare response.

---

## Features

- Doctor submission of disease reports (date, location, disease type, severity, notes)
- User authentication & role‑based access (doctor vs admin)
- Data validation and error handling

---

## Tech Stack

| Component   | Technology                          |
|-------------|-------------------------------------|
| Backend     | Python (FastAPI)                    |
| Frontend    | React / TypeScript                  |
| Database    | PostgreSQL / MongoDB                |
| API         | RESTful API / GraphQL               |
| Tools       | Docker, GitHub Actions, HuggingFace |

---

## Architecture

### Frontend

- **Typescript + NextJS**
- **Apollo Client** for GraphQL queries and mutations.
- **Rest** for certain endpoints (file uploads, form submission, etc.)
- Role Authentication based dashboard to upload patient data.

### Backend (FastAPI Micro-services)

- **API Gateway / Core Service**
  - Exposes **GraphQL API** for complex queries (via Strawberry)  
  - Exposes **REST API** for standard CRUD and integrations

- **RAG Service (Retrieval Augmented Generation)**
  - Leverages libraries like `LangChain`, `FAISS`, and `transformers`  
  - Provides intelligent summarization on medical outbreak data  

- **Data Service**
  - Manages PostgreSQL database (disease reports, user roles)  
  - Ensures ACID compliance and indexing for fast lookups

### Extensibility
The architecture is intentionally **extensible**.  
New services (e.g., ML forecasting, AI dashboards, mobile APIs) can be added as **separate micro-services** that plug into the ecosystem without changing the existing codebase.  
This keeps the system modular, easier to maintain, and deployable at scale.

---

### Communication & Integration
- Services communicate internally over REST/GraphQL.  
- Apollo Client in frontend consumes **both GraphQL (queries/mutations)** and **REST endpoints** seamlessly.  
- Backend services are designed to be **independent and scalable** (Docker-ready).

---

## Getting Started

1. Clone the repository:
   ```
   git clone https://github.com/LINSANITY03/MediAlertHub.git
   ```

2. **Frontend setup**:
   ```
   cd app-frontend
   npm install
   npm start
   ```

3. **Backend setup**:
   ```bash
   cd app-backend
   docker-compose -f docker-compose.yml up
   ```

4. Access the application at `http://localhost:3000`.

---

## What I Learned

- Designing systems end‑to‑end: from user input → validation → database → analysis → decision‑making.
- Building and Integrating GraphQL + REST in a single frontend using Apollo Client and Fetch.
- Handling real‑world constraints like data quality, role security, and usability under urgency.
- The importance of testing, modular architecture, and documentation.
- Building a RAG pipeline to add intelligence to outbreak and supply data.
- Containerizing services for modular deployment.
- Balancing real-time data flow with durable background processing.

---

## Future Improvements

To keep the system modular and scalable, future features will be developed as **separate projects/services**, rather than expanding this repository directly.  

- Advanced **AI dashboards** with data visualization and predictive analytics
- Add real‑time alerts (via SMS / email) for outbreaks beyond thresholds.
- Mobile app for doctors in low-connectivity regions
- Use machine learning models to forecast outbreaks and supply needs.
- Strengthen security & privacy (compliance with health data standards).

These extensions will live in separate repositories to ensure each service remains independent, easier to maintain, and can be scaled/deployed individually (also mindful of current hardware limits).