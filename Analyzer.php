<?php
//naimplementovat ignorovani komentaru
// include('XMLArgument.php');


Class Analyzer{
    //TODO: vytvorit constructor
    private $stdin;

    function __construct(){
        $this->stdin = fopen('php://stdin', 'r');
        do{
            $line = $this->readLine();
            $line = preg_replace('/\s*/','', $line);            
        }while($line == null);
        if(strtolower($line) != ".ippcode18"){
            print "EXIT";
            exit(21);
        }
        
    }

    //TODO mozna to trochu predelam
    function readLine(){
        if(feof($this->stdin)){
            return null;
        }
        $line = fgets($this->stdin);
        $lineFiltered = preg_replace('/#.*/','', $line);
            //neda se prepsat EOF?       
        print count($this->splitIntoWords($lineFiltered));
        //nebezpeci kontrolovat pocet prvku po splitIntoWords
        return $lineFiltered;
            //kdyz je prazdny radek error? wut?!
            // $filteredArray = $this->cleareComments($arrayOfWords);
        
    }
    
    function splitIntoWords($line){
        $arrayOfWords = preg_split('/\s+/', $line, -1, PREG_SPLIT_NO_EMPTY); //prepsat -> presunout treba split        
        return $arrayOfWords;
    }


    // function load(){
    //     $condition = true;
    //     $arg = new XMLCreator; //pridat do konstruktoru
    //     while(!feof($arrayOfWords)){
    //         $arrayOfWords = $this->getInput();
    //         // foreach($arrayOfWords as $word){
    //         //     print "$word\n";
    //         // }
    //         if($arrayOfWords != null){
    //             $arg->initiateXML();
    //             $instruction = $this->analyzeInstruction($arrayOfWords[0]);
    //             array_shift($arrayOfWords);
    //             $arrayOfArguments = $this->handleArguments($arrayOfWords, $instruction);
    //             // print $instruction->getName();
                
    //             $this->checkTypesOfArgumentsInInstruction($instruction, $arrayOfArguments);
        
    //             $arg->createArguments($instruction, $arrayOfArguments);
    //             $arg->endXML();                
    //         }
            
    //         // $arrayOfArguments = $this->analyzeArguments($arrayOfWords);
    //     }
        
    // }

    function checkTypesOfArgumentsInInstruction($instruction, $arrayOfArguments){
        
        $typeOfInstrucion = $instruction->getName();
        
        switch ($typeOfInstrucion){
            case "createframe":
            case "pushframe":
            case "popframe":
            case "return":
            case "break":
                if($arrayOfArguments != null){
                    print "ma argumenty";
                    exit(2); 
                }
                break;
            case "move":
            case "int2char":
            case "strlen":
            case "type":
                if(($arrayOfArguments[0]->getType() != "variable") || ($arrayOfArguments[1]->getType() != "variable" &&
                $arrayOfArguments[1]->getType() != "constant")){
                    print "var sym error";
                    exit(2);  
                }
                break;
            case "defvar":
            case "pops":
                if($arrayOfArguments[0]->getType() != "variable"){
                    print "var error";
                    exit(2);  
                }
                break;
            case "call":
                if($arrayOfArguments[0]->getType() != "label"){
                    print "label error";
                    exit(2);  
                }
                break;
            case "add":
            case "sub":
            case "mul":
            case "idiv":
            case "lt":
            case "gt":
            case "eq":
            case "and":
            case "or":
            case "not":
            case "stri2int":
            case "concat":
            case "getchar":
            case "setchar":
                if(($arrayOfArguments[0]->getType() != "variable") || ($arrayOfArguments[1]->getType() != "variable" &&
                $arrayOfArguments[1]->getType() != "constant")|| ($arrayOfArguments[2]->getType() != "variable" &&
                $arrayOfArguments[2]->getType() != "constant")){
                    print "var sym sym error";
                    exit(2);  
                }
                break;
            case "read":
                if(($arrayOfArguments[0]->getType() != "variable") || $arrayOfArguments[1]->getType() != "constant"){
                    print "var const error";
                    exit(2);  
                }
                break;
            case "write":
            case "dprint":
                if($arrayOfArguments[0]->getType() != "variable" && $arrayOfArguments[0]->getType() != "constant"){
                    print "sym error";
                    exit(2);  
                }
                break;
            case "label":
            case "jump":
            case "pushs";
                if($arrayOfArguments[0]->getType() != "label"){
                    print "lab error";
                    exit(2);  
                }
                break;
            case "jumpifeq":
            case "jumpifneq":
                if(($arrayOfArguments[0]->getType() != "label") || ($arrayOfArguments[1]->getType() != "variable" &&
                $arrayOfArguments[1]->getType() != "constant")|| ($arrayOfArguments[2]->getType() != "variable" &&
                $arrayOfArguments[2]->getType() != "constant")){
                    print "lab sym sym error";
                    exit(2);  
                }
                break;
            default: //34 instrukci
                print "default error";
                exit(2);
        }
    }

    function handleArguments($arrayOfArguments, $instruction){
        $stderr = fopen('php://stderr', 'w'); //refactor this to global        
        $numOfArguments = count($arrayOfArguments);
        $classifiedArguments; //smazat
        if(($instruction->getNumOfArguments()) == $numOfArguments){
            if($numOfArguments == 0){
                return null;
            }else{
                for($i = 0; $i < $numOfArguments; $i++){
                    $classifiedArguments[$i] = $this->analyzeArgument($arrayOfArguments[$i], $i);
                    if($classifiedArguments[$i] == null){
                        print "CHYBA";
                        exit(21);
                    }
                }
                return $classifiedArguments;
            }
            
        }else{
            fprintf($stderr, "Number of arguments differ");
            exit(2);            
        }
    }

    function analyzeArgument($argument, $position){
        if(preg_match('/^bool@/', $argument) || preg_match('/^int@/', $argument) || 
        preg_match('/^string@/', $argument)){
            $splitArgument = explode('@', $argument, 2);
            return new XMLArgument($splitArgument[0], $splitArgument[1], $position+1);
        }else if(preg_match('/^(G|g)(F|f)@/', $argument) || preg_match('/^(T|t)(F|f)@/', $argument) || 
        preg_match('/^(L|l)(F|f)@/', $argument)){
            $splitArgument = explode('@', $argument, 2);
            if(preg_match('/^([a-zA-Z_-]|[*]|[$]|[%]|[&])([a-zA-Z0-9_-]|[*]|[$]|[%]|[&])*$/',$splitArgument[1])){
                return new XMLArgument(strtoupper($splitArgument[0]), $splitArgument[1], $position+1);
            }
            return null;
        }else if(preg_match('/^([a-zA-Z_-]|[*]|[$]|[%]|[&])([a-zA-Z0-9_-]|[*]|[$]|[%]|[&])*$/',$argument)){
            return new XMLArgument("label", $argument, $position+1);            
        }else{
            return null;
        }
        
    }

    function analyzeInstruction($instruction){
        $length = strlen($instruction);
        $stderr = fopen('php://stderr', 'w'); 
        
        if($length == 2){
            if(preg_match('/(L|l)(T|t)/', $instruction)){
                $newInstruction = new XMLInstruction('lt',3);
            }elseif(preg_match('/(G|g)(T|t)/', $instruction)){
                $newInstruction = new XMLInstruction('gt',3);
            }elseif(preg_match('/(E|e)(Q|q)/', $instruction)){
                $newInstruction = new XMLInstruction('eq',3);
            }elseif(preg_match('/(O|o)(R|r)/', $instruction)){
                $newInstruction = new XMLInstruction('or',3);
            }else{
                fprintf($stderr, "Instruction missing");
                exit(2);
            }
        }elseif($length == 3){               
            if(preg_match('/(A|a)(D|d)(D|d)/',$instruction)){
                $newInstruction = new XMLInstruction('add',3);
            }elseif(preg_match('/(S|s)(U|u)(B|b)/', $instruction)){
                $newInstruction = new XMLInstruction('sub',3);    
            }elseif(preg_match('/(M|m)(U|u)(L|l)/', $instruction)){
                $newInstruction = new XMLInstruction('mul',3);    
            }elseif(preg_match('/(A|a)(N|n)(D|d)/', $instruction)){
                $newInstruction = new XMLInstruction('and',3);
            }elseif(preg_match('/(N|n)(O|o)(T|t)/', $instruction)){
                $newInstruction = new XMLInstruction('not',3);
            }else{
                fprintf($stderr, "Instruction missing");
                exit(2);
            }
        }elseif($length == 4){
            if(preg_match('/(M|m)(O|o)(V|v)(E|e)/',$instruction)){
                $newInstruction = new XMLInstruction('move',2);
            }elseif(preg_match('/(C|c)(A|a)(L|l)(L|l)/', $instruction)){
                $newInstruction = new XMLInstruction('call',1);
            }elseif(preg_match('/(P|p)(O|o)(P|p)(S|s)/', $instruction)){
                $newInstruction = new XMLInstruction('pops',1);
            }elseif(preg_match('/(I|i)(D|d)(I|i)(V|v)/', $instruction)){
                $newInstruction = new XMLInstruction('idiv',3);
            }elseif(preg_match('/(R|r)(E|e)(A|a)(D|d)/', $instruction)){
                $newInstruction = new XMLInstruction('read',2);
            }elseif(preg_match('/(T|t)(Y|y)(P|p)(E|e)/', $instruction)){
                $newInstruction = new XMLInstruction('type',2);
            }elseif(preg_match('/(J|j)(U|u)(M|m)(P|p)/', $instruction)){
                $newInstruction = new XMLInstruction('jump',1);
            }else{
                fprintf($stderr, "Instruction missing");
                exit(2);
            }
        }elseif($length == 5){
            if(preg_match('/(P|p)(U|u)(S|s)(H|h)(S|s)/', $instruction)){
                $newInstruction = new XMLInstruction('pushs',1);
            }elseif(preg_match('/(W|w)(R|r)(I|i)(T|t)(E|e)/', $instruction)){
                $newInstruction = new XMLInstruction('write',1);
            }elseif(preg_match('/(L|l)(A|a)(B|b)(E|e)(L|l)/', $instruction)){
                $newInstruction = new XMLInstruction('label',1);
            }elseif(preg_match('/(B|b)(R|r)(E|e)(A|a)(K|k)/', $instruction)){
                $newInstruction = new XMLInstruction('break',0);
            }else{
                fprintf($stderr, "Instruction missing");
                exit(2);
            }
        }elseif($length == 6){
            if(preg_match('/(D|d)(E|e)(F|f)(V|v)(A|a)(R|r)/', $instruction)){
                $newInstruction = new XMLInstruction('defvar',1);
            }elseif(preg_match('/(R|r)(E|e)(T|t)(U|u)(R|r)(N|n)/', $instruction)){
                $newInstruction = new XMLInstruction('return',0);
            }elseif(preg_match('/(C|c)(O|o)(N|n)(C|c)(A|a)(T|t)/', $instruction)){
                $newInstruction = new XMLInstruction('concat',3);
            }elseif(preg_match('/(S|s)(T|t)(R|r)(L|l)(E|e)(N|n)/', $instruction)){
                $newInstruction = new XMLInstruction('strlen',2);
            }elseif(preg_match('/(D|d)(P|p)(R|r)(I|i)(N|n)(T|t)/', $instruction)){
                $newInstruction = new XMLInstruction('dprint',1);
            }else{
                fprintf($stderr, "Instruction missing");
                exit(2);
            }
        }elseif($length == 7){
            if(preg_match('/(G|g)(E|e)(T|t)(C|c)(H|h)(A|a)(R|r)/', $instruction)){
             $newInstruction = new XMLInstruction('getchar',3);
            }elseif(preg_match('/(S|s)(E|e)(T|t)(C|c)(H|h)(A|a)(R|r)/', $instruction)){
                $newInstruction = new XMLInstruction('setchar',3);
            }else{
                fprintf($stderr, "Instruction missing");
                exit(2);
            }
        }elseif($length == 8){
            if(preg_match('/(P|p)(O|o)(P|p)(F|f)(R|r)(A|a)(M|m)(E|e)/', $instruction)){
                $newInstruction = new XMLInstruction('popframe',0);
            }elseif(preg_match('/(I|i)(N|n)(T|t)(2)(C|c)(H|h)(A|a)(R|r)/', $instruction)){
                $newInstruction = new XMLInstruction('int2char',2);
            }elseif(preg_match('/(S|s)(T|t)(R|r)(I|i)(2)(I|i)(N|n)(T|t)/', $instruction)){
                $newInstruction = new XMLInstruction('stri2int',3);
            }elseif(preg_match('/(J|j)(U|u)(M|m)(P|p)(I|i)(F|f)(E|e)(Q|q)/', $instruction)){
                $newInstruction = new XMLInstruction('jumpifeq',3);
            }else{
                fprintf($stderr, "Instruction missing");
                exit(2);
            }
        }elseif($length == 9){
            if(preg_match('/(P|p)(U|u)(S|s)(H|h)(F|f)(R|r)(A|a)(M|m)(E|e)/', $instruction)){
                $newInstruction = new XMLInstruction('pushframe',0);
            }elseif(preg_match('/(J|j)(U|u)(M|m)(P|p)(I|i)(F|f)(N|n)(E|e)(Q|q)/', $instruction)){
                $newInstruction = new XMLInstruction('jumpifneq',3);
            }else{
                fprintf($stderr, "Instruction missing");
                exit(2);
            }
        }elseif($length == 11){
            if(preg_match('/(C|c)(R|r)(E|e)(A|a)(T|t)(E|e)(F|f)(R|r)(A|a)(M|m)(E|e)/',$instruction)){
                $newInstruction = new XMLInstruction('createframe',0);
            }else{
                fprintf($stderr, "Instruction missing");
                exit(2);
            }
        }else{
            fprintf($stderr, "Instruction missing");
            exit(2);
        }
        
        return $newInstruction;
    }

   
}


?>