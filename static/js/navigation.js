// Get element that has id="menu"
const hamButton = document.querySelector('#menu');
// Get elements with class="navigation"
const navigation = document.querySelector('.navigation');

//add class to add or remove css styling on open class
hamButton.addEventListener('click', () => {
	navigation.classList.toggle('open');  //add or remove class="open"
	hamButton.classList.toggle('open');
});
