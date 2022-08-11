function del(id,isPrivate,mdp){
    var password = prompt("Enter in the password");
    console.log(mdp)
    if (isPrivate=="True") {
        if(password==mdp){
            fetch("/delete-note", {
                method: "POST",
                body: JSON.stringify({ noteId: id }),
              }).then((_res) => {
                window.location.href = "/portefeuille";
              });
        }
    }
    else 
    {
        if(password=="SUPPRIMER"){
            fetch("/delete-note", {
                method: "POST",
                body: JSON.stringify({ noteId: id }),
              }).then((_res) => {
                window.location.href = "/portefeuille";
              });
        }
    }

}

function change(id,state,myid){
  fetch("/change-ex", {
    method: "POST",
    body: JSON.stringify({ noteId: id ,state : state }),
  }).then((_res) => {
    window.location.href = "/explication?id="+myid;
  });
}


function delex(id,myid){
  fetch("/del_ex", {
    method: "POST",
    body: JSON.stringify({ noteId: id }),
  }).then((_res) => {
    window.location.href = "/explication?id="+myid;
  });
}

const selectElement = document.querySelector('#inputStat');
const  tootoo = [];
selectElement.addEventListener('change', (event) => {
  var temp = event.target.value;
  var divi= document.getElementById("addforstrat");
  if (!tootoo.includes( "crocodile") && temp == "crocodile"){
    var diva = document.createElement('div'); // is a node
    diva.classList.add("col-4");
    diva.innerHTML = '<h4 class="border-bottom">[Stategy]Aligator</h4>\
    <div class="media text-muted pt-3">\
        <a href="https://www.ig.com/en/trading-strategies/what-is-the-alligator-indicator-and-how-do-you-use-it-in-forex-t-210412">Explication Strategie</a>\
    </div>\
  </div><hr>';
  divi.appendChild(diva);
  tootoo.push("crocodile")
  }
  else if (!tootoo.includes( "adx") && temp == "adx"){
    var diva = document.createElement('div'); // is a node
    diva.classList.add("col-4");
    diva.innerHTML = '<h4 class="border-bottom">[Trend]ADX</h4>\
    <div class="media text-muted pt-3">\
        <a href="https://www.investopedia.com/articles/trading/07/adx-trend-indicator.asp">Explication indicateur</a>\
    </div>\
  </div><hr>';
  divi.appendChild(diva);
  tootoo.push("adx")
  }
  else if (!tootoo.includes( "emaxy") && temp == "emaxy"){
    var diva = document.createElement('div'); // is a node
    diva.classList.add("col-4");
    diva.innerHTML = '<h4 class="border-bottom">[Stategy]Simple sma</h4>\
    <div class="media text-muted pt-3">\
        <a href="https://www.investopedia.com/terms/d/double-exponential-moving-average.asp">Explication Strategie</a>\
    </div>\
  </div><hr>';
  divi.appendChild(diva);
  tootoo.push("emaxy")

  }
  else if (!tootoo.includes( "simple_ema") && temp == "simple_ema"){
    var diva = document.createElement('div'); // is a node
    diva.classList.add("col-4");
    diva.innerHTML = '<h4 class="border-bottom">[Trend]Simple EMA</h4>\
    <div class="media text-muted pt-3">\
        <a href="https://www.investopedia.com/terms/e/ema.asp">Explication indicateur</a>\
    </div>\
  </div><hr>';
  divi.appendChild(diva);
  tootoo.push("simple_ema")

  }
  else if (!tootoo.includes( "trix") && temp == "trix"){
    var diva = document.createElement('div'); // is a node
    diva.classList.add("col-4");
    diva.innerHTML = '<h4 class="border-bottom">[Stategy]Trix</h4>\
    <div class="media text-muted pt-3">\
        <a href="https://www.investopedia.com/articles/technical/02/092402.asp">Explication indicateur</a>\
    </div>\
  </div><hr>';
  divi.appendChild(diva);
  tootoo.push("trix")

  }
  else if (!tootoo.includes("simple_sma") && temp == "simple_sma"){
    var diva = document.createElement('div'); // is a node
    diva.classList.add("col-4");
    diva.innerHTML = '<h4 class="border-bottom">[Trend] Simple SMA</h4>\
    <div class="media text-muted pt-3">\
        <a href="https://www.investopedia.com/articles/active-trading/052014/how-use-moving-average-buy-stocks.asp">Explication indicateur</a>\
    </div>\
  </div><hr>';
  divi.appendChild(diva);
  tootoo.push("simple_sma")

  }
  else if (!tootoo.includes( "vortex_indicator") && temp == "vortex_indicator"){
    var diva = document.createElement('div'); // is a node
    diva.classList.add("col-4");
    diva.innerHTML = '<h4 class="border-bottom">[Trend]Vortex Indicator</h4>\
    <div class="media text-muted pt-3">\
        <a href="https://www.investopedia.com/terms/v/vortex-indicator-vi.asp">Explication indicateur</a>\
    </div>\
  </div><hr>';
  divi.appendChild(diva);
  tootoo.push("vortex_indicator");
  }
  else if (!tootoo.includes( "awesome_oscillator") && temp == "awesome_oscillator"){
    tootoo.push("awesome_oscillator");
  }
  else if (!tootoo.includes( "stochastic_oscillator") && temp == "stochastic_oscillator"){
    tootoo.push("stochastic_oscillator");
  }
  else if (!tootoo.includes( "stoch_rsi") && temp == "stoch_rsi"){
    tootoo.push("stoch_rsi");
  }
  else if (!tootoo.includes( "wiliamsr") && temp ==  "wiliamsr"){
    tootoo.push("wiliamsr");
  }
  else if (!tootoo.includes( "eom") && temp == "eom"){
    tootoo.push("eom");
  }
  else if (!tootoo.includes( "cmf") && temp == "cmf"){
    tootoo.push("cmf");
  }
  else if (!tootoo.includes( "mfi") && temp ==  "mfi"){
    tootoo.push("mfi");
  }
  else if (!tootoo.includes( "obv") && temp == "obv"){
    tootoo.push("obv");
  }
});





const tri = false;
const selecto = document.querySelector('#timing');
selecto.addEventListener('change', (event) => {
  var temp = event.target.value;
  console.log(temp);
  var divi= document.getElementById("morot");
 if(temp=="choice" && tri == false){
  var diva = document.createElement('div'); // is a node
  diva.classList.add("flex-column");
  diva.innerHTML ='<h6>Date de début de la simulation</h6>\
    <div class="row">\
        <div class="form-group col-4">\
            <label for="dayIn">Jour</label>\
            <input type="number" name="dayIn" id="dayIn" min="1" max="28" value="25"class="form-control" >\
        </div>\
        <div class="form-group col-4">\
            <label for="monthIn">Mois</label>\
            <select id="monthIn" name="monthIn" class="form-control">\
            <option   value="january">Janvier</option>\
            <option value="february">Fevier</option>\
            <option value="march">Mars</option>\
            <option value="april">Avril</option>\
            <option value="may">Mai</option>\
            <option selected value="june">Juin</option>\
            <option value="july">Juillet</option>\
            <option value="august">Aout</option>\
            <option value="september">Septembre </option>\
            <option value="october">Octobre </option>\
            <option value="november">Novembre</option>\
            <option value="december">Decembre</option>\
            </select>\
        </div>\
        <div class="col-2">\
            <label for="yearIn">Année</label>\
            <input type="number" id="yearIn" name="yearIn" min="2017" value="2021" max="2022" class="form-control" >\
        </div>\
    </div>\
    <h6>Date de fin de la simulation</h6>\
    <div class="row align-items-end">\
        <div class="col-4">\
            <label for="dayout">Jour</label>\
            <input type="number" id="dayout" name="dayout" min="1" max="28" class="form-control"  placeholder="1-28">\
        </div>\
        <div class=" col-4">\
            <label for="monthout">Mois</label>\
            <select id="monthout" name="monthout" class="form-control">\
            <option  selected value="january">Janvier</option>\
            <option value="february">Fevier</option>\
            <option value="march">Mars</option>\
            <option value="april">Avril</option>\
            <option value="may">Mai</option>\
            <option value="june">Juin</option>\
            <option value="july">Juillet</option>\
            <option value="august">Aout</option>\
            <option value="september">Septembre </option>\
            <option value="october">Octobre </option>\
            <option value="november">Novembre</option>\
            <option value="december">Decembre</option>\
            </select>\
        </div>\
        <div class="col-2">\
            <label for="yearout">Année</label>\
            <input type="number" name="yearout" id="yearout" min="2017" max="2022" class="form-control" placeholder="2017-2022">\
        </div>\
        <div class="col-2  ">\
                <input class="form-check-input"  type="checkbox" name="autoSizingCheck" id="autoSizingCheck" checked>\
                <label class="form-check-label" for="autoSizingCheck">\
                  Jusqu à aujourd hui\
                </label>\
        </div>'

        divi.appendChild(diva);
        tri=true;
 }
});