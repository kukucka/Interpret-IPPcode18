<?php
include('HTMLGenerator.php');

$shortopts  = "p::";
$shortopts  .= "i::";
$shortopts  .= "d::";
$shortopts  .= "h";
$shortopts  .= "r";

// Required value
//Existence parse and interpretu

$longopts  = array(
    "parse-script::",
    "int-script::",    // Optional value
    "directory::",        // No value
    "recursive",
    "help"         // No value
);
$options = getopt($shortopts, $longopts);

if((count($options) + 1) != $argc){
    print("You entered wrong arguments use --help for more informations\n");
    exit(21);
}
$generator = new HTMLGenerator();
$parse = "parse.php";
$int = "interpret.py";
$dir = "./";
$recur = False;
// Zjistit jestli se to ma ukoncit
if(array_key_exists('help', $options) || array_key_exists('h', $options)){
    print("--directory=path -path is the adress of folder to iterate through\n");
    print("--recursice - test.php will run through all folders in set folder recursively\n");
    print("--parse-script=file -file position of parse.php\n");
    print("--int-script=file -file position of interpret.py\n");
    exit(0);
}
if(array_key_exists('recursive', $options) || array_key_exists('r', $options)){
    $recur = True;
}
if(array_key_exists('directory', $options)){
    $dir = $options['directory'];
}
if(array_key_exists('d', $options)){
    $dir = $options['d'];
}
if(array_key_exists('int-script', $options)){
    $int = $options['int-script'];
}
if( array_key_exists('i', $options)){
    $int = $options['i'];
}
if(array_key_exists('parse-script', $options)){
    $parse = $options['parse-script'];
}
if(array_key_exists('p', $options)){
    $parse = $options['p'];
}
if($recur){
    $output = shell_exec("find $dir -name \*.src -type f" );    
}else{
    $output = shell_exec("find $dir -maxdepth 1 -name \*.src -type f");    
}
if(!file_exists($parse)){
    print("File parse.php doesnt exist\n");
    exit(21);
}

if(!file_exists($int)){
    print("File interpret.py doesnt exist\n");
    exit(21);    
}

$split = preg_split('/\s+/' , $output);
$num = 0;
foreach($split as $o){
    $split[$num] = preg_replace('/.src$/', "", trim($o));
    $num += 1;
}

foreach($split as $o){
    if($o != ""){
        $n = $o . '.out';    
        if(!file_exists($n)){
            $myfile = fopen("$o.out", "w") or die("Unable to open file!");
            fclose($myfile);
        }

        $n = $o . '.in';    
        if(!file_exists($n)){
            $myfile = fopen("$o.in", "w") or die("Unable to open file!");
            fclose($myfile);
        }

        $n = $o . '.rc';    
        if(!file_exists($n)){
            $myfile = fopen("$o.rc", "w") or die("Unable to open file!");
            fwrite($myfile, 0);
            fclose($myfile);
        }
    }

    
}
//php5.6 nez to nahraju a python3.6, co kdyz tam bude vic radku, vyresit read
foreach($split as $o){
    if($o != ""){
        $noMistake = true;
        $outCode = shell_exec("cat $o.src | php $parse > $o.xml; echo $?" );
        $rcCode = shell_exec("cat $o.rc");
        $outExpectedHTML = shell_exec("cat $o.out");
        $inHTML = shell_exec("cat $o.in");
        $outHTML = "";
        // $fileOc = fopen("$o".".oc", "r") or die("Unable to open file!");        
        // $code = fgets($fileOc);
        if(trim($outCode) != 0){
            if(trim($outCode) != trim($rcCode)){
                $noMistake = false;                
            }else{
                $noMistake = true;                
            }
        }else{
            $outCode = shell_exec("cat $o.in | python3.6 $int --source=$o.xml > $o.tmp; echo $?");
            $outHTML = shell_exec("cat $o.tmp");

            $diffOut = shell_exec("diff $o.out $o.tmp");
            if(trim($outCode) != trim($rcCode)){
                $noMistake = false;
            }else if($diffOut != ""){
                $noMistake = false;
            }
            unlink($o . ".tmp");
            unlink($o . ".xml");   
        }
        if($noMistake){
            $generator->tablePiece($o, "PASSED");
        }else{
            $generator->tablePiece($o, "FAILED");
        }
        $generator->textInputElementPiece($o, $inHTML);
        $generator->textOutputElementPiece($o, $outHTML);
        $generator->textExpectedOutputElementPiece($o, $outExpectedHTML);
        $generator->textOutputCodeElementPiece($o, $outCode);
        $generator->textExpectedOutputCodeElementPiece($o, $rcCode);
        // print "$out2";        
    }
}    
// $generator->tablePiece("test1", "FAILED");
// $generator->textInputElementPiece("test1", "42");
// $generator->textOutputElementPiece("test1", "Ahoj kame");
// $generator->textExpectedOutputElementPiece("test1", "ahoj Kame");
// $generator->textOutputCodeElementPiece("test1", "0");
// $generator->textExpectedOutputCodeElementPiece("test1", "21");

$generator->fullHTML();
// var_dump($split);

?>