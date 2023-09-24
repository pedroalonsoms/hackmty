# How to run

Create a virtual environment

```console
python3.10 -m venv env
```

Activate it

```console
source env/bin/activate
```

Install dependencies

```console
pip3 install -r requirements.txt
```

Save dependencies

```console
pip3 freeze > requirements.txt
```

Run the project

```console
python main.py
```

You can deactivate it when you finish

```console
deactivate
```

You may need to add this line to your `settings.json` file

```json
"python.defaultInterpreterPath": "./backend/env/bin/python"
```