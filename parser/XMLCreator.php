<?php

/**
 * Class XMLCreator
 * Slouzi k vytvoreni vysledneho vystupu ktery bude ve formatu XML
 */
class XMLCreator{
    static private $counter;
    private $xmlDocument;

    /**
     * XMLCreator constructor.
     * provede se inicializace pocitadla a xml dokumentu
     */
    function __construct(){
        self::$counter = 1;
        $this->xmlDocument = xmlwriter_open_memory();
    }

    /**
     * Provede zakladní nastaeni XML dokumentu
     */
    function initiateXML(){
        xmlwriter_start_document($this->xmlDocument, '1.0', 'UTF-8');
        xmlwriter_set_indent($this->xmlDocument, 1);#druhy argument je boolovska hodnota, ktera ovlada pristup do XML
        xmlwriter_start_element($this->xmlDocument, 'program');
        xmlwriter_start_attribute($this->xmlDocument, 'language');
        xmlwriter_text($this->xmlDocument, 'IPPcode18');
        xmlwriter_end_attribute($this->xmlDocument);
    }

    /**
     * Ukonci tvorbu xml souboru a vysise jej na vystup
     */
    function endXML(){
        xmlwriter_end_element($this->xmlDocument);
        xmlwriter_end_document($this->xmlDocument);
        echo xmlwriter_output_memory($this->xmlDocument);
    
    }

    /**
     * @param $instruction
     * Prevede instrukci do formatu XML
     */
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

    /**
     * @param $instruction
     * ukonci instrukci danou instrukci
     */
    private function endInstruction($instruction){
        xmlwriter_end_element($this->xmlDocument);
    }

    /**
     * @param $argument
     * prevede argument instrukce do formatu XML
     */
    private function newArgument($argument){
        xmlwriter_start_element($this->xmlDocument, 'arg' . $argument->getPosition());
        xmlwriter_start_attribute($this->xmlDocument, 'type');
        xmlwriter_text($this->xmlDocument,$argument->getName());
        xmlwriter_end_attribute($this->xmlDocument);
        xmlwriter_text($this->xmlDocument, $argument->getValue());
        xmlwriter_end_element($this->xmlDocument);
    }

    /**
     * @param $instruction
     * @param $arrayOfArguments - pole argumentu dane instrukce
     * provede prevod jedne instrukce a jejich argumentu z jazyka IPPcode18
     * do jazyka symbolickych instrukci
     */
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
