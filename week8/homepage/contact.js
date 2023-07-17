function clear_form()
{
    let contact_fields = document.querySelectorAll(".contact")
    for (let i = 0; i < contact_fields.length; i++)
    {
        contact_fields[i].value = "";
    }
}
function sned()
{
    let values = {}; 
    let name = document.querySelector("#name").value;  
    let lastname = document.querySelector("#lastname").value;
    let message = document.querySelector("#message").value;
    let email = document.querySelector("#email").value;
    values["name"] = name;
    values["lastname"] = lastname;
    values["email"] = email;
    values["message"] = message;

    for (let key in values)
    {
        if (values[key] == "")
        {
            alert("please fill all the fields :)");
            return
        }
    }
    let result = `Thank you ${values["name"]} ${values["lastname"]}\nyour message : ${values["message"]} was sent to me :)\nand now I can contact you on ${values["emial"]} as well!`;
    clear_form();
    alert(result);
}