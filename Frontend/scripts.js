




const designerCardsContainer = document.getElementById('designerCardsContainer');
const loaderContainer = document.getElementById('loaderContainer');

let designers = [];
let shortlistedIds = [];
let showOnlyShortlisted = false;



const leftButtons = document.querySelectorAll('.nav-left button');
const rightButtons = document.querySelectorAll('.nav-right button');

const buttons = [...leftButtons, ...rightButtons];  

buttons.forEach(button => {
  button.addEventListener('click', () => {
    
    // alert();
    buttons.forEach(b =>{
      b.style.color = 'black';
      b.querySelector('span').style.color = 'black';

    });

    const span = button.querySelector('span');
    if (button.style.color === '#E0A64E') {
      button.style.color = 'black'; 
      if (span) span.style.color = 'black';   
    } else {
      button.style.color = '#E0A64E'; 
      if (span) span.style.color = '#E0A64E';    
    }
  });
});

function saveShortlist() {
  localStorage.setItem('shortlistedIds', JSON.stringify(shortlistedIds));
}

function loadShortlist() {
  const stored = localStorage.getItem('shortlistedIds');
  if (stored) shortlistedIds = JSON.parse(stored);
}

function toggleShortlist(id) {
  if (shortlistedIds.includes(id)) {
    shortlistedIds = shortlistedIds.filter((sid) => sid !== id);
  } else {
    shortlistedIds.push(id);
  }
  saveShortlist();

  const card = document.getElementById(`designer-${id}`);
  if (card) {
    if (shortlistedIds.includes(id)) {
      card.classList.add('shortlisted');  
    } else {
      card.classList.remove('shortlisted');
    }
  }

  reloadDesigners();   
}


function createStarRating(rating) {
  const fullStars = Math.floor(rating);
  const halfStar = rating - fullStars >= 0.5;
  const emptyStars = 5 - fullStars - (halfStar ? 1 : 0);

  let starsHTML = '';

  for (let i = 0; i < fullStars; i++) {
    starsHTML += `<img src="assets/images/full_star.png" alt="★" class="star-icon" />`;
  }
  if (halfStar) {
    starsHTML += `<img src="assets/images/half_star.png" alt="☆" class="star-icon" />`;
  }
  for (let i = 0; i < emptyStars; i++) {
    starsHTML += `<img src="assets/images/empty_star.png" alt="☆" class="star-icon" />`;
  }

  return `<div class="star-rating">${starsHTML}</div>`;
}


function createDesignerCard(designer, index) {
  const isShortlisted = shortlistedIds.includes(designer._id);
  const starRatingHTML = createStarRating(designer.rating);

  const cardHTML = `
    <div id="designer-${designer._id}" class="designer-card ${index % 2 === 0 ? 'even' : 'odd'} ${isShortlisted ? 'shortlisted' : ''}">
      <div class="designer-left">
        <h3>${designer.name}</h3>
        ${starRatingHTML}
        <p>${designer.description}</p>
        <div class="stats-row">
          <div class="stat-item"><div class="number">${designer.projects}</div><div class="label">Projects</div></div>
          <div class="stat-item"><div class="number">${designer.years}</div><div class="label">Years</div></div>
          <div class="stat-item"><div class="number">${designer.price}</div><div class="label">Price</div></div>
        </div>
        <div class="phone-numbers">
          <div>${designer.phone1}</div>
          <div>${designer.phone2}</div>
        </div>
      </div>
      <div class="designer-right">
        <button type="button">
          <img src="assets/images/arrow-right-short.png" alt="Details" />
          <span style="font-size:10px">Details</span>
        </button>
        <button type="button">
          <img src="assets/images/eye-slash.png" alt="Hide" />
          <span style="font-size:10px">Hide</span>
        </button>
        <button type="button" onclick="toggleShortlist('${designer._id}')">
          <img src="assets/images/${isShortlisted ? 'Vector.png' : 'Vector_unfilled.png'}" alt="Shortlist" />
          <span style="font-size:10px">Shortlist</span>
        </button>
        <button type="button">
          <img src="assets/images/exclamation-circle.png" alt="Report" />
          <span style="font-size:10px">Report</span>
        </button>
      </div>
    </div>
  `;

  const card = document.createElement('div');
  card.innerHTML = cardHTML;
  return card.firstElementChild;  
}


function reloadDesigners() {
  designerCardsContainer.innerHTML = '';
  console.log(showOnlyShortlisted);
  const list = showOnlyShortlisted
  ? designers.filter(d => shortlistedIds.includes(d._id))
    : designers;

    console.log("list",list);
    if (list.length === 0) {
    designerCardsContainer.innerHTML = '<p style="color:black; text-align:center; padding: 2rem;">No designers to show.</p>';
    return;
  }
  
  list.forEach((designer, idx) => {
    designerCardsContainer.appendChild(createDesignerCard(designer, idx));
  });
}


document.getElementById('shortlistedBtn').addEventListener('click', toggleShortlistedView);
document.querySelector('.contacts').addEventListener('click', ()=>{
  showOnlyShortlisted = true;
  toggleShortlistedView();
});

function toggleShortlistedView() {
  showOnlyShortlisted = !showOnlyShortlisted;
  const btn = document.getElementById('shortlistedBtn');
  btn.style.color = showOnlyShortlisted ? '#E0A64E' : '#000';

  btn.querySelector('.icon-wrapper img').src= "assets/images/shortlisted.png"
  reloadDesigners();
}
// const API_BASE_URL = location.hostname === 'localhost'
//   ? 'http://localhost:5000'
//   : 'https://emptycup-assignment-2025-vedant-tathe.onrender.com';

let API_BASE_URL = 'http://localhost:5000';
if(location.hostname != 'localhost' && location.hostname != '127.0.0.1')
{
  API_BASE_URL = 'https://emptycup-assignment-2025-vedant-tathe.onrender.com';

}

console.log(API_BASE_URL);
console.log(location.port)

function loadDesigners() {
  loaderContainer.style.display = 'flex';
  // fetch('https://emptycup-assignment-2025-vedant-tathe.onrender.com/data')
  fetch(`${API_BASE_URL}/data`)
  .then(res => {
      if (!res.ok) throw new Error('Network error');
      return res.json();
    })
    .then(data => {
      designers = data;
      loaderContainer.style.display = 'none';
      showOnlyShortlisted = false;
      reloadDesigners();
    })
    .catch(err => {
      loaderContainer.style.display = 'none';
      console.log('Failed to load..! Please try again later.');
      console.error(err);
    });
}


loadShortlist();
loadDesigners();

