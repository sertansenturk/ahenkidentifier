import os
import json
import numpy as np
from future.utils import iteritems


class AhenkIdentifier(object):
    CENTS_IN_OCTAVE = 1200  # cents

    @classmethod
    def identify(cls, tonic_freq, symbol_in):
        assert 20.0 <= tonic_freq <= 20000.0, "The input tonic frequency " \
                                              "must be between and 20000 Hz"

        tonic_dict = cls._get_dict('tonic')
        ahenks = cls._get_dict('ahenk')

        # get the tonic symbol and frequency
        tonic_symbol, tonic_bolahenk_freq, makam = cls._get_tonic_symbol(
            symbol_in, tonic_dict)

        # get the transposition in cents, rounded to the closest semitone
        cent_dist = cls._hz_to_cent(tonic_freq, tonic_bolahenk_freq)
        mod_cent_dist = np.mod(cent_dist, cls.CENTS_IN_OCTAVE)

        # if the distance is more than 1150 cents wrap it to minus
        # so it will be mapped to 0 cents
        mod_cent_dist = (mod_cent_dist if mod_cent_dist < 1150
                         else mod_cent_dist - 1200)

        mod_cent_approx = int(np.round(mod_cent_dist * 0.01) * 100)
        mod_cent_dev = mod_cent_approx - mod_cent_dist
        abs_mod_cent_dev = abs(mod_cent_dev)

        # create the stats dictionary
        distance_to_bolahenk = {
            'performed': {'value': mod_cent_dist.tolist()[0], 'unit': 'cent'},
            'theoretical': {'value': mod_cent_approx, 'unit': 'cent'}}
        ahenk_dict = {'name': '', 'slug': '', 'makam': makam,
                      'tonic_symbol': tonic_symbol,
                      'distance_to_bolahenk': distance_to_bolahenk,
                      'deviation': {'value': mod_cent_dev.tolist()[0],
                                    'unit': 'cent'},
                      'abs_deviation': {'value': abs_mod_cent_dev.tolist()[0],
                                        'unit': 'cent'}}

        # get the ahenk
        for ahenk_slug, val in iteritems(ahenks):
            if val['cent_transposition'] == mod_cent_approx:
                ahenk_dict['name'] = val['name']
                ahenk_dict['slug'] = ahenk_slug
                return ahenk_dict

    @classmethod
    def _get_tonic_symbol(cls, symbol_in, tonic_dict):
        if symbol_in in tonic_dict.keys():  # tonic symbol given
            tonic_symbol = symbol_in
            makam = None
            tonic_bolahenk_freq = tonic_dict[symbol_in]['bolahenk_freq']
        else:  # check if the makam name is given
            makam = symbol_in
            tonic_symbol, tonic_bolahenk_freq = \
                cls._get_tonic_symbol_from_makam(symbol_in, tonic_dict)
            if not tonic_bolahenk_freq:
                raise ValueError("The second input has to be a tonic symbol "
                                 "or a makam slug!")

        return tonic_symbol, tonic_bolahenk_freq, makam

    @staticmethod
    def _get_tonic_symbol_from_makam(symbol_in, tonic_dict):
        tonic_bolahenk_freq = tonic_symbol = None
        for sym, val in iteritems(tonic_dict):
            if symbol_in in val['makams']:
                tonic_symbol = sym
                tonic_bolahenk_freq = val['bolahenk_freq']
                if not tonic_bolahenk_freq:  # tonic symbol is not known
                    raise KeyError("The tonic of this makam is not known.")
                break
        return tonic_symbol, tonic_bolahenk_freq

    @staticmethod
    def _get_dict(dict_type):
        dict_file = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'data', dict_type + '.json')
        return json.load(open(dict_file, 'r'))

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
