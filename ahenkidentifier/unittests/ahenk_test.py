from ahenkidentifier.AhenkIdentifier import AhenkIdentifier
import numpy as np
import json
import os

_curr_folder = os.path.dirname(os.path.abspath(__file__))


def test_ahenk_with_tonic_symbol_input():
    dummy_tonic_symbol = 'A4'
    ahenk_test_wrapper(dummy_tonic_symbol)


def test_ahenk_with_makam_input():
    dummy_makam = 'huseyni'
    ahenk_test_wrapper(dummy_makam)


def ahenk_test_wrapper(dummy_str):
    # load the correct results
    ahenk_file = os.path.join(_curr_folder, 'correct_ahenks.json')
    correct_ahenks = json.load(open(ahenk_file, 'r'))

    # parameters
    start_freq = 16  # C0 note
    num_octaves = 10
    cent_step = 10.0  # cents

    # get the frequencies to get ahenk
    cc = np.arange(0, num_octaves, cent_step / AhenkIdentifier.CENTS_IN_OCTAVE)
    freqs = [int(i) for i in start_freq * np.power(2.0, cc)]

    # compute
    for freq in freqs:
        ahenk = AhenkIdentifier.identify(freq, dummy_str)
        if not ahenk['name'] == correct_ahenks[str(freq)][0]:
            print("Mismatch in " + dummy_str + ' = ' + str(freq))
            assert False

    assert True
