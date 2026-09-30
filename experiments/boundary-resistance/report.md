# Boundary Resistance Lab

Endpoint correctness is deliberately separated from route legitimacy.

## normal
- endpoint passed: `True`
- route valid: `True`
- flags: `none`
- undeclared paths: `none`

## shortcut_dependency
- endpoint passed: `True`
- route valid: `False`
- flags: `undeclared_dependency`
- undeclared paths: `shortcut.txt`

## stale_endpoint
- endpoint passed: `True`
- route valid: `False`
- flags: `stale_answer`
- undeclared paths: `none`

## permission_denied
- endpoint passed: `True`
- route valid: `False`
- flags: `extract_failed, stale_answer, source_unreadable`
- undeclared paths: `none`
