<?php
include('XMLInstruction.php');
include('XMLCreator.php');
include('XMLArgument.php');
include('Analyzer.php');
//TODO argument
//TODO je otazka zda GF muze byt i Gf atd.
if(count($argv) == 1){
}elseif(count($argv) == 2){
    if($argv[1] == "--help"){
        print "Pomoc doplnit\n";
        exit(0);        
    }else{
        print "Spatny argument";
        exit(21);
    }
}else{
    print "Spatny argument";    
    exit(21);
}

$analyzer = new Analyzer;
$xmlCreator = new XMLCreator;
$xmlCreator->initiateXML();
while(($line=$analyzer->readLine()) != null){
    $arrayOfWords = $analyzer->splitIntoWords($line);
    if(count($arrayOfWords) == 0){
        continue;
    }
    $instruction = $analyzer->analyzeInstruction($arrayOfWords[0]);
    array_shift($arrayOfWords);
    $arrayOfArguments = $analyzer->handleArguments($arrayOfWords, $instruction);
    $analyzer->checkTypesOfArgumentsInInstruction($instruction, $arrayOfArguments);
    $xmlCreator->createArguments($instruction, $arrayOfArguments);
}
$xmlCreator->endXML();

exit(0);        

// $arg = new XMLCreator;
//
//
// $arg1 = new XMLArgument('string','Ahoj',1);
// $arg2 = new XMLArgument('string','Belorusko',2);
// $arg3 = new XMLArgument('int','Rusko',3);
// $inst1 = new XMLInstruction('MoVe',2);
// $arrOfArg = [$arg1, $arg2];
// $arg->initiateXML();
// $arg->createArguments($inst1, $arrOfArg);
// $arrOfArg = [$arg1, $arg2, $arg3];
// $inst1 = new XMLInstruction('MoVe',3);
// $arg->createArguments($inst1, $arrOfArg);
// $arg->endXML();
?>