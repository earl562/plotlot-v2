---
model: opus
allowed-tools: Bash, Read, Grep, Glob
---
Autonomous cross-model QA — send current work to Gemini CLI for independent review.

## Steps

1. Get the current diff:
   ```bash
   git diff HEAD~1 --stat
   ```

2. Generate a review prompt summarizing the changes and key questions.

3. Send to Gemini for independent review:
   ```bash
   gemini -p "You are reviewing a PlotLot code change. Here is the diff summary and key files. Review for: correctness, edge cases, security issues, test coverage gaps. Be specific and actionable.\n\n$(git diff HEAD~1)"
   ```

4. Present Gemini's review alongside your own assessment. Flag agreements and disagreements.
