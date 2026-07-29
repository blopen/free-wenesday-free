# free-wenesday-free

Community-free version of WenesdayOS: 1.2.3

This repository contains code and files for the Wenesday project. Wenesday is an experimental web application and community project for creating, sharing, and browsing algorithms, ideas, and collaborative AI-assisted workflows.

Provider: IT.lopez-be.ch >> lopez.codes >> lopez.zone >> lopez.one

## Project Values

free-wenesday-free is intended to be open, safe, privacy-aware, and inclusive.

- Human dignity, equal treatment, and non-discrimination are core project principles.
- Racism, antisemitism, sexism, homophobia, transphobia, hate speech, harassment, and exclusionary conduct are not accepted.
- Privacy and data minimization guide design and operations.
- Security issues should be reported responsibly and handled with care.
- AI-assisted features should be transparent, accountable, and reviewed by humans where they can affect people.

Please read the project foundation documents before contributing:

- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
- [Privacy Policy](PRIVACY.md)
- [Ethics Policy](ETHICS.md)

## Getting Started

Clone the repository:

```bash
git clone https://github.com/blopen/free-wenesday-free
cd free-wenesday-free
```

Install the project dependencies that match the part of the project you are working on. The repository currently contains Python, web, and experimental AI-related components, so check the relevant files before running services locally.

For the base Python application, start by reviewing `requirements.txt`, then configure required environment variables such as `OPENAI_API_KEY` only in a local environment file or secret manager. Do not commit secrets, personal data, API keys, tokens, session files, or generated credentials.

## Contributing

Contributions are welcome when they improve the project while respecting privacy, safety, security, and inclusion.

1. Create a feature branch from `main`.
2. Keep changes focused and easy to review.
3. Add or update documentation when behavior, configuration, privacy, or security expectations change.
4. Run relevant local checks before opening a pull request.
5. Open a pull request and describe the impact, validation, and any risks.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full contribution workflow.

## Dependencies

The project may include or reference:

- React
- React Router
- Redux
- Material UI
- Firebase
- TensorFlow
- OpenAI APIs
- Quantum/experimental components
- GPT-616-Quantinium alias free-wenesday-free
- LOPEZ model for emotional and mental health contexts

Use dependencies responsibly. Keep them updated, remove unused packages where possible, and avoid adding telemetry or data collection without a documented privacy reason.

## Security

Report suspected vulnerabilities privately. Do not open public issues containing exploit details, secrets, personal data, or live credentials.

See [SECURITY.md](SECURITY.md) for the disclosure process and secure development expectations.

## Privacy and DSGVO

The project follows privacy-by-design and data-minimization principles. Personal data should only be processed when necessary, documented, protected, and removable on request where legally required.

See [PRIVACY.md](PRIVACY.md) for the DSGVO-oriented privacy baseline.

## Ethics and Anti-Discrimination

The project must not be used to promote hatred, discrimination, harassment, unlawful surveillance, or harm against people or protected groups. Human oversight is required for sensitive use cases, especially where AI-assisted functionality can affect rights, safety, access, or wellbeing.

See [ETHICS.md](ETHICS.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Microservice Orchestration Guide

The application can be containerized and orchestrated as a collection of microservices to reduce coupling and scale independently:

- **Identify bounded contexts**: group related routes and models, for example authentication logic in `auth.py` and collaboration endpoints in `collaboration.py`, into separate services with their own data stores.
- **Isolate service interfaces**: expose only the necessary REST endpoints or message queues for each service. Keep cross-service communication asynchronous where possible.
- **Centralize shared contracts**: define common schemas and request/response contracts, for example JSON payloads for algorithm metadata, in a shared package.
- **Automate builds**: containerize each service with a Dockerfile. A base example lives at the repository root and installs Python dependencies from `requirements.txt` before running `app.py`.
- **Orchestrate deployments**: use Docker Compose or an orchestrator such as Azure Kubernetes Service to deploy services together.
- **Scale clients intelligently**: split large clients into domain-specific front-end bundles or API gateways that forward requests to the appropriate service.

### Running the Base Container Locally

```bash
docker build -t wenesday-app .
docker run -p 5000:5000 --env OPENAI_API_KEY=your_key_here wenesday-app
```

Once each service has its own Dockerfile, a `docker-compose.yml` can orchestrate them behind a reverse proxy. Azure users can lift the same images into Azure Container Apps or Azure Kubernetes Service without changing the Dockerfiles.

## Collaborative GPT-4 Sessions

The project provides experimental collaborative chat sessions powered by GPT-4.

Configure an `OPENAI_API_KEY` environment variable before starting the Flask application. The following endpoints are available:

- `POST /collab/create` creates a new collaborative session and returns a `session_id`.
- `POST /collab/<session_id>/chat` sends a message to the session and returns the model response with updated history.
- `GET /collab/<session_id>/history` retrieves the current history of a session.

Treat all conversation content as potentially sensitive. Avoid storing unnecessary personal data, and remove test data that is no longer needed.

## License

The Wenesday project is licensed under the MIT License. See the `LICENSE` directory for more details.

### License Amendment: Purchasing Version Availability for Large Inquiries

Licensee acknowledges and agrees that the purchasing version of the Software will not be readily available for large inquiries. Licensor shall make reasonable efforts to accommodate Licensee's request for the purchasing version, but such availability is not guaranteed.

For further assistance or questions regarding the availability of the purchasing version for large inquiries, contact https://github.com/blopen, https://it.lopez-be.ch, or https://lopez.codes.

## Contributors

The following people have contributed to the development of the Wenesday project:

@wenesday@W (wenesday@lopez.codes) Nelson Lopez (nelson@it.lopez-be.ch)

Command: `@w` as ChatGPT and Bing prompt.
