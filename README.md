# Astute Info Institute – Open edX Deployment

This repo contains the Tutor-based Open edX deployment for Astute Info Institute.

## Structure

- `config.yml`: Tutor platform configuration
- `env/`: Docker environment, themes, MFE settings, patches
- `plugins/`: Custom or external Tutor plugins
- `.gitignore`: Prevents pushing unwanted data (volumes, logs)

## Commands

Initialize:
```bash
tutor local launch
```

Update platform:
```bash
tutor local upgrade
```

