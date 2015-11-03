import os
import json
import numpy as np

def identify(tonic_freq, symbol_in):
	tonic_dict = get_tonic_dict()
	ahenks = get_ahenk_dict()

	# get the tonic symbol and frequency
	if symbol_in in tonic_dict.keys():  # tonic symbol given
		tonic_symbol = symbol_in
		tonic_bolahenk_freq = tonic_dict[symbol_in]['bolahenk_freq']
	else:  # check if the makam name is given
		for sym, val in tonic_dict.iteritems():
			if symbol_in in val['makams']:
				tonic_symbol = sym
				tonic_bolahenk_freq = val['bolahenk_freq']
				break
		if not tonic_bolahenk_freq:
			raise ValueError("The second input has to be the tonic " +
				"symbol or the makam slug!")

	# get the transposition in cents, rounded to the closest semitone
	cent_dist = hz_to_cent(tonic_bolahenk_freq, tonic_freq)
	wrapped_cent_dist = get_wrapped_cent_dist(cent_dist)
	wrapped_cent_approx = int(round(wrapped_cent_dist*0.01)*100)

	# get the ahenk
	for ahenk_slug, val in ahenks.iteritems():
		if val['cent_transposition'] == wrapped_cent_approx:
			return val['name']

def get_tonic_dict(): 
    tonic_dict_file = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'data', 'tonic.json')
    return json.load(open(tonic_dict_file, 'r'))

def get_ahenk_dict(): 
    ahenk_dict_file = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'data', 'ahenk.json')
    return json.load(open(ahenk_dict_file, 'r'))

def hz_to_cent(hz_track, ref_freq):
	"""-------------------------------------------------------------------------
	Converts an array of Hertz values into cents.
	----------------------------------------------------------------------------
	hz_track : The 1-D array of Hertz values
	ref_freq	: Reference frequency for cent conversion
	-------------------------------------------------------------------------"""
	hz_track = np.array(hz_track)

	# The 0 Hz values are removed, not only because they are meaningless,
	# but also logarithm of 0 is problematic.
	return np.log2(hz_track[hz_track>0] / ref_freq) * 1200.0

def get_wrapped_cent_dist(cent_dist):
	mod_res = np.mod(cent_dist, 1200)
	return min(mod_res, 1200 - mod_res)
