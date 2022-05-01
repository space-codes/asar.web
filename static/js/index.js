const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});

function checkUserName(){
    var userSurname = document.getElementById("userName");
    var userNameFormate = /^([A-Za-z.\s_-])/;
    var flag;
    if(userSurname.value.match(userNameFormate)){
        flag = false;
    }else {
        flag = true;
    }
    if(flag){
        document.getElementById("usernameError").innerHTML="Username&nbspis&nbspnot&nbspvalid.&nbspOnly&nbspcharacters&nbspA-Z,&nbspa-z&nbspand&nbsp'-'&nbspare&nbspacceptable.";
        document.getElementById("usernameError").style.display = "inline-block";
    }else{
        document.getElementById("usernameError").innerHTML="";
    }
}
// xxxxxxxxxx Confirm Password Validation xxxxxxxxxx
function checkConfirmPassword(){
    var userPassword = document.getElementById("userPassword");
    var userConfirmPassword = document.getElementById("userConfirmPassword");
    var flag;
    if(userPassword.value == userConfirmPassword.value){
        flag = false;
    }else{
        flag = true;
    }
    if(flag){
       document.getElementById("confirmPasswordError").innerHTML="Confirm&nbsppassword&nbspmust&nbspbe&nbsplike&nbspthe&nbsppassword";
       document.getElementById("confirmPasswordError").style.display = "inline-block";
    }else{
        document.getElementById("confirmPasswordError").style.display="none";
    }
}
// xxxxxxxxxx Password Validation xxxxxxxxxx
function checkUserPassword(){
    var userPassword = document.getElementById("userPassword");
    var flag;
    if(userPassword.value != ""){
        flag = false;
    }else{
        flag = true;
    }
    if(flag){
        document.getElementById("userPasswordError").innerHTML="Password&nbspis&nbsprequired.";
        document.getElementById("userPasswordError").style.display = "inline-block";
    }else{
        document.getElementById("userPasswordError").style.display = "none";
    }
}

function checkSIUsername(){
    var userSIUsername = document.getElementById("userSIUsername");
    var userNameFormate = /^([A-Za-z.\s_-])/;
    var flag;
    if(userSIUsername.value.match(userNameFormate)){
        flag = false;
    }else{
        flag = true;
    }
    if(flag){
        document.getElementById("usernameSIError").innerHTML = "Username&nbspis&nbspnot&nbspvalid.&nbspOnly&nbspcharacters&nbspA-Z,&nbspa-z&nbspand&nbsp'-'&nbspare&nbspacceptable.";
        document.getElementById("usernameSIError").style.display = "inline-block";
    }else{
        document.getElementById("usernameSIError").style.display = "none";
    }
}
// xxxxxxxxxx Sign In Password Validation xxxxxxxxxx
function checkUserSIPassword(){
    var userSIPassword = document.getElementById("userSIPassword");
    var flag;
    if(userSIPassword.value != ""){
        flag = false;
    }else{
        flag = true;
    }
    if(flag){
        document.getElementById("userSIPasswordError").innerHTML = "Password&nbspis&nbsprequired";
        document.getElementById("userSIPasswordError").style.display = "inline-block";
    }else{
        document.getElementById("userSIPasswordError").style.display = "none";
    }
}