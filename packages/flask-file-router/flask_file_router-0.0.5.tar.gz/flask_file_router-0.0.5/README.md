# DISCLAIMER

> This Library currently supports only static routing. The dynamic routing will be added in the future release

# Usage

## Basic Usage

- Create a folder with a name `home` in the root dir of your project. You can rename `home` folder to custom name in `router.config.json` which should be created in the root dir.
- The folder `home` is gonna be workspace directory of your all api routes.
- e.g. for path `home/api.py` the route will `http://localhost:<PORT>/api`
- create and open `app.py` in the root dir of your project.

### app.py

```python
    # app.py
    from flask import Flask
    from flask.cors import CORS
    from flask_file_router.router import Router

    app = Flask(__name__)
    CORS(app)
    app.config['CORS_HEADERS'] = "Content-Type"

    Router(app).run()

    if __name__=="main":
        app.run(host="0.0.0.0", port=4000, debug=True)
```

### home/api.py

```python
   # home/api.py
   from flask import request

   methods = ["POST"]  # put GET for GET request

   def main():  # This function have to be named as main. This gets triggered Whenever it hits api
        body = request['json']
        return ""
```

# Configurations

```json
{
  "root_dir": "./home", // name of the workspace home dir
  "default_index": "__main__.py", // This is the default index route for the given folder
  "ext_exclude_list": ["pyc"], // file with this extension will be ignored
  "ext_include_list": ["py"] //file with this extension will be considered for api router and rest are ignored
}
```

> **Note**: `ext_exclude_list` and `ext_include_list` are exclusive porps. e.g. if `ext_include_list` provided `ext_exclude_list` will be ignored.

## File Structure examples

Consider the following file system structure

- `home/v1/api.py`
- `home/v1/__main__.py`
- `home/v1/get_user.py`

The api router for the above file structure will be as follows

- `https://localhost:4000/v1/api`
- `https://localhost:4000/v1`
- `https://localhost:4000/v1/get_user`
