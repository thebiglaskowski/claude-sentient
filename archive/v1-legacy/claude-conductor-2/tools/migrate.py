#!/usr/bin/env python3
"""
Migration tool for Claude Conductor v1 to v2

Converts:
- Markdown skills to YAML skills
- Markdown commands to YAML commands
- LOOP_STATE.md to loop.state.json
- Various conventions to new schema

Usage:
    python migrate.py --from=v1              # Migrate from v1
    python migrate.py --from=v1 --dry-run    # Show what would be migrated
    python migrate.py --from=v1 --output=./  # Specify output directory
"""

import argparse
import json
import re
import uuid
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Missing pyyaml. Install with: pip install pyyaml")
    exit(1)


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter from Markdown content."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1]) or {}
            body = parts[2].strip()
            return frontmatter, body
    return {}, content


def migrate_skill(v1_path: Path) -> dict:
    """Convert v1 skill (Markdown) to v2 skill (YAML)."""
    content = v1_path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(content)

    # Build v2 structure
    v2_skill = {
        "name": frontmatter.get("name", v1_path.stem),
        "version": frontmatter.get("version", "1.0.0"),
        "description": frontmatter.get("description", "Migrated from v1")[:200],
        "triggers": frontmatter.get("triggers", []),
        "model": frontmatter.get("model", "sonnet"),
        "tags": frontmatter.get("tags", ["migrated"]),
        "content": body,
    }

    # Parse depends from content references
    depends = {}
    skill_refs = re.findall(r'`([a-z-]+)` skill', body)
    for ref in skill_refs:
        if ref != v2_skill["name"]:
            depends[ref] = ">=1.0.0"
    if depends:
        v2_skill["depends"] = depends

    # Parse events from content
    if "emit(" in body or "publishes:" in body:
        events = re.findall(r'emit\(["\']([a-z.]+)["\']', body)
        if events:
            v2_skill["publishes"] = list(set(events))

    if "subscribes:" in body or "on " in body.lower():
        events = re.findall(r'on\s+([a-z.]+)', body, re.IGNORECASE)
        if events:
            v2_skill["subscribes"] = [
                {"event": e, "handler": f"on{e.replace('.', '_').title()}"}
                for e in set(events)
            ]

    return v2_skill


def migrate_command(v1_path: Path) -> dict:
    """Convert v1 command (Markdown) to v2 command (YAML)."""
    content = v1_path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(content)

    name = frontmatter.get("name", v1_path.stem)
    if not name.startswith("cc-"):
        name = f"cc-{name}"

    v2_command = {
        "name": name.replace("cc-", ""),
        "version": frontmatter.get("version", "1.0.0"),
        "description": frontmatter.get("description", "Migrated from v1")[:200],
        "command": name,
        "category": determine_category(v1_path),
        "model": frontmatter.get("model", "sonnet"),
        "content": body,
    }

    # Parse argument hint
    if "argument-hint" in frontmatter:
        hint = frontmatter["argument-hint"]
        args = []
        # Simple parsing of "[arg1] [--flag]"
        for match in re.findall(r'\[([^\]]+)\]', hint):
            if match.startswith("--"):
                continue  # Handle as flag
            args.append({
                "name": match.replace("-", "_"),
                "type": "string",
                "required": False,
            })
        if args:
            v2_command["arguments"] = args

    return v2_command


def determine_category(path: Path) -> str:
    """Determine command category from path."""
    path_str = str(path).lower()
    if "planning" in path_str:
        return "planning"
    elif "execution" in path_str:
        return "execution"
    elif "quality" in path_str:
        return "quality"
    elif "git" in path_str:
        return "git"
    elif "doc" in path_str:
        return "docs"
    elif "operation" in path_str:
        return "operations"
    return "execution"


def migrate_loop_state(v1_path: Path) -> dict:
    """Convert LOOP_STATE.md to loop.state.json."""
    content = v1_path.read_text(encoding="utf-8")

    state = {
        "version": "2.0",
        "sessionId": str(uuid.uuid4()),
        "startedAt": datetime.now().isoformat(),
        "iteration": 0,
        "phase": "classify",
        "status": "running",
        "classification": None,
        "workQueue": [],
        "gates": {},
        "context": {
            "budgetUsed": 0,
            "level": "green",
            "compactionReady": False,
        },
        "metrics": {
            "iterationsTotal": 0,
            "gatesPassed": 0,
            "gatesFailed": 0,
            "tasksCompleted": 0,
        },
        "history": [],
        "decisions": [],
    }

    # Try to parse iteration
    iter_match = re.search(r'Current Iteration:\s*(\d+)', content)
    if iter_match:
        state["iteration"] = int(iter_match.group(1))

    # Try to parse work queue table
    queue_section = re.search(r'## Work Queue.*?\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if queue_section:
        rows = re.findall(r'\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|', queue_section.group(1))
        for i, (priority, item, status) in enumerate(rows[1:], 1):  # Skip header
            priority = priority.strip()
            if priority not in ["S0", "S1", "S2", "S3"]:
                continue
            state["workQueue"].append({
                "id": f"WQ-{i:03d}",
                "priority": priority,
                "title": item.strip(),
                "status": "done" if "✅" in status or "Done" in status else "pending",
                "blockedBy": [],
                "blocks": [],
            })

    return state


def migrate_project(v1_root: Path, v2_root: Path, dry_run: bool = False):
    """Migrate entire project from v1 to v2."""
    migrations = []

    # Find skills
    v1_skills = v1_root / "template" / ".claude" / "skills"
    if v1_skills.exists():
        for skill_path in v1_skills.glob("**/*.md"):
            if skill_path.name.startswith("_"):
                continue

            category = skill_path.parent.name
            output_path = v2_root / "skills" / category / f"{skill_path.stem}.skill.yaml"

            if not dry_run:
                v2_skill = migrate_skill(skill_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "w") as f:
                    yaml.dump(v2_skill, f, default_flow_style=False, sort_keys=False)

            migrations.append(("skill", skill_path, output_path))

    # Find commands
    v1_commands = v1_root / "template" / ".claude" / "commands"
    if v1_commands.exists():
        for cmd_path in v1_commands.glob("*.md"):
            if cmd_path.name.startswith("_"):
                continue

            output_path = v2_root / "commands" / "migrated" / f"{cmd_path.stem}.cmd.yaml"

            if not dry_run:
                v2_cmd = migrate_command(cmd_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "w") as f:
                    yaml.dump(v2_cmd, f, default_flow_style=False, sort_keys=False)

            migrations.append(("command", cmd_path, output_path))

    # Find state
    v1_state = v1_root / "LOOP_STATE.md"
    if v1_state.exists():
        output_path = v2_root / ".claude" / "state" / "loop.state.json"

        if not dry_run:
            state = migrate_loop_state(v1_state)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                json.dump(state, f, indent=2)

        migrations.append(("state", v1_state, output_path))

    return migrations


def main():
    parser = argparse.ArgumentParser(description="Migrate Claude Conductor v1 to v2")
    parser.add_argument("--from", dest="source", default="v1",
                        help="Source version (default: v1)")
    parser.add_argument("--input", "-i", default=".",
                        help="Input directory (v1 project root)")
    parser.add_argument("--output", "-o", default="./v2",
                        help="Output directory for v2 project")
    parser.add_argument("--dry-run", "-n", action="store_true",
                        help="Show what would be migrated without doing it")
    args = parser.parse_args()

    v1_root = Path(args.input).resolve()
    v2_root = Path(args.output).resolve()

    print(f"Migrating from: {v1_root}")
    print(f"Migrating to: {v2_root}")
    if args.dry_run:
        print("(DRY RUN - no files will be created)")
    print()

    migrations = migrate_project(v1_root, v2_root, args.dry_run)

    for kind, source, dest in migrations:
        action = "Would migrate" if args.dry_run else "Migrated"
        print(f"{action} [{kind}]: {source.relative_to(v1_root)} → {dest.relative_to(v2_root)}")

    print()
    print(f"Total: {len(migrations)} files")

    if not args.dry_run:
        print()
        print("Migration complete!")
        print("Run 'python tools/validate.py' to check the migration.")


if __name__ == "__main__":
    main()
