# Cursor MCP Training Guide (Simple English)

This guide is written in very simple steps.
Your team can copy, run, and learn quickly.

---

## Decks you now have

1. **Participant deck (full spoon-feed)**  
   `Solution_Assessment_Cursor_AI_Capabilities_Integration_Review_Participant.pptx`

2. **Trainer deck (45-minute version)**  
   `Solution_Assessment_Cursor_AI_Capabilities_Integration_Review_Trainer_45min.pptx`

3. **Legacy file name (same as participant deck)**  
   `Solution_Assessment_Cursor_AI_Capabilities_Integration_Review.pptx`

Use trainer deck for delivery, and participant deck for sharing after session.

---

## Recommended video links (for self-learning)

Use these links for homework after training:

1. Cursor AI beginner tutorial  
   https://www.youtube.com/results?search_query=Cursor+AI+beginner+tutorial
2. Cursor MCP setup tutorial  
   https://www.youtube.com/results?search_query=Cursor+MCP+setup+tutorial
3. Model Context Protocol explained  
   https://www.youtube.com/results?search_query=Model+Context+Protocol+explained
4. Anthropic MCP tutorial  
   https://www.youtube.com/results?search_query=Anthropic+MCP+tutorial
5. Jira REST API tutorial  
   https://www.youtube.com/results?search_query=Jira+REST+API+tutorial+developers
6. Figma API tutorial  
   https://www.youtube.com/results?search_query=Figma+API+tutorial+for+developers
7. Bitbucket API tutorial  
   https://www.youtube.com/results?search_query=Bitbucket+API+tutorial
8. Prompt engineering for developers  
   https://www.youtube.com/results?search_query=Prompt+engineering+for+software+developers
9. AI agent workflow tutorials  
   https://www.youtube.com/results?search_query=AI+agent+workflow+tutorial+developers
10. Build MCP server in Python  
    https://www.youtube.com/results?search_query=Build+MCP+server+Python+tutorial
11. API token security best practices  
    https://www.youtube.com/results?search_query=API+token+security+best+practices
12. LLM governance for enterprise  
    https://www.youtube.com/results?search_query=LLM+governance+for+enterprise+teams

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

## Prompt formula cheat sheet (always use this)

Use this structure in every prompt:

1. **Context** -> where to work (repo, Jira key, Figma file)
2. **Task** -> what you want (summary, checklist, code, tests)
3. **Constraints** -> limits (read-only, short output, style guide)
4. **Output format** -> bullet list, table, JSON, markdown

Example:

`Context: PROJ-101 in Jira. Task: write acceptance criteria and test cases. Constraints: no status change. Output: bullet list.`

---

## Do / Don't quick guide

### Do
- Use short, clear prompts
- Start in read-only mode
- Ask for approval before write actions
- Save good prompts as reusable skills
- Check logs weekly

### Don't
- Do not use admin tokens
- Do not merge without review
- Do not skip test/checklist steps
- Do not ignore failed automations
- Do not keep old skills without review

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

## Common errors and quick fixes

| Error | What it means | Quick fix |
|---|---|---|
| 401 Unauthorized | Token wrong or expired | Create new token and update `.env` |
| 403 Forbidden | No access to project/file | Ask for correct permission |
| 404 Not Found | Wrong key/URL/workspace | Check Jira key, file key, repo/workspace |
| Empty result | Query/filter too strict | Use wider query and test again |
| MCP server missing in Cursor | `mcp.json` not loaded | Save file and restart Cursor |

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

## 5-minute daily routine (for every developer)

1. **Minute 1:** Open top Jira task.
2. **Minute 2:** Ask Cursor for task plan.
3. **Minute 3:** Run PR quality/test checklist skill.
4. **Minute 4:** Update status with safe prompt.
5. **Minute 5:** Save one useful prompt to skill library.

This small habit gives fast adoption.

---

## Trainer script (simple timing)

- **0-10 min:** Demo Cursor + MCP connection.
- **10-35 min:** Pair lab (Jira flow).
- **35-55 min:** Pair lab (Figma or Bitbucket flow).
- **55-75 min:** Build first skill together.
- **75-90 min:** Troubleshooting using Common Errors slide + Q&A.

---

## Simple safety rules

1. Use low-access tokens only.
2. Ask human approval for write actions.
3. Keep logs for all MCP actions.
4. Review failures every week.

This is the easiest way to learn fast and adopt safely.
