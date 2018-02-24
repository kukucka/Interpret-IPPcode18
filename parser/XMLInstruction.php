<?php

/**
 * Class XMLInstruction
 * slouzi k reprezentaci jednotlivych instrukci
 * jednotlive instance tridy obsahuji jmeno instrukce
 * a pocet jejich argumentu
 */
class XMLInstruction{
    private $name;
    private $numOfArguments;

    /**
     * XMLInstruction constructor.
     * @param $name - jmeno instrukce
     * @param $numOfArguments - pocet argumentu
     */
    function __construct($name, $numOfArguments){
        $this->name = $name;
        $this->numOfArguments = $numOfArguments;
    }

    /**
     * @return $name
     * vrati jmeno instrukce
     */
    function getName(){
        return $this->name;
    }

    /**
     * @return $numberOfArgumets
     * vrati pocet argumentu instrukce
     */
    function getNumOfArguments(){
        return $this->numOfArguments;
    }

}

?>