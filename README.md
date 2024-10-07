# Cydar Card Deck Display (CCDD)
## A scalable system status display

The cydar card deck display (ccdd) is designed to take many sources of data and show them in a scalable way, by using fixed size and aspect ratio cards which are laid out, scaled, shuffled and organised by the CardMatrix component.

## Technology choices
The CCDD is a svelte app. Vite is used as a build tool and Vitest is used for testing.

## Setting up dev environment
1. Clone the repository && cd into cydar-card-deck folder
2. Install libraries
3. Run `npm run dev` to run the svelte dev server
4. Open a new terminal window
5. Navigate to the etc directory
6. Create a virtual env with `python3 -m venv env`, activate `source env/bin/activate` and install requirements `pip install -r requirements.txt` 
7. Run the test data generator with `flask run`
8. Open a web browser and go to `http://localhost:5173/?url=http://localhost:5000&token=banana`

## Usage
Data is gathered from URLs provided in the query string `?url=` (as many as required). The auth token for vault endpoints is also set in the query string `&token=`. For dev **banana** is the default token.

Building a URL this way manually is annoying so there's a pythons script in /etc `url_builder.py` which is used like so... 
`python3 url_builder.py http://card-deck-location --urls http://data1 http://data2 --token actualtoken`

The CCDD can render any data sent to it as long as it has a globally unique identifier, a status (defined in interfaces.ts) and a type, so that we know which card to render.

## Testing
More work is required for full test coverage.

There are example tests for the `TransferCard.svele` component which can be run with `npm run test`.
