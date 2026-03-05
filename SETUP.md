# SAgentai Development Setup Guide

## Overview

SAgentai is built by extending the VS Code codebase with AI agent-specific features. This guide will help you set up the development environment.

## Step 1: Clone & Setup

Since SAgentai extends VS Code, you have two options:

### Option A: Fork VS Code Repository (Recommended)
```bash
# Fork microsoft/vscode on GitHub, then:
git clone https://github.com/YOUR_USERNAME/vscode.git
cd vscode
git remote add upstream https://github.com/microsoft/vscode.git
```

### Option B: Create New Repository from VS Code
```bash
# Download VS Code source, create new repo with SAgentai branding
```

## Step 2: Customize Branding

### package.json
```json
{
  "name": "sagentai",
  "version": "0.1.0",
  "displayName": "SAgentai",
  "description": "AI-Agent Focused IDE"
}
```

### Update Product Name
- `product.json` - Update `nameLong`, `nameShort`, `applicationName`
- `src/` files - Search and replace VS Code branded strings

### Resources
- Update icons in `resources/` folders
- Create SAgentai logo and splash screen

## Step 3: Create Agent Module

```bash
mkdir -p src/vs/workbench/contrib/agent
```

Create the following structure:
- `src/vs/workbench/contrib/agent/` - Agent features
- `src/vs/workbench/contrib/chat/` - Chat integration (extend existing)
- `extensions/agent-tools/` - Agent-specific extensions

## Step 4: Build & Test

```bash
# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Watch mode (recommended for development)
npm run watch

# Run the application
./scripts/code.bat  # Windows
./scripts/code.sh   # macOS/Linux
```

## Step 5: Key Files to Modify

### 1. Main Application Entry
- `src/vs/code/electron-main/main.ts` - Electron main process

### 2. Workbench Configuration
- `src/vs/workbench/workbench.web.main.ts` - Web workbench
- `src/vs/workbench/browser/layout.ts` - UI layout

### 3. Services
- Create `src/vs/workbench/services/agent/` for agent services
- Hook into dependency injection system

### 4. UI Components
- Extend `src/vs/workbench/browser/parts/` for custom panels
- Add sidebar entries in `src/vs/workbench/contrib/`

### 5. Extensions
- Add agent-specific extensions in `extensions/`
- Examples:
  - `extensions/agent-builder/` - Visual agent builder
  - `extensions/agent-monitor/` - Real-time monitoring
  - `extensions/model-manager/` - LLM model management

## Step 6: Architecture Decisions

### Key Areas to Customize

1. **Agent Framework Integration**
   - Location: `src/vs/workbench/contrib/agent/`
   - Support for: Python agents, JS agents, multi-agent systems
   - Integration points: Command palette, sidebar, chat

2. **Chat System**
   - Extend existing chat in `src/vs/workbench/contrib/chat/`
   - Add agent context awareness
   - Enable code-aware conversations

3. **Workflow Visualization**
   - New feature: Visual workflow designer for agents
   - Location: `src/vs/workbench/contrib/workflows/`
   - Use canvas/SVG for rendering

4. **Model Management**
   - Support local and remote LLMs
   - Integration with Azure OpenAI, Ollama, etc.
   - Settings UI in preferences

5. **Agent Debugging**
   - Extend debugging infrastructure
   - Show agent execution traces
   - Real-time metric monitoring

## Useful VS Code Documentation

- [Extension Development](https://code.visualstudio.com/api)
- [Workbench Architecture](https://github.com/microsoft/vscode/wiki/TypeScript-Guidelines)
- [Dependency Injection](https://github.com/microsoft/vscode/wiki/ServiceLocator)

## Next Steps

1. ✅ Complete this setup
2. ⬜ Customize branding (logos, colors, names)
3. ⬜ Create agent service infrastructure
4. ⬜ Build chat integration
5. ⬜ Develop agent builder UI
6. ⬜ Add model management features
7. ⬜ Create sample agents
8. ⬜ Release MVP

## Commands Reference

```bash
# Development
npm run watch           # Watch mode (recommended)
npm run compile         # One-time compile
npm run watch-changes   # Compile on changes

# Testing
npm run test            # Run tests
npm run test-smoke      # Run smoke tests

# Code Quality
npm run eslint          # Lint check
npm run valid-layers    # Check layer violations

# Building
npm run build           # Create distribution
npm run build:linux     # Linux build
npm run build:win32     # Windows build
npm run build:darwin    # macOS build
```

## Troubleshooting

### Build Issues
- Clear `node_modules/` and reinstall: `npm install --force`
- Clear compilation cache: `rm -rf out/`
- Rebuild natives: `npm rebuild`

### Missing Extensions
- Run `npm install` in root
- Check `extensions/` folder exists
- Verify `.gitmodules` for submodules

### Performance Issues
- Run in watch mode for faster iteration
- Use VSCode's built-in profiler
- Check `build/` folder for build optimizations

---

**Happy coding! 🚀**
