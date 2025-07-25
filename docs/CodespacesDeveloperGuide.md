# Working in Visual Studio Codespaces

This guide walks Better Process Group developers through editing the Multi-Agent Custom Automation Engine solution accelerator using Visual Studio Codespaces and previewing changes before committing.

## Prerequisites

- Access to the BPG GitHub Enterprise repository.
- Permission to create Codespaces.
- An Azure subscription that already contains the resources listed in the deployment overview.

## Opening the repository in Codespaces

1. Navigate to your fork or the main repository in GitHub Enterprise.
2. Select **Code** > **Codespaces** and click **Create codespace**.
3. Choose the branch you want to work on (typically `features-001`).
4. Wait for the container to initialize. A browser-based VS Code window opens.

## Making changes

1. Use the built-in terminal to create a new feature branch if needed:
   ```bash
   git checkout -b my-feature
   ```
2. Edit files directly in the Codespace using VS Code.
3. Save your changes. The development container automatically builds your project so you can run the backend and frontend locally:
   ```bash
   cd src/backend && python app_kernel.py
   # In another terminal
   cd src/frontend && python frontend_server.py
   ```
4. Open <http://localhost:3000> within the Codespace browser preview to verify your modifications.

## Committing and pushing

1. Stage and commit your changes via the VS Code Source Control view or command line:
   ```bash
   git add .
   git commit -m "Describe your change"
   ```
2. Push the branch to GitHub Enterprise:
   ```bash
   git push --set-upstream origin my-feature
   ```
3. When ready, open a pull request against `features-001` or `main`.

Once pushed, GitHub Actions builds Docker images and deploys to the `dev-slot` environment at
`https://app-macae-novkmzdbkmlk-dev-slot.azurewebsites.net` so you can preview the running app.

