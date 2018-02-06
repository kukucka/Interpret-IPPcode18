<?php

class XMLArgument{
    private $type;
    private $value;
    private $position;

    function __construct($type, $value, $position){
        $this->type = $type;
        $this->value = $value;
        $this->position = $position;
    }

    function getType(){
        return $this->type;
    }

    function getValue(){
        return $this->value;
    }

    function getPosition(){
        return $this->position;
    }
}


?>