$('#addevent').on('submit', function() {

    let tagsbtn = document.querySelectorAll(".tagsbtn");
    let tags = document.querySelector("#tags");
    for(let i = 0; i < tagsbtn.length; i++){
        if (document.querySelector("#"+tagsbtn[i].value).value == "1"){
            tags.value += tagsbtn[i].value+";"
        }          
    }

    return true;
});

function addtag(){
    document.getElementById
    if (this.value == "0"){
        this.classList.remove("btn-secondary");
        this.classList.add("btn-success");
        this.value = "1";
    }
    else if (this.value == "1"){
        this.classList.remove("btn-success");
        this.classList.add("btn-secondary");
        this.value = "0";
    }
        
}