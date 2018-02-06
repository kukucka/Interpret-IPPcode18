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
        xmlwriter_start_attribute($this->xw, 'opcode');
        xmlwriter_text($this->xw, 'IPPcode18');
        xmlwriter_end_attribute($this->xw, 'opcode');
        echo xmlwriter_output_memory($this->xw);
        print "\n";
    }

    function endXML(){
        xmlwriter_end_element($this->xw, 'program');        
        xmlwriter_end_document($this->xw);
        
    }

    function createInstruction(){

    }

    function argumentType(){
    }

    private function typeCheck(){

    }

    //pak poresit napriklad nejaky znaku co tam nejdou v XML

    function test(){

    }

}
