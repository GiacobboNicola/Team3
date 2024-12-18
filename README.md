# Team3

Il progetto ABC è un prototipo di un servizio pensato per assistere i clienti di Aruba nel calcolo del budget per i loro progetti basati sul cloud. Tramite l'interfaccia web l'utente è in grado di configurare le risorse che vuole allocare sui propri progetti (container, cloud computing, storage e networking) **fornendo informazioni sui prezzi in tempo reale**. Inoltre l'applicazione consentirà agli utenti di passare, senza interruzioni, dalla stima dei costi all'effettivo ordine e deploy delle risorse.

## Technology Stack

- Docker & Docker Compose

### Backend Stack

- Python 3.12
- PDM (Python dependency manager)
- FastAPI (for API endpoints)
- Redis

### Frontend Stack

- SvelteKit
- TypeScript
- TailwindCSS
- Vite (Build tool)
- Node.js

## Prerequisites

- Taskfile
- Docker & Docker Compose

### Backend Requirements

- Python 3.12 or higher
- PDM (Python dependency manager)
- Redis

### Frontend Requirements

- Node.js (v18 or higher)
- npm (comes with Node.js)
- Modern web browser (Chrome, Firefox, Safari, or Edge)

## Backend

Backend service for the Aruba Cloud Services Budget Calculator, designed to help users with setup and budgeting of Aruba cloud services.

### Project Structure

```bash
aruba-budget-calc-be/
├── team3-lib/         # Shared library code
├── team3-core/        # Core business logic
├── team3-api/         # API service
└── team3-test/        # Test suite
```

### Docker Build Stages

The project uses a multi-stage Dockerfile that includes:

- `runtime`: Base Python runtime environment
- `pdm`: PDM package manager setup
- `lib`: Team3 library package
- `core`: Core business logic
- `api`: API service
- `test`: Testing environment

Each stage is optimized for its specific purpose and includes only necessary dependencies.

### Environment Variables

The following environment variables are supported:

- `ENV`: Set to 'development' or 'production'
- `PYTHONPATH`: Automatically configured in Docker
- Additional environment variables can be configured via `.env` file

### Testing

Run tests using:

```bash
docker compose up api core test bondy
# or with Taskfile
task be:test
```

After a while, if everything works fine, you should see the ping message like the following:
![Test bus wamp](docs/test_aruba.png)
> To be implemented:

```bash
docker compose run test pytest
```

## Frontend

### Developing

To start the project simply run

```bash
npm install
npm run dev
# or start the server and open the app in a new browser tab
npm run dev -- --open
```

### Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
