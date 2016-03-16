import os
import json
import numpy as np
from future.utils import iteritems


class AhenkIdentifier2(object):
    CENTS_IN_OCTAVE = 1200  # cents

    def __init__(self):
        pass

    @classmethod
    def identify(cls, tonic_freq, symbol_in):
        tonic_dict = cls._get_tonic_dict()
        ahenks = cls._get_ahenk_dict()

        # get the tonic symbol and frequency
        tonic_bolahenk_freq = None
        if symbol_in in tonic_dict.keys():  # tonic symbol given
            # tonic_symbol = symbol_in
            tonic_bolahenk_freq = tonic_dict[symbol_in]['bolahenk_freq']
        else:  # check if the makam name is given
            for sym, val in iteritems(tonic_dict):
                if symbol_in in val['makams']:
                    # tonic_symbol = sym
                    tonic_bolahenk_freq = val['bolahenk_freq']
                    break
            if not tonic_bolahenk_freq:
                raise ValueError("The second input has to be the tonic " +
                                 "symbol or the makam slug!")

        # get the transposition in cents, rounded to the closest semitone
        cent_dist = cls._hz_to_cent(tonic_freq, tonic_bolahenk_freq)
        mod_cent_dist = np.mod(cent_dist, cls.CENTS_IN_OCTAVE)

        # if the distance is more than 1150 cents wrap it to minus
        # so it will be mapped to 0 cents
        mod_cent_dist = (mod_cent_dist if mod_cent_dist < 1150
                         else mod_cent_dist - 1200)

        mod_cent_approx = int(np.round(mod_cent_dist * 0.01) * 100)
        mod_cent_dev = abs(mod_cent_approx - mod_cent_dist)

        # create the stats dictionary
        distance_to_bolahenk = {
            'performed': {'value': mod_cent_dist.tolist()[0], 'unit': 'cent'},
            'theoretical': {'value': mod_cent_approx, 'unit': 'cent'}}
        dist_dict = {'distance_to_bolahenk': distance_to_bolahenk,
                     'deviation': {'value': mod_cent_dev.tolist()[0],
                                   'unit': 'cent'}}

        # get the ahenk
        for ahenk_slug, val in iteritems(ahenks):
            if val['cent_transposition'] == mod_cent_approx:
                return val['name'], dist_dict

    @staticmethod
    def _get_tonic_dict():
        tonic_dict_file = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'data', 'tonic.json')
        return json.load(open(tonic_dict_file, 'r'))

    @staticmethod
    def _get_ahenk_dict():
        ahenk_dict_file = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'data', 'ahenk.json')
        return json.load(open(ahenk_dict_file, 'r'))

    @staticmethod
    def _hz_to_cent(hz_track, ref_freq):
        """--------------------------------------------------------------------
        Converts an array of Hertz values into cents.
        -----------------------------------------------------------------------
        hz_track : The 1-D array of Hertz values
        ref_freq    : Reference frequency for cent conversion
        --------------------------------------------------------------------"""
        hz_track = np.array(hz_track)

        # The 0 Hz values are removed, not only because they are meaningless,
        # but also logarithm of 0 is problematic.
        return np.log2(hz_track[hz_track > 0] / ref_freq) * 1200.0
