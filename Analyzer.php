<?php
//naimplementovat ignorovani komentaru
Class Analyzer{
    private $multiLineComent = false;

    function getInput(){
        $line = fgets(STDIN);
        $arrayOfWords = preg_split('/((^\p{P}+)|(\p{P}*\s+\p{P}*)|(\p{P}+$))/', $line, -1, PREG_SPLIT_NO_EMPTY);
        return $arrayOfWords;
    }

    function startLoading(){
        $condition = true;
        while($condition){
            $arrayOfWords = $this->getInput();
            // foreach($arrayOfWords as $word){
            //     print "$word\n";
            // }
            $instruction = $this->analyzeInstruction($arrayOfWords[0]);
            // $arrayOfArguments = $this->analyzeArguments($arrayOfWords);
        }
    }

    function analyzeInstruction($instruction){
        $length = strlen($instruction);
        if($length == 2){
            if(preg_match('/(A|a)(D|d)(D|d)/',$instruction)){
                $newInstruction = new XMLInstruction('add',3);
            }
        }elseif($length == 3){               
            if(preg_match('/(A|a)(D|d)(D|d)/',$instruction)){
                $newInstruction = new XMLInstruction('add',3);
            }elseif(preg_match('/(S|s)(U|u)(B|b)/', $instruction)){
                $newInstruction = new XMLInstruction('sub',3);    
            }elseif(preg_match('/(M|m)(U|u)(L|l)/', $instruction)){
                $newInstruction = new XMLInstruction('mul',3);    
            }
        }

        return $newInstruction;
    }

   
}


?>