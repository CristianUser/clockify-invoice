# Clockify Invoice Generator

## Description
this is a simple clockify invoice generator.

## Installation
- `brew install wkhtmltopdf` or `apt-get install wkhtmltopdf` if linux based.
- `pip3 install -r requirements.txt`
- `cp config.yaml.example config.yaml`

## Setup
- Set the desired workspace as default in your account settings _(in the future this will be a cli option)_
- Create a clockify api key [here](https://clockify.me/user/settings)
- Add your api key to the config.yaml file or set it as an environment variable `export CLOCKIFY_API_KEY=your_api_key`
- Replace all the values in the config.yaml file with your own

## Usage
python3 -m invoicify generate --config config.yaml -d0 25-10-2023 -d1 24-11-2023
