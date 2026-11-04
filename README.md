# Subs

A personal, single-user web app I built to track my subscriptions and recurring expenses.

Subs provides a simple dashboard for tracking active and cancelled subscriptions, monitoring monthly and yearly spending, visualizing expenses by category, and keeping track of upcoming payments through an iCalendar feed.

## Development

### Requirements

- Python 3.14+ and uv
- Node.js and npm
- PostgreSQL

### Setup

Clone the repository and install the dependencies:

```bash
git clone https://github.com/Juraj326/subs.git
cd subs

uv sync
npm install
```

Create your local environment file:

```bash
cp .env.example .env
```

Configure the values in `.env`, including your PostgreSQL connection URL, secret key, passphrase hash, and calendar feed token.

Run the database migrations:

```bash
uv run flask --app app db upgrade
```

Start the frontend development server:

```bash
npm run dev
```

Then start Flask in another terminal:

```bash
uv run flask run --debug
```

## Production login rate limiting

Vercel Firewall enforces login rate limits before requests reach Flask. Configure and publish the rule separately in the Vercel dashboard; this repository does not provision it:

- Match Request Path equal to `/login` **and** Method equal to `POST`.
- Use a fixed window of 5 requests per 60 seconds, counted by IP address.
- Return `429 Too Many Requests` when the limit is exceeded.
- Apply the rule to all publicly accessible deployment environments and hostnames.

This rule replaces the application's previous 5-per-minute and 20-per-hour limits; it does not preserve the hourly cap. Vercel counts requests per region.

Local Flask and the Flask test client do not enforce login rate limits. Other hosting must provide equivalent protection. PostgreSQL is still required, but Redis is no longer used.

When migrating an existing deployment, verify the firewall rule in Vercel's traffic logs before deploying this code. Keep the existing Redis service and `RATELIMIT_STORAGE_URI` available until the new production deployment is verified, then remove them. Verify normal login and an excess login request blocked by the firewall; a `429` from the old Flask limiter alone does not verify the firewall.

## Tests

Run the test suite with:

```bash
uv run pytest
```

Run the linter with:

```bash
uv run ruff check .
```
