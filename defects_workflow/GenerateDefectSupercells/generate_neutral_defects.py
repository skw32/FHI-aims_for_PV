### Example usage:
# For As-on-Cu antisites:
# python3 generate_defects.py -i CZTS.in -f aims -a As -b Cu
# For Cu vacancies:
# python3 generate_defects.py -i CZTS.in -f aims -v Cu
#################################################################################################


# A workflow for setting up supercell geometry files for defect calculations with either vasp or FHI-aims (currently only for vacancies or antisites)
# Transformer libraries by J. M. Skelton
# Workflow python script by S. K. Wallace

### User inputs:
# -i specifies name of geometry file of unit cell, default is geometry.in
# -f sets format as vasp or FHI-aims, options are vasp or aims, default is aims
# -t sets the tolerance for recognising the symmetry of the structure, default is 1.0e-5 (same as in step 1)
# -x, y, z sets desired supercell dimensions, if not specified default is set to 1x1x1
# -v specifies type of vacancy the user wishes to generate, e.g. '-v S' would be sulfur vacancies
# -a specifies the species to place into the lattice as an antisite
# -b specifies the species to be replaced in the lattice when forming an antisite defect, e.g. '-a Cu -b Zn' would create Cu-on-Zn antisites

### Outputs:
# The code will produce a directory containing either your vacancy or antisite defects, in a tar format, with sub directories for structures with different space groups
# The first tar file (the one containing 'DefectType_001_...' is always the perfect supercell, then each subsequent are all possible defective supercells for each new lower symmetry space group

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
parser.add_option("-t",
                  action="store", type="float", dest="symm_tolerance", default=1.0e-5,
                  help="The tolerance for recognising the symmetry of the crystal structure.")
parser.add_option("-x",
                  action="store", type="int", dest="x_dim", default=1,
                  help="x-dimension of supercell you wish to generate. Default set to 1.")
parser.add_option("-y",
                  action="store", type="int", dest="y_dim", default=1,
                  help="y-dimension of supercell you wish to generate. Default set to 1.")
parser.add_option("-z",
                  action="store", type="int", dest="z_dim", default=1,
                  help="z dimension of supercell you wish to generate. Default set to 1.")
parser.add_option("-v",
                  action="store", type="string", dest="vac", default="no_vacancy",
                  help="Specify the species to remove from the structure when creating vacancies.")
parser.add_option("-a",
                  action="store", type="string", dest="anti_in", default="no_antisite",
                  help="Specify the species to add into the crystal when forming an antisite.")
parser.add_option("-b",
                  action="store", type="string", dest="anti_out", default="no_antisite",
                  help="Specify the species to be replaced from the crystal when forming an antisite.")
(options, args) = parser.parse_args()

# Reading in command line inputs
geom_file = options.input_file
geom_format = options.format
tolerance = options.symm_tolerance
xdim = options.x_dim
ydim = options.y_dim
zdim = options.z_dim
vacancy = options.vac
antisite_in = options.anti_in
antisite_out = options.anti_out

# ----------------------------------------------------------------------------------------------------------
# Generate supercell and defects requested by user
# ----------------------------------------------------------------------------------------------------------

if (geom_format == "aims"):
  structure = ReadAIMSGeometryFile(geom_file);
else:
  structure = ReadPOSCARFile(geom_file);

supercell = structure.GetSupercell((xdim, ydim, zdim));

# Generating vacancies if requested by user
if (vacancy != "no_vacancy"):
  substitutions = [(vacancy, None)];
  # Use the AtomicSubstitutions convenience function to generate the defective structures.
  _, resultSet = AtomicSubstitutions(
    supercell, substitutions, tolerance = tolerance
    );
  # Export the results.
#  ExportAtomicSubstitutionResultSet(
#      resultSet, prefix = "V-{0}".format(vacancy), workingDirectory = r"VacancySupercells", fileFormat = geom_format
#      );
  # Export the results with updated Transformer functions (09.08.17)
  ExportResultSet(
      resultSet, prefix = "V-{0}".format(vacancy), workingDirectory = r"VacancySupercells", fileFormat = geom_format
      );

# Generating antisite if requested by user
if (antisite_in != "no_antisite"):
   substitutions = [(antisite_out, antisite_in)];
   # Use the AtomicSubstitutions convenience function to generate the defective structures.
   _, resultSet = AtomicSubstitutions(
    supercell, substitutions, tolerance = tolerance
    );
   # Export the results.
   ExportResultSet(
      resultSet, prefix = "{0}-{1}".format(antisite_in, antisite_out), workingDirectory = r"AntisiteSupercells", fileFormat = geom_format
      );
