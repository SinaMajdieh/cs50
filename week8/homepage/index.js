document.addEventListener("DOMContentLoaded", initial);
function initial()
{
    prompt_name();
    sport_listener();

}
function prompt_name()
{
    let name = "";
    while (name == "")
    {
        name = prompt("Greetings my friend :)\nMay I ask for your name?","")
    }
    let visitor_names = document.querySelectorAll(".visitor_name");
    for (let i = 0; i < visitor_names.length; i++)
    {
        visitor_names[i].innerHTML = `${name}`;
    }
}
function sport_listener()
{
    let sport_options = document.querySelectorAll(".sport_option");
    for (let i = 0; i < sport_options.length; i++)
    {
        sport_options[i].addEventListener("click", sport);
    }
}
function sport()
{
    let value = this.innerHTML;
    switch (value)
    {
        case "Basketball":
            document.querySelector(".sport_basketball").style.display = "inline";
            break;
        case "Soccer":
            document.querySelector(".sport_soccer").style.display = "inline";
            break;
        case "Ping Pong":
            document.querySelector(".sport_ping_pong").style.display = "inline";
            break;
        default:
            document.querySelector(".sport_nothing").style.display = "inline";
            break;
    }
    let sport_querry = document.querySelector(".sport_querry_input");
    sport_querry.style.display = "none";
    let continue_querry = document.querySelectorAll(".sport_querry_continue");
    for (let i = 0; i < continue_querry.length; i++)
    {
        continue_querry[i].style.display = "inline";
    }
}
function programming(like)
{
    if (like == true)
    {
        document.querySelector(".programming_querry_positive").style.display = "inline";
    }
    else
    {
        document.querySelector(".programming_querry_negative").style.display = "inline";
    }
    let querry_btns = document.querySelectorAll(".programming_prompt_btn");
    for (let i = 0; i < querry_btns.length; i++)
    {
        querry_btns[i].setAttribute("hidden", "true");
    }
    let continue_querry = document.querySelectorAll(".programming_querry_continue");
    for (let i = 0; i < continue_querry.length; i++)
    {
        continue_querry[i].style.display = "block";
    }
    document.querySelector(".sin-bg-image").style.backgroundImage = "url('images/guitar.jpg')";
}
function music()
{
    let favorite = document.querySelector(".music_ask_input").value;
    if (favorite == "")
    {
        alert("Awww you didn't tell me your favorite music :(");
        return;
    }
    let ask = document.querySelectorAll(".music_ask");
    for (let i = 0; i < ask.length; i++)
    {
        ask[i].style.display = "none";
    }
    let respnse = document.querySelectorAll(".music_querry");
    for (let i = 0; i < respnse.length; i++)
    {
        respnse[i].style.display = "inline";
    }
    let feedback = document.querySelector(".music_querry_feedback");
    feedback.innerHTML = ` ${favorite}. `;
    let continue_querry = document.querySelectorAll(".music_querry_continue");
    for (let i = 0; i < continue_querry.length; i++)
    {
        continue_querry[i].style.display = "inline";
    }
    document.querySelector(".sin-bg-image").style.backgroundImage = "url('images/basketball.jpg')"
}