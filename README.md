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

## EU Data and AI Governance

The repository includes a practical governance package for deployments that process personal data, affect real people, or use AI-assisted functionality:

- [EU Data and AI Governance Pack](docs/compliance/README.md)
- [GDPR Data Protection Pack](docs/compliance/gdpr-data-protection-pack.md)
- [Data Subject Request Playbook](docs/compliance/data-subject-request-playbook.md)
- [EU AI Act Readiness Pack](docs/compliance/eu-ai-act-readiness.md)
- [Human Impact Assessment](docs/compliance/human-impact-assessment.md)

Use these documents before merging or deploying features that collect personal data, rely on AI, classify or recommend content, affect access or opportunity, or create safety, discrimination, privacy, or human-rights risks.

## Getting Started

Clone the repository:

```bash
git clone https://github.com/blopen/free-wenesday-free
cd free-wenesday-free
```

Install the project dependencies that match the part of the project you are working on. The repository currently contains Python, web, and experimental AI-related components, so check the relevant files before running services locally.

For the base Python application, start by reviewing `requirements.txt`, then configure required environment variables such as `OPENAI_API_KEY` only in a local environment file or secret manager. Do not commit secrets, personal data, API keys, tokens, session files, or generated credentials.

## Working With `.wd` Files

Files ending in `.wd` are Wenesday definition files. In this repository they can be used as lightweight text instructions, command definitions, prompts, workflow notes, or small project-specific configuration blocks.

Treat `.wd` files as data first, not trusted executable code. Read, validate, and interpret them with a small parser in the host language instead of directly executing their contents.

A simple `.wd` file can look like this:

```text
# hello.wd
name: hello-wenesday
kind: command
version: 1

run: say hello from Wenesday
```

Recommended basic rules:

- Use UTF-8 text.
- Use `#` for comments.
- Use `key: value` lines for simple metadata.
- Leave blank lines between logical sections.
- Do not store secrets, tokens, passwords, personal data, or private prompts in `.wd` files.
- Validate allowed keys before using the file in an app, agent, script, or service.

### Reading `.wd` Files With Python

```python
from pathlib import Path


def read_wd(path: str) -> dict[str, str]:
    data: dict[str, str] = {}

    for raw_line in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"Invalid .wd line: {raw_line}")

        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()

    allowed_keys = {"name", "kind", "version", "run"}
    unknown_keys = set(data) - allowed_keys
    if unknown_keys:
        raise ValueError(f"Unknown .wd keys: {sorted(unknown_keys)}")

    return data


command = read_wd("hello.wd")
print(command["name"], command.get("run", ""))
```

### Reading `.wd` Files With C++

```cpp
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>

static std::string trim(const std::string& value) {
    const auto start = value.find_first_not_of(" \t\r\n");
    if (start == std::string::npos) return "";
    const auto end = value.find_last_not_of(" \t\r\n");
    return value.substr(start, end - start + 1);
}

std::map<std::string, std::string> readWd(const std::string& path) {
    std::ifstream file(path);
    if (!file) throw std::runtime_error("Could not open .wd file");

    std::map<std::string, std::string> data;
    std::set<std::string> allowed = {"name", "kind", "version", "run"};
    std::string line;

    while (std::getline(file, line)) {
        std::string cleaned = trim(line);
        if (cleaned.empty() || cleaned[0] == '#') continue;

        const auto separator = cleaned.find(':');
        if (separator == std::string::npos) {
            throw std::runtime_error("Invalid .wd line: " + line);
        }

        std::string key = trim(cleaned.substr(0, separator));
        std::string value = trim(cleaned.substr(separator + 1));

        if (!allowed.contains(key)) {
            throw std::runtime_error("Unknown .wd key: " + key);
        }

        data[key] = value;
    }

    return data;
}

int main() {
    auto command = readWd("hello.wd");
    std::cout << command["name"] << " -> " << command["run"] << '\n';
}
```

### Safety Notes for `.wd`

- Never pass `.wd` content directly into a shell, compiler, AI tool, browser, database query, or network call.
- Use allowlists for commands, file paths, model/tool names, and environment variables.
- Keep a human review step for `.wd` files that can affect people, privacy, security, or AI behavior.
- For AI-related `.wd` files, apply the [EU AI Act Readiness Pack](docs/compliance/eu-ai-act-readiness.md) and [Human Impact Assessment](docs/compliance/human-impact-assessment.md).

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
