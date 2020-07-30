function update(json){
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
                imgdiv.setAttribute("src", "../images/gray_back.png");
                imgdiv.setAttribute("alt", " ");
                imgdiv.setAttribute("class", "card");
                playercards.getElementsByClassName("cardWrapper")[playercards.getElementsByClassName("cardWrapper").length-1].appendChild(imgdiv);
                console.log("add");
            }
        } else if (diff < 0){
            for (j=0; j < Math.abs(diff); j++){
                playercards.getElementsByClassName("cardWrapper")[0].remove();
                console.log("remove");
            }
        }

        if (cardnumber_new != 0){
            playercards.getElementsByClassName("cardWrapper")[0].classList.add("firstcard");
            playercards.getElementsByClassName("cardWrapper")[playercards.getElementsByClassName("cardWrapper").length - 1].classList.add("lastcard");
        }
        console.log("next");

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
            imgdiv.setAttribute("src", "../images/cards/"+String(mycards_new[i])+".png");
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

function ask() {
    document.getElementsByClassName("askbox")[0].style.display = "block";
}
