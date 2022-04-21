var adoptionCenters = [];


var uEmailInput = document.querySelector("#testemail"); 
var uPasswordInput = document.querySelector("#testpassword"); 
var uFirstNameInput = document.querySelector("#testfirstname"); 
var uLastNameInput = document.querySelector("#testlastname"); 
var createusermenuButton = document.querySelector("#createmenu");
var createuserButton = document.querySelector("#createuser");
var signinButton = document.querySelector("#signin");

var submitButton = document.querySelector("#submit");
var editsubmitbutton = document.querySelector("#editsubmit");

var cNameInput = document.querySelector("#centerName"); 
var cLocationInput = document.querySelector("#centerLocation"); 
var cRatingInput = document.querySelector("#centerRating"); 
var cURLInput = document.querySelector("#centerURL"); 
var cSelectionInput = document.querySelector("#centerSelection"); 


submitButton.onclick = function(){
	var adoptionCenterName = cNameInput.value;
	var adoptionCenterLocation = cLocationInput.value;
	var adoptionCenterRating = cRatingInput.value;
	var adoptionCenterURL = cURLInput.value;
	var adoptionCenterSelection = cSelectionInput.value;
	createNewCenter(adoptionCenterName, adoptionCenterLocation, adoptionCenterRating, adoptionCenterURL, adoptionCenterSelection);
	cNameInput.value = "";
	cLocationInput.value = "";
	cRatingInput.value = "";
	cURLInput.value = "";
	cSelectionInput.value = "";
};
editsubmitbutton.onclick = function(){
	var adoptionCenterName = cNameInput.value;
	var adoptionCenterLocation = cLocationInput.value;
	var adoptionCenterRating = cRatingInput.value;
	var adoptionCenterURL = cURLInput.value;
	var adoptionCenterSelection = cSelectionInput.value;
	updateCenterFromServer(id, adoptionCenterName, adoptionCenterLocation, adoptionCenterRating, adoptionCenterURL, adoptionCenterSelection);
	cNameInput.value = "";
	cLocationInput.value = "";
	cRatingInput.value = "";
	cURLInput.value = "";
	cSelectionInput.value = "";
	document.getElementById("hadd").style.display = "Block";
	document.getElementById("hedit").style.display = "None";
	document.getElementById("editsubmit").style.display = "None";
	document.getElementById("submit").style.display = "Block";
};

createusermenuButton.onclick = function(){
	document.getElementById("testfirstname").style.display = "Block";
	document.getElementById("testlastname").style.display = "Block";
	document.getElementById("createuser").style.display = "Block";
	document.getElementById("createmenu").style.display = "None";
	document.getElementById("signin").style.display = "None";
};

createuserButton.onclick = function(){
	var userEmail = uEmailInput.value;
	var userPassword = uPasswordInput.value;
	var userFirstName = uFirstNameInput.value;
	var userLastName = uLastNameInput.value;
	createNewUser(userEmail, userPassword, userFirstName, userLastName);
	document.getElementById("testfirstname").style.display = "None";
	document.getElementById("testlastname").style.display = "None";
	document.getElementById("createuser").style.display = "None";
	document.getElementById("createmenu").style.display = "Block";
	document.getElementById("signin").style.display = "Block";
	uEmailInput.value = "";
	uPasswordInput.value = "";
	uFirstNameInput.value = "";
	uLastNameInput.value = "";
};

signinButton.onclick = function(){
	var userEmail = uEmailInput.value;
	var userPassword = uPasswordInput.value;
	createNewSession(userEmail, userPassword);
	uEmailInput.value = "";
	uPasswordInput.value = "";
};
//Put "credentials: 'include'" wherever you see fetch

//create new center on server
function createNewCenter(adoptionCenterName, adoptionCenterLocation, adoptionCenterRating, adoptionCenterURL, adoptionCenterSelection){
	var dataname = "name=" +encodeURIComponent(adoptionCenterName);
	var datalocation = "&location=" +encodeURIComponent(adoptionCenterLocation);
	var datarating = "&rating=" +encodeURIComponent(adoptionCenterRating);
	var dataurl = "&url=" +encodeURIComponent(adoptionCenterURL);
	var dataselection = "&selection=" +encodeURIComponent(adoptionCenterSelection);
	//data += "&cuisine=" + encodedURIComponent(restaurantCuisine)
	console.log("This is the New Center Data I am going to send over the server", dataname+datalocation+datarating+dataurl+dataselection);
	
	fetch("https://southernutahadoption.herokuapp.com/adoptioncenters",{
		method: 'POST',
		credentials: 'include',
		body:dataname+datalocation+datarating+dataurl+dataselection,
		headers:{
			'Content-Type':'application/x-www-form-urlencoded'
		}
	}).then(function(response){
		if (response.status == "201"){
			loadAdoptionCenters();}
	});
};

function deleteCenterFromServer(centerID) {
	fetch("https://southernutahadoption.herokuapp.com/adoptioncenters/" + centerID, {
	method: "DELETE",
	credentials: 'include'
	}).then(function(response){
		if (response.status == "200"){
		console.log("The Adoption Center was Successfully Deleted!");
		loadAdoptionCenters();
		}	
	});
};


function updateCenterFromServer(adoptionCenterID, adoptionCenterName, adoptionCenterLocation, adoptionCenterRating, adoptionCenterURL, adoptionCenterSelection){
	var dataid = "id=" +encodeURIComponent(adoptionCenterID);
	var dataname = "&name=" +encodeURIComponent(adoptionCenterName);
	var datalocation = "&location=" +encodeURIComponent(adoptionCenterLocation);
	var datarating = "&rating=" +encodeURIComponent(adoptionCenterRating);
	var dataurl = "&url=" +encodeURIComponent(adoptionCenterURL);
	var dataselection = "&selection=" +encodeURIComponent(adoptionCenterSelection);
	var data = dataid+dataname+datalocation+datarating+dataurl+dataselection;
	console.log("This is the data i am going to send over the server", dataid+dataname+datalocation+datarating+dataurl+dataselection);
	fetch("https://southernutahadoption.herokuapp.com/adoptioncenters/"+ adoptionCenterID,{
		method: 'PUT',
		credentials: 'include',
		body: data,
		headers:{'Content-Type':'application/x-www-form-urlencoded'}
	}).then(function(response){
		if (response.status == "200"){
		console.log("The Adoption Center was Successfully Edited!");
		loadAdoptionCenters();
		}
	});
};

function loadAdoptionCenters(){
	fetch("https://southernutahadoption.herokuapp.com/adoptioncenters", {
		credentials: 'include'
	}).then(function(response){
	response.json().then(function(data){
		document.getElementById("login").style.display = "None";
		document.getElementById("grid").style.display = "Block";
		adoptionCenters = data;
		console.log("Centers from the server", adoptionCenters);
		var adoptionCenterList =  document.querySelector("#center-list");
		adoptionCenterList.innerHTML = "";
		document.getElementById("editsubmit").style.display = "None";
		document.getElementById("submit").style.display = "Block";
		document.getElementById("hadd").style.display = "Block";
		document.getElementById("hedit").style.display = "None";
		adoptionCenters.forEach(function(aCenter){
			var newCenterLi = document.createElement("li");
				var nameDiv = document.createElement("div");
				nameDiv.innerHTML = aCenter.name;
				//nameDiv.classList.add("restaurant-name");
				newCenterLi.appendChild(nameDiv);
				var locationDiv = document.createElement("div");
				locationDiv.innerHTML = "Location:   "+aCenter.location;
				newCenterLi.appendChild(locationDiv);
				var ratingDiv = document.createElement("div");
				ratingDiv.innerHTML = "Rating:   "+aCenter.rating;
				newCenterLi.appendChild(ratingDiv);
				var urlDiv = document.createElement("div");
				urlDiv.innerHTML = "URL:   "+aCenter.url;
				newCenterLi.appendChild(urlDiv);
				var selectionDiv = document.createElement("div");
				selectionDiv.innerHTML = "Animal Selection:   " +aCenter.selection;
				newCenterLi.appendChild(selectionDiv);
				//One Button element for delete
				//this is called a closure
				var deleteButton = document.createElement("button");
				deleteButton.innerHTML = "Delete";
				deleteButton.onclick = function(){
					console.log("Delete Button Clicked", aCenter.id);
					if (confirm("Are you sure?")){
					deleteCenterFromServer(aCenter.id);}
				}
				newCenterLi.appendChild(deleteButton);
				var editButton = document.createElement("button");
				editButton.innerHTML = "Edit";
				editButton.onclick = function(){
					console.log("Edit Button Clicked", aCenter.id);
					displayEditForm(aCenter.id, aCenter.name, aCenter.location, aCenter.rating, aCenter.url, aCenter.selection);
					window.id = aCenter.id;
				}
				newCenterLi.appendChild(editButton);



			adoptionCenterList.appendChild(newCenterLi);
		});
	});
	});
};

function displayEditForm(centerid,centername, centerlocation, centerrating, centerurl, centerselection) {
		document.getElementById("editsubmit").style.display = "Block";
		document.getElementById("submit").style.display = "None";
		document.getElementById("hadd").style.display = "None";
		document.getElementById("hedit").style.display = "Block";
		var h1 = document.querySelector("h1");
		h1.value = "Edit Mode Enabled";
		cNameInput.value = centername;
		cLocationInput.value = centerlocation;
		cRatingInput.value = centerrating;
		cURLInput.value = centerurl;
		cSelectionInput.value = centerselection;
}

function createNewUser(userEmail, userPassword, userFirstName, userLastName){
	var dataemail = "email=" +encodeURIComponent(userEmail);
	var datapassword = "&password=" +encodeURIComponent(userPassword);
	var datafname = "&firstname=" +encodeURIComponent(userFirstName);
	var datalname = "&lastname=" +encodeURIComponent(userLastName);
	console.log("This is the New User Data I am going to send over the server", dataemail+datapassword+datafname+datalname);
	fetch("https://southernutahadoption.herokuapp.com/users",{
		method: 'POST',
		credentials: 'include',
		body:dataemail+datapassword+datafname+datalname,
		headers:{
			'Content-Type':'application/x-www-form-urlencoded'
		}
	}).then(function(response){
		if (response.status == "422"){
			console.log("user already exists");
			document.getElementById("creation").style.display = "None"; 
			document.getElementById("emailexists").style.display = "Block"; 
			document.getElementById("signinsuccess").style.display = "None"; 
		loadAdoptionCenters();
		}
		else if (response.status == "201"){
			console.log("Sign in Success");
			document.getElementById("creation").style.display = "None"; 
			document.getElementById("emailexists").style.display = "None"; 
			document.getElementById("signinsuccess").style.display = "Block"; 
		loadAdoptionCenters();
		}
	});
};

function createNewSession(userEmail, userPassword){
	var dataemail = "email=" +encodeURIComponent(userEmail);
	var datapassword = "&password=" +encodeURIComponent(userPassword);
	console.log("This is the User Sign In Data I am going to send over the server", dataemail+datapassword);
	fetch("https://southernutahadoption.herokuapp.com/sessions",{
		method: 'POST',
		credentials: 'include',
		body:dataemail+datapassword,
		headers:{
			'Content-Type':'application/x-www-form-urlencoded'
		}
	}).then(function(response){
		if (response.status == "401"){
			console.log("Wrong Password");
			document.getElementById("wrongpasswd").style.display = "Block";} 
			document.getElementById("creation").style.display = "None";
		if (response.status == "201"){
			console.log("Sign in Success");
			document.getElementById("login").style.display = "None"; 
			document.getElementById("grid").style.display = "Block"; 
			loadAdoptionCenters();
		}	
	});
};


document.getElementById("testfirstname").style.display = "None";
document.getElementById("testlastname").style.display = "None";
document.getElementById("createuser").style.display = "None";
document.getElementById("createmenu").style.display = "Block";
document.getElementById("signin").style.display = "Block";

document.getElementById("creation").style.display = "Block"; 
document.getElementById("emailexists").style.display = "None"; 
document.getElementById("signinsuccess").style.display = "None"; 
document.getElementById("wrongpasswd").style.display = "None"; 


document.getElementById("login").style.display = "Block"; 
document.getElementById("grid").style.display = "None"; 

