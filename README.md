# SAgentai - AI Agent IDE

[![GitHub](https://img.shields.io/github/license/Sandeep-AdaptIQ/SAgentai)](https://github.com/Sandeep-AdaptIQ/SAgentai/blob/sagentai-dev/LICENSE.txt)
[![GitHub issues](https://img.shields.io/github/issues/Sandeep-AdaptIQ/SAgentai)](https://github.com/Sandeep-AdaptIQ/SAgentai/issues)

## About

**SAgentai** is an AI-powered Agent IDE built on top of the VS Code open-source codebase. It provides a streamlined development environment tailored for AI agent workflows, Salesforce development, and modern web development — with a curated set of built-in extensions and the custom **SAgentai Dark** theme.

## Features

- **AI Agent Workflows** — Built-in support for prompt authoring, Mermaid chat features, and AI-assisted development
- **Salesforce Development** — Bundled Salesforce DX Extension Pack with support for Apex, Lightning Web Components, SOQL, Visualforce, and more
- **Modern Web Stack** — First-class support for JavaScript, TypeScript, HTML, CSS, JSON, Markdown, and Python
- **Curated Extensions** — Lean set of ~35 built-in extensions focused on productivity, removing unnecessary language packs
- **Custom Theming** — SAgentai Dark theme plus GitHub themes and VS Code defaults
- **Full VS Code Compatibility** — Install any extension from the VS Code Marketplace

## Built-in Extensions

SAgentai ships with a focused set of built-in extensions:

| Category | Extensions |
|---|---|
| **Core** | Configuration Editing, Debug Auto Launch, Debug Server Ready, Diff, Emmet, Extension Editing, Merge Conflict, References View, Search Result, Simple Browser, Terminal Suggest, Tunnel Forwarding |
| **Git & Auth** | Git, Git Base, GitHub, GitHub Authentication, Microsoft Authentication |
| **Web / JS / TS** | CSS, CSS Language Features, HTML, HTML Language Features, JavaScript, JSON, JSON Language Features, TypeScript Basics, TypeScript Language Features, npm, Gulp |
| **Python** | Python |
| **Salesforce** | Salesforce DX Extension Pack (Expanded) — recommends 20 Salesforce extensions |
| **Formats** | Docker, Dotenv, Log, Markdown Basics, Markdown Language Features, Markdown Math, Media Preview, XML, YAML, SQL |
| **AI / Chat** | Mermaid Chat Features, Prompt Basics |
| **Shell** | PowerShell, ShellScript |
| **Notebooks** | IPython Notebooks, Notebook Renderers |
| **Themes** | SAgentai Dark, Dark+, Light+, Dark Modern, Light Modern, High Contrast, GitHub Themes, Seti Icon Theme |

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org) (v18 or later)
- [Git](https://git-scm.com)
- [Python](https://www.python.org) (for native modules)
- C/C++ build tools (Visual Studio Build Tools on Windows)

### Build from Source

```bash
# Clone the repository
git clone https://github.com/Sandeep-AdaptIQ/SAgentai.git
cd SAgentai

# Install dependencies
npm install

# Launch SAgentai
# Windows
.\scripts\code.bat

# macOS / Linux
./scripts/code.sh
```

### Development

```bash
# Build the project
npm run watch

# Run tests
.\scripts\test.bat
```

## Contributing

Contributions are welcome! Please feel free to:

* [Submit bugs and feature requests](https://github.com/Sandeep-AdaptIQ/SAgentai/issues)
* [Review source code changes](https://github.com/Sandeep-AdaptIQ/SAgentai/pulls)
* Fork the repository and submit pull requests

## Feedback

* [File an issue](https://github.com/Sandeep-AdaptIQ/SAgentai/issues)
* [Start a discussion](https://github.com/Sandeep-AdaptIQ/SAgentai/discussions)

## License

Copyright (c) Sandeep-AdaptIQ. All rights reserved.

Licensed under the [MIT](LICENSE.txt) license.

---

*SAgentai is built on the [VS Code](https://github.com/microsoft/vscode) open-source project by Microsoft.*
