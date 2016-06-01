from ahenkidentifier.ahenkidentifier import AhenkIdentifier
import numpy as np
import json
import os

_curr_folder = os.path.dirname(os.path.abspath(__file__))


def test_ahenk_with_tonic_symbol_input():
    dummy_tonic_symbol = 'A4'
    assert t_wrapper(dummy_tonic_symbol)


def test_ahenk_with_makam_input():
    dummy_makam = 'huseyni'
    assert t_wrapper(dummy_makam)


def test_ahenk_with_makam_with_unknown_tonic_input():
    dummy_makam = 'dusems'
    wrong_str_err = "The tonic of this makam is not known."
    correct_err_msg = t_error_wrapper(dummy_makam, KeyError, wrong_str_err)

    assert correct_err_msg


def test_ahenk_with_random_str():
    dummy_tonic_symbol = 'eheh'
    wrong_str_err = "The second input has to be a tonic symbol or a " \
                    "makam slug!"
    correct_err_msg = t_error_wrapper(dummy_tonic_symbol, ValueError,
                                      wrong_str_err)

    assert correct_err_msg


def t_error_wrapper(wrong_str, err_type, wrong_str_err):
    correct_err_msg = False
    try:
        t_wrapper(wrong_str)
    except err_type as e:
        # str(e) returns the error message with trailing '', that's why we
        # check the validitiy with "in"
        correct_err_msg = wrong_str_err in str(e)

    return correct_err_msg


def t_wrapper(dummy_str):
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
    success = True
    for freq in freqs:
        ahenk = AhenkIdentifier.identify(freq, dummy_str)
        if not ahenk['name'] == correct_ahenks[str(freq)][0]:
            print("Mismatch in " + dummy_str + ' = ' + str(freq))
            success = False

    return success
