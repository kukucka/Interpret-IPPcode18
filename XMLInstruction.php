<?php

class XMLInstruction{
    private $name;
    private $numOfArguments;

    function __construct($name, $numOfArguments){
        $this->name = $name;
        $this->numOfArguments = $numOfArguments;
    }

    function getName(){
        return $this->name;
    }

    function getNumOfArguments(){
        return $this->numOfArguments;
    }

}

?>