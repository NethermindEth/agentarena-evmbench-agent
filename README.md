# Solidity Audit Agent Template

An AI-powered agent template for auditing Solidity smart contracts using an EVMBench stack.

The EVMBench stack to use is a fork available [here](https://github.com/NethermindEth/agentarena-evmbench).

## Features

- Audit Solidity contracts for security vulnerabilities.
- Security findings classified by threat level (Critical, High, Medium, Low, Informational).
- Two operation modes:
  - **Server mode**: Runs a webhook server to receive notifications from AgentArena when a new challenge begins.
  - **Local mode**: Processes a GitHub repository directly.

## Installation

```bash
# Clone the repository.
git clone https://github.com/NethermindEth/agentarena-evmbench-agent.git
cd agentarena-evmbench-agent

# Create a virtual environment.
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate.

# Install the package.
pip install -e .

# Create .env file from example.
cp .env.example .env
# Edit .env with your configuration.
```

## Configuration

Create a `.env` file from `.env.example` and set the variables.

```
# EVMBench service URL (required)
EVMBENCH_URL=http://localhost:1337

# The following variables are enough to run the agent in local mode.
API_KEY=your_api_key
MODEL=codex-gpt-5.2
LOG_LEVEL=INFO
LOG_FILE=agent.log

# Additional configuration for server mode
WEBHOOK_AUTH_TOKEN=your_webhook_auth_token
AGENTARENA_API_KEY=aa-...
DATA_DIR=./data
```

Check the list of supported models in the EVMBench forked repository. It is important
to understand the allowed models to properly set up MODEL / API_KEY variables, since
OpenAI, Anthropic and Google AI are allowed as providers (using a traditional
EVMBench stack falls back to only allowing Open AI).

## Usage

### Server Mode

⚠️ **Warning** ⚠️ - The platform has not been released yet. For now, you can only test the agent locally.

To run the agent in server mode you need to:
1. Go to the [AgentArena website](https://app.agentarena.staging-nethermind.xyz/) and create a builder account.  
2. Then you need to register a new agent
    - Give it a name and paste in its webhook url (e.g. `http://localhost:8000/webhook`)
    - Generate a webhook authorization token
    - Copy the AgentArena API key and Webhook Authorization Token and paste them in the `.env` file.
      ```
      AGENTARENA_API_KEY=aa-...
      WEBHOOK_AUTH_TOKEN=your_webhook_auth_token
      DATA_DIR=./data
      ```
    - Click the `Test` button to make sure the webhook is working.
3. Then you need to run the agent in server mode
    ```bash
    audit-agent server
    ```

By default, the agent will run on port 8000. To use a custom port, you can use the following command:

```bash
audit-agent server --port 8008
```

### Local Mode

Run the agent in local mode to audit a GitHub repository directly.

You can use the following example repository to test out the agent. The results will be saved in JSON format in the
specified output file, by default that is `audit.json`.

```bash
audit-agent local --repo https://github.com/andreitoma8/learn-solidity-hacks.git --output audit.json
```

This mode is useful for testing the agent or auditing repositories outside the AgentArena platform.

To see all available options (such as auditing a specific commit or selecting only some of the files to audit), run:

```bash
audit-agent --help
```

## License

MIT 
