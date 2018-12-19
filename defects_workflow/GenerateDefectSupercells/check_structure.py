### Example usage:
# python3 check_structure.py -i CZTS.in -s 82 -f aims -t 5.0e-5
#################################################################################################


### User inputs
# -i specifies name of geometry file of unit cell, default is geometry.in
# -f sets format as vasp or FHI-aims, options are vasp or aims, default is aims
# -s sets expected space group of input unit cell (number) so we can check that spglib recognises the correct symmetry for the input file (if left blank the script doesn't check the symmetry with spglib)
# -t sets the tolerance for recognising the symmetry of the structure, default is 1.0e-5

# ----------------------------------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------------------------------

# For command line arguments
from optparse import OptionParser

# Routines from Transformer
from Transformer.IO.AIMS import ReadAIMSGeometryFile;
from Transformer.IO.VASP import ReadPOSCARFile;
from Transformer.Framework.BatchIO import ExportResultSet;
from Transformer.Framework.Core import AtomicSubstitutions;
from Transformer.Constants import AtomicNumberToSymbol;

# ----------------------------------------------------------------------------------------------------------
# Read in and store user command line options
# ----------------------------------------------------------------------------------------------------------

parser = OptionParser()
parser.add_option("-i",
                  action="store", type="string", dest="input_file", default="geometry.in",
                  help="The filename for the unit cell geometry file. Default is geometry.in.")
parser.add_option("-f",
                  action="store", type="string", dest="format", default="aims",
                  help="Set the format of geometry files to either vasp or aims. Default is aims.")
parser.add_option("-s",
                  action="store", type="int", dest="input_spacegroup", default=1000,
                  help="The spacegroup number of the input crystal structure if you wish to check that spglib")
parser.add_option("-t",
                  action="store", type="float", dest="symm_tolerance", default=1.0e-5,
                  help="The tolerance for recognising the symmetry of the crystal structure.")
(options, args) = parser.parse_args()

# Reading in command line inputs
geom_file = options.input_file
geom_format = options.format
spacegroup = options.input_spacegroup
tolerance = options.symm_tolerance

# ----------------------------------------------------------------------------------------------------------
# Read input geometry file and check symmetry of input file is recognised by spglib
# ----------------------------------------------------------------------------------------------------------

if (geom_format == "aims"):
  structure = ReadAIMSGeometryFile(geom_file);
else:
  structure = ReadPOSCARFile(geom_file);

sgNumber, sgString = structure.GetSpacegroup(tolerance = tolerance);

print("");

# If spacegroup is not default value of 1000, assume user wishes to check the symmetry for the spacegroup they entered
if (spacegroup != 1000):
  if (sgNumber != spacegroup):
    print("Outcome of your symmetry check...");
    print("Oh dear, spglib has recognised {0} as the spacegroup of your input structure, but you entered {1}. Maybe you should double check your structure? Or try reducing the tolerance a little using '-t'. Maybe 5.0e-5?".format(sgNumber, spacegroup));
  else:
    print("Outcome of your symmetry check...");
    print("Good news, spglib has recognised your input structure spacegroup as {0}, you're good to go!".format(spacegroup));

# ----------------------------------------------------------------------------------------------------------
# Outputting number of inequivalent sites for each species
# ----------------------------------------------------------------------------------------------------------

print("");

indices, counts = structure.GetUniqueAtomIndices(tolerance);
atomTypeNumbers = structure.GetAtomTypeNumbers();

print("Unique atoms (site degeneracy):");

for index, count in zip(indices, counts):
    print("{0: >2} ({1: >2})".format(AtomicNumberToSymbol(atomTypeNumbers[index]), count));
