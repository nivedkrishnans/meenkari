//code for displaying the time since last update
var lastUpdated = document.getElementById("lastUpdated");
var last_timestamp = new Date();
console.log("ls",last_timestamp);
var timestamp_display = setInterval(function(){
    now = new Date();
    //console.log("ls",last_timestamp);
    diff = Math.round((now - last_timestamp)/1000);
    //if(diff > 600) location.reload();
    lastUpdated.innerHTML = time_sec(diff) + " ago";
},1000);




function update(json){
    // this function takes data in the format '{"player1" : [64,24,84,46,22,15,25], "player2" : 2,"player3" : 6,"player4" : 8,"player5" : 15,"player6" : 3}'
    // it updates the cards on the screen, without considering the actul player numbers, but their positions  on the screen
    // the positions are 1 for the current player, and 2 to 6 are the players clockwise from the current player
    var updatedata=JSON.parse(json);

    var cardnumber_old = [];
    var cardnumber_new = [];

    for (i=2; i<7; i++){

        var playercards = document.getElementsByClassName("player"+String(i))[0].getElementsByClassName('cardbox')[0];
        cardnumber_old[cardnumber_old.length] = playercards.getElementsByClassName("cardWrapper").length;
        eval("cardnumber_new[cardnumber_new.length] = updatedata.player"+i+";");

        var diff = cardnumber_new[i-2] - cardnumber_old[i-2];
        if (diff > 0){
            for (j=0; j<diff; j++){
                var newdiv = document.createElement("div");
                newdiv.setAttribute("class", "cardWrapper")
                playercards.appendChild(newdiv);
                var imgdiv = document.createElement("img");
                imgdiv.setAttribute("src", "../static/images/gray_back.png");
                imgdiv.setAttribute("alt", " ");
                imgdiv.setAttribute("class", "card");
                playercards.getElementsByClassName("cardWrapper")[playercards.getElementsByClassName("cardWrapper").length-1].appendChild(imgdiv);

            }
        } else if (diff < 0){
            for (j=0; j < Math.abs(diff); j++){
                playercards.getElementsByClassName("cardWrapper")[0].remove();

            }
        }

        if (cardnumber_new != 0){
            playercards.getElementsByClassName("cardWrapper")[0].classList.add("firstcard");
            playercards.getElementsByClassName("cardWrapper")[playercards.getElementsByClassName("cardWrapper").length - 1].classList.add("lastcard");
        }


    }

    mycardbox = document.getElementsByClassName("player1")[0].getElementsByClassName("cardbox")[0];

    mycards_new = updatedata.player1;
    mycards_old = [];

    for (i=0; i < mycardbox.getElementsByClassName("cardWrapper").length; i++){
        mycards_old[mycards_old.length] = parseInt(mycardbox.getElementsByClassName("cardWrapper")[i].id);
    }

    for (i=0; i < mycards_old.length; i++){
        if (!(mycards_new.includes(mycards_old[i]))){
            document.getElementById(String(mycards_old[i])).remove();
        }
    }

    for (i=0; i < mycards_new.length; i++){
        if (!(mycards_old.includes(mycards_new[i]))){
            var newdiv = document.createElement("div");
            newdiv.setAttribute("class", "cardWrapper");
            newdiv.id = String(mycards_new[i]);
            mycardbox.appendChild(newdiv);
            var imgdiv = document.createElement("img");
            imgdiv.setAttribute("src", "../static/images/cards/"+String(mycards_new[i])+".png");
            imgdiv.setAttribute("alt", " ");
            imgdiv.setAttribute("class", "card");
            mycardbox.getElementsByClassName("cardWrapper")[mycardbox.getElementsByClassName("cardWrapper").length-1].appendChild(imgdiv);
        }
    }

    if (mycards_new.length != 0){
        mycardbox.getElementsByClassName("cardWrapper")[0].classList.add("firstcard");
        mycardbox.getElementsByClassName("cardWrapper")[mycardbox.getElementsByClassName("cardWrapper").length - 1].classList.add("lastcard");
    }

    return [mycards_old, mycards_new];
}


function refresh_cards(){
  //this function takes the value of game_status_json and updates the cards using the update()
  //prior to calling the update() function, it arranges it into the format required
  //this function converts cards information from the back-end player numbering system to the front-end numbering
  var game_status = JSON.parse(game_status_json);
  var game_info = JSON.parse(game_info_json);
  var my = game_status["my"];
  var my_cards = my[1];
  if (my_cards.length != 0) { my_cards = my_cards.substring(0,my_cards.length-1);}
  my_cards = my_cards.split(',');
  var temp = {"player1" : my_cards,}

  for(var i=1; i<7; i++){
    j = (i+my[0]-2)%6;
    if(i>1){
        temp["player" + i] = game_status["hl"][j];
    }
    document.querySelector(".player" + (i) + " .playercardno").innerHTML = game_status["hl"][j];
    document.querySelector(".player" + (i) + " .playerboxh").innerHTML = game_info["pl"][j];
    if(game_info["pl"][j] ==  game_status["p0"]){
        //current player indicator
        document.querySelector(".player" + (i) + " .playerboxh").classList.add("playernow");
    }
    else{
        document.querySelector(".player" + (i) + " .playerboxh").classList.remove("playernow");
    }
  }

  document.getElementById('log_temp').innerHTML = game_status["me"];

  document.getElementById('gameName').innerHTML = game_info["na"];
  document.getElementById('team1score').innerHTML = game_status["te"][0];
  document.getElementById('team2score').innerHTML = game_status["te"][1];
  last_timestamp = new Date(game_status["ts"]*1000);
  temp= JSON.stringify(temp);
  // console.log("update text = " +temp);
  update(temp);

  try{
    //audio1.play();
  }
  catch{
      console.log("Could not play audio");
  }

  document.getElementById('currentPlayer').innerHTML = game_status["p0"]
  document.getElementById('teamName').innerHTML = (parseInt(game_status["my"][0])+1)%2 +1;
  
  console.log("Refresh Initiated", game_status["ts"], last_timestamp, temp);
  //return temp;
}


// script to pop up askbox and declbox
var askbutton = document.getElementsByClassName("askbutton")[0];
var askbox = document.getElementsByClassName("askbox")[0];
var declbutton = document.getElementsByClassName("declbutton")[0];
var declbox = document.getElementsByClassName("declbox")[0];
var container = document.getElementsByClassName("container")[0];

askbutton.onclick = function() {
    askbox.style.display = "block";
    declbox.style.display = "none";
    ask();
}



declbutton.onclick = function() {
    declbox.style.display = "block";
    askbox.style.display = "none";
    declare();
}



// window,onclick = function(event) {
//     if (event.target == askbox){
//         console.log("inside box");
//     } else {
//         if (event.target == askbutton){
//             console.log("inside button");
//         } else {
//             askbox.style.display = "none";
//             console.log("hidden");
//         }
//     }
// }

var askclose = askbox.getElementsByClassName("close")[0];
askclose.onclick = function() {
    askbox.style.display = "none";
    declbox.style.display = "none";
}

var declclose = declbox.getElementsByClassName("close")[0];
declclose.onclick = function() {
    askbox.style.display = "none";
    declbox.style.display = "none";
}


//  The follwing function is triggered upon clinking the ask button and
// it creates a JSON in a global varibale called send_data which can be
// sent to server.
function ask() {
    var game_status = JSON.parse(game_status_json);
    var game_info = JSON.parse(game_info_json);
    var formbox = askbox.getElementsByClassName("formbox")[0];
    var askform = formbox.getElementsByClassName("askform");

    if(askform.length != 0){
        askform[0].remove();
    }


    var oppteam = [];

    for(i=0; i<3 ; i++){
        j=(game_status.my[0]+(2*i))%6;
        oppteam[i] = game_info.pl[j];
    }

    var my_suits = findmysuits(game_status.my[1]);


    var askform = document.createElement("form");
    askform.setAttribute("class", "askform");
    formbox.appendChild(askform);

    var askform = formbox.getElementsByClassName("askform")[0];

    var head1 = document.createElement("label");
    head1.innerHTML = "Select a player to ask to"+"<br>";
    askform.appendChild(head1);

    for(i=0; i<oppteam.length; i++){
        var input = document.createElement("input");
        input.setAttribute("type", "radio");
        input.setAttribute("id", oppteam[i]);
        input.setAttribute("name", "toplayer");
        input.setAttribute("value", oppteam[i]);
        askform.appendChild(input);

        var label = document.createElement("label");
        label.setAttribute("for", oppteam[i]);
        label.innerHTML = oppteam[i];
        askform.appendChild(label);
    }

    var head2 = document.createElement("label");
    head2.innerHTML = "Select suit"+"<br>";
    head2.setAttribute("style", "display : block")
    head2.setAttribute("for", "suit");
    askform.appendChild(head2);

    var suitselect = document.createElement("select");
    suitselect.setAttribute("id", "asksuit");
    suitselect.setAttribute("name", "suit");
    suitselect.setAttribute("onchange", "showcardlist(this.value)")
    askform.appendChild(suitselect);

    suitselect = document.getElementById("asksuit");

    for(i=0; i<my_suits.length; i++){
        var option = document.createElement("option");
        option.setAttribute("value", my_suits[i]);
        option.innerHTML = suitlist[my_suits[i]];
        suitselect.appendChild(option);
    }

    var head3 = document.createElement("label");
    head3.innerHTML = "Select card"+"<br>";
    head3.setAttribute("style", "display : block")
    askform.appendChild(head3);


    askform.addEventListener("submit", handleFormSubmit);

}

// This function returns what are the suits in a string of card number given in
// an array.
function findmysuits(my_cards){
    if (my_cards.length != 0) { my_cards = my_cards.substring(0,my_cards.length-1);}
    my_cards = my_cards.split(',');

    my_suits = [];

    for(j=0; j<my_cards.length; j++) {
            if (!(my_suits.includes(my_cards[j][0]))){
                my_suits.push(my_cards[j][0])
            }
    }

    return my_suits;

}

// This function selectively creates the list of cards for asking
// according to the suit selected for asking.
function showcardlist(value){

    var askform = askbox.getElementsByClassName("askform")[0];
    var askcardlist = askform.getElementsByClassName("askcardlist");

    // console.log(askcardlist);

    if(askcardlist.length != 0){
        lmax = askcardlist.length;
        for(l=0; l<lmax; l++){
            askcardlist[0].remove();
        }
    }



    for(j=1; j<7; j++){
            var card = document.createElement("input");
            card.setAttribute("type", "radio");
            card.setAttribute("name", "askcard");
            card.setAttribute("value", value+String(j));
            card.setAttribute("onchange", "showask()");
            card.setAttribute("class", "askcardlist");
            askform.appendChild(card);

            var label = document.createElement("label");
            label.setAttribute("for", value+String(j));
            label.setAttribute("class", "askcardlist");
            label.innerHTML = cardlist[value+String(j)];
            askform.appendChild(label);
    }
}

// This function shows the ask button after card is selected.
function showask(){

    var askform = askbox.getElementsByClassName("askform")[0];
    var asksubmit = askform.getElementsByClassName("asksubmit");

    if(asksubmit.length != 0){
        asksubmit[0].remove();
    }


    var submit = document.createElement("input");
    submit.setAttribute("type", "submit");
    submit.setAttribute("value", "ask");
    submit.setAttribute("name", "action")
    submit.setAttribute("class", "asksubmit");
    submit.setAttribute("style", "display : block");
    askform.appendChild(submit);
}

var suitlist = {
    "1" : "8's and Jokers" ,
    "2" : "Higher Spades",
    "3" : "Higher Diamonds",
    "4" : "Higher Clubs",
    "5" : "Higher Hearts",
    "6" : "Lower Spades",
    "7" : "Lower Diamonds",
    "8" : "Lower Clubs",
    "9" : "Lower Hearts"
};

var cardlist = makecardlist();

// This function makes the cardlist object which gives relation between
// the card numbers and its actual names.
function makecardlist(){
    var cardlist = {
        "11" : "Black Joker",
        "12" : "8 of Spades",
        "13" : "8 of Diamonds",
        "14" : "8 of Clubs",
        "15" : "8 of Hearts",
        "16" : "White Joker",
    };

    lower = ["2", "3", "4", "5", "6", "7"];
    higher = ["9", "10", "Jack", "Queen", "King", "Ace"];
    suit = ["Spades", "Diamonds", "Clubs", "Hearts"];

    for(i=0; i<4; i++){
        for(j=0; j<6; j++){
            cardlist[String(i+2)+String(j+1)] = higher[j]+" of "+suit[i];
        }
    }

    for(i=0; i<4; i++){
        for(j=0; j<6; j++){
            cardlist[String(i+6)+String(j+1)] = lower[j]+" of "+suit[i];
        }
    }

    return cardlist;
}

// This function converts the form to JSON
const formtoJSON = elements => [].reduce.call(elements, (data, element) => {

    if(isValidValue(element)){
        data[element.name] = element.value;
    }
    return data;

},{});

// This function prevents the default action of form submit button and
// instead makes the contents of the form into a JSON
const handleFormSubmit = event => {

    askform = document.getElementsByClassName("askform")[0];
    event.preventDefault();
    data = formtoJSON(askform.elements);
    console.log(data);
    send_data = JSON.stringify(data);
    valet(send_data);
    askform.remove();
    askbox.style.display = "none";
}

// THis function makes sure that only the checked radio buttons'
// value appear in the final JSON.
const isValidValue = element => {
    return (!['checkbox', 'radio'].includes(element.type) || element.checked);
}

//  The follwing function is triggered upon clinking the ask button and
// it creates a JSON in a global varibale called send_data which can be
// sent to server.
function declare() {
    var game_status = JSON.parse(game_status_json);
    var game_info = JSON.parse(game_info_json);
    var formbox = declbox.getElementsByClassName("formbox")[0];
    var declform = formbox.getElementsByClassName("declform");

    if(declform.length != 0){
        declform[0].remove();
    }


    var declsuits = game_status["te"][0]+game_status["te"][1]
    if (declsuits.length != 0) { declsuits = declsuits.substring(0,declsuits.length-1);}
    declsuits = declsuits.split(',');
    allsuits = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    declsuits = _.difference(allsuits, declsuits)

    var declform = document.createElement("form");
    declform.setAttribute("class", "declform");
    formbox.appendChild(declform);

    var declform = formbox.getElementsByClassName("declform")[0];

    var head1 = document.createElement("label");
    head1.innerHTML = "Select the team to declare the suit for "+"<br>";
    declform.appendChild(head1);

    for(i=1; i<3; i++){
        var input = document.createElement("input");
        input.setAttribute("type", "radio");
        input.setAttribute("id", "team"+String(i));
        input.setAttribute("name", "for team");
        input.setAttribute("value", "team"+String(i));
        input.setAttribute("onchange", "finddeclteam()")
        declform.appendChild(input);

        var label = document.createElement("label");
        label.setAttribute("for", "team"+String(i));
        label.innerHTML = "Team "+String(i);
        declform.appendChild(label);
    }

    var head2 = document.createElement("label");
    head2.innerHTML = "Select suit"+"<br>";
    head2.setAttribute("style", "display : block")
    head2.setAttribute("for", "suit");
    declform.appendChild(head2);

    var suitselect = document.createElement("select");
    suitselect.setAttribute("id", "declsuit");
    suitselect.setAttribute("name", "suit");
    suitselect.setAttribute("onchange", "showcardlist_decl(this.value)")
    declform.appendChild(suitselect);

    suitselect = document.getElementById("declsuit");

    for(i=0; i<declsuits.length; i++){
        var option = document.createElement("option");
        option.setAttribute("value", declsuits[i]);
        option.innerHTML = suitlist[declsuits[i]];
        suitselect.appendChild(option);
    }

    // var head3 = document.createElement("label");
    // head3.innerHTML = "Select card"+"<br>";
    // head3.setAttribute("style", "display : block")
    // askform.appendChild(head3);


    declform.addEventListener("submit", handleFormSubmit_decl);

}

var declteam = ""

function finddeclteam(){
    radio = document.getElementsByName("for team");
    for(i=0; i<radio.length; i++){
        if(radio[i].checked){
            declteam = radio[i].value;
        }
    }
}


function showcardlist_decl(value){
    var game_info = JSON.parse(game_info_json);
    var declform = declbox.getElementsByClassName("declform")[0];
    var declcardlist = declform.getElementsByClassName("declcardlist");

    // console.log(askcardlist);

    if(declcardlist.length != 0){
        lmax = declcardlist.length;
        for(l=0; l<lmax; l++){
            declcardlist[0].remove();
        }
    }

    pl = game_info["pl"];
    team1 = [pl[0], pl[2], pl[4]];
    team2 = [pl[1], pl[3], pl[5]];

    if(declteam == "team1") {team = team1;}
    if(declteam == "team2") {team = team2;}

    for(j=1; j<7; j++){
        var head3 = document.createElement("label");
        head3.innerHTML = cardlist[value+String(j)]+"<br>";
        head3.setAttribute("style", "display : block");
        head3.setAttribute("class", "declcardlist");
        declform.appendChild(head3);

        for(k=0; k<3; k++){
            var card = document.createElement("input");
            card.setAttribute("type", "radio");
            card.setAttribute("name", "card"+String(j));
            card.setAttribute("value", team[k]);
            card.setAttribute("onchange", "showdecl()");
            card.setAttribute("class", "declcardlist");
            card.setAttribute("required", "required")
            declform.appendChild(card);

            var label = document.createElement("label");
            label.setAttribute("for", team[k]);
            label.setAttribute("class", "declcardlist");
            label.innerHTML = team[k];
            declform.appendChild(label);
        }
    }
}


function showdecl(){

    var declform = declbox.getElementsByClassName("declform")[0];
    var declsubmit = declform.getElementsByClassName("declsubmit");

    if(declsubmit.length != 0){
        declsubmit[0].remove();
    }


    var submit = document.createElement("input");
    submit.setAttribute("type", "submit");
    submit.setAttribute("value", "declare");
    submit.setAttribute("name", "action")
    submit.setAttribute("class", "declsubmit");
    submit.setAttribute("style", "display : block");
    declform.appendChild(submit);
}

const handleFormSubmit_decl = event => {

    declform = document.getElementsByClassName("declform")[0];
    event.preventDefault();
    data = formtoJSON(declform.elements);
    console.log(data);
    send_data = JSON.stringify(data);
    valet(send_data);
    declform.remove();
    declbox.style.display = "none";
}
