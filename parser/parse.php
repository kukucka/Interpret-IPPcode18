<?php
include('XMLInstruction.php');
include('XMLCreator.php');
include('XMLArgument.php');
include('Analyzer.php');
//TODO argument
//TODO zkontrolovat errory cisla
//TODO je otazka zda GF muze byt i Gf atd.
//TODO popsat rozsireni ze vytvori prazdny soubor
$loc = false;
$comm = false;
$stats = false;
$file = "";

$shortopts  = "h";

$longopts  = array(
    "stats::",
    "comments",    // Optional value
    "loc",        // No value
    "help"         // No value
);
$options = getopt($shortopts, $longopts);

if((count($options) + 1) != $argc){
    print("You entered wrong arguments use --help for more informations\n");
    exit(21);
}
if(array_key_exists('help', $options) || array_key_exists('h', $options)){
    print("Parse.php prevadi kod IPPcode18 do symbolickuch intrukci\n");
    print("Vstup do parse.php se zadava na stdin\n");    
    print("Implementovane rozsireni:\n");    
    print("--stats=file soubor do ktereho se ulozi vysledek, tento parametr je povinny\n");    
    print("--loc pocita vyskyt instrukciv souboru\n");
    print("--comments pocita vyskyt komentaru\n");
    exit(0);
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
$commentNumbers = $analyzer->getCommentsNumber();
$instructionNumber = $analyzer->getInstructionNumber();

//Extension

if(array_key_exists('loc', $options)){
    $loc = true;
    $locPos = getPositon('--loc', $argc, $argv);
}
if(array_key_exists('comments', $options)){
    $comm = true;
    $commPos = getPositon('--comments', $argc, $argv);
}
if(array_key_exists('stats', $options)){
    $file = $options['stats'];
    $stats = true;
}else if($comm || $loc){
    exit(10);
}
function getPositon($str, $num, $argv){
    for($i = 0; $i < $num; $i++){
        if($argv[$i] == $str){
            return $i;
        }
    }
}

if($stats){
    $myfile = fopen($file, "w");
    if($comm && $loc){
        if($locPos > $commPos){
            fwrite($myfile, $commentNumbers);    
            fwrite($myfile, "\n");        
            fwrite($myfile, $instructionNumber);    
        }else{
            fwrite($myfile, $instructionNumber); 
            fwrite($myfile, "\n");                
            fwrite($myfile, $commentNumbers);    
        }
    }else{
        if($comm){
            fwrite($myfile, $commentNumbers);    
        }
        if($loc){
            fwrite($myfile, $instructionNumber);    
        }
    }
    fclose($myfile);
}

exit(0);
?>