# Campus Tutor
Our Tutoring Service App for MSU Students

## Installation

After cloning this repo, install the requirements

```bash
pip install -r requirements.txt
```

## Usage

To start the server run

```bash
python3 server.py
```

## Known Issues
- [COMMON] When creating an account or basically making any changes to the database, you will not be able to view those changes without restarting the server
- [RARE] there are instances you might get an error parsing the email from the session. to solve just go to ```http://localhost:3000/logout``` and the session will be reset and everything will function properly

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.