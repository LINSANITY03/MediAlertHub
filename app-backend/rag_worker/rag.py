"""
rag.py

This module processes patient clinical data using LangChain RAG components.
It creates vector embeddings of clinical notes and generates concise summaries
via a RetrievalQA chain using a local ChatOpenAI-compatible model.

Functions:
- format_patient_template: Formats raw patient input into a structured string.
- prepare_documents: Splits the input text into smaller chunks for embedding.
- build_vectorstore: Builds a FAISS vectorstore using HuggingFace embeddings.
- get_prompt_template: Returns a structured clinical prompt template.
- build_qa_chain: Creates a RetrievalQA chain using the prompt and retriever.
- summarize_patient_data: High-level interface to summarize the patient data.
"""
from typing import Optional

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain.schema.runnable import Runnable
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI

# Mocked form data
form_data = {
    "age_group": "30-40",
    "province": "Bagmati",
    "district": "Kathmandu",
    "disease_status": "The patient is showing a set of symptoms that may be consistent with a viral infection, "
                        "possibly Dengue or Chikungunya, but Malaria can’t be ruled out either at this point. "
                        "Given the persistence of high fever, joint stiffness, and rashes that have appeared intermittently, further lab confirmation is required."
                        "Initial blood tests showed low platelet count and mild dehydration. However, the patient also recently returned from an area where there was an uptick in enteric fever cases. So, there's also a slight possibility it could be typhoid fever. The overlap of symptoms makes a definitive diagnosis tricky without further diagnostic support like NS1 antigen or PCR. Until then, symptomatic management and isolation precautions have been advised. The provisional diagnosis is Dengue with possible co-infection, but it’s being treated conservatively.",
    "current_condition": "Patient presented with sustained fever for 5 days, around 102–103°F, accompanied by chills, headache, pain behind the eyes, and fatigue. "
                    "On physical examination, there is notable tenderness in joints and muscle soreness, particularly in the lower limbs. "
                     "Patient also reported intermittent episodes of nausea, some vomiting, and occasional abdominal discomfort. "
                     "No known underlying chronic illness, but the patient appeared visibly weak and dehydrated. "
                     "The rashes appeared on Day 3 and have not spread further. Slight swelling of lymph nodes in the neck. "
                     "Pulse and blood pressure within normal range but trending downward. Advised bed rest, fluid intake, and paracetamol. "
                     "CBC indicated reduced platelets and elevated hematocrit. Skin turgor is mildly reduced. "
                     "Patient remains conscious, alert, but complains of severe tiredness. Rehydration via ORS and monitoring vitals every 4 hours.",
    "disease_symptoms": "Initial symptoms included fever, chills, and intense headache, followed by a dull pain in the joints and behind the eyes. "
                    "On Day 2, patient began experiencing fatigue and minor vomiting. As the fever persisted, red patches resembling rashes started developing, first on the chest and then near the elbows. "
                    "The rash was not itchy but slightly raised and warm to touch. Joint stiffness and tenderness increased over time, especially during mornings. "
                    "The patient also experienced a metallic taste and occasional dizziness when standing. By Day 4, there were signs of dehydration — dry mouth and low urine output. "
                    "Other noted symptoms: sensitivity to light, mild cough, no sore throat. Appetite has decreased significantly. "
                    "The patient hasn’t had diarrhea but complains of a “weird sensation” in the stomach, possibly bloating. "
                    "Occasional shivering noted during nighttime. Swelling of hands and feet reported on Day 5. "
                    "Patient reports improvement in fever with paracetamol, but symptoms quickly return after 6–7 hours. "
                    "leeping patterns have been disturbed, and anxiety due to illness has made the patient irritable. No signs of severe respiratory distress yet.",
  }

def format_patient_template(form_data: dict) -> str:
    """
    Format the patient data dictionary into a structured diagnostic report string.

    Args:
        form_data (dict): Dictionary containing patient information and medical notes.

    Returns:
        str: Formatted patient diagnosis report.
    """

    return f"""
    Patient Diagnosis Report

    Age Group: {form_data['age_group']}
    Province: {form_data['province']}
    District: {form_data['district']}

    Reported Symptoms:
    {form_data['disease_symptoms']}

    Current Condition:
    {form_data['current_condition']}

    Doctor's Disease Status & Notes:
    {form_data['disease_status']}
    """

def prepare_documents(text: str) -> list[Document]:
    """
    Split a large text into smaller document chunks using a recursive character splitter.

    Args:
        text (str): The full patient report as a single string.

    Returns:
        list[Document]: A list of smaller Document chunks with metadata.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    document = Document(page_content=text, metadata={"source": "patient_001"})
    return splitter.split_documents([document])


def build_vectorstore(documents: list[Document]) -> FAISS:
    """
    Create a FAISS vector store from a list of LangChain Documents.

    Args:
        documents (list[Document]): List of document chunks to be embedded.

    Returns:
        FAISS: A FAISS vector store with embedded document representations.
    """
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.from_documents(documents, embedding=embedding)

def get_prompt_template() -> PromptTemplate:
    """
    Returns a predefined prompt template for clinical diagnosis summarization.

    This prompt instructs the language model to summarize patient notes
    into a medically sound report using only the provided context.

    Returns:
        PromptTemplate: The LangChain prompt template object.
    """
    return PromptTemplate(
        input_variables=["context", "question"],
        template="""
            You are a professional clinical assistant supporting doctors in a digital health surveillance system.

            Your goal is to analyze the provided patient notes and return a medically sound, concise summary. Include:
            - Key symptoms
            - Likely diagnosis
            - Any critical warning signs
            - Suggested follow-ups or lab tests (if applicable)

            Only use the given context and do not make up any new information.

            Context:
            {context}

            Question: {question}

            Answer (Clinical Summary):
            """
    )

def build_qa_chain(llm, retriever) -> RetrievalQA:
    """
    Build a RetrievalQA chain using the provided language model and retriever.

    Args:
        llm (Runnable): A language model that supports LangChain's Runnable interface.
        retriever: A retriever that fetches relevant documents based on a query.

    Returns:
        RetrievalQA: A LangChain RetrievalQA chain ready for question answering.
    """
    prompt = get_prompt_template()
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )

def summarize_patient_data(form_data: dict, llm:Optional[Runnable]=None) -> str:
    """
    Generate a clinical summary from patient form data using a RetrievalQA chain.

    Args:
        form_data (dict): Patient information and medical notes.
        llm (Optional[Runnable], optional): Language model instance to use.
            If None, a default ChatOpenAI instance is created. Defaults to None.

    Returns:
        str: Clinical summary generated by the QA chain.
    """
    template = format_patient_template(form_data)
    documents = prepare_documents(template)
    vectorstore = build_vectorstore(documents)
    retriever = vectorstore.as_retriever(search_type="similarity", k=3)

    if llm is None:
        llm = ChatOpenAI(
            base_url="http://localhost:12434/engines/v1",
            model="ai/smollm2",
            api_key="not-needed"
        )

    qa_chain = build_qa_chain(llm, retriever)
    response = qa_chain.invoke("Summarize this patient's diagnosis and symptoms.")
    return response["result"]
