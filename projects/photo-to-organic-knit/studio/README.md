# Publication Studio

Local operator interface for the installed `photo-to-conceptual-art` publication templates.

Run from `projects/photo-to-organic-knit/`:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -B studio/server.py
```

Open `http://127.0.0.1:8877/`.

The server binds only to `127.0.0.1`, accepts only the four maintained template IDs, uses fixed project Key Art paths, limits request bodies, and stores rendered files under an operating-system temporary directory. Stop it with `Ctrl+C`; the temporary directory is deleted during shutdown.

The studio is a sample publication workspace. It does not verify facts, consent, brand approval, licenses, legal copy or publication authority.
