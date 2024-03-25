# English to Azerbaijani(Arabic Script) Translator (Arabic Script)

This package provides an easy-to-use interface for translating text from English to Azerbaijani using Arabic script. Built with [PyTorch](https://pytorch.org/), it leverages advanced neural network models for accurate and fast translations.

## Features

- High-quality translation from English to Azerbaijani (Arabic Script).
- Simple and intuitive API.
- Lightweight and fast.

## Installation

Install the package using pip:

    pip install chevir_kartalol

Requirements
List your package requirements, but typically:

    Python >= 3.9
    Torch >= 2.0.0
    torchtext==0.6.0
    spacy
### To use the translator, follow these steps:

    import Dilmanc

    # Initialize the translator (make sure to adjust parameters as needed)
    translator = Dilmanc()

    # Translate text
    translated_text = translator.chevir("Your English text here")
    print(translated_text)



### License


This project is licensed under the Apache-2.0 License - see the LICENSE file for details.

### Support
For support and queries, raise an issue in the GitHub repository or contact the maintainers directly.