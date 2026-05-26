---
name: run-python
description: Run Python code using the miniforge_env conda environment.
---

# Run Python code with miniforge_env

When the user asks to run Python code, always use this environment:

```bash
conda run -n miniforge_env python <file.py>
```

Steps:

1. Save the Python code into a temporary `.py` file.

2. Run it with:

```bash
conda run -n miniforge_env python <file.py>
```

3. Return the stdout and stderr to the user.

4. Do not use the system Python interpreter.
