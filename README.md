# Smart Calculator
Safe Python calculator with an arithmetic parser, history, memory, and tests.
## Run
```bash
python -m unittest discover -s tests -v
python -m src.cli "(12 + 8) / 4"
```
The parser uses Python's AST module and explicitly allows only arithmetic nodes; it never calls eval.
