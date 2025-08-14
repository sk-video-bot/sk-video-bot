
# Deploy to Render (Telegram Bot)

This project has been prepared to run on Render as a **Worker** service using a Dockerfile.

## Steps

1. Create a new **Worker** on Render.
2. Connect your Git repo or upload this zip as a new repo.
3. In **Environment Variables**, add:
   - `BOT_TOKEN` = **your Telegram bot token**
4. Deploy. The service will run your bot continuously.

### Local development

- Create a `.env` file with:
  ```
  BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
  ```
- For Python: run `pip install -r requirements.txt` then `python bot.py` (or the correct entry file).
- For Node: run `npm install` then `npm start`.

> Note: The codebase was automatically scanned to replace any hardcoded token usage with an environment variable reference (`BOT_TOKEN`). If your entry file has a different name, update the Dockerfile `CMD` accordingly.
