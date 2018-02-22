<?php

class XMLCreator{
    static private $counter;
    private $xmlDocument;
    function __construct(){
        self::$counter = 1;
        $this->xmlDocument = xmlwriter_open_memory();
    }

    function initiateXML(){
        xmlwriter_start_document($this->xmlDocument, '1.0', 'UTF-8');
        xmlwriter_set_indent($this->xmlDocument, 1);#druhy argument je boolovska hodnota, ktera ovlada pristup do XML
        xmlwriter_start_element($this->xmlDocument, 'program');
        xmlwriter_start_attribute($this->xmlDocument, 'language');
        xmlwriter_text($this->xmlDocument, 'IPPcode18');
        xmlwriter_end_attribute($this->xmlDocument);
    }

    function endXML(){
        xmlwriter_end_element($this->xmlDocument);
        xmlwriter_end_document($this->xmlDocument);
        echo xmlwriter_output_memory($this->xmlDocument);
    
    }

    private function newInstruction($instruction){
        xmlwriter_start_element($this->xmlDocument, 'instruction');
        xmlwriter_start_attribute($this->xmlDocument, 'order');
        xmlwriter_text($this->xmlDocument, self::$counter);
        xmlwriter_end_attribute($this->xmlDocument);
        xmlwriter_start_attribute($this->xmlDocument, 'opcode');
        xmlwriter_text($this->xmlDocument, strtoupper($instruction->getName())); // mozna vraci navratovou hodnotu, nemusi to nic udelat
        xmlwriter_end_attribute($this->xmlDocument);
        self::$counter++;
    }

    private function endInstruction($instruction){
        xmlwriter_end_element($this->xmlDocument);
    }

    private function newArgument($argument){
        xmlwriter_start_element($this->xmlDocument, 'arg' . $argument->getPosition());
        xmlwriter_start_attribute($this->xmlDocument, 'type');
        xmlwriter_text($this->xmlDocument,$argument->getName());
        xmlwriter_end_attribute($this->xmlDocument);
        xmlwriter_text($this->xmlDocument, $argument->getValue());
        xmlwriter_end_element($this->xmlDocument);
    }

    function createArguments($instruction, $arrayOfArguments){
        $this->newInstruction($instruction);
        $count = count($arrayOfArguments);
        if(($instruction->getNumOfArguments()) != $count){
            exit(21);
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
            exit(21);
        }

        $this->endInstruction($instruction);
    }

}
