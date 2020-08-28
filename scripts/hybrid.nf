db_qc =  Channel.fromPath('inputs/*.sqlite3')
db_hybrid =  Channel.fromPath('inputs/*.sqlite3')

basedir = "$baseDir"

process skeleton_qc {
  input:
  path x from db_qc

  output:
  file "skeleton_input_Hybrid_IS_IonType_DRJ_v2.tsv_output.tsv" into skeleton_output

  publishDir 'qc_files'

  script:
  """
  python3 $basedir/scripts/skeleton.py $x "${SKELETON_QC_INPUT}"
  """
}

process skeleton_hybrid {
  input:
  path x from db_hybrid

  output:
  file "Skeleton_input_Hybrid_IonType_100919.tsv_output.tsv" into skeleton_hybrid_output

  publishDir 'inputs'

  script:
  """
  python3 $basedir/scripts/skeleton.py $x "${SKELETON_HYBRID_INPUT}"
  """
}

process skeleton_qc_cv {
	
	input:
	file x from skeleton_output

	output:
	file "${x}_CV.tsv" into qc_skeleton

	publishDir 'qc_files'

	script:
	"""
	python3 $basedir/scripts/qc.py $x $basedir/inputs/Groups.tsv
	"""
}

process cv_plots {
	
	input:
	file x from qc_skeleton

	output:
	file 'plot' into plot

	publishDir 'qc_files'

	script:
	"""
	python3 $basedir/scripts/qc.plot.py $x $basedir/inputs/Groups.tsv
	"""
}


