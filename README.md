# sonic_signatures/
Summer 2017 research into visual text analysis of sonic signatures/

Sonic signatures is an exploration of the relationship between the sound of words and the people who speak them.
It is a collection of data visualization and analysis techniques to explore the kinds of vowels an consonants that show up in a text and in what concentrations.
Sonic signatures has its origins as a technique to explore whether there are similarities in the way that certain Shakespeare characters sound - do villains use lots of phonemes that cause one to bear one’s teeth when spoken? Do rich old men use a higher concentration of “dark” sounding vowels? 
This technique will hopefully be extendable to other bodies of text as the project progresses.

## Getting Started

The foundational process of our software is using nltk to convert texts from American English to phonemes, which are then categorized and analyzed by frequency. 

With Shakespeare, the texts went from res to dest using phonetic_transcriber.py. The phonetic_transcript method(self, file_name) will do the same for another file.

### Prerequisites

NLTK - Can be installed using instructions at https://www.nltk.org/install.html

bs4 - https://www.crummy.com/software/BeautifulSoup/bs4/doc/#quick-start

<!-- 
```
Give examples
```

### Installing

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system
 -->

## Built With

* [Flask](http://flask.pocoo.org/) - The web framework used


## Authors

* **Eric Alexander** - *Supervision* - [EAlexander](https://github.com/EAlexander)

* **Estelle Bayer** - [EstelleEvelyn](https://github.com/EstelleEvelyn)
* **Liz Nichols** - [nicholsl](https://github.com/nicholsl)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under

## Acknowledgments

* Inspired by University of Utah's Poemage