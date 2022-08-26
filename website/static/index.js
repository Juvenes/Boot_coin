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
let  tootoo = false;
selectElement.addEventListener('change', (event) => {
  var temp = event.target.value;
  var divi= document.getElementById("addforstrat");
  if ( temp == "crocodile"){
    if (tootoo == true){
      document.getElementById("stratopi").remove();
      tootoo = false
    }
    
    var diva = document.createElement('div'); // is a node
    diva.classList.add("col-4");
    diva.setAttribute('id','stratopi');
    diva.innerHTML = '<h4 class="border-bottom">[Stategy]Aligator</h4>\
    <div class="media text-muted pt-3">\
        <a href="https://www.ig.com/en/trading-strategies/what-is-the-alligator-indicator-and-how-do-you-use-it-in-forex-t-210412">Explication Strategie</a>\
    </div>\
  </div><hr>';
  divi.appendChild(diva);
  tootoo =true;
  }
  else if (temp == "adx"){
    if (tootoo == true){
      document.getElementById("stratopi").remove();
      tootoo = false
    }
    var diva = document.createElement('div'); // is a node
    diva.classList.add("col-4");
    diva.setAttribute('id','stratopi');
    diva.innerHTML = '<h4 class="border-bottom">[Trend]ADX</h4>\
    <div class="media text-muted pt-3">\
        <a href="https://www.investopedia.com/articles/trading/07/adx-trend-indicator.asp">Explication indicateur</a>\
    </div>\
  </div><hr>';
  divi.appendChild(diva);
  tootoo =true;

  }
});





let tri = false;
const selecto = document.querySelector('#timing');
selecto.addEventListener('change', (event) => {
  var temp = event.target.value;
  console.log(temp);
  var divi= document.getElementById("morot");
 if(temp=="choice" && tri == false){
  var diva = document.createElement('div'); // is a node
  diva.classList.add("flex-column");
  diva.setAttribute('id','temporise');
  diva.innerHTML ='<h6>Date de début de la simulation</h6>\
    <div class="row">\
        <div class="form-group col-4">\
            <label for="dayIn">Jour</label>\
            <input type="number" name="dayIn" id="dayIn" min="1" max="28" value="25"class="form-control" >\
        </div>\
        <div class="form-group col-4">\
            <label for="monthIn">Mois</label>\
            <select id="" name="monthIn" class="form-control">\
            <option   value="1">Janvier</option>\
            <option value="2">Fevier</option>\
            <option value="3">Mars</option>\
            <option value="4">Avril</option>\
            <option value="5">Mai</option>\
            <option selected value="6">Juin</option>\
            <option value="7">Juillet</option>\
            <option value="8">Aout</option>\
            <option value="9">Septembre </option>\
            <option value="10">Octobre </option>\
            <option value="11">Novembre</option>\
            <option value="12">Decembre</option>\
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
            <option  selected value="1">Janvier</option>\
            <option value="2">Fevier</option>\
            <option value="3">Mars</option>\
            <option value="4">Avril</option>\
            <option value="5">Mai</option>\
            <option value="6">Juin</option>\
            <option value="7">Juillet</option>\
            <option value="8">Aout</option>\
            <option value="9">Septembre </option>\
            <option value="10">Octobre </option>\
            <option value="11">Novembre</option>\
            <option value="12">Decembre</option>\
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
        console.log(tri)
    }
    else if (tri ==true){
      console.log("elsooo")
      document.getElementById("temporise").remove();
      tri=false;}
});


