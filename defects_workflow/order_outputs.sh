### Ensure you have a control.in and a submission script in the same directory as this bash script
#### Set JobNamePlaceholder as the job name in your submission script
#### Include '#charge ChargePlaceholder' in your control.in
#### Enter the name of your submission script at the top of this script 

#################################################################################################

#! /bin/sh

# ENTER NAME OF SUBMISSION SCRIPT
SubmissionScriptName="submit.sh"


for defect in Vacancy Antisite
  do
 
  cd ${defect}Supercells

  # Taking defect-type to make directories
  ls * > files.dat
  cut -d_ -f1 files.dat > DirNames.dat
  # Remove duplicate directory names and cleanup
  awk '!seen[$0]++' DirNames.dat > UniqueDirNames.dat
  rm files.dat DirNames.dat

  # Making directories for each defect type and moving tar files for structures to correct directory 
  while read dirname others; do
      mkdir "$dirname"
      mv ${dirname}*.gz $dirname
  done < UniqueDirNames.dat

  # Extracting structure for perfect reference and moving to its own directory
  while read dirname others; do
     cd $dirname
     tar -xvf ${dirname}_001*         # 001 directory is always perfect structure
     mkdir PerfectReference
     cp ${dirname}_001*/*geometry.in PerfectReference/perfect_geometry.in
     rm -r ${dirname}_001*
     cp ../../control.in PerfectReference
     cp ../../${SubmissionScriptName} PerfectReference
     # Name job in submission script
     sed -i -e "s/JobNamePlaceholder/PerfectSupercell/g" PerfectReference/${SubmissionScriptName}
     rm PerfectReference/${SubmissionScriptName}-e  # cleanup
     cd ..
  done < UniqueDirNames.dat

  # Extracting structures for point defect
  while read dirname others; do
     cd $dirname
     tar -xvf ${dirname}_002*         # 002 directory contains structures for point defect
     # Extracting spacegroup from filename to use as directory
     cd ${dirname}_002*
     ls * > filename_spacegroups.dat
     awk '{print $NF}' FS=- filename_spacegroups.dat > filenames_sg_trimmed.dat  # Takes everything after hyphen     
     cut -d_ -f1 filenames_sg_trimmed.dat > filenames_sg_trimmed2.dat  # Deletes everything after _


     while read spacegroup others; do
       mkdir ../DefectSpacegroup${spacegroup}
       mv *SG-${spacegroup}_* ../DefectSpacegroup${spacegroup}/geometry.in
       cp ../../../control.in ../DefectSpacegroup${spacegroup}
       cp ../../../${SubmissionScriptName} ../DefectSpacegroup${spacegroup}
       # Name job in submission script
       sed -i -e "s/JobNamePlaceholder/${dirname}_SG_${spacegroup}_neutral/g" ../DefectSpacegroup${spacegroup}/${SubmissionScriptName}
       rm ../DefectSpacegroup${spacegroup}/${SubmissionScriptName}-e  # cleanup
     done < filenames_sg_trimmed2.dat
     rm filenames_sg_trimmed.dat filenames_sg_trimmed2.dat  # cleanup    

     cd ..
     rm -r ${dirname}_002*
     cd ..
  done < UniqueDirNames.dat

  rm UniqueDirNames.dat  # cleanup
  cd ..  

done
