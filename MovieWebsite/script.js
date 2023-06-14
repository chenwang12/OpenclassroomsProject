const defaultImage = 'https://user.oc-static.com/upload/2020/09/18/16004298835178_P5.png';

const showImages = 5;
const maxImages = 7;

const movieTracker = {
    "top": {
        "start": 1,
        "end": showImages
    },
    "action": {
        "start": 0,
        "end": showImages - 1
    },
    "comedy": {
        "start": 0,
        "end": showImages - 1
    },
    "horror": {
        "start": 0,
        "end": showImages - 1
    }
};

async function loaded() {
    getMoviesForCategory();
    getMoviesForCategory('action');
    getMoviesForCategory('comedy');
    getMoviesForCategory('horror');
    //Commented only displayed below for testing best movie logic
    //getMoviesForCategory('drama');
}

async function setBestMovie(movie) {
    const bestMovieContainer = document.getElementById('banner__contents');
    document.getElementById('banner').style.backgroundImage = `url(${movie.image_url})`;
    console.log('Setting best movie ...');
    console.log(document.getElementById('banner').style.backgroundImage);
    const movieData = await getMovieAttributes(movie.id);
    bestMovieContainer.innerHTML = `
        <h1 class="banner__title">${movie.title}</h1>
        <div class="banner__buttons">
            <button class="banner__button">Play</button>
        </div>
        <div class="banner__description">
            ${movieData.description}
        </div>
    `;
}

async function getMovieAttributes(movieId) {
    const response = await fetch(`http://localhost:8000/api/v1/titles/${movieId}`);
    if (!response.ok) {
        throw new Error('Unable to retrieve movie details.');
    }
    const movieData = await response.json();
    return movieData;
}

async function getTopMovies(category) {
    let hasNext = true;
    const movies = [];
    let url = 'http://localhost:8000/api/v1/titles/?sort_by=-imdb_score';
    if (category) {
        url = `${url}&genre=${category}`;
    } else {
        console.log('Getting top movies');
    }
    while(hasNext) {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Network response was not OK.');
        }
        const data = await response.json(); // Parse the response body as JSON
        movies.push.apply(movies, data.results);
        if(!data.next || movies.length >= 10) {
            hasNext = false;
        }
        url = data.next;
    }
    return movies;
}

async function getMoviesForCategory(name) {
    let moviesContainer = null;
    //get movies sorted by score
    let movies = null;
    const id = `${name}Movies`;

    if (name) {
        moviesContainer = document.getElementById(id);
        movies = await getTopMovies(name); 
    }
    else {
        moviesContainer = document.getElementById('topMovies');
        movies = await getTopMovies();
    }
    console.log(movies)
    moviesContainer.innerHTML = `<a class="switchLeft sliderButton" onclick="sliderScrollLeft('${name}')"><</a>`;
    if (name === undefined) {
        name = 'top';
    }
    let lower = movieTracker[name]["start"] || 0;
    let upper = movieTracker[name]["end"] || showImages;
    console.log(name);
    if (name === 'top') {
        lower = lower + 1;
        upper = upper + 1;
        setBestMovie(movies[0]);
        name = undefined;
    }

    for(let i = lower; i < upper; ++i) {
        if (!movies[i].image_url) {
            movies[i].image_url = defaultImage;
        }
        moviesContainer.innerHTML = moviesContainer.innerHTML + `<img src="${movies[i].image_url}" onerror="this.onerror=null; this.src='${defaultImage}'; this.style.background='white'; this.alt='Movie Image Not Available'; this.title='Movie Image Not Available';" onclick="openModal(${movies[i].id}, '${movies[i].imdb_url}')" onmouseover="this.focus()" alt="" class="row__poster row__posterLarge"></img>`
    }
    moviesContainer.innerHTML = moviesContainer.innerHTML + `<a class="switchRight sliderButton" onclick="sliderScrollRight('${name}')">></a>`;
}

async function retrieveModalContent(movieId, imdbUrl) {
    const modalContent = document.getElementById('modalContent')
    const movieData = await getMovieAttributes(movieId);
    // TODO: create generic image to be assigned to movieData.image_url
    if (!movieData.image_url) {
        movieData.image_url = 'https://user.oc-static.com/upload/2020/09/18/16004298835178_P5.png';
    }
    modalContent.style.backgroundImage = movieData.image_url;
    modalContent.innerHTML = `
        <img src="${movieData.image_url}" onerror="this.onerror=null; this.src='${defaultImage}'; this.alt='Movie Image Not Available'; this.title='Movie Image Not Available';" />    
        <h2>${movieData.title}</h2>
        <p><b>Genres:</b>${movieData.genres.join(', ')}</p> <p><b>Country of origin:</b> ${movieData.countries.join(', ')}</p>
        <p><b>Release date:</b> ${movieData.date_published}</p>
        <p><b>MPAA rating:</b> ${movieData.rated}</p>
        <a target="_blank" href="${imdbUrl}"><b>IMDB Score:</b> ${movieData.imdb_score}</a>
        <p><b>Budget:</b> ${movieData.budget} ${movieData.budegt_currency}</p>
        <p><b>USA gross income:</b>${movieData.usa_gross_income}</p>
        <p><b>Worldwide gross income:</b> ${movieData.worldwide_gross_income}</p>
        <p><b>Directed by:</b> ${movieData.directors.join(', ')}</p>
        <p><b>Cast:</b> ${movieData.actors.join(', ')}</p>       
        <p><b>Duration:</b> ${movieData.duration} mins </p>        
        <p><b>Summary:</b> ${movieData.description}</p>
            
    `;
    //missing budget or box office data 
}

//toggle or construct the modal infromation to display full selected movie details
function openModal(movieId, imdbUrl) {
    retrieveModalContent(movieId, imdbUrl)
    document.getElementById('modal').style.display = 'block';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

// scroll arrow
function sliderScrollLeft(category) {
    /*const sliders = document.getElementById(movieId);
    var ImagePadding = 20
    var scrollAmount = 0;
    var scrollPerClick = document.getElementsByClassName("row__poster").clientWidth + ImagePadding;

    sliders.scrollTo({
        top: 0,
        left: (scrollAmount -= scrollPerClick),
        behavior: "smooth"
    });
    if(scrollAmount < 0) {
        scrollAmount = 0
    }*/
    let startLimit = 0;
    if (category === undefined || category === 'undefined') {
        category = 'top';
        startLimit = 1;
    }
    if (movieTracker[category]["start"] > startLimit) {
        movieTracker[category]["start"] = movieTracker[category]["start"] - 1;
        movieTracker[category]["end"] = movieTracker[category]["start"] + showImages - 1;
    }
    if (category === 'top') {
        category = undefined;
    }
    getMoviesForCategory(category);
}

function sliderScrollRight(category) {
    /*const sliders = document.getElementById(movieId);
    var ImagePadding = 20
    var scrollAmount = 0;
    var scrollPerClick = document.getElementsByClassName("row__poster").clientWidth + ImagePadding;

    if(scrollAmount <= sliders.scrollWidth - sliders.clientWidth) {
        sliders.scrollTo({
            top: 0,
            left: (scrollAmount += scrollPerClick),
            behavior: "smooth",
        })
    }*/
    let topLimit = 7;
    if (category === undefined || category === 'undefined') {
        category = 'top';
        topLimit = 8;
    }
    if (movieTracker[category]["end"] < topLimit) {
        movieTracker[category]["end"] = movieTracker[category]["end"] + 1;
        movieTracker[category]["start"] = movieTracker[category]["end"] - showImages + 1;
    }
    if (category === 'top') {
        category = undefined;
    }
    getMoviesForCategory(category);
}
