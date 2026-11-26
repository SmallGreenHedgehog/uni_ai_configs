# commits

Structure:
header: type(scope)!: description
one blank line, optional body, one blank line, optional footers
type is required and lowercase; scope is optional in parentheses; ! is optional immediately before the colon
a colon followed by a single space is required; description stays on the same line

Types:
feat - a new feature
fix - a bug fix
docs - documentation only
style - formatting or whitespace change that does not affect the meaning of the code
refactor - a change that neither fixes a bug nor adds a feature
perf - a change that improves performance
test - adding or fixing tests
build - build system or external dependency change
ci - continuous integration configuration change
chore - routine maintenance not covered by other types
revert - reverts a previous commit
feat maps to SemVer MINOR, fix maps to PATCH, breaking changes map to MAJOR

Scope:
optional noun describing the affected area
examples: api, auth, ui, config, deps, tests, docs, db, build

Description:
short and clear, imperative mood, lowercase start, no trailing period

Body:
optional, separated from the description by one blank line
explain what changed and why

Breaking Changes:
mark with ! immediately before the colon and/or a BREAKING CHANGE: <description> footer
BREAKING-CHANGE is an accepted synonym; never change the uppercase BREAKING CHANGE token

Footers:
one token per line, using - instead of spaces (BREAKING CHANGE keeps its space)
format Token: value or Token #value; value may span multiple lines

Revert:
use the revert type and reference the reverted commit in the body or a Refs: footer
