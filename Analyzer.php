<?php

Class Analyzer{
    private $stdin;

    function __construct(){
        $this->stdin = fopen('php://stdin', 'r');
        do{
            $line = utf8_encode($this->readLine());
            $line = preg_replace('/\s*/','', $line);          
        }while($line == null);
        if(strtolower($line) != ".ippcode18"){
            exit(21);
        }
    }

    function readLine(){
        if(feof($this->stdin)){
            return null;
        }
        $line = fgets($this->stdin);
        $filteredLine = preg_replace('/#.*/','', $line);
        return $filteredLine;
    }

    function splitIntoWords($line){
        $arrayOfWords = preg_split('/\s+/', $line, -1, PREG_SPLIT_NO_EMPTY);
        if(count($arrayOfWords) == 0){
            return null;
        }
        return $arrayOfWords;
    }

    function handleArguments($arrayOfArguments, $instruction){
        $numOfArguments = count($arrayOfArguments);
        $classifiedArguments = null;
        if(($instruction->getNumOfArguments()) == $numOfArguments){
            if($numOfArguments == 0){
                return null;
            }else{
                for($i = 0; $i < $numOfArguments; $i++){
                    $classifiedArguments[$i] = $this->analyzeArgument($arrayOfArguments[$i], $i);
                    if($classifiedArguments[$i] == null){
                        exit(21);
                    }
                }
                return $classifiedArguments;
            }
        }else{
            exit(21);
        }
    }

    function checkEscapeSequences($string){
        $isOn = false;
        $num = 0;
        for($i=0; $i<strlen($string); $i++){
            if($isOn){
                if(preg_match('/[0-9]/', $string[$i])){
                    $num += 1;
                    if($num == 3){
                        $num = 0;
                        $isOn = false;
                    }
                }else{
                    exit(21);
                }
            }
            if($string[$i] == '\\'){
                $isOn = true;                
            }
        }
        if($isOn){
            exit(21);
        }
    }
        // toConvert = []
        // strToMod = list(str)
        // found = False
        // i = 0
        // for letter in str:
        //     if found:
        //         if re.match(r'[0-9]', strToMod[i]):
        //             toConvert.append(letter)
        //             if(len(toConvert) == 3):
        //                 code = ''.join(toConvert)
        //                 code = int(code)
        //                 strToMod[i] = ''
        //                 strToMod[i-1] = ''
        //                 strToMod[i-2] = ''
        //                 strToMod[i-3] = chr(code)  
        //                 found = False
        //                 toConvert = []
        //         else:
        //             print("ERROR")
        //             exit(124)
        //     if letter == '\\':
        //         found = True
        //     i += 1
        // if found:
        //     print("ERROR")
        //     exit(125)
    // }

    function analyzeArgument($argument, $position){
        if(preg_match('/^int@/', $argument)){
            $splitArgument = explode('@', $argument, 2);
            //tady poresit asi jestli je to true nebo false
            return new XMLArgument($splitArgument[0], $splitArgument[1], $position+1);
        }else if(preg_match('/^string@/', $argument)){
            $splitArgument = explode('@', $argument, 2);
            $this->checkEscapeSequences($splitArgument[1]);
            return new XMLArgument($splitArgument[0], $splitArgument[1], $position+1);            
        }else if(preg_match('/^bool@/', $argument)){
            $splitArgument = explode('@', $argument, 2);            
            if($splitArgument[1] == 'true' || $splitArgument[1] == 'false'){
                return new XMLArgument($splitArgument[0], $splitArgument[1], $position+1);        
            }else{
                exit(21);                
            }
        }else if(preg_match('/^GF@/', $argument) || preg_match('/^TF@/', $argument) || 
        preg_match('/^LF@/', $argument)){
            $splitArgument = explode('@', $argument, 2);
            if(preg_match('/^([a-zA-Z_-]|[*]|[$]|[%]|[&])([a-zA-Z0-9_-]|[*]|[$]|[%]|[&])*$/',$splitArgument[1])){
                return new XMLArgument("var", $argument, $position+1);
            }
            return null;
        }else if(preg_match('/^([a-zA-Z_-]|[*]|[$]|[%]|[&])([a-zA-Z0-9_-]|[*]|[$]|[%]|[&])*$/',$argument)){
            return new XMLArgument("label", $argument, $position+1);            
        }else{
            return null;
        }
    }

    function checkTypesOfArgumentsInInstruction($instruction, $arrayOfArguments){
        switch ($instruction->getName()){
            case "createframe":
            case "pushframe":
            case "popframe":
            case "return":
            case "break":
                if($arrayOfArguments != null){
                    exit(21);
                }
                break;
            case "move":
            case "int2char":
            case "strlen":
            case "type":
                if(($arrayOfArguments[0]->getType() != "variable") || ($arrayOfArguments[1]->getType() != "variable" &&
                        $arrayOfArguments[1]->getType() != "constant")){
                    exit(21);
                }
                break;
            case "defvar":
            case "pops":
                if($arrayOfArguments[0]->getType() != "variable"){
                    exit(21);
                }
                break;
            case "call":
                if($arrayOfArguments[0]->getType() != "label"){
                    exit(21);
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
                    exit(21);
                }
                break;
            case "read":
                if(($arrayOfArguments[0]->getType() != "variable") || $arrayOfArguments[1]->getType() != "constant"){
                    exit(21);
                }
                break;
            case "write":
            case "dprint":
            case "pushs":
                if($arrayOfArguments[0]->getType() != "variable" && $arrayOfArguments[0]->getType() != "constant"){
                    exit(21);
                }
                break;
            case "label":
            case "jump":
                if($arrayOfArguments[0]->getType() != "label"){
                    exit(21);
                }
                break;
            case "jumpifeq":
            case "jumpifneq":
                if(($arrayOfArguments[0]->getType() != "label") || ($arrayOfArguments[1]->getType() != "variable" &&
                        $arrayOfArguments[1]->getType() != "constant")|| ($arrayOfArguments[2]->getType() != "variable" &&
                        $arrayOfArguments[2]->getType() != "constant")){
                    exit(21);
                }
                break;
            default:
                exit(21);
        }
    }

    function analyzeInstruction($instruction){
        $length = strlen($instruction);

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
                exit(21);
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
                exit(21);
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
                exit(21);
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
                exit(21);
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
                exit(21);
            }
        }elseif($length == 7){
            if(preg_match('/(G|g)(E|e)(T|t)(C|c)(H|h)(A|a)(R|r)/', $instruction)){
             $newInstruction = new XMLInstruction('getchar',3);
            }elseif(preg_match('/(S|s)(E|e)(T|t)(C|c)(H|h)(A|a)(R|r)/', $instruction)){
                $newInstruction = new XMLInstruction('setchar',3);
            }else{
                exit(21);
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
                exit(21);
            }
        }elseif($length == 9){
            if(preg_match('/(P|p)(U|u)(S|s)(H|h)(F|f)(R|r)(A|a)(M|m)(E|e)/', $instruction)){
                $newInstruction = new XMLInstruction('pushframe',0);
            }elseif(preg_match('/(J|j)(U|u)(M|m)(P|p)(I|i)(F|f)(N|n)(E|e)(Q|q)/', $instruction)){
                $newInstruction = new XMLInstruction('jumpifneq',3);
            }else{
                exit(21);
            }
        }elseif($length == 11){
            if(preg_match('/(C|c)(R|r)(E|e)(A|a)(T|t)(E|e)(F|f)(R|r)(A|a)(M|m)(E|e)/',$instruction)){
                $newInstruction = new XMLInstruction('createframe',0);
            }else{
                exit(21);
            }
        }else{
            exit(21);
        }
        return $newInstruction;
    }
}
?>