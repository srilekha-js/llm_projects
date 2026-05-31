Here is the extended developer guide covering both unit testing strategies and deployment as a microservice using FastAPI.
------------------------------
## 🧪 Unit Testing Strategies
Testing an agent framework requires isolating your tool logic (deterministic functions) from the agent's decision-making routing (probabilistic AI execution).
Create a test file named test_app.py. We will use pytest and unittest.mock to mock the LLM network calls, ensuring your tests run instantly without relying on a running Ollama instance.
## 1. Install Testing Dependencies

pip install pytest

## 2. Testing Implementation (test_app.py)

import pytestfrom unittest.mock import MagicMock, patchfrom app import summarize_text, extract_keywords, generate_title
# Mock response structure mimicking LangChain's AIMessage objectclass MockAIMessage:
    def __init__(self, content):
        self.content = content

@patch('app.llm')def test_summarize_text_tool(mock_llm):
    """Ensure the summarize tool formats the prompt properly and extracts raw content."""
    # Arrange
    mock_llm.invoke.return_value = MockAIMessage("This is a mocked summary.")
    sample_text = "Long text input here."
    
    # Act
    result = summarize_text(text=sample_text)
    
    # Assert
    assert result == "This is a mocked summary."
    mock_llm.invoke.assert_called_once()
    
    # Verify the prompt text was structured inside the tool before invoking LLM
    called_prompt = mock_llm.invoke.call_args[0][0]
    assert "TEXT: Long text input here." in called_prompt


@patch('app.llm')def test_extract_keywords_tool(mock_llm):
    """Ensure the keyword extraction tool formats and responds correctly."""
    mock_llm.invoke.return_value = MockAIMessage("keyword1, keyword2")
    
    result = extract_keywords(text="Some text")
    
    assert result == "keyword1, keyword2"
    called_prompt = mock_llm.invoke.call_args[0][0]
    assert "Extract the main keywords" in called_prompt


@patch('app.llm')def test_generate_title_tool(mock_llm):
    """Ensure the title generation tool formats and responds correctly."""
    mock_llm.invoke.return_value = MockAIMessage("A Mocked Title")
    
    result = generate_title(text="Some text")
    
    assert result == "A Mocked Title"
    called_prompt = mock_llm.invoke.call_args[0][0]
    assert "Generate a concise title" in called_prompt

## 3. Run Your Tests
Execute the tests locally from your terminal:

pytest test_app.py

------------------------------
## ⚡ FastAPI Production Deployment
To serve this agent as a microservice, you can wrap it inside a FastAPI web server. This provides an HTTP POST endpoint for web applications or frontend clients to query your agent.
## 1. Install Deployment Dependencies

pip install fastapi uvicorn pydantic

## 2. Microservice Implementation (main.py)

from fastapi import FastAPI, HTTPExceptionfrom pydantic import BaseModel, Fieldimport uvicorn
# Import the logic function from your application core filefrom app import run_agent
# Initialize FastAPI Appapp = FastAPI(
    title="Text Analysis Agent API",
    description="Microservice for automated text summarization, keyword extraction, and title generation.",
    version="1.0.0"
)
# Define request validation schemaclass AgentRequest(BaseModel):
    query: str = Field(
        ..., 
        description="The natural language instruction for the agent.",
        example="Summarize this article and give me 5 keywords: [Your text here]"
    )
# Define response validation schemaclass AgentResponse(BaseModel):
    status: str = "success"
    result: str

@app.post("/api/v1/analyze", response_model=AgentResponse)async def analyze_text(payload: AgentRequest):
    """
    Accepts natural language user requests and passes them to the LangGraph ReAct agent.
    The agent dynamically determines which tools to execute.
    """
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query text cannot be empty.")
        
    try:
        # Run the agent pipeline
        agent_output = run_agent(payload.query)
        return AgentResponse(result=agent_output)
        
    except Exception as e:
        # Catch unexpected pipeline failures gracefully
        raise HTTPException(status_code=500, detail=f"Agent runtime error: {str(e)}")
# Healthcheck endpoint for monitoring systems (Docker, Kubernetes, AWS)
@app.get("/health")async def health_check():
    return {"status": "healthy"}
if __name__ == "__main__":
    # Start server locally on port 8000
    uvicorn.run("main.py:app", host="0.0.0.0", port=8000, reload=True)

## 3. Running and Testing the API

   1. Start the API Server:
   
   python main.py
   
   2. Access Swagger UI Documentation:
   Open your browser and navigate to http://127.0.0. FastAPI automatically generates an interactive UI where you can click "Try it out" to send real payloads directly to your running Llama 3.2 engine.
   3. Example cURL Request:
   
   curl -X 'POST' \
     'http://127.0.0' \
     -H 'Content-Type: application/json' \
     -d '{
     "query": "Give me a catchy title for an article about the future of local AI models."
   }'
   
   
------------------------------
Would you like to explore adding persistent chat history to the FastAPI microservice so the agent remembers previous questions, or should we look into packaging this server into a Docker container?

Here is the implementation for adding persistent chat history to your FastAPI microservice and packaging the entire application inside a production-ready Docker container.
------------------------------
## 💾 Part 1: FastAPI with Persistent Chat History
To give the agent a memory, we will use LangGraph's built-in memory management system (MemorySaver). This allows the agent to remember context across different API calls using a unique thread_id for each user conversation.
## 1. Updated Core Code (app.py)
Modify your core file to add the checkpointer to the agent instantiation.

from langchain_ollama.chat_models import ChatOllamafrom langchain.tools import toolfrom langgraph.prebuilt import create_react_agentfrom langgraph.checkpoint.memory import MemorySaver  # In-memory checkpointer
def llm_creation():
    return ChatOllama(model="llama3.2", temperature=0, max_tokens=1000)
llm = llm_creation()
# (Keep your summary_prompt, keyword_extraction_prompt, title_generation_prompt here)

@tool("summarize_text")def summarize_text(text: str) -> str:
    """Summarize the given text or article."""
    return llm.invoke(summary_prompt.format(text=text)).content

@tool("extract_keywords")def extract_keywords(text: str) -> str:
    """Extract keywords from the given text."""
    return llm.invoke(keyword_extraction_prompt.format(text=text)).content

@tool("generate_title")def generate_title(text: str) -> str:
    """Generate a title for the given text."""
    return llm.invoke(title_generation_prompt.format(text=text)).content
tools = [summarize_text, extract_keywords, generate_title]
# Create an in-memory checkpointer to persist conversation historymemory = MemorySaver()
# Pass the checkpointer to the agentagent = create_react_agent(model=llm, tools=tools, checkpointer=memory)
def run_agent_with_memory(user_query: str, thread_id: str):
    """Executes the agent while maintaining history isolated by thread_id."""
    config = {"configurable": {"thread_id": thread_id}}
    response = agent.invoke(
        {"messages": [{"role": "user", "content": user_query}]},
        config=config
    )
    return response["messages"][-1].content

## 2. Updated API Code (main.py)
Update your API endpoints to accept a thread_id parameter from the client.

from fastapi import FastAPI, HTTPExceptionfrom pydantic import BaseModel, Fieldimport uvicornfrom app import run_agent_with_memory
app = FastAPI(title="Text Analysis Agent API with Memory")
class AgentRequest(BaseModel):
    query: str = Field(..., description="Your prompt for the agent.")
    thread_id: str = Field(..., description="Unique ID to isolate individual user chat histories.", example="user_session_123")
class AgentResponse(BaseModel):
    status: str = "success"
    result: str

@app.post("/api/v1/analyze", response_model=AgentResponse)async def analyze_text(payload: AgentRequest):
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query text cannot be empty.")
    try:
        # Run agent passing both query and thread tracking configuration
        agent_output = run_agent_with_memory(payload.query, payload.thread_id)
        return AgentResponse(result=agent_output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent runtime error: {str(e)}")
if __name__ == "__main__":
    uvicorn.run("main.py:app", host="0.0.0.0", port=8000)

------------------------------
## 🐳 Part 2: Packaging with Docker
To make your application completely portable, you can package it inside a lightweight Docker container.
## 1. Create a requirements.txt
List all python dependencies at the root of your project:

langchain-ollama
langgraph
fastapi
uvicorn
pydantic
pytest

## 2. Create the Dockerfile
Create a file named Dockerfile (no file extension) in the same directory:

# Use an official, lightweight Python base imageFROM python:3.11-slim
# Set system-level environment variablesENV PYTHONDONTWRITEBYTECODE=1ENV PYTHONUNBUFFERED=1
# Set the working directory inside the containerWORKDIR /app
# Install system dependencies if needed (curl helps with docker healthchecks)RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
# Copy requirements file first to optimize Docker layer cachingCOPY requirements.txt /app/
# Install Python packagesRUN pip install --no-cache-dir -r requirements.txt
# Copy the rest of the application files into the containerCOPY app.py main.py /app/
# Expose the API port outside the containerEXPOSE 8000
# Run the FastAPI server using uvicorn when the container startsCMD ["uvicorn", "main.py:app", "--host", "0.0.0.0", "--port", "8000"]

## 3. Build and Run instructions## step 1: Build the Docker Image

docker build -t text-agent-service:latest .

## Step 2: Run the Container
Because Ollama runs on your host system machine, you need to tell the Docker container how to reach your local localhost network using host.docker.internal.

* Linux / macOS / Windows: Run the container with host networking capabilities:

docker run -d -p 8000:8000 --add-host=host.docker.internal:host-gateway --name agent-service text-agent-service:latest


## Step 3: Configure Ollama for Cross-Origin Calls
If the container fails to connect to Ollama, ensure your local Ollama engine is configured to accept connections from Docker. Set this environment variable on your machine before running Ollama:

* Linux/macOS terminal: export OLLAMA_HOST=0.0.0.0
* Windows PowerShell: $env:OLLAMA_HOST="0.0.0.0"

(Note: In your core python code, you may need to update your instantiation to explicitly point to the host address if running inside Docker: ChatOllama(model="llama3.2", base_url="http://docker.internal")).
------------------------------
Would you like to explore saving conversation logs permanently to a SQLite or PostgreSQL database instead of using temporary RAM, or should we look at setting up GitHub Actions to automate running your tests?

Here is a direct, practical explanation of exactly why you need SQLite, Docker, and Cloud Providers (AWS/GCP) for your agent application.
------------------------------
## 🗹 Why You Need SQLite (Data Persistence)
Right now, your application uses MemorySaver(). This stores chat history inside your computer's temporary Random Access Memory (RAM).

* The Problem with RAM: If your FastAPI server restarts, crashes, or gets updated, all chat history is completely wiped out. Your users will lose their context.
* The SQLite Fix: SQLite saves the chat history onto a physical file on a hard drive. If the server crashes or restarts, the agent reads the file and instantly remembers everything. It is lightweight and requires zero server configuration.

------------------------------
## 🐳 Why You Need Docker (Environment Consistency)
Your Python code depends on exact versions of Python, LangChain, LangGraph, and FastAPI.

* The "Works on My Machine" Problem: If you deploy your raw Python script directly to a cloud server, it might fail because the server has a different Python version, missing OS packages, or conflicting libraries.
* The Docker Fix: Docker takes your code, your Python version, and your exact libraries, and locks them inside a standard Container. This container will run exactly the same way on your laptop, your coworker's computer, AWS, or GCP.

------------------------------
## ☁️ Why Use AWS or GCP (Global Availability)
Right now, your API only runs on your local machine (localhost). No one else in the world can access it.

* Production Deployment: AWS and GCP provide cloud computers (servers) that stay powered on 24/7/365 with perfect internet connections.
* Scaling: If 10,000 users suddenly start using your text-analysis agent at the same time, cloud providers can automatically spin up 10 extra copies of your Docker container to handle the traffic (Auto-scaling).

------------------------------
## 🚀 How They All Fit Together in the Cloud
When you deploy your application to production, the tools work together like this:

  [ User Client ] ──(Sends Request with Thread ID)──► [ AWS / GCP Cloud ]
                                                            │
                                                   (Runs your Docker Container)
                                                            │
                                                   [ FastAPI Agent App ]
                                                      │           │
                     (Reads/Writes Chat History) ─────┘           └─────► (Calls Local LLM API)
                                 │                                              │
                           [ SQLite Database ]                             [ Ollama/Bedrock ]
                      (Saved on Cloud Storage Vol)


   1. Docker wraps your FastAPI application so it can easily launch on AWS or GCP.
   2. AWS / GCP hosts the container so your API is live on the public internet.
   3. SQLite ensures that when users talk to your cloud-hosted agent, their chat history is safely stored and never lost.

------------------------------
Would you like to see how to replace MemorySaver() with SQLite memory in your code, or would you prefer a step-by-step guide on how to upload your Docker container to AWS (using App Runner/ECS) or GCP (using Cloud Run)?

To provide a complete setup, here is how to upgrade your code to use a persistent SQLite database for memory, followed by the deployment steps for AWS and GCP.
------------------------------
## 💾 1. Upgrading to SQLite Memory (app.py)
Using SqliteSaver replaces temporary RAM storage with a persistent database file (memory.db), ensuring history survives application restarts [1].

from langchain_ollama.chat_models import ChatOllamafrom langchain.tools import toolfrom langgraph.prebuilt import create_react_agentfrom langgraph.checkpoint.sqlite import SqliteSaver  # SQLite Checkpointer
def llm_creation():
    return ChatOllama(model="llama3.2", temperature=0, max_tokens=1000)
llm = llm_creation()
# (Keep your summary_prompt, keyword_extraction_prompt, title_generation_prompt here)

@tool("summarize_text")def summarize_text(text: str) -> str:
    """Summarize the given text or article."""
    return llm.invoke(summary_prompt.format(text=text)).content

@tool("extract_keywords")def extract_keywords(text: str) -> str:
    """Extract keywords from the given text."""
    return llm.invoke(keyword_extraction_prompt.format(text=text)).content

@tool("generate_title")def generate_title(text: str) -> str:
    """Generate a title for the given text."""
    return llm.invoke(title_generation_prompt.format(text=text)).content
tools = [summarize_text, extract_keywords, generate_title]
# Initialize persistent SQLite checkpointer (creates memory.db automatically)memory = SqliteSaver.from_conn_string("memory.db")
# Pass the persistent checkpointer to the agentagent = create_react_agent(model=llm, tools=tools, checkpointer=memory)
def run_agent_with_memory(user_query: str, thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    response = agent.invoke(
        {"messages": [{"role": "user", "content": user_query}]},
        config=config
    )
    return response["messages"][-1].content

------------------------------
## ☁️ 2. Cloud Deployment Strategies
When deploying a containerised LLM application to the cloud, you cannot use a local Ollama instance inside the cloud container. In production, you replace ChatOllama with hosted cloud LLMs like AWS Bedrock (Claude / Llama 3) or GCP Vertex AI (Gemini).
## Option A: Deploying to Google Cloud Platform (GCP Cloud Run)
GCP Cloud Run is the easiest and most cost-effective way to deploy Docker containers. It automatically scales down to zero when no one is using your API.

* Step 1: Install GCP CLI
Make sure you have the Google Cloud CLI installed and authenticated on your machine.
* Step 2: Build and Deploy directly from your source folder
Run this single command in your terminal where your Dockerfile is located:

gcloud run deploy text-agent-service --source . --region us-central1 --allow-unauthenticated

* How it works: GCP automatically uploads your code, builds the Docker image in the cloud, creates a public HTTPS URL, and launches your FastAPI server.

## Option B: Deploying to Amazon Web Services (AWS App Runner)
AWS App Runner is a fully managed service that takes your Docker container and deploys it with a secure URL, SSL, and load balancing built-in.

* Step 1: Push your image to AWS ECR (Elastic Container Registry)
Create a private repository in AWS ECR, log in via your terminal, and push your image:

aws ecr create-repository --repository-name text-agent-service
docker tag text-agent-service:latest <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>://
docker push <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>://

* Step 2: Launch App Runner
1. Open the AWS App Runner console.
   2. Click Create Service.
   3. Choose Container registry and select the ECR image you just pushed.
   4. Set the port to 8000 (matching your FastAPI configuration).
   5. Click deploy. AWS will generate a public URL for your microservice.

------------------------------
Would you like me to show you the Python code updates needed to switch from ChatOllama to a cloud LLM like AWS Bedrock or GCP Vertex AI so it works flawlessly after deployment?

Amazon EKS (Elastic Kubernetes Service) is the most powerful, enterprise-grade way to run your Docker containers on AWS [1]. It is used when you need deep control over networking, advanced autoscaling, or want to run your local LLM right alongside your app using cloud GPUs.
Here is the developer blueprint to deploy your text analysis agent to Amazon EKS.
------------------------------
## 1. The Core Infrastructure Problem (And How to Fix It)
When deploying a stateful agent app to Kubernetes, you have to handle two infrastructure shifts:

* The LLM: You can deploy an open-source model using frameworks like vLLM on a GPU-enabled node pool within your cluster, or simply route out to a managed service like AWS Bedrock.
* The SQLite File: Pods in Kubernetes are ephemeral (temporary). If a Pod gets deleted or rescheduled, your local memory.db file disappears. To fix this, you must back it with an AWS EFS (Elastic File System) volume so all instances of your app share the same database file safely.

------------------------------
## 2. The Kubernetes Deployment Blueprint
Create a file named eks-deployment.yaml in your project folder. This single configuration file tells EKS how to configure storage, launch your API containers, and expose them to the public internet via an AWS Load Balancer.

# ==========================================# 1. STORAGE CONFIGURATION (Persistent Volume)# ==========================================apiVersion: v1kind: PersistentVolumeClaimmetadata:
  name: agent-sqlite-pvcspec:
  accessModes:
    - ReadWriteMany  # Allows multiple API pods to write to the database file
  storageClassName: efs-sc  # Backed by AWS Elastic File System (EFS)
  resources:
    requests:
      storage: 5Gi
---# ==========================================# 2. APPLICATION DEPLOYMENT (The Pods)# ==========================================apiVersion: apps/v1kind: Deploymentmetadata:
  name: text-agent-deployment
  labels:
    app: text-agentspec:
  replicas: 3  # High Availability: Runs 3 parallel copies of your API
  selector:
    matchLabels:
      app: text-agent
  template:
    metadata:
      labels:
        app: text-agent
    spec:
      containers:
      - name: api-container
        image: <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.<REGION>://
        ports:
        - containerPort: 8000
        env:
        - name: OLLAMA_HOST
          value: "http://cluster.local" # If hosting model in-cluster
        volumeMounts:
        - name: sqlite-storage
          mountPath: /app/data  # Mounts the shared database directory
      volumes:
      - name: sqlite-storage
        persistentVolumeClaim:
          claimName: agent-sqlite-pvc
---# ==========================================# 3. SERVICE CONFIGURATION (Public Load Balancer)# ==========================================apiVersion: v1kind: Servicemetadata:
  name: text-agent-servicespec:
  type: LoadBalancer  # Automatically provisions an AWS Network/Application Load Balancer
  ports:
  - port: 80
    targetPort: 8000
  selector:
    app: text-agent

Note: If you use the /app/data mount path as shown above, change your python code connection string to initialize SQLite inside that folder: SqliteSaver.from_conn_string("/app/data/memory.db").
------------------------------
## 3. Step-by-Step Deployment Guide
Follow these sequential steps using the AWS CLI and kubectl to push your application live:
## Step 1: Install the AWS EFS CSI Driver
Your EKS cluster needs a driver plugin to talk to AWS storage systems. Run this via your terminal:

kubectl apply -k "://github.com"

## Step 2: Apply the Deployment Blueprint
Deploy the entire configuration file directly into your cluster:

kubectl apply -f eks-deployment.yaml

## Step 3: Monitor Your Deployment
Check the status of your app copies to make sure they transition to a healthy running state:

kubectl get pods -l app=text-agent

## Step 4: Retrieve Your Public URL
Fetch the live DNS endpoint generated by the AWS Load Balancer:

kubectl get service text-agent-service

Copy the long address from the EXTERNAL-IP column. Your FastAPI endpoints are now fully accessible worldwide at http://<YOUR_EXTERNAL_IP>/api/v1/analyze.
------------------------------
Would you like to explore setting up an HPA (Horizontal Pod Autoscaler) so your EKS cluster automatically spawns more API containers when traffic surges, or do you want to see how to run vLLM with a GPU inside the cluster to replace Ollama?

AWS ECS (Elastic Container Service) is the clear winner for your project because it gives you production-grade stability without the massive complexity of Kubernetes.
You are entirely right: AWS ECS is significantly easier to learn, configure, and maintain.
------------------------------
## 🆚 Head-to-Head Comparison

| Feature | AWS ECS (Fargate) | AWS EKS (Kubernetes) |
|---|---|---|
| Learning Curve | Low (Learn it in an afternoon) | Very High (Requires dedicated engineers) |
| Maintenance | Zero (AWS manages the servers) | High (You must handle cluster upgrades) |
| Cost | Pay-as-you-go (Cheaper for small/mid apps) | Base fee (~$70/month baseline just for the cluster) |
| Setup Time | Minutes | Days or Weeks |

------------------------------
## 💡 Why ECS is Perfect for Your Agent App

   1. Serverless Infrastructure (AWS Fargate): With ECS Fargate, you do not manage virtual machines. You simply tell AWS, "Run my Docker container," and it handles the rest.
   2. Built-in Storage: You can link your persistent SQLite memory.db file directly to an AWS EFS volume using a simple dropdown menu in the AWS Console.
   3. No Setup Overhead: Kubernetes requires configuring YAML files for deployments, services, ingress controllers, and storage classes just to get a single URL. ECS handles all of this automatically with a clean graphical user interface.

------------------------------
## 🎯 The Verdict

* Choose AWS ECS if your goal is to launch your application quickly, keep costs low, and focus on writing Python agent logic instead of managing cloud infrastructure.
* Choose Kubernetes (EKS) only if your company already runs hundreds of microservices, has a dedicated DevOps team, or requires complex multi-cloud deployments.

------------------------------
If you want to take the easiest path to production, I can walk you through the AWS ECS Console steps to mount your SQLite storage and launch your API container. Would you like to do that, or would you prefer to look at how to budget and calculate the monthly cost for running this on ECS?

