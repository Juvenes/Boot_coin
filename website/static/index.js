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