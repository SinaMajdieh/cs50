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
}