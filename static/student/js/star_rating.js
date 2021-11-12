const quality_rating = document.querySelector('#qaulity-rating');
const quality_items = quality_rating.querySelectorAll('.rating-item')
quality_rating.onclick = e => {
    const elClass = e.target.classList;
    // change the rating if the user clicks on a different star
    if (!elClass.contains('active')) {
        quality_items.forEach( // reset the active class on the star
            item => item.classList.remove('active')
        );
    quality_rating.querySelector('input').value = e.target.getAttribute("data-rate");
    elClass.add('active'); // add active class to the clicked star
}
};

const location_rating = document.querySelector('#location-rating');
const location_items = location_rating.querySelectorAll('.rating-item')
location_rating.onclick = e => {
    const elClass = e.target.classList;
    // change the rating if the user clicks on a different star
    if (!elClass.contains('active')) {
        location_items.forEach( // reset the active class on the star
            item => item.classList.remove('active')
        );
        location_rating.querySelector('input').value = e.target.getAttribute("data-rate");
    elClass.add('active'); // add active class to the clicked star
}
};

const food_rating = document.querySelector('#food-rating');
const food_items = food_rating.querySelectorAll('.rating-item')
food_rating.onclick = e => {
    const elClass = e.target.classList;
    // change the rating if the user clicks on a different star
    if (!elClass.contains('active')) {
        food_items.forEach( // reset the active class on the star
            item => item.classList.remove('active')
        );
        food_rating.querySelector('input').value = e.target.getAttribute("data-rate");
    elClass.add('active'); // add active class to the clicked star
}
};

const space_rating = document.querySelector('#space-rating');
const space_items = space_rating.querySelectorAll('.rating-item')
space_rating.onclick = e => {
    const elClass = e.target.classList;
    // change the rating if the user clicks on a different star
    if (!elClass.contains('active')) {
        space_items.forEach( // reset the active class on the star
            item => item.classList.remove('active')
        );
        space_rating.querySelector('input').value = e.target.getAttribute("data-rate");
    elClass.add('active'); // add active class to the clicked star
}
};

const service_rating = document.querySelector('#service-rating');
const service_items = service_rating.querySelectorAll('.rating-item')
service_rating.onclick = e => {
    const elClass = e.target.classList;
    // change the rating if the user clicks on a different star
    if (!elClass.contains('active')) {
        service_items.forEach( // reset the active class on the star
            item => item.classList.remove('active')
        );
        service_rating.querySelector('.rating input').value = e.target.getAttribute("data-rate");
    elClass.add('active'); // add active class to the clicked star
}
};

const price_rating = document.querySelector('#price-rating');
const price_items = price_rating.querySelectorAll('.rating-item')
price_rating.onclick = e => {
    const elClass = e.target.classList;
    // change the rating if the user clicks on a different star
    if (!elClass.contains('active')) {
        price_items.forEach( // reset the active class on the star
            item => item.classList.remove('active')
        );
        price_rating.querySelector('.rating input').value = e.target.getAttribute("data-rate");
    elClass.add('active'); // add active class to the clicked star
}
};