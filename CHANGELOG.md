# Changelog

All notable changes to the Langchain-Agents project will be documented in this file.

## [v0.1.5] - 2024-03-XX

### Fixed

- Resolved circular import issues between agent_b.py and graph_builder.py
- Fixed StateGraph edge conditions by replacing 'condition' with 'when' parameter
- Corrected subgraph implementation with proper START and END nodes

### Changed

- Refactored workflow management into dedicated WorkflowManager class
- Simplified main execution flow in run.py
- Updated error handling to be more informative

### Added

- New core/commands.py for base command functionality
- Enhanced error reporting in workflow execution

## [v0.1.4] - 2024-03-XX

### New Features

- Implemented human review integration with approval workflow
- Added streaming output functionality
- Created error handling integration
- Introduced configuration management system

### Modifications

- Enhanced state management with TypedDict implementation
- Improved logging system with structured messages
- Updated agent processing logic for better data flow

## [v0.1.3] - 2024-03-XX

### Features

- Created core graph building functionality
- Implemented subgraph processing capabilities
- Added state management system
- Introduced agent A and B implementations

### Changes

- Restructured project layout for better organization
- Enhanced dependency management
- Improved type hints and documentation

## [v0.1.2] - 2024-03-XX

### Features (v0.1.2)

- Setup.py for package management
- Requirements.txt with version-pinned dependencies
- Installation script (install.sh)
- Environment configuration template

### Changed (v0.1.2)

- Updated project structure
- Enhanced package dependencies
- Improved installation process

## [v0.1.1] - 2024-03-XX

### Added (v0.1.1)

- Initial project structure
- Basic agent framework
- Core dependencies
- README documentation
- Basic workflow implementation

### Changed (v0.1.1)

- Organized directory structure
- Implemented basic state management
- Added type hints
- Created documentation structure

## Types of Changes

- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` in case of vulnerabilities

## Commit Convention

- feat: (new feature)
- fix: (bug fix)
- docs: (changes to documentation)
- style: (formatting, missing semi colons, etc)
- refactor: (refactoring code)
- test: (adding tests, refactoring tests)
- chore: (updating grunt tasks etc)
