# Nexus AI Agent Platform - Product Requirements Document

Updated_By: Google Code Assist 2025.05.06-1533h.

## 1. Overview

### 1.1 Purpose
The Nexus AI Agent Platform is an open-source system designed to assist in the development, testing, and hosting of AI Agents. It aims to provide a user-friendly environment for creating intelligent dashboards, prototypes, and AI-Agent chat applications, while also serving as an educational tool for understanding core AI Agent concepts. This document outlines the requirements for Version 2.0 of the platform.

### 1.2 Scope
The platform encompasses functionalities for agent creation and management, persona definition, action/tool integration, knowledge and memory management (including RAG capabilities), multi-agent support, and user interaction via a Streamlit-based web interface. It supports integration with external LLM providers like OpenAI and Groq.

### 1.3 Intended Audience
- AI developers and researchers building and experimenting with AI agents.
- Readers and users of the "AI Agents In Action" book by Manning Publications, for which this platform is a companion.
- Hobbyists and students learning about AI agent architecture and development.

## 2. Functional Requirements

### 2.1 Agent Management
- **FR-AM-001**: The system must allow users to define and create new AI agents.
- **FR-AM-002**: The system must allow users to list and select from available agent types (e.g., GroqAgent, OpenAI Assistants).
- **FR-AM-003**: Each agent instance must be configurable with specific attributes (e.g., model, temperature, max_tokens), with options displayed in the UI based on agent capabilities.
- **FR-AM-004**: The system must allow users to view and manage existing agent instances.
- **FR-AM-005**: The system must persist agent configurations.
- **FR-AM-006**: The system must support associating agents with specific profiles/personas.
- **FR-AM-007**: The system must support associating agents with available actions/tools.
- **FR-AM-008**: The system must support associating agents with knowledge stores.
- **FR-AM-009**: The system must support associating agents with memory stores.
- **FR-AM-010**: The system must load available agent types dynamically.
- **FR-AM-011**: The system must provide a mechanism to set an active agent for interaction in the UI.

### 2.2 Profile/Persona Management
- **FR-PP-001**: The system must allow users to define and manage agent profiles/personas.
- **FR-PP-002**: A persona definition must include attributes such as personality, primary motivator, and a system-level prompt or instructions.
- **FR-PP-003**: The system must allow users to assign a defined persona to an agent.
- **FR-PP-004**: The assigned persona must influence the agent's behavior and responses.
- **FR-PP-005**: The system must persist profile/persona definitions.
- **FR-PP-006**: The system must allow users to list and select from existing profiles.

### 2.3 Action/Tool Management
- **FR-AT-001**: The system must support the definition and integration of actions/tools that agents can utilize.
- **FR-AT-002**: Actions can be semantic (prompt-based) or native (code-based functions).
- **FR-AT-003**: The system must provide a mechanism to register and load available actions.
- **FR-AT-004**: The system must allow users to assign specific actions/tools to an agent, if the agent type supports actions.
- **FR-AT-005**: Agent's planning capabilities should be able to select and execute assigned actions based on user input or goals. (Detailed planning requirements TBD)
- **FR-AT-006**: The system must persist action definitions and their associations with agents.

### 2.4 Knowledge Management
- **FR-KM-001**: The system must allow users to create and manage knowledge stores.
- **FR-KM-002**: Knowledge stores must use a vector database (ChromaDB) for storing document embeddings.
- **FR-KM-003**: The system must support uploading documents of various types (txt, md, html, csv, py, json, pdf, docx) into a knowledge store.
- **FR-KM-004**: Uploaded documents must be processed, chunked, and their embeddings stored.
- **FR-KM-005**: The system must allow configuration of chunking strategy (e.g., CharacterTextSplitter, RecursiveCharacterTextSplitter) and parameters (chunk size, overlap) per knowledge store.
- **FR-KM-006**: The system must provide Retrieval Augmented Generation (RAG) capabilities, allowing agents to query knowledge stores based on user input.
- **FR-KM-007**: The RAG process must retrieve relevant document chunks and provide them as context to the agent.
- **FR-KM-008**: The system must allow users to view/examine documents and their embeddings within a knowledge store via the UI.
- **FR-KM-009**: The system must support deletion of knowledge stores.
- **FR-KM-010**: The system must support compression of knowledge within a store by summarizing and re-indexing documents.
- **FR-KM-011**: The system must persist knowledge store configurations and metadata.
- **FR-KM-012**: The system must use an embedding manager to generate embeddings for documents.

### 2.5 Memory Management
- **FR-MM-001**: The system must allow users to create and manage memory stores for agents.
- **FR-MM-002**: Memory stores must use a vector database (ChromaDB) for storing memory embeddings.
- **FR-MM-003**: The system must support different types of memory (e.g., conversational, semantic).
- **FR-MM-004**: Conversational memory should store interaction history.
- **FR-MM-005**: Semantic memory should store extracted concepts or facts from interactions.
- **FR-MM-006**: The system must allow agents to append new memories (user input, agent response, extracted semantic data) to their associated memory store.
- **FR-MM-007**: The system must provide RAG capabilities for memory, allowing agents to query relevant memories as context.
- **FR-MM-008**: The system must allow configuration of memory functions (e.g., augmentation prompt, function prompt, summarization prompt, keys) for semantic memory processing.
- **FR-MM-009**: The system must allow users to view/examine memories and their embeddings within a memory store via the UI.
- **FR-MM-010**: The system must support deletion of memory stores.
- **FR-MM-011**: The system must support compression of memories within a store.
- **FR-MM-012**: The system must persist memory store configurations and metadata.
- **FR-MM-013**: The system must use an embedding manager to generate embeddings for memories.

### 2.6 Thought & Prompt Template Management
- **FR-TPT-001**: The system must provide a "Thought Template Manager" for creating, editing, and testing thought templates.
- **FR-TPT-002**: Thought templates define a sequence of inputs, prompts, and outputs for structured agent reasoning.
- **FR-TPT-003**: The system must allow execution of thought templates with given inputs, producing a result.
- **FR-TPT-004**: The system must provide a "Prompt Function Template Manager" for creating and managing prompt templates.
- **FR-TPT-005**: Prompt templates should be reusable components for generating prompts.
- **FR-TPT-006**: The system must persist thought and prompt templates.
- **FR-TPT-007**: The UI must provide a code editor for writing and editing templates.

### 2.7 Multi-Agent Support & Interaction
- **FR-MA-001**: The system must support the configuration and operation of multiple agent instances simultaneously.
- **FR-MA-002**: The system should facilitate interactions between different agents (details of inter-agent communication TBD).
- **FR-MA-003**: The system must manage context and state for each agent independently.

### 2.8 User Management & Chat Interface
- **FR-UC-001**: The system must allow users to create an account or log in.
- **FR-UC-002**: The system must manage chat participants (users, agents, assistants).
- **FR-UC-003**: The system must provide a chat interface for users to interact with selected agents.
- **FR-UC-004**: The chat interface must display conversation history.
- **FR-UC-005**: The chat interface must support sending user messages and receiving agent responses.
- **FR-UC-006**: Agent responses can be streamed to the chat interface.
- **FR-UC-007**: The system must persist chat threads and messages associated with users and agents/assistants.
- **FR-UC-008**: The system must allow users to create and manage chat threads.
- **FR-UC-009**: The system must provide a feature to download the current chat history as a human-readable markdown file. The filename should be formatted as `{chat_agent_name}_history_{datetime}.md` and saved in a `chat_history_archive` directory.
- **FR-UC-010**: The system must provide a feature to delete the chat history for the current agent, with a confirmation dialog before proceeding.

### 2.9 OpenAI Assistants Integration
- **FR-OAI-001**: The system must support integration with OpenAI Assistants API.
- **FR-OAI-002**: Users must be able to create, retrieve, update, and delete OpenAI Assistants via the Nexus interface.
- **FR-OAI-003**: Users must be able to configure assistants with name, instructions, model, and tools.
- **FR-OAI-004**: The system must manage threads for OpenAI Assistants.
- **FR-OAI-005**: The system must support streaming responses from OpenAI Assistants.

### 2.10 Error Handling & Feedback
- **FR-EH-001**: The system must gracefully handle errors during agent operations, API calls, data processing, and UI interactions.
- **FR-EH-002**: The system must provide clear and informative error messages to the user in the UI (e.g., using `st.error`).
- **FR-EH-003**: The system must validate user inputs for configurations and operations.
- **FR-EH-004**: Failures in API calls (e.g., to OpenAI, Groq) must be reported with relevant details.
- **FR-EH-005**: Issues with database operations (SQLite, ChromaDB) must be handled and reported.

## 3. Technical Requirements

### 3.1 Development & Architecture
- **TR-DA-001**: The system must be implemented primarily in Python (version 3.10 recommended).
- **TR-DA-002**: The web user interface must be built using Streamlit.
- **TR-DA-003**: The system must use Peewee ORM for interacting with the relational database.
- **TR-DA-004**: The system must use ChromaDB for vector storage and similarity search.
- **TR-DA-005**: The system should follow a modular design, with clear separation of concerns (e.g., managers for agents, knowledge, memory).
- **TR-DA-006**: Code must be well-documented with comments and docstrings.
- **TR-DA-007**: The system must be designed for extensibility, allowing new agents, tools, and managers to be added.

### 3.2 Dependencies
- **TR-DP-001**: Key Python libraries include: `streamlit`, `groq`, `openai`, `chromadb`, `peewee`, `langchain-text-splitters`, `python-dotenv`, `pandas`, `code-editor` (streamlit component).
- **TR-DP-002**: All Python dependencies must be manageable via `pyproject.toml` (Poetry) or a `requirements.txt` file.
- **TR-DP-003**: The system must specify dependencies for optional document types (e.g., `pdfplumber` for PDF, `python-docx` for DOCX).

### 3.3 Data Persistence
- **TR-DP-004**: A relational database (SQLite, e.g., `nexus.db`) must be used for storing metadata such as user accounts, agent configurations, profile definitions, knowledge/memory store metadata, chat threads, and messages.
- **TR-DP-005**: ChromaDB must be used for storing embeddings for knowledge documents and agent memories in specified directories (`nexus_knowledge_chroma_db/`, `nexus_memory_chroma_db/`).
- **TR-DP-006**: Thought and prompt templates should be persisted (e.g., as files or in the database).

### 3.4 API Integration & Keys
- **TR-AK-001**: The system must securely manage API keys for external services (e.g., OpenAI, Groq).
- **TR-AK-002**: API keys should be configurable via environment variables or a `.env` file.
- **TR-AK-003**: The system must not expose API keys in the frontend or logs.

### 3.5 Performance
- **TR-PF-001**: The system should handle interactions with multiple concurrent users (within Streamlit's typical operational limits).
- **TR-PF-002**: Embedding generation and vector database queries should be performed efficiently.
- **TR-PF-003**: Document uploading and processing should provide feedback for long operations (e.g., `st.spinner`).
- **TR-PF-004**: Streaming of agent responses should be implemented to improve perceived responsiveness in the chat interface.

### 3.6 Installation & Configuration
- **TR-IC-001**: The system must be installable via pip from a Git repository.
- **TR-IC-002**: A development setup involving cloning the repository and installing in editable mode must be supported.
- **TR-IC-003**: The system must be runnable via a command-line entry point (e.g., `nexus run`).
- **TR-IC-004**: Essential configurations (like API keys) must be clearly documented for setup.

## 4. User Interface (Streamlit Web Application)

### 4.1 General UI
- **UI-GN-001**: The application must present a clean, intuitive, and user-friendly interface.
- **UI-GN-002**: Navigation between different sections (Chat, Managers, Configuration) must be clear.
- **UI-GN-003**: The UI must be responsive and adapt to different screen sizes where possible with Streamlit's capabilities.
- **UI-GN-004**: Consistent styling and terminology must be used throughout the application.

### 4.2 Chat Page
- **UI-CP-001**: A dedicated page for chat interactions with agents.
- **UI-CP-002**: Display of current chat thread messages.
- **UI-CP-003**: Input area for user messages.
- **UI-CP-004**: Mechanism to select the active agent for the chat.
- **UI-CP-005**: Option to create new chat threads or switch between existing ones.
- **UI-CP-006**: A "Download Chat History" button must be available on the chat page.
- **UI-CP-007**: A "Delete Chat History" button must be available on the chat page, triggering a confirmation dialog before action.

### 4.3 Agent Panel / Configuration
- **UI-AP-001**: A sidebar or dedicated section for selecting and configuring the active agent.
- **UI-AP-002**: Display agent-specific configurable attributes (model, temperature, etc.) with appropriate input widgets (sliders, dropdowns, text boxes).
- **UI-AP-003**: Options to link agents with profiles, knowledge stores, and memory stores.

### 4.4 Management Pages
- **UI-MP-001**: **Knowledge Store Manager Page**:
    - Create, list, select, and delete knowledge stores.
    - Upload documents to a selected store.
    - Configure chunking options.
    - View documents/embeddings in a store.
    - Trigger knowledge compression.
- **UI-MP-002**: **Memory Store Manager Page**:
    - Create, list, select, and delete memory stores.
    - Configure memory types and functions.
    - View memories/embeddings in a store.
    - Trigger memory compression.
- **UI-MP-003**: **Thought Template Manager Page**:
    - Tabs for "Write Templates", "Test Templates", "Exercise Templates".
    - Select, create, or edit thought templates using a code editor.
    - Input fields for testing templates.
    - Display area for template execution results.
- **UI-MP-004**: **Prompt Function Template Manager Page**:
    - Select, create, or edit prompt templates using a code editor.
- **UI-MP-005**: **Profile Manager Page** (Implied, for creating/editing profiles).
    - Create, list, select, edit, and delete profiles/personas.
- **UI-MP-006**: **Action Manager Page** (Implied, for viewing/managing actions).
    - List available actions and their descriptions.
- **UI-MP-007**: **Assistants Manager Page** (Implied, for OpenAI Assistants).
    - Create, list, configure, and delete OpenAI Assistants.

### 4.5 User Feedback
- **UI-FB-001**: The UI must provide immediate feedback for user actions (e.g., button clicks, form submissions).
- **UI-FB-002**: Use spinners or progress indicators for long-running operations.
- **UI-FB-003**: Display success messages upon completion of operations (e.g., `st.success`).
- **UI-FB-004**: Display error messages clearly and non-intrusively (e.g., `st.error`).

## 5. Logging and Error Handling (System-Level)

### 5.1 Logging
- **LG-SL-001**: The system must implement logging for key events, operations, and errors.
- **LG-SL-002**: Logs should include timestamps and relevant context (e.g., function name, agent ID).
- **LG-SL-003**: Application startup, API calls, database operations, and significant errors should be logged.
- **LG-SL-004**: Log output should primarily be to the console, visible when running the `nexus run` command. (File-based logging TBD if needed).

### 5.2 Error Handling (Backend)
- **EH-BE-001**: Backend functions must handle exceptions gracefully (e.g., API errors, database errors, file I/O errors).
- **EH-BE-002**: Errors propagated to the UI layer should be transformed into user-friendly messages.
- **EH-BE-003**: The system should prevent data corruption in case of errors.

## 6. Output Requirements (Agent & System)

### 6.1 Agent Responses
- **OR-AR-001**: Agent text responses must be displayed in the chat interface.
- **OR-AR-002**: Streamed responses must update character by character or token by token in the UI.
- **OR-AR-003**: If agents produce structured output (e.g., JSON from a tool), it should be handled appropriately (displayed or used by the system).

### 6.2 Data Display
- **OR-DD-001**: The UI must display lists of configurable items (agents, profiles, knowledge stores, etc.).
- **OR-DD-002**: Content of knowledge stores (document names, snippets) and memory stores must be viewable.
- **OR-DD-003**: Results from thought template execution must be displayed.

## 7. Change Log

### Version 1.0 (Initial PRD Release - `Product_Reqts_Doc_Copilot_GGem_v1.md`)
- **Core Features Outlined**:
    - Profiles/Personas definition.
    - Actions/Tools integration (semantic/prompt and native/code).
    - Knowledge/Memory incorporation (short-term to semantic).
    - Planning/Feedback options.
    - Multi-Agents Support.
- **User Management**:
    - User login and creation.
    - Participant Management (retrieve all participants).
- **Technical Foundation**:
    - Platform built with Python and Streamlit.
    - Installation via pip from GitHub.
    - OpenAI API Key integration.
- **General Scope**: High-level definition of platform goals and target audience.

### Version 2.0 (Current Document - `Nexus_Agents_PRD_Copilot_GGem_v2.md`)
- **Detailed Functional Requirements**:
    - Expanded and itemized requirements for Agent Management (FR-AM), Profile/Persona Management (FR-PP), Action/Tool Management (FR-AT).
    - Comprehensive requirements for Knowledge Management (FR-KM) including ChromaDB, document types, chunking, RAG, UI viewing, compression.
    - Comprehensive requirements for Memory Management (FR-MM) including ChromaDB, memory types, RAG, memory functions, UI viewing, compression.
    - Added requirements for Thought & Prompt Template Management (FR-TPT) with UI editor and testing.
    - Clarified Multi-Agent Support (FR-MA) and User Management & Chat Interface (FR-UC) including persistence.
    - Added specific requirements for OpenAI Assistants Integration (FR-OAI).
    - Detailed Error Handling & Feedback within functional requirements (FR-EH).
    - Incorporated chat history download and delete functionalities from `README_Enhancements_TBD.md` (FR-UC-009, FR-UC-010, UI-CP-006, UI-CP-007).

- **Detailed Technical Requirements**:
    - Specified development stack (Python, Streamlit, Peewee, ChromaDB) (TR-DA).
    - Listed key dependencies (TR-DP).
    - Detailed Data Persistence mechanisms for metadata and vector stores (TR-DP).
    - Added requirements for API Integration & Key Management (TR-AK).
    - Outlined Performance considerations (TR-PF) and Installation & Configuration (TR-IC).
- **Detailed User Interface Requirements**:
    - Broke down UI into General (UI-GN), Chat Page (UI-CP), Agent Panel (UI-AP), specific Management Pages (UI-MP) for knowledge, memory, templates, etc.
    - Added requirements for User Feedback in the UI (UI-FB).
- **System-Level Logging and Error Handling**:
    - Added dedicated sections for system-level Logging (LG-SL) and backend Error Handling (EH-BE).
- **Output Requirements**:
    - Specified requirements for Agent Responses (OR-AR) and Data Display (OR-DD) in the UI.
- **Structure and Detail**: Adopted a more granular requirement ID system (e.g., FR-AM-001) and significantly increased the level of detail to match the provided `PRD_EXAMPLE.md`.
- **Future Enhancements Section**: Added a section for potential future development.

## 8. Future Enhancements

### 8.1 Feature Enhancements
- **FE-001**: Advanced inter-agent communication protocols and collaboration frameworks.
- **FE-002**: More sophisticated planning and feedback mechanisms for agents.
- **FE-003**: UI for visualizing agent thought processes or decision trees.
- **FE-004**: Support for a wider range of LLM providers and local models.
- **FE-005**: Versioning for profiles, templates, and agent configurations.
- **FE-006**: User roles and permissions system.
- **FE-007**: Batch processing capabilities for agents.
- **FE-008**: Export/import functionality for agent configurations, knowledge/memory stores.
- **FE-009**: Enhanced testing and evaluation framework for agents within Nexus.
- **FE-010**: Integration with more data sources for knowledge.

### 8.2 Technical Enhancements
- **TE-001**: Asynchronous processing for more backend tasks to improve UI responsiveness.
- **TE-002**: Comprehensive automated testing suite (unit, integration, UI).
- **TE-003**: Scalability improvements for handling a larger number of users and agents.
- **TE-004**: Option for alternative database backends (e.g., PostgreSQL for metadata).
- **TE-005**: More robust security audit and hardening.
