# Run formatter
format:
    uv run ruff check --select I --fix
    uv run ruff check . --fix

# Run formatter - no fix
format-check:
    uv run ruff check --select I 
    uv run ruff check .

test:
    uv run pytest 

typecheck:
    uvx ty check