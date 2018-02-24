<?php

/**
 * Class XMLArgument
 * slouzi k reprezentaci argumentu, jednotlivych instrukci
 * jednotlive instance tridy obsahuji jmeno, hodnotu, pozici a
 * typ argumentu
 */

class XMLArgument{
    private $name;
    private $value;
    private $position;
    private $type;

    /**
     * XMLArgument constructor.
     * @param $name - jmeno argumentu
     * @param $value - hodnota argumentu
     * @param $position - pozice argumentu
     */
    function __construct($name, $value, $position){
        $this->name = $name;
        $this->value = $value;
        $this->position = $position;
        $this->setType();
    }

    /**
     * Rozhodne jakeho je argument typu v zavislosti na jeho jmene
     * a priradi jej do promenne type
     */
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

    /**
     * @return $name
     * vrati jmeno argumentu
     */
    function getName(){
        return $this->name;
    }

    /**
     * @return $type
     * vrati typ argumentu
     */
    function getType(){
        return $this->type;
    }

    /**
     * @return $value
     * vrati hodnotu argumentu
     */
    function getValue(){
        return $this->value;
    }

    /**
     * @return $position
     * vrati pozici argumentu
     */
    function getPosition(){
        return $this->position;
    }
}
?>