<?php
class XMLCreator{
    static private $counter;
    private $xw;
    function __construct(){
        self::$counter = 1;
        $this->xw = xmlwriter_open_memory();       
    }

    function lol(){
        echo self::$counter;        
        $numOfOranges = 4;
        echo $numOfOranges;
        self::$counter++;
        echo self::$counter;
    }

    function initiateXML(){
        xmlwriter_start_document($this->xw, '1.0', 'UTF-8');
        xmlwriter_set_indent($this->xw, 1);#druhy argument je boolovska hodnota, ktera ovlada pristup do XML
        xmlwriter_start_element($this->xw, 'program');
        xmlwriter_start_attribute($this->xw, 'language');
        xmlwriter_text($this->xw, 'IPPcode18');
        xmlwriter_end_attribute($this->xw, 'language');
    }

    function endXML(){
        xmlwriter_end_element($this->xw, 'program');        
        xmlwriter_end_document($this->xw);
        echo xmlwriter_output_memory($this->xw);
    
    }

    function newInstruction($instruction){
        xmlwriter_start_element($this->xw, $instruction);
        xmlwriter_start_attribute($this->xw, 'order');
        xmlwriter_text($counter);
        xmlwriter_end_attribute($this->xw, 'order');
        xmlwriter_start_attribute($this->xw, 'opcode'); 
        xmlwriter_text(strtoupper($instruction->getName())); // mozna vraci navratovou hodnotu, nemusi to nic udelat
        xmlwriter_end_attribute($this->xw, 'opcode');
        self::$counter++;
    }

    function endInstruction($instruction){
        xmlwriter_end_element($this->xw, $instruction);
    }

    function newArgument($argument){
        xmlwriter_start_element($this->xw, 'arg' . $argument->getPosition());
        xmlwriter_start_attribute($this->xw, 'type');
        xmlwriter_text($argument->getType());
        xmlwriter_end_attribute($this->xw, 'type');
        xmlwriter_text($argument->getValue());
    }
    //presunout jinam
    function createArguments($instruction, $arrayOfArguments){
        $count = count($arrayOfArguments);
        if($numOfArguments != $count){
            fprintf(STDERR, "Syntakticka chyba?!");       
            exit(2);   
        }
        if($count == 1){

        }elseif($count == 2){

        }elseif($count == 3){

        }else{
            fprintf(STDERR, "Syntakticka chyba?!");
            exit(2);        
        }

        endInstruction($instruction);
    }

    //pak poresit napriklad nejaky znaku co tam nejdou v XML

    function test(){

    }

}
