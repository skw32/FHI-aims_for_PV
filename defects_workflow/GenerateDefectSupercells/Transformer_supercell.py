### Example usage:
# python3 Transformer_supercell.py -i geometry.in -f aims -x 2 -y 2 -z 2
#################################################################################################


# For command line arguments
from optparse import OptionParser

# Routines from Transformer
from Transformer.IO.AIMS import ReadAIMSGeometryFile;
from Transformer.IO.VASP import ReadPOSCARFile;
from Transformer.IO.AIMS import WriteAIMSGeometryFile;
from Transformer.IO.VASP import WritePOSCARFile;
from Transformer.Constants import AtomicNumberToSymbol;

parser = OptionParser()
parser.add_option("-i",
                  action="store", type="string", dest="input_file", default="geometry.in",
                  help="The filename for the unit cell geometry file. Default is geometry.in.")
parser.add_option("-f",
                  action="store", type="string", dest="format", default="aims",
                  help="Set the format of geometry files to either vasp or aims. Default is aims.")
parser.add_option("-x",
                  action="store", type="int", dest="x_dim", default=1,
                  help="x-dimension of supercell you wish to generate. Default set to 1.")
parser.add_option("-y",
                  action="store", type="int", dest="y_dim", default=1,
                  help="y-dimension of supercell you wish to generate. Default set to 1.")
parser.add_option("-z",
                  action="store", type="int", dest="z_dim", default=1,
                  help="z dimension of supercell you wish to generate. Default set to 1.")
(options, args) = parser.parse_args()

# Reading in command line inputs
geom_file = options.input_file
geom_format = options.format
xdim = options.x_dim
ydim = options.y_dim
zdim = options.z_dim

if (geom_format == "aims"):
  structure = ReadAIMSGeometryFile(geom_file);
else:
  structure = ReadPOSCARFile(geom_file);

supercell = structure.GetSupercell((xdim, ydim, zdim));
if (geom_format == "aims"):
  supercell_file = WriteAIMSGeometryFile(supercell, "supercell_geometry.in", None);
else:
  supercell_file = WritePOSCARFile(supercell, "supercell_POSCAR", None);
