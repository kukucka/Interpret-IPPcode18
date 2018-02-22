<?php
//TODO boool testovani obsahu?
class XMLArgument{
    private $name;
    private $value;
    private $position;
    private $type;

    function __construct($name, $value, $position){
        $this->name = $name;
        $this->value = $value;
        $this->position = $position;
        $this->setType();
    }

    private function setType(){
        if($this->name == "label"){
            $this->type = "label";
        }elseif($this->name == "bool" || $this->name == "string" ||
        $this->name == "int"){
            $this->type = "constant";
        }elseif($this->name == "var"){
            $this->type = "variable";
        }elseif($this->name == "type"){
            $this->type = "type";
        }else{
            exit(21);
        }
    }

    function getName(){
        return $this->name;
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