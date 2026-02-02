/**
 * Profile detection and loading for Claude Sentient SDK.
 */

import * as fs from "fs";
import * as path from "path";
import type { Profile, GateConfig } from "./types.js";

/** Default profile definitions */
const DEFAULT_PROFILES: Record<string, Partial<Profile>> = {
  python: {
    detectFiles: ["pyproject.toml", "setup.py", "requirements.txt"],
    detectExtensions: [".py"],
    gates: {
      lint: { command: "ruff check .", blocking: true, timeout: 300 },
      test: { command: "pytest", blocking: true, timeout: 300 },
      type: { command: "pyright", blocking: false, timeout: 300 },
    },
  },
  typescript: {
    detectFiles: ["tsconfig.json", "package.json"],
    detectExtensions: [".ts", ".tsx"],
    gates: {
      lint: { command: "npm run lint", blocking: true, timeout: 300 },
      test: { command: "npm test", blocking: true, timeout: 300 },
      type: { command: "npx tsc --noEmit", blocking: true, timeout: 300 },
    },
  },
  go: {
    detectFiles: ["go.mod"],
    detectExtensions: [".go"],
    gates: {
      lint: { command: "golangci-lint run", blocking: true, timeout: 300 },
      test: { command: "go test ./...", blocking: true, timeout: 300 },
    },
  },
  rust: {
    detectFiles: ["Cargo.toml"],
    detectExtensions: [".rs"],
    gates: {
      lint: { command: "cargo clippy", blocking: true, timeout: 300 },
      test: { command: "cargo test", blocking: true, timeout: 300 },
    },
  },
  general: {
    detectFiles: [],
    detectExtensions: [],
    gates: {},
  },
};

export class ProfileLoader {
  private profilesDir?: string;
  private profilesCache: Map<string, Profile> = new Map();

  constructor(profilesDir?: string) {
    this.profilesDir = profilesDir;
  }

  /** Auto-detect project profile from files in cwd */
  detect(cwd: string): string {
    const profilePriority = [
      "python",
      "typescript",
      "go",
      "rust",
      "java",
      "ruby",
      "shell",
    ];

    for (const profileName of profilePriority) {
      const profile = this.load(profileName);
      if (!profile) continue;

      // Check detection files
      for (const detectFile of profile.detectFiles) {
        if (fs.existsSync(path.join(cwd, detectFile))) {
          return profileName;
        }
      }

      // Check for files with detection extensions
      for (const ext of profile.detectExtensions) {
        try {
          const files = fs.readdirSync(cwd);
          if (files.some((f) => f.endsWith(ext))) {
            return profileName;
          }
        } catch {
          continue;
        }
      }
    }

    return "general";
  }

  /** Load a profile by name */
  load(profileName: string): Profile | null {
    if (this.profilesCache.has(profileName)) {
      return this.profilesCache.get(profileName)!;
    }

    let profileData: Partial<Profile> | undefined;

    // Try to load from YAML file (simplified - would need yaml parser)
    if (this.profilesDir) {
      const yamlFile = path.join(this.profilesDir, `${profileName}.yaml`);
      if (fs.existsSync(yamlFile)) {
        // Note: In production, use a proper YAML parser
        // For now, fall back to defaults
      }
    }

    // Fall back to defaults
    if (!profileData) {
      profileData = DEFAULT_PROFILES[profileName];
    }

    if (!profileData) {
      return null;
    }

    const profile: Profile = {
      name: profileName,
      detectFiles: profileData.detectFiles ?? [],
      detectExtensions: profileData.detectExtensions ?? [],
      gates: profileData.gates ?? {},
      conventions: profileData.conventions ?? {},
      tools: profileData.tools ?? [],
    };

    this.profilesCache.set(profileName, profile);
    return profile;
  }

  /** Get the command for a specific gate */
  getGateCommand(profileName: string, gateName: string): string | null {
    const profile = this.load(profileName);
    if (profile && gateName in profile.gates) {
      return profile.gates[gateName].command;
    }
    return null;
  }

  /** Check if a gate is blocking */
  isGateBlocking(profileName: string, gateName: string): boolean {
    const profile = this.load(profileName);
    if (profile && gateName in profile.gates) {
      return profile.gates[gateName].blocking;
    }
    return true; // Default to blocking
  }
}

export type { Profile, GateConfig };
