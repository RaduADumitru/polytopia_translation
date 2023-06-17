# polytopia_translation
This script generates a translation of a JSON file's values, using the `deep-translator` library for translating each field through [DeepL](https://www.deepl.com/translator) or [Google Translate](https://translate.google.com/). Normally, only one line can be translated at a time; thus, for added efficiency, the translation works in a multithreaded manner, each thread translating an approximately equal number of lines simultaneously.

Originally, I built this script in order to translate a localization file built for the game [Polytopia](https://polytopia.io/) (check it out if you like strategy games!). I then extended the script to work on multiple threads, as an exercise in multithreading. 

**Disclaimer:** Polytopia no longer supports custom translations in recent versions, as it has always been a beta feature of the game, and now it has been cut :(

## How to use
* (if you wish to use DeepL) add a [DeepL API KEY](https://www.deepl.com/docs-api/accessing-the-api/) as an environment variable named `DEEPL_API_KEY`
* run the script and input your choice of translator and how many threads you'd like to run

The difference in execution time should be noticeable the more you increase the number of threads! However, too many threads can lead to instability.
## Prerequisites
* [deep-translator](https://pypi.org/project/deep-translator/)

