<?php


function getInput(){
    $line = fgets(STDIN);
    $arrayOfWords = preg_split('/((^\p{P}+)|(\p{P}*\s+\p{P}*)|(\p{P}+$))/', $line, -1, PREG_SPLIT_NO_EMPTY);
    // $filteredArray = $this->cleareComments($arrayOfWords);
    return $arrayOfWords;
}

while(true){
    $a = getInput();
    $numOfArg = $a[1];
    $atl = strtolower($a[0]);
    $result = str_split($a[0]);
    $count = count($result);
    print "elseif(\$length == $count){\n";
    print 'elseif(preg_match(\'/';
    foreach($result as $c){
        $a = strtoupper($c);
        $b = strtolower($c);
        print "($a|$b)";
    }
    print '/\', $instruction)){';
    print "\n \$newInstruction = new XMLInstruction('$atl',$numOfArg);\n}\n}";
    }

?>