# Cursor MCP Training Guide (Simple English)

This guide is written in very simple steps.
Your team can copy, run, and learn quickly.

---

## What is the goal?

Use Cursor with MCP so developers can:
- finish tasks faster
- write clearer Jira updates
- create better pull requests
- reduce rework between design and code

---

## Top MCP tools for development

Start with these first:
1. Bitbucket/Git MCP
2. Jira MCP
3. Figma MCP
4. Docs MCP (Confluence or Notion)
5. CI/CD MCP
6. Database MCP

---

## Top agent skills to create first

Create these six starter skills:
1. `jira-ticket-triage`
2. `figma-handoff`
3. `pr-quality-check`
4. `release-note-writer`
5. `bug-root-cause`
6. `test-case-generator`

---

## Step 1: Local setup commands

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

## Step 2: Add your tokens

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

echo '.env' >> .gitignore
```

Important:
- Never commit `.env` to git.
- Rotate tokens every 90 days.

---

## Step 3: Open Cursor settings and connect MCP

In Cursor:
1. Open **Settings**
2. Open **Features**
3. Click **MCP**
4. Turn MCP **ON**
5. Click **Open mcp.json**

The presentation includes screenshot slides for this process:
- `cursor_settings_screen.png`
- `cursor_mcp_json_screen.png`
- `cursor_status_screen.png`

---

## Step 4: Add mcp.json

Create `.cursor/mcp.json`:

```json
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
```

Then restart Cursor.

---

## Step 5: Test Jira connection

```bash
source .venv/bin/activate && source .env
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/myself" | jq '.displayName'
```

Prompt in Cursor:
- `Using Jira MCP, summarize PROJ-101 and draft acceptance criteria.`

---

## Step 6: Test Figma connection

```bash
source .venv/bin/activate && source .env
export FIGMA_FILE_KEY=<file_key>
curl -s -H "X-Figma-Token: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/files/$FIGMA_FILE_KEY" | jq '.name'
```

Prompt in Cursor:
- `Using Figma MCP, extract design tokens and map components to stories.`

---

## Step 7: Test Bitbucket connection

```bash
source .venv/bin/activate && source .env
curl -s -u "$BITBUCKET_USERNAME:$BITBUCKET_APP_PASSWORD" \
  "https://api.bitbucket.org/2.0/repositories/$BITBUCKET_WORKSPACE" | jq '.values[0].full_name'
```

Prompt in Cursor:
- `Using Bitbucket MCP, summarize PR #123 and create a review checklist.`

---

## Step 8: Create first agent skill

```bash
mkdir -p skills/jira-ticket-triage
cd skills/jira-ticket-triage

cat > skill.yaml <<'YAML'
name: jira-ticket-triage
version: 1.0.0
description: Triage issue and return action plan
tools: [jira.search, jira.get_issue]
YAML

cat > prompts.md <<'MD'
# Inputs
- issue_key
- team_context
- done_definition

# Outputs
- summary
- acceptance_criteria
- test_cases
MD

echo '[{"input":"PROJ-101","assert_contains":["Summary","Acceptance"]}]' > tests.json
```

---

## Easy weekly team routine

1. Monday: review top Jira tasks with Cursor.
2. Daily: use PR quality skill before review.
3. Wednesday: improve one weak prompt.
4. Friday: check KPIs and publish one skill update.

Track these KPIs:
- cycle time
- PR lead time
- reopen rate
- prompt reuse
- automation success

---

## Simple safety rules

1. Use low-access tokens only.
2. Ask human approval for write actions.
3. Keep logs for all MCP actions.
4. Review failures every week.

This is the easiest way to learn fast and adopt safely.
