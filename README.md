[![Build Status](https://travis-ci.org/sertansenturk/ahenkidentifier.svg?branch=master)](https://travis-ci.org/sertansenturk/ahenkidentifier) [![codecov.io](https://codecov.io/github/sertansenturk/ahenkidentifier/coverage.svg?branch=master)](https://codecov.io/github/sertansenturk/ahenkidentifier?branch=master) [![Code Climate](https://codeclimate.com/github/sertansenturk/ahenkidentifier/badges/gpa.svg)](https://codeclimate.com/github/sertansenturk/ahenkidentifier) [![GitHub version](https://badge.fury.io/gh/sertansenturk%2Fahenkidentifier.svg)](https://badge.fury.io/gh/sertansenturk%2Fahenkidentifier) [![DOI](https://zenodo.org/badge/21104/sertansenturk/ahenkidentifier.svg)](https://zenodo.org/badge/latestdoi/21104/sertansenturk/ahenkidentifier) [![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-ff69b4.svg)](http://www.gnu.org/licenses/agpl-3.0)

# ahenkidentifier
Identifies the ahenk (transposition) of a makam music recording given the tonic frequency and the symbol (or the makam)

If you are using ahenkidentifier in your work, please cite:

> Şentürk, S. (2016). [Computational Analysis of Audio Recordings and Music Scores for the Description and Discovery of Ottoman-Turkish Makam Music](compmusic.upf.edu/senturk2016thesis). PhD thesis, Universitat Pompeu Fabra, Barcelona, Spain.

Usage
-------

```python
from ahenkidentifier.ahenkidentifier import AhenkIdentifier

ahenk = AhenkIdentifier.identify(tonic_freq, makam)
# or 
ahenk = AhenkIdentifier.identify(tonic_freq, tonic_symbol)
```

The inputs are:
```python
# tonic_freq 	    :	The frequency of the tonic in Hz.
# makam/tonic_symbol:	The algorithm can either accept the makam-slug or 
#					    the note symbol of the tonic in SymbTr format as a string (e.g. B4b1).
```
For the makam-slug names, check the json file in the data folder. The slugs are the same with the ones in the filenames of the scores in the [SymbTr](https://github.com/MTG/SymbTr) collection. The tonic symbols are notated as \[Note pitch-class\]\[Octave\](Accidental Symbol(Holderian Comma)), e.g. B4b1

The output is:
```python
# ahenk 		  :	The name of the ahenk as a unicode string and a dictionary of computed stats
```

Please refer to [demo.ipynb](https://github.com/sertansenturk/ahenkidentifier/blob/master/demo.ipynb) for an interactive demo.

Installation
-------

If you want to install ahenkidentifier, it is recommended to install the package and dependencies into a virtualenv. In the terminal, do the following:

    virtualenv env
    source env/bin/activate
    python setup.py install

If you want to be able to edit files and have the changes be reflected, then install the repository like this instead:

    pip install -e .

Issues
-------
The "Bolahenk Nısfiye" ahenk, which is an octave higher than the default ahenk ("Bolahenk"), is omitted. In solo performances, automatic identification of this ahenk requires the frequency range of the instrument being performed. Moreover, it is ambiguous to distinguish it from "Bolahenk" in multi-instrument recordings.

Authors
-------
Sertan Şentürk
contact@sertansenturk.com
