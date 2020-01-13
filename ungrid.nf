Channel.fromPath('inputs/SQ0452.sqlite3').set{ db }
basedir = "$baseDir"


process ungrid {
  input:
  file x from db

  output:

  file "${skeleton_input_name}" into skeleton_input

  publishDir 'test'

  script:
  """
  python3 $basedir/scripts/ungrid.py $x $PPM $RT_DELTA $MIN_SIGNAL $MIN_RANGE
  """
}


process skeleton {
    input:
    file skeleton_tsv from skeleton_input

    output:
    file "${skeleton_tsv}_output.tsv" into skeleton_output

    publishDir 'test'

    """
    python3 $basedir/scripts/skeleton.py $basedir/inputs/SQ0452.sqlite3 $skeleton_tsv
    """
}

