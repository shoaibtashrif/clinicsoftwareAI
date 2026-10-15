# ClinicSoftware.ai website

Restored website baseline: original multi-page layout with the official logo and full-width white header, before the October 15 redesign.

## Run locally

Requires Python 3:

```sh
python3 serve.py
```

Open http://127.0.0.1:8081/ . `serve.py` serves `www.lassomd.com` at the root and resolves the mirrored asset folders.

## Production

Production service: `clinicsoftware-site.service`, port 5501. The root URL serves the same website as any cache-refresh query URL. The chatbot is loaded from the separate backend on port 8000; its implementation, credentials, and data are not included here.

## Restore this version

The `logo-approved-baseline` tag identifies the approved restored version. To inspect or run it without changing ongoing work:

```sh
git worktree add ../clinicsoftware-restored logo-approved-baseline
cd ../clinicsoftware-restored
python3 serve.py
```

Deploy the checked-out website and `serve.py` to the service directory, then restart the service. Never deploy `.git` or local credentials.

## Assets

This snapshot includes existing third-party mirrored assets. They retain their respective ownership and licensing; this repository does not grant a license to them.
