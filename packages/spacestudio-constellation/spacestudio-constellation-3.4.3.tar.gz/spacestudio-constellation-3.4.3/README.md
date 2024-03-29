# space**studio**™ Scripting API Documentation

## Table of contents

### 1. [Installation](#installation)

### 2. [Connection](#connection)

- [Environment variables](#environment-variables)

---

## Installation

1. You will need to have both Python and pip installed on your computer.
2. Install the space**studio™** constellation client with the following command:

```bash
pip install spacestudio-constellation
```

This will install the `spacestudio` package, the `requests` library, used to perform HTTP calls, and the `jwt` library, used to decode JWTs.

3. In your Python script, import the library by adding this line at the very top of your file:

```python
import spacestudio
```

4. The library has now been imported, you can start using it.

---

## Connection

In order to use the library, you need to be connected. You can do so by calling the `connect()` function:

```python
spacestudio.connect(url, mail, password, client_id)
```

You need to replace the parameter `url` with the URL you have been given in order to use the scripting API, `mail` with the email address you use to connect to spacestudio™, `password` with your password and `client_id` by the client identifier that was provided to you by Exotrail.

From this point on, you will be connected to the API.

### Environment variables

Alternatively to writing your `url`, `mail`, `password` and `client_id` each time you create a new script, these informations can also be saved in an external file, so that the API script needs only to read it. This can be particularly useful for sharing scripts between different users, where each user could keep the sensitive information file private and share only the script.

This can be done by using a `.env` file, as the one provided as example. This file contains a default `url` and placeholders for the user's `mail`, `password`, and `client_id` in the form of the variables `LOG_BASE_URL`, `LOG_MAIL`, `LOG_PASSWORD` and `CLIENT_ID`, respectively. To use this file in your script, you must add the following lines to the start of your script:

```python
  from dotenv import load_dotenv
  load_dotenv()
```

and the connection can be done by:

```python
  base_url = spacestudio.log_base_url
  mail = spacestudio.log_mail
  password = spacestudio.log_password
  client_id = spacestudio.log_client_id
  spacestudio.connect(base_url, mail, password, client_id)
```
