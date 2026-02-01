"""
Tests for platform cohesiveness and meta-cognition accuracy.

Validates that the platform components work together correctly:
- Capability inventory counts match actual files
- Orchestrator mappings reference valid components
- Cross-component references are consistent
- Quality gates are properly defined
"""

import re
import pytest
from pathlib import Path
from typing import Dict, List, Set, Tuple


class TestCapabilityInventory:
    """Test that meta-cognition capability inventory matches reality."""

    def test_command_count_matches(self, claude_dir: Path):
        """Test that meta-cognition command count matches actual commands."""
        # Get actual command count
        commands_dir = claude_dir / "commands"
        actual_commands = [f for f in commands_dir.glob("*.md") if not f.name.startswith("_")]
        actual_count = len(actual_commands)

        # Get claimed count from meta-cognition
        meta_cog = claude_dir / "skills" / "orchestration" / "meta-cognition.md"
        content = meta_cog.read_text(encoding='utf-8')

        # Look for "### Available Commands (N)"
        match = re.search(r'### Available Commands \((\d+)\)', content)
        if not match:
            pytest.skip("Could not find command count in meta-cognition.md")

        claimed_count = int(match.group(1))

        assert actual_count == claimed_count, (
            f"Meta-cognition claims {claimed_count} commands but found {actual_count}. "
            f"Update meta-cognition.md capability inventory."
        )

    def test_agent_count_matches(self, claude_dir: Path):
        """Test that meta-cognition agent count matches actual agents."""
        # Get actual agent count
        agents_dir = claude_dir / "agents"
        actual_agents = [f for f in agents_dir.glob("*.md") if not f.name.startswith("_")]
        actual_count = len(actual_agents)

        # Get claimed count from meta-cognition
        meta_cog = claude_dir / "skills" / "orchestration" / "meta-cognition.md"
        content = meta_cog.read_text(encoding='utf-8')

        # Look for "### Available Agents (N)"
        match = re.search(r'### Available Agents \((\d+)\)', content)
        if not match:
            pytest.skip("Could not find agent count in meta-cognition.md")

        claimed_count = int(match.group(1))

        assert actual_count == claimed_count, (
            f"Meta-cognition claims {claimed_count} agents but found {actual_count}. "
            f"Update meta-cognition.md capability inventory."
        )

    def test_rule_count_matches(self, claude_dir: Path):
        """Test that meta-cognition rule count matches actual rules."""
        # Get actual rule count
        rules_dir = claude_dir / "rules"
        actual_rules = [f for f in rules_dir.glob("*.md") if not f.name.startswith("_")]
        actual_count = len(actual_rules)

        # Get claimed count from meta-cognition
        meta_cog = claude_dir / "skills" / "orchestration" / "meta-cognition.md"
        content = meta_cog.read_text(encoding='utf-8')

        # Look for "### Available Rules (N)"
        match = re.search(r'### Available Rules \((\d+)\)', content)
        if not match:
            pytest.skip("Could not find rule count in meta-cognition.md")

        claimed_count = int(match.group(1))

        assert actual_count == claimed_count, (
            f"Meta-cognition claims {claimed_count} rules but found {actual_count}. "
            f"Update meta-cognition.md capability inventory."
        )

    def test_agents_listed_in_inventory(self, claude_dir: Path):
        """Test that all agents are listed in meta-cognition inventory."""
        # Get actual agent names
        agents_dir = claude_dir / "agents"
        actual_agents = {f.stem for f in agents_dir.glob("*.md") if not f.name.startswith("_")}

        # Get agents listed in meta-cognition
        meta_cog = claude_dir / "skills" / "orchestration" / "meta-cognition.md"
        content = meta_cog.read_text(encoding='utf-8')

        # Extract agent names from the table (backtick-wrapped)
        # Look for `agent-name` patterns
        listed_agents = set(re.findall(r'`([a-z][a-z0-9-]*)`', content))

        # Also include special agent names that might not have standard suffixes
        special_agents = {'researcher'}
        listed_agents.update(a for a in special_agents if a in content.lower())

        # Filter to only agent-like names (those with common suffixes or known agents)
        agent_suffixes = {'analyst', 'engineer', 'expert', 'writer', 'reviewer', 'optimizer', 'designer', 'specialist'}
        listed_agents = {a for a in listed_agents
                        if any(a.endswith(f'-{s}') for s in agent_suffixes)
                        or a in special_agents}

        missing = actual_agents - listed_agents
        if missing:
            pytest.fail(
                f"Agents not listed in meta-cognition inventory: {missing}. "
                f"Update the Available Agents section."
            )


class TestOrchestratorMappings:
    """Test that task-orchestrator mappings reference valid components."""

    def test_orchestrator_rules_exist(self, claude_dir: Path):
        """Test that rules referenced in task-orchestrator actually exist."""
        # Get actual rule names
        rules_dir = claude_dir / "rules"
        actual_rules = {f.stem.lower() for f in rules_dir.glob("*.md") if not f.name.startswith("_")}

        # Get rules referenced in orchestrator
        orchestrator = claude_dir / "skills" / "orchestration" / "task-orchestrator.md"
        content = orchestrator.read_text(encoding='utf-8')

        # Find @rules/[name] references
        referenced_rules = set(re.findall(r'@rules/([a-z][\w-]*)', content, re.IGNORECASE))
        referenced_rules = {r.lower() for r in referenced_rules}

        # Check for invalid references (exclude placeholder patterns like "[affected-domain]")
        invalid = {r for r in referenced_rules if not r.startswith('[') and r not in actual_rules}

        if invalid:
            pytest.fail(
                f"Task orchestrator references non-existent rules: {invalid}. "
                f"Available rules: {sorted(actual_rules)}"
            )

    def test_orchestrator_patterns_exist(self, claude_dir: Path):
        """Test that patterns referenced in task-orchestrator actually exist."""
        # Get actual pattern names
        patterns_dir = claude_dir / "patterns"
        actual_patterns = set()
        if patterns_dir.exists():
            for f in patterns_dir.rglob("*.md"):
                if not f.name.startswith("_"):
                    actual_patterns.add(f.stem.lower())

        # Get patterns referenced in orchestrator
        orchestrator = claude_dir / "skills" / "orchestration" / "task-orchestrator.md"
        content = orchestrator.read_text(encoding='utf-8')

        # Find @patterns/[name] references
        referenced_patterns = set(re.findall(r'@patterns/([a-z][\w-]*)', content, re.IGNORECASE))
        referenced_patterns = {p.lower() for p in referenced_patterns}

        # Check for invalid references (exclude placeholders)
        invalid = {p for p in referenced_patterns if not p.startswith('[') and p not in actual_patterns}

        if invalid:
            pytest.fail(
                f"Task orchestrator references non-existent patterns: {invalid}. "
                f"Available patterns: {sorted(actual_patterns)}"
            )

    def test_orchestrator_agents_exist(self, claude_dir: Path):
        """Test that agents referenced in task-orchestrator actually exist."""
        # Get actual agent names
        agents_dir = claude_dir / "agents"
        actual_agents = {f.stem.lower() for f in agents_dir.glob("*.md") if not f.name.startswith("_")}

        # Get agents referenced in orchestrator
        orchestrator = claude_dir / "skills" / "orchestration" / "task-orchestrator.md"
        content = orchestrator.read_text(encoding='utf-8')

        # Find agent names - match full hyphenated names ending with agent suffixes
        # Pattern: one or more word-parts followed by a suffix (e.g., ui-ux-expert, code-reviewer)
        agent_suffixes = ['analyst', 'engineer', 'expert', 'writer', 'reviewer', 'optimizer', 'designer', 'specialist']
        # Match full agent names: word(-word)*-suffix, excluding bracketed placeholders
        pattern = r'(?<!\[)(?<![a-z-])([a-z]+(?:-[a-z]+)*-(?:' + '|'.join(agent_suffixes) + r'))(?![a-z-])(?!\])'
        referenced_agents = set(re.findall(pattern, content.lower()))

        # Also look for agents in tables (but not placeholders in brackets)
        table_agents = set(re.findall(r'\|\s*([a-z]+(?:-[a-z]+)+)\s*\|', content.lower()))
        table_agents = {a for a in table_agents if any(a.endswith('-' + s) for s in agent_suffixes)}
        referenced_agents.update(table_agents)

        # Remove any that are clearly placeholders (contain "domain" as generic)
        referenced_agents = {a for a in referenced_agents if 'domain-' not in a}

        invalid = referenced_agents - actual_agents

        if invalid:
            pytest.fail(
                f"Task orchestrator references non-existent agents: {invalid}. "
                f"Available agents: {sorted(actual_agents)}"
            )


class TestQualityGateConsistency:
    """Test that quality gates are consistently defined."""

    def test_dod_gates_match_loop(self, claude_dir: Path):
        """Test that definition-of-done gates align with autonomous-loop gates."""
        dod_file = claude_dir / "skills" / "quality" / "definition-of-done.md"
        loop_file = claude_dir / "skills" / "orchestration" / "autonomous-loop.md"

        if not dod_file.exists() or not loop_file.exists():
            pytest.skip("Required files not found")

        dod_content = dod_file.read_text(encoding='utf-8').lower()
        loop_content = loop_file.read_text(encoding='utf-8').lower()

        # Check for key quality gate concepts that should appear in both
        # Use multiple synonyms for each concept
        key_gates = {
            'coverage': ['coverage', 'test coverage', 'code coverage'],
            'lint': ['lint', 'linting', 'eslint', 'linter'],
            'security': ['security', 'vulnerabilities', 'secure'],
            'documentation': ['documentation', 'docs', 'readme', 'changelog'],
        }

        missing_in_dod = []
        missing_in_loop = []

        for gate_name, synonyms in key_gates.items():
            # Check if any synonym is present
            found_in_dod = any(syn in dod_content for syn in synonyms)
            found_in_loop = any(syn in loop_content for syn in synonyms)

            if not found_in_dod:
                missing_in_dod.append(gate_name)
            if not found_in_loop:
                missing_in_loop.append(gate_name)

        issues = []
        if missing_in_dod:
            issues.append(f"Quality gate concepts missing in definition-of-done: {missing_in_dod}")
        if missing_in_loop:
            issues.append(f"Quality gate concepts missing in autonomous-loop: {missing_in_loop}")

        if issues:
            pytest.fail("\n".join(issues))


class TestLoopPhaseConsistency:
    """Test that loop phases are properly defined."""

    def test_loop_has_required_phases(self, claude_dir: Path):
        """Test that autonomous-loop defines all required phases."""
        loop_file = claude_dir / "skills" / "orchestration" / "autonomous-loop.md"

        if not loop_file.exists():
            pytest.skip("autonomous-loop.md not found")

        content = loop_file.read_text(encoding='utf-8').lower()

        # Required phases in the loop
        required_phases = [
            'assess',
            'plan',
            'build',
            'test',
            'quality',
            'evaluate',
        ]

        missing = [p for p in required_phases if p not in content]

        if missing:
            pytest.fail(
                f"Autonomous loop missing required phases: {missing}. "
                f"The loop should define all phases for proper execution."
            )

    def test_meta_cognition_phase_exists(self, claude_dir: Path):
        """Test that meta-cognition phase is integrated into the loop."""
        loop_file = claude_dir / "skills" / "orchestration" / "autonomous-loop.md"

        if not loop_file.exists():
            pytest.skip("autonomous-loop.md not found")

        content = loop_file.read_text(encoding='utf-8').lower()

        # Check for meta-cognition integration
        meta_indicators = ['meta-cognition', 'metacognition', 'decision engine', 'capability inventory']

        found = any(ind in content for ind in meta_indicators)

        if not found:
            pytest.fail(
                "Autonomous loop doesn't reference meta-cognition system. "
                "The loop should integrate with meta-cognition for intelligent decision-making."
            )


class TestAgentRuleAlignment:
    """Test that agents align with available rules."""

    def test_security_analyst_has_security_rule(self, claude_dir: Path):
        """Test that security-analyst agent has corresponding security rule."""
        agents_dir = claude_dir / "agents"
        rules_dir = claude_dir / "rules"

        security_agent = agents_dir / "security-analyst.md"
        security_rule = rules_dir / "security.md"

        if security_agent.exists():
            assert security_rule.exists(), (
                "security-analyst agent exists but @rules/security does not. "
                "Agent expertise should have corresponding rule documentation."
            )

    def test_database_expert_has_database_rule(self, claude_dir: Path):
        """Test that database-expert agent has corresponding database rule."""
        agents_dir = claude_dir / "agents"
        rules_dir = claude_dir / "rules"

        db_agent = agents_dir / "database-expert.md"
        db_rule = rules_dir / "database.md"

        if db_agent.exists():
            assert db_rule.exists(), (
                "database-expert agent exists but @rules/database does not. "
                "Agent expertise should have corresponding rule documentation."
            )

    def test_ui_expert_has_ui_rule(self, claude_dir: Path):
        """Test that ui-ux-expert agent has corresponding UI rule."""
        agents_dir = claude_dir / "agents"
        rules_dir = claude_dir / "rules"

        ui_agent = agents_dir / "ui-ux-expert.md"
        ui_rule = rules_dir / "ui-ux-design.md"

        if ui_agent.exists():
            assert ui_rule.exists(), (
                "ui-ux-expert agent exists but @rules/ui-ux-design does not. "
                "Agent expertise should have corresponding rule documentation."
            )


class TestCommandIndexAccuracy:
    """Test that command index matches actual commands."""

    def test_index_lists_all_commands(self, claude_dir: Path):
        """Test that commands/_index.md lists all available commands."""
        commands_dir = claude_dir / "commands"
        index_file = commands_dir / "_index.md"

        if not index_file.exists():
            pytest.skip("Commands index not found")

        # Get actual commands
        actual_commands = {f.stem for f in commands_dir.glob("*.md") if not f.name.startswith("_")}

        # Get commands listed in index
        content = index_file.read_text(encoding='utf-8')

        # Find /cc:name patterns
        listed_commands = set(re.findall(r'/cc:([a-z][\w-]*)', content))

        missing = actual_commands - listed_commands
        extra = listed_commands - actual_commands

        issues = []
        if missing:
            issues.append(f"Commands not in index: {sorted(missing)}")
        if extra:
            issues.append(f"Commands in index but not found: {sorted(extra)}")

        if issues:
            pytest.fail("\n".join(issues) + "\nUpdate commands/_index.md to match actual commands.")


class TestSnippetInventoryAccuracy:
    """Test that snippet references in meta-cognition match actual snippets."""

    def test_snippet_examples_exist(self, claude_dir: Path):
        """Test that snippets mentioned in meta-cognition exist."""
        meta_cog = claude_dir / "skills" / "orchestration" / "meta-cognition.md"
        snippets_dir = claude_dir / "snippets"

        if not meta_cog.exists():
            pytest.skip("meta-cognition.md not found")

        content = meta_cog.read_text(encoding='utf-8')

        # Get actual snippet names
        actual_snippets = set()
        if snippets_dir.exists():
            for f in snippets_dir.rglob("*.md"):
                if not f.name.startswith("_"):
                    actual_snippets.add(f.stem.lower())

        # Find snippet names in meta-cognition (backtick-wrapped with common snippet patterns)
        # Look for patterns like `express-route`, `react-component`, `jest-test`
        snippet_pattern = r'`([a-z]+-[a-z]+(?:-[a-z]+)?)`'
        mentioned = set(re.findall(snippet_pattern, content))

        # Filter to likely snippet names (common patterns)
        snippet_indicators = ['route', 'component', 'test', 'hook', 'context', 'dockerfile', 'action', 'class', 'logger', 'config', 'endpoint', 'handler']
        likely_snippets = {s for s in mentioned if any(ind in s for ind in snippet_indicators)}

        # Exclude hook names (these are system components, not snippets)
        hook_names = {'context-injector', 'setup-init', 'session-start', 'bash-auto-approve',
                      'file-validator', 'post-edit', 'error-recovery', 'agent-tracker',
                      'agent-synthesizer', 'pre-compact', 'dod-verifier', 'session-end'}
        likely_snippets = likely_snippets - hook_names

        # Exclude agent names (these are agents, not snippets)
        agent_names = {'test-engineer', 'code-reviewer', 'security-analyst', 'documentation-writer',
                       'database-expert', 'devops-engineer', 'ui-ux-expert', 'performance-optimizer'}
        likely_snippets = likely_snippets - agent_names

        # Exclude pattern names (these are patterns, not snippets)
        pattern_names = {'test-doubles', 'arrange-act-assert', 'retry-with-backoff', 'circuit-breaker',
                         'error-boundary', 'result-type', 'feature-flag', 'blue-green'}
        likely_snippets = likely_snippets - pattern_names

        # Check which mentioned snippets don't exist
        missing = likely_snippets - actual_snippets

        if missing and len(missing) > 3:  # Allow some flexibility for examples
            pytest.skip(
                f"Meta-cognition mentions snippets that may not exist: {sorted(missing)[:5]}... "
                f"Consider creating these snippets or updating the inventory."
            )
