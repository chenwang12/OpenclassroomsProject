async function loaded() {
    getMoviesForCategory();
    getMoviesForCategory('action');
    getMoviesForCategory('comedy');
    getMoviesForCategory('horror');
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
        if(!data.next || movies.length >= 7) {
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
    
    if (name) {
        moviesContainer = document.getElementById(`${name}Movies`);
        movies = await getTopMovies(name); 
    }
    else {
        moviesContainer = document.getElementById('topMovies');
        movies = await getTopMovies();
    }
    console.log(movies)
    moviesContainer.innerHTML = '';
    for(let i = 1; i <= 7; ++i) {
        if (!movies[i].image_url) {
            movies[i].image_url = 'https://user.oc-static.com/upload/2020/09/18/16004298835178_P5.png';
        }
        moviesContainer.innerHTML = moviesContainer.innerHTML + `<img src="${movies[i].image_url}" onclick="openModal(${movies[i].id}, '${movies[i].imdb_url}')" alt="" class="row__poster row__posterLarge"></img>`
    }
}

async function retrieveModalContent(movieId, imdbUrl) {
    const modalContent = document.getElementById('modalContent')
    const response = await fetch(`http://localhost:8000/api/v1/titles/${movieId}`);
    if (!response.ok) {
        throw new Error('Unable to retrieve movie details.');
    }
    const movieData = await response.json();
    // TODO: create generic image to be assigned to movieData.image_url
    if (!movieData.image_url) {
        movieData.image_url = 'https://user.oc-static.com/upload/2020/09/18/16004298835178_P5.png';
    }
    modalContent.style.backgroundImage = movieData.image_url;
    modalContent.innerHTML = `
        <img src="${movieData.image_url}" />    
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