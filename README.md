-----

# `Seram Tokenizer`

-----

### Project Description

`Seram Tokenizer` is a Python library designed to provide tokenization functionality for languages spoken on Seram Island, specifically Geser, Gorom, and Waru. These languages are part of the Austronesian family and are considered under-resourced in the field of natural language processing (NLP). This tool helps break down Seram text into smaller linguistic units—such as words or sub-words—which is a crucial step in NLP pipelines, corpus development, and linguistic analysis.

-----

### Key Features

  * **Efficient Tokenization**: Accurately tokenizes Seram texts based on the morphological and phonological patterns of Geser, Gorom, and Waru.
  * **Paragog Normalizer**: Detects and normalizes suffix-like sound variations (e.g., `-a`, `-ra`) that do not alter meaning but affect surface forms.
  * **Suffix and Prefix Tokenizer**: Detects and tokenize suffix and Prefix (e.g., `na_`, `da_`).
  * **Lightweight**: Minimal dependencies, easy to integrate into your projects.
  * **Easy to Use**: Simple and intuitive API interface.

-----

### Installation

You can install `seram tokenizer` directly from GitHub using `pip`:

```bash
pip install git+https://github.com/Airukua/MinakSeran.git@v2.1.0
```

**Note**: It's recommended to install a tagged version (like `@v2.1.0` or the latest stable release) to ensure you get a stable build.

-----

### Usage

Here's a basic example of how to use `seram tokenizer` in your Python code:

```python
# Import the library
from seram_tokenizer import SeramTokenizer

# Text in Seram language
text = "aku nugu ngasana habiba, aku atamari wanu karay."

# Initialize the tokenizer
tokenizer = SeramTokenizer(text)

# Perform tokenization
tokens = tokenizer.tokenize()

# Print the results
print(f"Original text: {text}")
print(f"Tokens: {tokens}")
```

**Expected output (example)**:

```
Original text: aku nugu ngasana habiba, aku atamari wanu karay.
Tokens: ['aku', 'nugu', 'ngasana', 'habiba', ',', 'aku', 'atamari', 'wanu', 'karay', '.']
```

Or, if we could also utilise prefix and suffix level tokenization. However, this is a naive tokenization
and it would not provide accurate tokenization since it relies only on dictionary lookup and rule-based
tokenisation. Consequently, it might tokenize name such as `'habiba'` to `'habib' '_a'` which are not recommended.
Nevertheless, it can be usefull in some areas.

```python
# Import the library
from seram_tokenizer import SeramTokenizer

# Text in Seram language
text = "aku fas anggur a tura fudicastelara. Si dafakaleus ayaira"

# Initialize the tokenizer
tokenizer = SeramTokenizer(text, use_suffix=True, use_prefix=True)

# Perform tokenization
tokens = tokenizer.tokenize()

# Print the results
print(f"Original text: {text}")
print(f"Tokens: {tokens}")
```

**Expected output (example)**:

```
Original text: aku fas anggura tura fudicastelara. Si dafakaleus ayaira
Tokens: ['aku', 'fas', 'anggu', '_ra', 'tura', 'fudicastela', '_ra', '.', 'Si', 'da_', 'fakaleus', 'ayai', '_ra']
```

See [experiment.ipynb](experiment.ipynb) to get more example usage.

-----

### Contributing

We welcome contributions from the community\! If you find a bug, have a feature suggestion, or want to contribute code, please:

1.  Fork this repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes and commit them (`git commit -m 'Add feature X'`).
4.  Push to your branch (`git push origin feature/your-feature-name`).
5.  Open a new Pull Request.

Make sure to read `CONTRIBUTING.md` (if you plan to create one) for more details.

-----

### License

This project is licensed under the **MIT License** – see the [LICENSE.md](LICENSE.md) file for full details.

-----

### Contact

If you have any questions or would like to connect, feel free to reach out:

  * **Name**: Abdul Wahid Rukua
  * **Email**: rukuaabdulwahid@gmail.com
  * **GitHub**: [Airukua](https://github.com/Airukua)