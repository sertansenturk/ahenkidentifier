from ahenkidentifier.AhenkIdentifier import AhenkIdentifier
import numpy as np
import json
import os

_curr_folder = os.path.dirname(os.path.abspath(__file__))


def test_ahenk():
    # load the correct results
    ahenk_file = os.path.join(_curr_folder, 'correct_ahenks.json')
    correct_ahenks = json.load(open(ahenk_file, 'r'))

    # parameters
    start_freq = 16  # C0 note
    num_octaves = 10
    cent_step = 10.0  # cents
    dummy_note_symbol = 'A4'

    # get the frequencies to get ahenk
    cc = np.arange(0, num_octaves, cent_step / AhenkIdentifier.CENTS_IN_OCTAVE)
    freqs = [int(i) for i in start_freq * np.power(2.0, cc)]

    # compute
    for freq in freqs:
        ahenk = AhenkIdentifier.identify(freq, dummy_note_symbol)
        if not ahenk['name'] == correct_ahenks[str(freq)][0]:
            print("Mismatch in " + dummy_note_symbol + ' = ' + str(freq))
            assert False

    assert True
