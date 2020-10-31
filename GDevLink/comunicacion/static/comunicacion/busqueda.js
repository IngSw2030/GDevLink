const userList = document.getElementById('usuarios');
const searchBar = document.getElementById('searchBar');
let characters = [];


searchBar.addEventListener('keyup', (e) => {
    const searchString = e.target.value.toLowerCase();

    const filteredCharacters = characters.filter((character) => {
        return (
            character.username.toLowerCase().includes(searchString)
            
        );
    });
    displayCharacters(filteredCharacters);
});

const loadCharacters = async () => {
    try {
       // const value = JSON.parse(document.getElementById('users').textContent);
      //const res = await fetch('https://hp-api.herokuapp.com/api/characters');
       alert(res);
       characters = await temp;
       for(var x in res){ 
        console.log(x); 
        } 
        console.log(res);
      // displayCharacters(characters);
      
    } catch (err) {
        console.error(err);
    }
};

const displayCharacters = (characters) => {
    const htmlString = characters
        .map((character) => {
            return `
            <li class="character">
                <button value="${character.username}" >${character.username}</button>
            </li>
        `;
        })
        .join('');
    userList.innerHTML = htmlString;
};


loadCharacters();