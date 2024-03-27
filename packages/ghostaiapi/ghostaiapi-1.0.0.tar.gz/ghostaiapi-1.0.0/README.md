# GhostAI

[![PyPI version](https://badge.fury.io/py/ghostaiapi.svg)](https://badge.fury.io/py/ghostaiapi)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python library for interacting with the GhostAI API.

## Installation

You can install `ghostaiapi` via pip:

```
pip install ghostaiapi
```

## Usage

```python
import ghostai

# Example usage for ghostai
chat("api_key", "model", "prompt") # Model is either chat or img

# Api key can be found by emailing
# cyberzendev@gmail.com


# Example usage for generating a chat
response = chat("api_key", "chat", "prompt")

print(response)

# Example usage for generating an image

import ghostai

# Define your API key and model
api_key = "YOUR_API_KEY"
model = "YOUR_MODEL"

# Send a message and receive the response with an image
message = "Your prompt here"
decoded_image = ghostai.chat_with_image(api_key, model, message)

# Display the decoded image
if decoded_image:
    decoded_image.show()
else:
    print("Failed to receive or decode the image.")

```

## API Key

You need to obtain an API key from GhostAI to use this library. Visit [GhostAI](https://ghostai.me) for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
