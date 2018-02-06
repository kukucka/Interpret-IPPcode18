<?php
include("XMLCreator.php");
include("XMLArgument.php");
include("XMLInstruction.php");

$woo = new XMLCreator;
$woo->lol();
$woo->initiateXML();
$woo->endXML();

function createArguments($instruction, $arrayOfArguments){
    $count = count($arrayOfArguments);
    if($instruction->getNumOfArguments != $count){
        fprintf(STDERR, "Syntakticka chyba?!");       
        exit(2);   
    }
    if($count == 1){

    }elseif($count == 2){

    }elseif($count == 3){

    }else{
        fprintf(STDERR, "Syntakticka chyba?!");
        exit(2);        
    }

    endInstruction($instruction);
}
?>