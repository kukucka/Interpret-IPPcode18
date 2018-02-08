<?php

class XMLCreator{
    static private $counter;
    private $xw;
    function __construct(){
        self::$counter = 1;
        $this->xw = xmlwriter_open_memory();       
    }

    function initiateXML(){
        xmlwriter_start_document($this->xw, '1.0', 'UTF-8');
        xmlwriter_set_indent($this->xw, 1);#druhy argument je boolovska hodnota, ktera ovlada pristup do XML
        xmlwriter_start_element($this->xw, 'program');
        xmlwriter_start_attribute($this->xw, 'language');
        xmlwriter_text($this->xw, 'IPPcode18');
        xmlwriter_end_attribute($this->xw);
    }

    function endXML(){
        xmlwriter_end_element($this->xw);        
        xmlwriter_end_document($this->xw);
        echo xmlwriter_output_memory($this->xw);
    
    }

    private function newInstruction($instruction){
        xmlwriter_start_element($this->xw, 'instruction');
        xmlwriter_start_attribute($this->xw, 'order');
        xmlwriter_text($this->xw, self::$counter);
        xmlwriter_end_attribute($this->xw);
        xmlwriter_start_attribute($this->xw, 'opcode'); 
        xmlwriter_text($this->xw, strtoupper($instruction->getName())); // mozna vraci navratovou hodnotu, nemusi to nic udelat
        xmlwriter_end_attribute($this->xw);
        self::$counter++;
    }

    private function endInstruction($instruction){
        xmlwriter_end_element($this->xw);
    }

    private function newArgument($argument){
        xmlwriter_start_element($this->xw, 'arg' . $argument->getPosition());
        xmlwriter_start_attribute($this->xw, 'type');
        xmlwriter_text($this->xw,$argument->getName());
        xmlwriter_end_attribute($this->xw);
        xmlwriter_text($this->xw, $argument->getValue());
        xmlwriter_end_element($this->xw);
    }
    //presunout jinam
//////////////TEST/////////////////////////////////////
//Prejmenovat !!!! 
    function createArguments($instruction, $arrayOfArguments){
        $this->newInstruction($instruction);
        $count = count($arrayOfArguments);
        if(($instruction->getNumOfArguments()) != $count){
            fprintf(STDERR, "Syntaktick2 chyba?!");
            exit(2);
        }
        if($count == 0){
        }
        elseif($count == 1){
            $this->newArgument($arrayOfArguments[0]);
        }elseif($count == 2){
            $this->newArgument($arrayOfArguments[0]);
            $this->newArgument($arrayOfArguments[1]);
        }elseif($count == 3){
            $this->newArgument($arrayOfArguments[0]);
            $this->newArgument($arrayOfArguments[1]);
            $this->newArgument($arrayOfArguments[2]);
        }else{
            fprintf(STDERR, "Syntakticka chyba?!");
            exit(2);
        }

        $this->endInstruction($instruction);
    }
/////////////////////////////////////////////////////////////////

    function test(){

    }

}
