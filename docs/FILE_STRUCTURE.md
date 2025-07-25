# Repository File Structure

This document provides an overview of the top-level directories and files in the repository and their purposes.

| Path | Description |
|------|-------------|
| `.azdo/` | Azure DevOps pipeline configurations. |
| `.devcontainer/` | Configuration for the development container environment. |
| `.flake8` | Configuration file for the flake8 linter. |
| `.github/` | GitHub-specific files, templates and workflows. |
| `CODE_OF_CONDUCT.md` | Project code of conduct. |
| `CONTRIBUTING.md` | Guidelines for contributing to this project. |
| `LICENSE` | Project license information. |
| `README.md` | Main project documentation and overview. |
| `SECURITY.md` | Security reporting guidelines. |
| `SUPPORT.md` | Information on how to get support for the project. |
| `TRANSPARENCY_FAQS.md` | FAQ on transparency policies. |
| `azure.yaml` | Azure deployment configuration for the accelerator. |
| `docs/` | Additional documentation for setup, deployment and customization. |
| `infra/` | Infrastructure as code files (Bicep templates and scripts). |
| `src/` | Source code for the backend and frontend applications. |
| `tests/` | End-to-end tests and supporting test resources. |
| `next-steps.md` | Suggested next actions after deployment. |

Below is a high level tree of the repository (depth 2):

```text
.
├── .azdo
│   └── pipelines
├── .devcontainer
│   ├── devcontainer.json
│   └── setupEnv.sh
├── .flake8
├── .git
│   ├── FETCH_HEAD
│   ├── HEAD
│   ├── branches
│   ├── config
│   ├── description
│   ├── hooks
│   ├── index
│   ├── info
│   ├── logs
│   ├── objects
│   ├── packed-refs
│   └── refs
├── .github
│   ├── CODEOWNERS
│   ├── CODE_OF_CONDUCT.md
│   ├── ISSUE_TEMPLATE
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── dependabot.yml
│   └── workflows
├── .gitignore
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── Multi-Agent-Custom-Automation-Engine-Solution-Accelerator.code-workspace
├── README.md
├── SECURITY.md
├── SUPPORT.md
├── TRANSPARENCY_FAQS.md
├── __azurite_db_queue__.json
├── __azurite_db_queue_extent__.json
├── azure.yaml
├── docs
│   ├── AzureAccountSetUp.md
│   ├── AzureGPTQuotaSettings.md
│   ├── CodespacesDeveloperGuide.md
│   ├── CustomizeSolution.md
│   ├── CustomizingAzdParameters.md
│   ├── DeleteResourceGroup.md
│   ├── DeploymentGuide.md
│   ├── FILE_STRUCTURE.md
│   ├── LocalDeployment.md
│   ├── ManualAzureDeployment.md
│   ├── NON_DEVCONTAINER_SETUP.md
│   ├── SampleQuestions.md
│   ├── TRANSPARENCY_FAQ.md
│   ├── azure_app_service_auth_setup.md
│   ├── create_new_app_registration.md
│   ├── images
│   ├── quota_check.md
│   └── re-use-log-analytics.md
├── infra
│   ├── abbreviations.json
│   ├── bicepconfig.json
│   ├── main.bicep
│   ├── main.parameters.json
│   ├── modules
│   ├── old
│   └── scripts
├── next-steps.md
├── pytest.ini
├── src
│   ├── .dockerignore
│   ├── __init__.py
│   ├── backend
│   └── frontend
└── tests
    └── e2e-test

25 directories, 50 files
```
