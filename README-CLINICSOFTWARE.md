# ClinicSoftware.ai Webflow mirror

This folder is the downloaded multi-page Webflow site with ClinicSoftware.ai content applied in place. The original page structure, responsive styles, animations and downloaded media remain in the mirror.

## Run locally

From this directory:

```bash
python3 serve.py
```

Open:

```text
http://127.0.0.1:8081
```

Run the existing chatbot backend separately from the repository root:

```bash
python3 backend/main.py
```

The marketing pages load the dedicated `/static/clinicsoftware-embed.js` sales assistant from `http://127.0.0.1:8000`. In production, the loader automatically uses port 8000 on the public website host.

`customize_clinicsoftware.py` records the main content conversion. `apply_brand_tweaks.py` applies the ClinicSoftware wordmark, removes inherited vendor marks, and is safe to rerun.
