//code for displaying the time since last update
var lastUpdated = document.getElementById("lastUpdated");
var last_timestamp = new Date();
console.log("ls",last_timestamp);
var timestamp_display = setInterval(function(){
    now = new Date();
    //console.log("ls",last_timestamp);
    diff = Math.round((now - last_timestamp)/1000);
    if(diff > 90) manual_refresh(); // attempts refresh via ajax at 1.5min of no update
    if(diff > 150) location.reload(); // reloads page after 2.5min of no update
    lastUpdated.innerHTML = time_sec(diff) + " ago";
},1000);




function update(json){
    // this function takes data in the format '{"player1" : [64,24,84,46,22,15,25], "player2" : 2,"player3" : 6,"player4" : 8,"player5" : 15,"player6" : 3}'
    // it updates the cards on the screen, without considering the actul player numbers, but their positions  on the screen
    // the positions are 1 for the current player, and 2 to 6 are the players clockwise from the current player
    var updatedata=JSON.parse(json);

    // Stores the old and new card counts for the 5 other players as an array to change the display accordingly
    var cardnumber_old = [];
    var cardnumber_new = [];

    for (i=2; i<7; i++){
        var playercards = document.getElementsByClassName("player"+String(i))[0].getElementsByClassName('cardbox')[0];
        cardnumber_old.push( playercards.getElementsByClassName("cardWrapper").length );
        // Safe property access instead of eval()
        cardnumber_new.push(updatedata["player" + i]);

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

        if (cardnumber_new[i-2] != 0){
            playercards.getElementsByClassName("cardWrapper")[0].classList.add("firstcard");
            playercards.getElementsByClassName("cardWrapper")[playercards.getElementsByClassName("cardWrapper").length - 1].classList.add("lastcard");
        }

        if (cardnumber_new[i-2] == 0){
            playercards.innerHTML = '';
        }


    }

    mycardbox = document.getElementsByClassName("player1")[0].getElementsByClassName("cardbox")[0];

    mycards_new = updatedata.player1;
    console.log("mycards", mycards_new, updatedata);
    mycards_old = [];

    if (mycards_new != 0){
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
    } else {
        mycardbox.innerHTML = '';
    }

    return [mycards_old, mycards_new];
}


function refresh_cards(){
  //this function takes the value of game_status_json and updates the cards using the update()
  //prior to calling the update() function, it arranges it into the format required
  //this function converts cards information from the back-end player numbering system to the front-end numbering
  var game_status = JSON.parse(game_status_json);
    if (game_status["st"] === "over" || game_status["st"] === "stopped") {
        window.location.href = "/gameover/";
        return;
    }
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


// Action Panel UI - Modern Left-Bottom Selector
const actionPanel = document.querySelector(".actionPanel");
const actionClose = document.querySelector(".actionClose");
const actionBody = document.querySelector(".actionBody");
const askbutton = document.querySelector(".askbutton");
const declbutton = document.querySelector(".declbutton");

// Initialize event listeners
askbutton.addEventListener("click", function() {
    showActionPanel("ask");
});

declbutton.addEventListener("click", function() {
    showActionPanel("declare");
});

actionClose.addEventListener("click", function() {
    hideActionPanel();
});

// Close panel on ESC key
document.addEventListener("keydown", function(event) {
    if (event.key === "Escape") {
        hideActionPanel();
    }
});

function showActionPanel(mode) {
    actionPanel.style.display = "block";
    const title = document.querySelector(".actionTitle");
    actionBody.innerHTML = "";
    
    if (mode === "ask") {
        title.textContent = "Ask for a Suit";
        buildAskPanel();
    } else if (mode === "declare") {
        title.textContent = "Declare a Suit";
        buildDeclarePanel();
    }
}

function hideActionPanel() {
    actionPanel.style.display = "none";
    actionBody.innerHTML = "";
}


//  Modern ask panel builder
function buildAskPanel() {
    const game_status = JSON.parse(game_status_json);
    const game_info = JSON.parse(game_info_json);
    
    // Get opponent team (3 players opposite to current player)
    const oppteam = [];
    for (let i = 0; i < 3; i++) {
        const j = (game_status.my[0] + (2 * i)) % 6;
        oppteam[i] = game_info.pl[j];
    }
    
    const my_suits = findmysuits(game_status.my[1]);
    
    // Create form container
    const form = document.createElement("form");
    form.className = "actionForm";
    form.addEventListener("submit", handleAskSubmit);
    
    // Player selection section
    const playerSection = document.createElement("div");
    playerSection.className = "formSection";
    playerSection.innerHTML = `<div class="formSectionLabel">Select Player</div>`;
    const playerChipGroup = document.createElement("div");
    playerChipGroup.className = "chipGroup";
    
    oppteam.forEach(player => {
        const chip = document.createElement("button");
        chip.type = "button";
        chip.className = "chip";
        chip.textContent = player;
        chip.dataset.value = player;
        chip.addEventListener("click", function(e) {
            e.preventDefault();
            document.querySelectorAll(".chipGroup .chip").forEach(c => c.classList.remove("selected"));
            this.classList.add("selected");
            document.getElementById("askPlayer").value = player;
        });
        playerChipGroup.appendChild(chip);
    });
    playerSection.appendChild(playerChipGroup);
    form.appendChild(playerSection);
    
    // Hidden input for selected player
    const playerInput = document.createElement("input");
    playerInput.type = "hidden";
    playerInput.id = "askPlayer";
    playerInput.name = "toplayer";
    form.appendChild(playerInput);
    
    // Suit selection section
    const suitSection = document.createElement("div");
    suitSection.className = "formSection";
    suitSection.innerHTML = `<div class="formSectionLabel">Select Suit from Your Hand</div>`;
    const suitSelect = document.createElement("select");
    suitSelect.className = "suitSelect";
    suitSelect.id = "askSuit";
    suitSelect.name = "suit";
    
    const emptyOption = document.createElement("option");
    emptyOption.value = "";
    emptyOption.textContent = "Choose a suit...";
    suitSelect.appendChild(emptyOption);
    
    my_suits.forEach(suit => {
        const option = document.createElement("option");
        option.value = suit;
        option.textContent = suitlist[suit];
        suitSelect.appendChild(option);
    });
    
    suitSelect.addEventListener("change", function() {
        updateAskCards(this.value, form);
    });
    
    suitSection.appendChild(suitSelect);
    form.appendChild(suitSection);
    
    // Card selection section (initially hidden)
    const cardSection = document.createElement("div");
    cardSection.className = "formSection";
    cardSection.id = "askCardSection";
    cardSection.style.display = "none";
    cardSection.innerHTML = `<div class="formSectionLabel">Select Card</div>`;
    const cardGrid = document.createElement("div");
    cardGrid.className = "cardGrid";
    cardGrid.id = "askCardGrid";
    cardSection.appendChild(cardGrid);
    form.appendChild(cardSection);
    
    // Hidden input for selected card
    const cardInput = document.createElement("input");
    cardInput.type = "hidden";
    cardInput.id = "askCard";
    cardInput.name = "askcard";
    form.appendChild(cardInput);
    
    // Submit button
    const submitBtn = document.createElement("button");
    submitBtn.type = "submit";
    submitBtn.className = "actionSubmit";
    submitBtn.textContent = "Ask";
    submitBtn.disabled = true;
    form.appendChild(submitBtn);
    
    actionBody.appendChild(form);
}

function updateAskCards(suitValue, form) {
    const cardSection = document.getElementById("askCardSection");
    const cardGrid = document.getElementById("askCardGrid");
    const cardInput = document.getElementById("askCard");
    const submitBtn = form.querySelector(".actionSubmit");
    
    if (!suitValue) {
        cardSection.style.display = "none";
        cardInput.value = "";
        submitBtn.disabled = true;
        return;
    }
    
    cardSection.style.display = "block";
    cardGrid.innerHTML = "";
    
    for (let j = 1; j < 7; j++) {
        const cardValue = suitValue + String(j);
        const cardBtn = document.createElement("button");
        cardBtn.type = "button";
        cardBtn.className = "cardButton";
        cardBtn.textContent = cardlist[cardValue];
        cardBtn.dataset.value = cardValue;
        cardBtn.addEventListener("click", function(e) {
            e.preventDefault();
            document.querySelectorAll("#askCardGrid .cardButton").forEach(c => c.classList.remove("selected"));
            this.classList.add("selected");
            cardInput.value = cardValue;
            submitBtn.disabled = false;
        });
        cardGrid.appendChild(cardBtn);
    }
}

function handleAskSubmit(event) {
    event.preventDefault();
    
    const playerValue = document.getElementById("askPlayer").value;
    const suitValue = document.getElementById("askSuit").value;
    const cardValue = document.getElementById("askCard").value;
    
    if (!playerValue || !suitValue || !cardValue) {
        console.log("Incomplete form");
        return;
    }
    
    const data = {
        toplayer: playerValue,
        suit: suitValue,
        askcard: cardValue
    };
    
    console.log("Ask submission:", data);
    valet(JSON.stringify(data));
    hideActionPanel();
}

//  Modern declare panel builder
function buildDeclarePanel() {
    const game_status = JSON.parse(game_status_json);
    const game_info = JSON.parse(game_info_json);
    
    // Get available suits (not yet declared)
    let declsuits = game_status["te"][0] + game_status["te"][1];
    if (declsuits.length != 0) { 
        declsuits = declsuits.substring(0, declsuits.length - 1); 
    }
    declsuits = declsuits.split('<br>').filter(Boolean);
    const allsuits = ["1", "2", "3", "4", "5", "6", "7", "8", "9"];
    declsuits = _.difference(allsuits, declsuits);
    
    const pl = game_info["pl"];
    const team1 = [pl[0], pl[2], pl[4]];
    const team2 = [pl[1], pl[3], pl[5]];
    
    // Create form container
    const form = document.createElement("form");
    form.className = "actionForm";
    form.addEventListener("submit", handleDeclareSubmit);
    
    // Team selection section
    const teamSection = document.createElement("div");
    teamSection.className = "formSection";
    teamSection.innerHTML = `<div class="formSectionLabel">Select Team</div>`;
    const teamChipGroup = document.createElement("div");
    teamChipGroup.className = "chipGroup";
    
    ["team1", "team2"].forEach((teamId, idx) => {
        const chip = document.createElement("button");
        chip.type = "button";
        chip.className = "chip";
        chip.textContent = "Team " + (idx + 1);
        chip.dataset.value = teamId;
        chip.addEventListener("click", function(e) {
            e.preventDefault();
            document.querySelectorAll(".teamChipGroup .chip").forEach(c => c.classList.remove("selected"));
            this.classList.add("selected");
            document.getElementById("declTeam").value = teamId;
        });
        teamChipGroup.appendChild(chip);
    });
    teamChipGroup.className = "chipGroup teamChipGroup";
    teamSection.appendChild(teamChipGroup);
    form.appendChild(teamSection);
    
    // Hidden input for selected team
    const teamInput = document.createElement("input");
    teamInput.type = "hidden";
    teamInput.id = "declTeam";
    teamInput.name = "for team";
    form.appendChild(teamInput);
    
    // Suit selection section
    const suitSection = document.createElement("div");
    suitSection.className = "formSection";
    suitSection.innerHTML = `<div class="formSectionLabel">Select Suit to Declare</div>`;
    const suitSelect = document.createElement("select");
    suitSelect.className = "suitSelect";
    suitSelect.id = "declSuit";
    suitSelect.name = "suit";
    
    const emptyOption = document.createElement("option");
    emptyOption.value = "";
    emptyOption.textContent = "Choose a suit...";
    suitSelect.appendChild(emptyOption);
    
    declsuits.forEach(suit => {
        const option = document.createElement("option");
        option.value = suit;
        option.textContent = suitlist[suit];
        suitSelect.appendChild(option);
    });
    
    suitSelect.addEventListener("change", function() {
        updateDeclareCards(this.value, form, team1, team2);
    });
    
    suitSection.appendChild(suitSelect);
    form.appendChild(suitSection);
    
    // Card selection section (initially hidden)
    const cardSection = document.createElement("div");
    cardSection.className = "formSection";
    cardSection.id = "declCardSection";
    cardSection.style.display = "none";
    cardSection.innerHTML = `<div class="formSectionLabel">Select Player for Each Card</div>`;
    const cardContainer = document.createElement("div");
    cardContainer.id = "declCardContainer";
    cardSection.appendChild(cardContainer);
    form.appendChild(cardSection);
    
    // Hidden container for card selections
    const cardInputsContainer = document.createElement("div");
    cardInputsContainer.id = "declCardInputs";
    cardInputsContainer.style.display = "none";
    form.appendChild(cardInputsContainer);
    
    // Submit button
    const submitBtn = document.createElement("button");
    submitBtn.type = "submit";
    submitBtn.className = "actionSubmit";
    submitBtn.textContent = "Declare";
    submitBtn.disabled = true;
    form.appendChild(submitBtn);
    
    actionBody.appendChild(form);
}

function updateDeclareCards(suitValue, form, team1, team2) {
    const cardSection = document.getElementById("declCardSection");
    const cardContainer = document.getElementById("declCardContainer");
    const cardInputsContainer = document.getElementById("declCardInputs");
    const submitBtn = form.querySelector(".actionSubmit");
    
    if (!suitValue) {
        cardSection.style.display = "none";
        cardInputsContainer.innerHTML = "";
        submitBtn.disabled = true;
        return;
    }
    
    cardSection.style.display = "block";
    cardContainer.innerHTML = "";
    cardInputsContainer.innerHTML = "";
    
    // Get selected team
    const teamValue = document.getElementById("declTeam").value;
    let team = teamValue === "team1" ? team1 : team2;
    
    let allCardsSelected = true;
    
    for (let j = 1; j < 7; j++) {
        const cardValue = suitValue + String(j);
        const cardLabel = document.createElement("div");
        cardLabel.style.marginBottom = "12px";
        
        const cardName = document.createElement("div");
        cardName.className = "formSectionLabel";
        cardName.style.marginBottom = "6px";
        cardName.textContent = cardlist[cardValue];
        cardLabel.appendChild(cardName);
        
        const playerChips = document.createElement("div");
        playerChips.className = "chipGroup";
        playerChips.id = `playerGroup${j}`;
        
        team.forEach(player => {
            const chip = document.createElement("button");
            chip.type = "button";
            chip.className = "chip";
            chip.textContent = player;
            chip.dataset.value = player;
            chip.addEventListener("click", function(e) {
                e.preventDefault();
                document.querySelectorAll(`#playerGroup${j} .chip`).forEach(c => c.classList.remove("selected"));
                this.classList.add("selected");
                
                // Store in hidden input
                const hidden = document.getElementById(`declCard${j}`);
                hidden.value = player;
                
                // Check if all cards have selections
                const allInputs = document.querySelectorAll("[id^='declCard']");
                allCardsSelected = Array.from(allInputs).every(inp => inp.value !== "");
                submitBtn.disabled = !allCardsSelected;
            });
            playerChips.appendChild(chip);
        });
        
        cardLabel.appendChild(playerChips);
        cardContainer.appendChild(cardLabel);
        
        // Create hidden input for this card
        const hiddenInput = document.createElement("input");
        hiddenInput.type = "hidden";
        hiddenInput.id = `declCard${j}`;
        hiddenInput.name = `card${j}`;
        cardInputsContainer.appendChild(hiddenInput);
    }
    
    form.appendChild(cardInputsContainer);
    submitBtn.disabled = true; // Initially disabled until all cards selected
}

function handleDeclareSubmit(event) {
    event.preventDefault();
    
    const teamValue = document.getElementById("declTeam").value;
    const suitValue = document.getElementById("declSuit").value;
    
    if (!teamValue || !suitValue) {
        console.log("Incomplete form");
        return;
    }
    
    const data = {
        "for team": teamValue,
        suit: suitValue
    };
    
    // Add all card selections
    const cardInputs = document.querySelectorAll("[id^='declCard']");
    cardInputs.forEach(input => {
        if (input.value) {
            data[input.name] = input.value;
        }
    });
    
    console.log("Declare submission:", data);
    valet(JSON.stringify(data));
    hideActionPanel();
}

//  The follwing function is triggered upon clinking the ask button and
// it creates a JSON in a global varibale called send_data which can be
// Helper: Extract suits from player's card list
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

// Suit and card mappings
var suitlist = {
    "1": "8 and J",
    "2": "High ♠",
    "3": "High ◆",
    "4": "High ♣",
    "5": "High ♥",
    "6": "Low ♠",
    "7": "Low ◆",
    "8": "Low ♣",
    "9": "Low ♥"
}

var cardlist = makecardlist();

// This function makes the cardlist object which gives relation between
// the card numbers and its actual names.
function makecardlist(){
    var cardlist = {
        "11": "Black J",
        "12": "8 of ♠",
        "13": "8 of ◆",
        "14": "8 of ♣",
        "15": "8 of ♥",
        "16": "White J",
    };

    lower = ["2", "3", "4", "5", "6", "7"];
    higher = ["9", "10", "Jack", "Queen", "King", "Ace"];
    suit = ["♠", "◆", "♣", "♥"];

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
