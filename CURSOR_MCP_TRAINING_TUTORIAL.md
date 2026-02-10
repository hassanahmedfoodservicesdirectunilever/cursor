# Cursor MCP Training Tutorial (Jira, Figma, Bitbucket)

This guide is a practical runbook for developer teams to learn and adopt Cursor + MCP quickly.

## 1) Prerequisites

- Cursor installed and signed in
- Python 3.10+ and Node.js 18+
- Access tokens for Jira, Figma, and Bitbucket
- A pilot repo and Jira project

---

## 2) Local setup commands

```bash
mkdir -p ~/cursor-mcp-training/{servers,skills,logs}
cd ~/cursor-mcp-training

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install mcp httpx python-dotenv pyyaml

python --version && node --version && npm --version
sudo apt-get update && sudo apt-get install -y jq
```

---

## 3) Save credentials

```bash
cat > .env <<'EOF'
JIRA_BASE_URL=https://your-company.atlassian.net
JIRA_EMAIL=you@company.com
JIRA_API_TOKEN=<jira_token>
FIGMA_TOKEN=<figma_token>
BITBUCKET_WORKSPACE=<workspace>
BITBUCKET_USERNAME=<username>
BITBUCKET_APP_PASSWORD=<app_password>
EOF
```

---

## 4) Configure MCP in Cursor

Create `.cursor/mcp.json` (template):

```bash
mkdir -p .cursor
cat > .cursor/mcp.json <<'JSON'
{
  "mcpServers": {
    "jira": {
      "command": "python",
      "args": ["servers/jira_server.py"],
      "envFile": ".env"
    },
    "figma": {
      "command": "python",
      "args": ["servers/figma_server.py"],
      "envFile": ".env"
    },
    "bitbucket": {
      "command": "python",
      "args": ["servers/bitbucket_server.py"],
      "envFile": ".env"
    }
  }
}
JSON
```

> Replace `servers/*.py` with your MCP server executable paths.

---

## 5) Validate integrations

### Jira

```bash
source .venv/bin/activate && source .env
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/myself" | jq '.displayName'
```

### Figma

```bash
source .venv/bin/activate && source .env
export FIGMA_FILE_KEY=<file_key>
curl -s -H "X-Figma-Token: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/files/$FIGMA_FILE_KEY" | jq '.name'
```

### Bitbucket

```bash
source .venv/bin/activate && source .env
curl -s -u "$BITBUCKET_USERNAME:$BITBUCKET_APP_PASSWORD" \
  "https://api.bitbucket.org/2.0/repositories/$BITBUCKET_WORKSPACE" | jq '.values[0].full_name'
```

---

## 6) Team lab prompts (run in Cursor chat)

### Jira lab

- `Using Jira MCP, summarize PROJ-101, draft acceptance criteria, and generate test cases.`
- `Generate standup update with blockers, risks, and next actions for PROJ sprint.`

### Figma lab

- `Using Figma MCP, extract design tokens and component variants for frame HomePage.`
- `Map design components to frontend stories with acceptance criteria.`

### Bitbucket lab

- `Using Bitbucket MCP, summarize PR #123 and list review risk areas.`
- `Create release notes from commits merged since the previous tag.`

---

## 7) Add agent skills (reusable templates)

```bash
mkdir -p skills/jira-ticket-triage
cd skills/jira-ticket-triage

cat > skill.yaml <<'YAML'
name: jira-ticket-triage
version: 1.0.0
description: Triage issue and output action plan
tools: [jira.search, jira.get_issue]
YAML

cat > prompts.md <<'MD'
# Inputs
- issue_key
- team_context
- definition_of_done

# Outputs
- summary
- acceptance_criteria
- test_cases
MD

echo '[{"input":"PROJ-101","assert_contains":["summary","acceptance_criteria","test_cases"]}]' > tests.json
```

---

## 8) Weekly operations and adoption commands

```bash
mkdir -p logs metrics

# Replace scripts with your internal automation tooling
python scripts/export_mcp_logs.py --last-days 7 > logs/mcp_weekly.json
python scripts/calc_kpis.py --input logs/mcp_weekly.json --output metrics/weekly_kpis.csv

echo 'date,cycle_time,pr_lead_time,reopen_rate,prompt_reuse,automation_success' > metrics/template.csv
```

Track these KPIs weekly:
- Cycle time
- PR lead time
- Reopen/rework rate
- Prompt reuse rate
- Automation success rate

---

## 9) Easy adoption model (recommended)

1. Start with one pilot squad (5-8 developers).
2. Use read-only MCP actions first.
3. Add write actions only with approval checkpoints.
4. Publish 3-5 team skills in month 1.
5. Run weekly 30-minute office hours.

This model keeps rollout safe, practical, and easy for developers to adopt.
