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
if($recur){
    $output = shell_exec("find $dir -name \*.src -type f" );    
}else{
    $output = shell_exec("find $dir -maxdepth 1 -name \*.src -type f");    
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
        $out = shell_exec("cat $o.src | php $parse > $o.xml; echo $?" );
        $fileRc = fopen("$o".".rc", "r") or die("Unable to open file!");        
        $code2 = fgets($fileRc);
        fclose($fileRc);   
        // $fileOc = fopen("$o".".oc", "r") or die("Unable to open file!");        
        // $code = fgets($fileOc);
        if(trim($out) != 0){
            if(trim($out) != trim($code2)){
                print("ERROR PARSE");
            }else{
                print("PLANNED");
            }
        }else{
            $out2 = shell_exec("cat $o.in | python3.6 $int --source=$o.xml > $o.tmp; echo $?");
            shell_exec("cat $o.xml");
            $diffOut = shell_exec("diff $o.out $o.tmp");
            if(trim($out2) != trim($code2)){
                print("ERROR INT CODES");
            }else if($diffOut != ""){
                print("ERROR INT VALUE");
            }
            unlink($o . ".tmp");
            unlink($o . ".xml");   
        }
        // print "$out2";        
    }
}    

var_dump($split);

?>