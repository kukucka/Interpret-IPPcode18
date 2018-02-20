<?php

$shortopts  = "";
// Required value

$longopts  = array(
    "parse-script::",
    "int-script::",    // Optional value
    "directory::",        // No value
    "recursive",
    "help"         // No value
);
$options = getopt($shortopts, $longopts);

if((count($options) + 1) != $argc){
    exit(21);
}

$parse = "parse.php";
$int = "interpret.py";
$dir = "./";
$recur = False;
// Zjistit jestli se to ma ukoncit
if(array_key_exists('help', $options)){
    print("--directory=path -path is the adress of folder to iterate through\n");
    print("--recursice - test.php will run through all folders in set folder recursively\n");
    print("--parse-script=file -file position of parse.php\n");
    print("--int-script=file -file position of interpret.py\n");
    exit(0);
}
if(array_key_exists('recursive', $options)){
    $recur = True;
}
if(array_key_exists('directory', $options)){
    $dir = $options['directory'];
}
if(array_key_exists('int-script', $options)){
    $int = $options['int-script'];
}
if(array_key_exists('parse-script', $options)){
    $parse = $options['parse-script'];
}

$output = shell_exec("ls $dir");
$split = preg_split('/\s+/' , $output);
var_dump($split);

?>