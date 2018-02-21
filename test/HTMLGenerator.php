<?php

Class HTMLGenerator{
    private $style;
    private $script;
    private $head;
    private $textElements = [];
    private $table= [];
    private $body;
    private $span;

    function __construct(){
        $this->setHead();
        $this->setScript();
        $this->setStyle();
        $this->setBody();
        $this->setSpan();        
    }

    function setHead(){
        $this->head = "<!DOCTYPE html> <html> <head> <title>Page Title</title> <meta charset=\"UTF-8\"> <meta name=\"description\" content=\"Tests\"> <meta name=\"author\" content=\"Marek Kukucka, xkukuc04, 2BIT\"> </head>";
    }

    function setScript(){
        $this->script = "<script>var cur=document.getElementById(\"mySelect\").value;var table=document.getElementById(\"myTable\");var tr=table.getElementsByTagName(\"tr\");var visible='all';var isShowing=false;var outputs=\"\";var lastName=\"\";show();function filter(){this.cur=document.getElementById(\"mySelect\").value;show()}function show(){for(i=0;i<tr.length;i++){td=tr[i].getElementsByTagName(\"td\")[1].innerText;if(td===\"PASSED\"&&this.cur===\"passed\"){tr[i].style.display=\"\"}else if(td===\"FAILED\"&&this.cur===\"failed\"){tr[i].style.display=\"\"}else if(this.cur===\"all\"){tr[i].style.display=\"\"}else{tr[i].style.display=\"none\"}}}function showMore(name,status){if(this.isShowing){if(name===this.lastName){for(i=0;i<outputs.length;i++){this.outputs[i].style.display=\"none\"}this.isShowing=false;this.outputs=\"\";showInfo(\"\",\"\")}else{for(i=0;i<outputs.length;i++){this.outputs[i].style.display=\"none\"}this.lastName=name;this.outputs=document.getElementsByClassName(name);for(i=0;i<outputs.length;i++){this.outputs[i].style.display=\"\"}showInfo(name,status)}}else{this.lastName=name;this.outputs=document.getElementsByClassName(name);for(i=0;i<outputs.length;i++){this.outputs[i].style.display=\"\"}this.isShowing=true;showInfo(name,status)}}function showInfo(name,status){document.getElementById(\"info-name\").innerText=name;document.getElementById(\"info-status\").innerHTML=status;if(status===\"FAILED\"){document.getElementById(\"info-status\").setAttribute(\"class\",\"fail\")}else{document.getElementById(\"info-status\").setAttribute(\"class\",\"pass\")}}</script>";
    }

    function setStyle(){
        $this->style = "<style> #myTable { border-collapse: collapse; border: 1px solid #ddd; font-size: 16px; } .myTr{ border-bottom: 1px solid #ddd; } .pass{ color: green; } .fail{ color: red; } .myTd{ padding-right: 25px; } #info-name{ font-size: 18px; padding-left: 15px; padding-right: 25px; } #info-status{ font-size: 18px; } </style>";
    }

    function setBody(){
        $this->body = "<body> <h1>Tester</h1> <div>Choose tests: <select id=\"mySelect\" onchange=\"filter()\"> <option value=\"all\" selected=\"selected\">All</option> <option value=\"passed\">Passed</option> <option value=\"failed\">Failed</option> </select> <h2>Test result/s</h2> </div> <table id=\"myTable\">";
    }

    function setSpan(){
        $this->span="</table> <p> <span id=\"info-name\"></span> <span id=\"info-status\"></span> </p>";
    }
}

?>

