# branches

Model: gitflow

Types:
feature/example-name-of-feature-branch - a new feature; created from develop
fix/example-name-of-fix-branch - a bug fix; created from develop
hotfix/example-name-of-hotfix-branch - an urgent production fix; created from main

Naming:
lowercase kebab-case after the type prefix
describe the change the branch makes
examples: feature/user-login, fix/empty-cart, hotfix/payment-timeout

Pull Requests:
always open a pull request as a draft
feature and fix pull requests target develop
hotfix pull requests target main
