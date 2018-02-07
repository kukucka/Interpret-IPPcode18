<?php
include('XMLInstruction.php');
include('XMLArgument.php');
include('XMLCreator.php');
include('Analyzer.php');

$a = new Analyzer;

$a->startLoading();

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