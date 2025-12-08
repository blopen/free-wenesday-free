This repository contains code and files for the "Wenesday" project. Wenesday is a web application that allows users to create and share their favorite recipes, as well as browse recipes from other users.

Provider: IT.lopez-be.ch >> lopez.codes >> lopez.zone >> lopez.one

Getting Started:

This project is a web application called "Wenesday" that allows users to create, share, and browse their favorite algorithms. The application is built using React, React-Router, Redux, Material-UI, and Firebase and includes endpoints that enable the creation, updating, and deletion of algorithms. Users can also search for algorithms and filter them by various criteria. The goal of Wenesday is to create a vibrant community of algorithm enthusiasts and foster the exchange of algorithmic ideas.

If you would like to contribute to the Wenesday project, you can do so by cloning the repository to your local machine. To do this, you will need to have Git installed on your computer. Once you have Git installed, you can clone the repository by running the following command in your terminal:

>> git clone https://github.com/blopen/free-wenesday-free

After you have cloned the repository, you can make changes to the code and files as needed. When you are ready to commit your changes, be sure to create a new branch and commit your changes to that branch. Once you have committed your changes, you can submit a pull request to the main branch for review.

Dependencies:

React
React-Router
Redux
Material-UI
Firebase
TensorFlow
OpenAI
Quantum
GPT-616-Quantinium (alias free-wenesday-free)
LOPEZ-Modell für emotionale und psychische Gesundheit

License:

The Wenesday project is licensed under the MIT License. See the LICENSE file for more details.

License Amendment: Purchasing Version Availability for Large Inquiries

Availability of Purchasing Version for Large Inquiries
Licensee acknowledges and agrees that the purchasing version of the Software will not be readily available for large inquiries. Licensor shall make reasonable efforts to accommodate Licensee's request for the purchasing version, but such availability is not guaranteed.

Contact Information
For further assistance or questions regarding the availability of the purchasing version for large inquiries, Licensee may contact Licensor at https://github.com/blopen, or visit https://it.lopez-be.ch and 
https://lopez.codes.

Effect of Amendment
This Amendment shall be deemed incorporated into and made a part of the Agreement, and all other terms and conditions of the Agreement shall remain in full force and effect.

In witness whereof, the parties have executed this Amendment as of the date set forth below.

Contributors:

The following people have contributed to the development of the Wensday project:

@wenesday@W (wenesday@lopez.codes) Nelson Lopez (nelson@it.lopez-be.ch)

Command:"@w" as ChatGPT and Bing prompt.
If you would like to contribute to the project, please submit a pull request with your changes. We welcome all contributions!
# free-wenesday-free
-- Community-free-Version of WenesdayOS: 1.2.3

## Microservice orchestration guide

The application can be containerized and orchestrated as a collection of microservices to reduce coupling and scale independently:

- **Identify bounded contexts**: group related routes and models (for example, the authentication logic in `auth.py` and collaboration endpoints in `collaboration.py`) into separate services with their own data stores.
- **Isolate service interfaces**: expose only the necessary REST endpoints or message queues for each service. Keep cross-service communication asynchronous where possible to avoid tight coupling.
- **Centralize shared contracts**: define common schemas and request/response contracts (for example JSON payloads for algorithm metadata) in a shared package that services can import to stay in sync.
- **Automate builds**: containerize each service with a Dockerfile. A base example lives at the repository root and installs Python dependencies from `requirements.txt` before running `app.py`.
- **Orchestrate deployments**: use Docker Compose or an orchestrator such as Azure Kubernetes Service to deploy services together. Compose files can specify per-service images, environment variables, and shared networks so that clients can reach each service by name.
- **Scale clients intelligently**: split large clients into domain-specific front-end bundles or API gateways that forward requests to the appropriate service. This keeps the client lightweight while still supporting the full feature set.

### Running the base container locally

To build and run the monolithic app in a container (as a starting point before splitting services):

```
docker build -t wenesday-app .
docker run -p 5000:5000 --env OPENAI_API_KEY=your_key_here wenesday-app
```

Once each service has its own Dockerfile, a `docker-compose.yml` can orchestrate them behind a reverse proxy. Azure users can lift the same images into Azure Container Apps or Azure Kubernetes Service without changing the Dockerfiles.

## Collaborative GPT-4 Sessions

The project provides experimental collaborative chat sessions powered by GPT-4.

To use this feature, configure an `OPENAI_API_KEY` environment variable before
starting the Flask application. The following endpoints are available:

- `POST /collab/create` – create a new collaborative session and obtain a
  `session_id`.
- `POST /collab/<session_id>/chat` – send a message to the session and receive
  the model's response along with the updated history.
- `GET /collab/<session_id>/history` – retrieve the current history of a
  session.

These endpoints make it easy for multiple clients to share a conversation and
receive GPT-4 powered responses.
