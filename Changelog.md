#### ahenkidentifier v1.5.2
 - Input tonic frequency is validation added.
 - The tonic symbol of is returned as "unknown", if the tonic symbol of a makam is not given in the file [tonic.json](https://github.com/sertansenturk/ahenkidentifier/commit/d617f74e6b358fa0f42f81d44f049f3a219a4e86)
 
#### ahenkidentifier v1.5.1
 - Corrected Sultaniyegah tonic symbol from D5 to D4

#### ahenkidentifier v1.5.0
 - Changed the makam/tonic symbol error from IOError to ValueError

#### ahenkidentifier v1.4.0
 - Added more unittests
 - Code coverage integration
 - Code climate integration

#### ahenkidentifier v1.3.0
 - Merged the two outputs into a single dictionary
 - Added missing MANIFEST file and the data packages when installing from github

#### ahenkidentifier v1.2.0
 - Refactored the methods into the AhenkIdentifier object

#### ahenkidentifier v1.1.1
 - Fixed input tonic_symbol/makam_slug checking

#### ahenkidentifier v1.1
 - Python 3.3, 3.4, 3.5 compatibility

#### ahenkidentifier v1.0.1
 - Fixes the ahenk identification bug due to erroneous cent distance computation (Issue: [MTG/dunya#307](https://github.com/MTG/dunya/issues/307))

#### ahenkidentifier v1.0
 - First public release
