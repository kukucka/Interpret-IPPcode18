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
    if($arrayOfWords == null){
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
?>