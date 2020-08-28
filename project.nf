
ch = Channel.from( 'test' )
ch2 = Channel.from( 'sadfasdfasdfasd' )




process input_file_2 {
  input:
  val nextflow_input from ch2

  output:
  val nextflow_input into methods12, methods22

  """
  echo $nextflow_input > result.txt
  """

}


process input_file {
  input:
  val x from ch

  output:
  val x into methods1, methods2

  """
  echo $x > result.txt
  """

}





process foo2 {
  input:
  file x from methods1

  """
  cat $x
  """

}

process foo3 {
  input:
  file x from methods2

  output:
  file x into combine

  """
  cat $x
  """

}


process foo3_2 {
  input:
  file x from methods22

  output:
  file x into combine2

  """
  cat $x
  """

}




process combine {
  input:
  val x from combine

  val y from combine2

  """
  echo $x $y
  """
}
