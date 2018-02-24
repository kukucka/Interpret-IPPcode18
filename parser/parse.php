<?php
include('XMLInstruction.php');
include('XMLCreator.php');
include('XMLArgument.php');
include('Analyzer.php');
//TODO popsat rozsireni ze vytvori prazdny soubor


/**
 * Argumenty jsou zpracovani za vyuziti funkce getopt.
 * Podporuji zpracovani argumentu help/h dale podporuji argumenty
 * pro rozsireni STATP stats/loc/comments.
 * Pri zadani jineho komentare dojde chybe
 */

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
    exit(10);
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

/**
 * Provede se vytvoreni nove instance objektu Analyzer a XMLCreator.
 * Pote probehne inicializace tvorby XML souboru.
 * Nasleduje nacitani a zpracovavani instrukci ze vstupu(stdin).
 * V momente kdy j intrukce a jeji argumnty zpracovany dojde k jejich
 * je jejich zpracovany tvar predan funkci createArgument()
 * ktera pote vytvori instrukci v pozadovanem formatu.
 * Po zpracovani vsech udaju ze vstupu je vygenerovan vysledek
 * ve forme XML na vystup(stdout)
 */
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


//Extension
/**
 * Rozsireni STATP
 * V zavislosti na zadanych argumentech vygeneruje vystupni soubor, ktery
 * muze obsahovat pocet radku, na kterych se vyskytuji komentare a/nebo pocet
 * radku, na kterych se vyskytuji instrukce.
 * Argumenty:
 * --stats=file - znaci soubor do ktereho se ma ulozit vysledek
 * --loc - do vysledneho souvoru bude vypsan pocet radku s instrucki
 * --comments - do vysledneho souboru bude vypsan pocet radsku s komentarem
 * V pripade ze bude zadan pouze argument --stats=file, dojde k vygenerovani
 * prazdneho souboru, dale pokud budou zadany oba argument poradi vysledku
 * v cilovem souboru file je urceno podle jejich poradi pri zadani
 */

/**
 * do commentNumbers je ulozen pocet radku,na kterych se vyskytl komentar
 * do instructionNumber je ulozen pocet radku,na kterych se vyskytla instrukce
 */
$commentNumbers = $analyzer->getCommentsNumber();
$instructionNumber = $analyzer->getInstructionNumber();

/**
 * pokud by argument zadan ulozi se bool hodnota true do prommene
 * ktera znaci argument(jmenovite) a v pripade zadani stats se do promenne
 * file ulozi nazev souboru ze --stats=file
 */
$loc = false;
$comm = false;
$stats = false;
$file = "";

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

/**
 * pokud je zadan argument stats je proveden vypis
 * do souboru v zavislosti na dalsich zadanych argumentech
 * patricich k rozsireni STATP
 */
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